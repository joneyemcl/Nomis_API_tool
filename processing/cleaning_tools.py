"""
Functions for cleaning the raw indicator datasets
"""
import logging
import os
import string
from typing import List

import pandas as pd

from definitions import Nom, PathsFile, AgeBands, Aps

logger = logging.getLogger(__name__)


# importing tsv files

def get_tsv_files(dir: str) -> List[str]:
    """
    Get list of all tsv files in the current directory
    """
    files = [os.path.join(dir, file) for file in os.listdir(dir) if file.endswith('.tsv')]
    logger.debug(files)
    return files


def import_tsv(path: str) -> pd.DataFrame:
    logger.debug(f'the path is {path}')
    df = pd.read_csv(path, sep='\t')
    logger.debug(f'importing tsv data:\n{df.head()}')
    logger.debug(f'\n{df.dtypes}')
    return df

def import_nomis_API(url: str) -> pd.DataFrame:
    logger.debug(f'the url is {url}')
    df = pd.read_csv(url, sep='\t')
    logger.debug(f'importing tsv data via Nomis API:\n{df.head()}')
    logger.debug(f'\n{df.dtypes}')
    return df
    


def read_all_tsv(files: List) -> List[pd.DataFrame]:
    return [import_tsv(file) for file in files]


def append_all(df: List[pd.DataFrame]) -> pd.DataFrame:
    """
    Append all DataFrames vertically
    """
    df = pd.concat(df)
    logger.info(f'appending all dataframes: \n{df.head()}')
    return df


def get_combined_data(path: str):
    """
    get all tsv paths in a dir, read them all and append them into one DataFrame
    """
    files = get_tsv_files(path)
    data = read_all_tsv(files)
    return append_all(data)


# cleaning and creating columns

def merging_areacode(df: pd.DataFrame) -> pd.DataFrame:
    """
    Merging the area code onto dataset via area name, for .tsv data this is 
    necessaru before you split by colon
    """
    areacode_lookup = import_tsv(PathsFile.AREACODE_LOOKUP)
    areacode_lookup.columns = [Nom.AREA_CD, Nom.AREA]
    merged = pd.merge(df, areacode_lookup, how='left', on=Nom.AREA)
    logger.debug(f'merging the area codes\n{merged.head()}')
    return merged


def split_by_colon(df, col: str, namel: str, namer: str) -> None:
    for item in df[col].str.split(':'):

        if len(item) == 2:
            coll, colr = item
            # Process coll and colr
        else:
            # Handle the case where the split doesn't produce two parts
            # For example, print the problematic item
            print("Unexpected split result:", item)
            

    df[namel] = coll.strip()
    df[namer] = item.strip()
    logger.debug(f'cleaning the {col} column\n{df.head()}')


def clean_area(df: pd.DataFrame) -> None:
    split_by_colon(df, Nom.AREA, Nom.AREA_TYPE, Nom.AREA_NM)

def fix_meyede_col_names(df):
    df.rename(columns={Nom.AREA: Nom.AREA_NM}, inplace=True)
    df.rename(columns={Nom.CODE: Nom.AREA_CD}, inplace=True)


def clean_area_and_sic(df: pd.DataFrame) -> pd.DataFrame:
    """
    cleans the area and sic column of data from Nomis
    """
    split_by_colon(df, Nom.AREA, Nom.AREA_TYPE, Nom.AREA_NM)
    split_by_colon(df, Nom.INDUSTRY, Nom.SIC_CODE, Nom.SECTOR)
    logger.debug(f'cleaning columns\n{df.head()}')
    return df


def get_digits(text: str) -> str:
    """
    return only numerical digits from a string
    """
    ls = [char for char in text if char in string.digits]
    char = ''.join(ls)
    logger.debug(f'returning {char} from {text}')
    return char


# population related functions

def clean_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    for every element in the age columns return the digits, then set the column to numeric type
    """
    logger.debug('cleaning the age column')
    age = df['C_AGE_NAME']
    df['age'] = age.str.strip('Aged +')
    df['age'] = pd.to_numeric(df['age'])
    df['age_band'] = age_bins(df['age'])
    logger.debug(f'\n{df.head()}')
    return df


def age_bins(ser: pd.Series) -> pd.Series:
    labels = [AgeBands.youth, AgeBands.working_age, AgeBands.retirement]
    bins = [0, 15, 64, 999]
    age_bins = pd.cut(ser, bins=bins, labels=labels, include_lowest=True)
    logger.debug(f'creating age bins\n{age_bins.head()}')
    return age_bins


def set_val_to_num(df: pd.DataFrame) -> None:
    df[Nom.VALUE] = pd.to_numeric(df[Nom.VALUE], errors='coerce')
    logger.debug(f'val to num:\n{df.dtypes}')


# aps related functions

def clean_occ_var(df: pd.DataFrame) -> None:
    num, occ = df[Aps.VAR].str.split(':').str
    df[Aps.ORDER] = num.str.split('-').str[1].str.strip().astype(int)
    df[Aps.OCC] = occ.str.split('(').str[0].str.strip()


def clean_skill_var(df: pd.DataFrame) -> None:
    df[Aps.SKILL] = df[Aps.VAR].str.strip('% with ').str.split('-').str[0].str.strip()
    logger.debug(f'cleaning skills var:\n{df.head()}')