"""
a collection of funcitons for processing the cleaned data to get it into the right format and return statistics
from the data
"""

import logging
import numbers
import string
from datetime import datetime
from typing import List, Dict, Callable, Tuple

import pandas as pd

from definitions import Nom, Pop, AgeBands, Aps, PathsDir
from impact_areas import ImpactAreas

logger = logging.getLogger(__name__)


def get_start_less_ten_years(years: pd.Series) -> Tuple[int, int]:
    """
    returns the most recent (max) YEAR and less ten years in a tuple
    """
    recent = years.max()
    less_ten = recent - 10
    logger.debug(f'YEAR recent and less ten ({recent}, {less_ten})')
    return (recent, less_ten)


def get_start_end_years(years: pd.Series) -> Tuple[int, int]:
    """
    return the smallest and largest YEAR in a series in a tuple
    """
    start_end_years = (years.min(), years.max())
    logger.debug(f'getting start and end years {start_end_years}')
    return start_end_years


def filter_and_save(df: pd.DataFrame, writer: pd.ExcelWriter, sheet_name: str, impact_areas: ImpactAreas) -> pd.DataFrame:
    """
    filtering the dataset and saving to excel writer
    """
    logger.debug(f'imported {sheet_name} cleaned\n{df.head()}')
    df = df.dropna(axis=1, how='all') # need this in here because area_code has been duplicated somehow
    df = df[df[Nom.AREA_CD].isin(impact_areas.area_codes)]
    logger.debug(f'filtering for impact areas\n{df[Nom.AREA_NM].value_counts()}')
    df.to_excel(writer, sheet_name=sheet_name, index=False)
    return df


def add_to_struct_by_area_code(struct: List[Dict], var_name: str, func: Callable, impact_areas, *func_vars) -> None:
    """
    allows you to apply a function that takes arguments to each area (dictionary) of the struct
    """
    for area_code in impact_areas.area_codes:
        for area in struct:
            if area[Nom.AREA_CD] == area_code:
                area[var_name] = func(area_code, *func_vars)
    logger.debug(f'\n{struct}')


def get_elem(struct: List[Dict], area_code: str) -> Dict:
    """
    returns a one of the dicts (area) from the struct
    """
    for area in struct:
        if area[Nom.AREA_CD] == area_code:
            return area


def get_total_population(area_code: str, df: pd.DataFrame, year: int) -> numbers.Number:
    df.dropna(axis=1, how='all', inplace=True)
    df.to_csv('C:\\Users\\hub11\\Documents\\Python\\misc\\nomis_report_tool\\output.csv', index=False)
    cond = (df[Nom.AREA_CD] == area_code) & (df[Nom.DATE] == year)
    df_filt = df[cond]
    total_pop = df_filt[Nom.VALUE].sum()
    logger.debug(f'total pop {total_pop}, area {area_code} year {year}')
    return total_pop


def get_population_bands(area_code: str, df: pd.DataFrame, year: int) -> Dict:
    """
    takes in a population DataFrame and returns a dictionary of the population age band for a certain area code
    in a certain YEAR
    """
    cond = (df[Nom.AREA_CD] == area_code) & (df[Nom.DATE] == year)
    df_filt = df[cond]
    pop_youth = df_filt[df_filt[Pop.age_band] == AgeBands.youth][Nom.VALUE].sum()
    pop_working_age = df_filt[df_filt[Pop.age_band] == AgeBands.working_age][Nom.VALUE].sum()
    pop_retirement = df_filt[df_filt[Pop.age_band] == AgeBands.retirement][Nom.VALUE].sum()
    pop_band = {
        AgeBands.youth: pop_youth,
        AgeBands.working_age: pop_working_age,
        AgeBands.retirement: pop_retirement
    }
    logger.debug(f'pop bands {area_code}, {year}:\n{pop_band}')
    return pop_band


def add_pop_band_pct(struct, input_band: str, output_band: str) -> None:
    """
    for each area in struct takes in a band and returns it in pct format
    """
    for area in struct:
        area[output_band] = dict_value_pct(area[input_band])
        logger.debug(f'{area[Nom.AREA_NM]}, {area[output_band]}')


