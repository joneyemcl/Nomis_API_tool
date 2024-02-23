"""
Takes the selected impact area from the Menu and returns a data structure with comparator areas
containing area name, area code, area name lower
"""

# imports
import os
import pandas as pd
import logging
from collections import namedtuple
from typing import List, Dict, NamedTuple

from definitions import PathsFile
from definitions import Nom, LookUp

logger = logging.getLogger(__file__)

# defining named tuple
ImpactArea = namedtuple('ImpactArea', 'area_name area_code area_name_lower')


def load_lookup() -> pd.DataFrame:
    """
    Load the ONS geography lookup
    """
    path_lookup = PathsFile.LOOKUP
    logging.debug(f'loading lookup dataframe with path {path_lookup}')
    return pd.read_csv(path_lookup, dtype=str)


def get_row(impact_area:str, lookup: pd.DataFrame):
    """
    Return the row of the lookup that corresponds to the user's selection
    """
    logging.debug('getting impact area row from dataframe')
    lookup['lad_lower'] = lookup[LookUp.LAD_NM].str.lower()
    return lookup[lookup['lad_lower'] == impact_area]


def assemble_areas_structure(lookup_flt) -> List[NamedTuple]:
    logging.debug('making named tuples for impact area and benchmarks')
    
    impact_area_lad = ImpactArea(
        lookup_flt[LookUp.LAD_NM].values[0],
        lookup_flt[LookUp.LAD_CD].values[0],
        lookup_flt[LookUp.LAD_NM].values[0].lower()
    )
    logging.debug(f'impact area: {impact_area_lad}')

    benchmark_rgn = ImpactArea(
        lookup_flt[LookUp.rgn_nm].values[0],
        lookup_flt[LookUp.rgn_cd].values[0],
        lookup_flt[LookUp.rgn_nm].values[0].lower()
    )
    logging.debug(f'impact area: {benchmark_rgn}')

    benchmark_ctry = ImpactArea(
        lookup_flt[LookUp.ctry_nm].values[0],
        lookup_flt[LookUp.ctry_cd].values[0],
        lookup_flt[LookUp.ctry_nm].values[0].lower()
    )
    logging.debug(f'impact area: {benchmark_ctry}')

    return [impact_area_lad, benchmark_rgn, benchmark_ctry]


def gen_impact_areas(impact_area: str) -> List[NamedTuple]:
    lookup = load_lookup()
    # logging.debug(f'this is the "lookup" variable {lookup}')
    
    lookup_flt = get_row(impact_area, lookup)
    return assemble_areas_structure(lookup_flt)


class ImpactAreas:
    """
    Creayes impact area struct and allows lists of any of the columns to be accessed as attributes of the class, also
    facilitates creation of dictionary struct
    """
    def __init__(self, impact_areas: List[NamedTuple]):
        self.struct = impact_areas

    @property
    def area_codes(self):
        return [area.area_code for area in self.struct]

    @property
    def area_names(self):
        return [area.area_name for area in self.struct]

    @property
    def impact_area(self):
        return self.area_names[0]

    @property
    def region(self):
        return self.area_names[1]

    @property
    def country(self):
        return self.area_names[2]

    @property
    def area_names_lower(self):
        return [area.area_name_lower for area in self.struct]

    def __repr__(self):
        return f'<{self.struct}>'

    def new_dict_struct(self) -> List[Dict]:
        new_struct = []
        for item in self.struct:
            new_struct.append({
                Nom.AREA_NM: item.area_name,
                Nom.AREA_CD: item.area_code,
                Nom.AREA_NM_LOWER: item.area_name_lower,
            })
        logger.debug(f'creating new struct from impact_areas:\n{new_struct}')
        return new_struct


