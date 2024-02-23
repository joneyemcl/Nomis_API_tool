"""
cleans the raw myede data into a structured format
"""

import logging

import pandas as pd

from definitions import Nom, Pop
from definitions import PathsFile, NomisAPI
from processing.cleaning_tools import import_tsv, import_nomis_API, merging_areacode, clean_area, clean_age, fix_meyede_col_names

logger = logging.getLogger(__name__)

# pandas display settings
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)


# functions specific to myede cleaning
def select_cols_myede(df: pd.DataFrame) -> pd.DataFrame:
    logger.debug('selecting myede columns from: ')
    logger.debug(f'\n{df.columns}')
    logger.debug(f'\n{df.head()}')
    df = df[[Nom.DATE, Nom.TYPE, Nom.AREA_NM, Nom.AREA_CD, Pop.age, Pop.value, 'age_band']]
    logger.debug(f'\n{df.head()}')
    return df


# importing and cleaning myede data
"""
legacy tsv import:
    myede = import_tsv(PathsFile.MYEDE_TSV)
"""
myede = import_nomis_API(NomisAPI.myede_api)
myede = merging_areacode(myede)
#clean_area(myede)
fix_meyede_col_names(myede)
myede = clean_age(myede)
myede = select_cols_myede(myede)