def dict_value_pct(data: Dict) -> Dict:
    return {k: round(v / sum(data.values()), 2) for k, v in data.items()}


def add_pop_chg(struct: List[Dict]) -> None:
    for area in struct:
        area[Pop.pop_chg] = area[Pop.total_pop] - area[Pop.total_pop_past]
        area[Pop.pop_chg_pct] = round(area[Pop.pop_chg] / area[Pop.total_pop_past], 2)
        logger.debug(f'adding pop chg {area[Nom.AREA_NM]}, {area[Pop.pop_chg]}, {area[Pop.pop_chg_pct]}')


def add_pop_chg_band(struct: List[Dict]) -> None:
    for area in struct:
        area[Pop.pop_bands_chg] = {k: v - area[Pop.pop_bands_past][k] for k, v in area[Pop.pop_bands].items()}
        area[Pop.pop_bands_chg_pct] = {k: round(v / area[Pop.pop_bands_past][k], 2) for k, v in area[Pop.pop_bands_chg].items()}
        logger.debug(f'adding pop chg band {area[Nom.AREA_NM]}, {area[Pop.pop_bands_chg]}, '
                     f'{area[Pop.pop_bands_chg_pct]}')


def pct(x) -> str:
    return f'{x:.0%}'


def num(x) -> str:
    if x > 100:
        x = round(x, 2 - len(str(int(x))))
    elif x < 100:
        x = round(x, 3 - len(str(int(x))))
    elif abs(x) > 10:
        x = round(x, -1)
    else:
        x = x
    x = int(round(x))
    return f'{x:,}'


def fmt_dict_values(d: Dict[str, float], fmt_pct=True) -> Dict[str, str]:
    for k, v in d.items():
        if fmt_pct == True:
            d[k] = pct(v)
        else:
            d[k] = num(v)
    return d


def is_large(test: bool) -> str:
    """
    returns either larger or smaller based on the value of the test
    """
    if test:
        return 'larger'
    else:
        return 'smaller'


def get_digits(text: str) -> str:
    """
    returns only the digits (and sign) from a string as a string
    """
    return ''.join([char for char in text if char in string.digits + '-'])


def str_pct_test(one: str, two: str) -> bool:
    """
    returns only the digits of a string and tests if one if bigger than two ie one > two
    """
    one_int = int(get_digits(one))
    two_int = int(get_digits(two))
    return one_int > two_int


def sort_by_first_col(df: pd.DataFrame) -> None:
    logger.debug('the df is: ')
    logger.debug(print(df))
    df.sort_values(df.columns[0], ascending=False, inplace=True)


def sort_drop_toplevel(df: pd.DataFrame, impact_areas: ImpactAreas) -> pd.DataFrame:
    df = df[impact_areas.area_codes]
    df.columns = df.columns.droplevel()
    logger.debug(f'ordering and dropping top column: \n{df.head()}')
    return df


def df_to_list_components(df: pd.DataFrame) -> Dict[str, List]:
    comps = {
        'cols': df.columns.tolist(),
        'index': df.index.tolist(),
        'data': df.values.tolist(),
    }
    logger.debug(f'list parts of df:\n{comps}')
    return comps


# aps related function

def filter_value_type(df: pd.DataFrame, type: str) -> pd.DataFrame:
    filt = df[df[Aps.VAL_TYPE] == type]
    logger.debug(f'filtering val type: \n{filt.head()}')
    return filt


def get_datetime(df: pd.DataFrame) -> None:
    """
    convert the end of the aps style date to datetime format
    """
    df[Aps.END_DATE] = df[Aps.DATE].str.split('-').str[-1]
    df[Aps.END_DATE] = pd.to_datetime(df[Aps.END_DATE])


def fmt_dt(dt: datetime) -> str:
    """
    format datetime to a string format
    """
    return datetime.strftime(dt, '%Y-%b')


