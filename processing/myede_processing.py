"""
1. takes in the cleaned data generates the required statistics for populate the word template
2. generates the conditions that dictate which text is included in the word template
3. populates the text with the generated statistics
4. populates the word document
"""

import logging
import pprint
from typing import Dict

import pandas as pd

from definitions import Nom, Pop
from impact_areas import ImpactAreas
from processing.myede_cleaning import myede
from processing.processing_tools import (
    add_to_struct_by_area_code,
    get_total_population,
    get_population_bands,
    add_pop_chg,
    add_pop_chg_band,
    pct,
    num,
    fmt_dict_values,
    get_start_less_ten_years,
    filter_and_save,
    add_pop_band_pct,
)

logger = logging.getLogger(__name__)


def get_struct(impact_areas: ImpactAreas):
    return impact_areas.new_dict_struct()


year_recent, year_less_ten = get_start_less_ten_years(myede[Nom.DATE])


def myede_calculations(struct, impact_areas):
    # total population
    add_to_struct_by_area_code(struct, 'total_pop', get_total_population, impact_areas, myede, year_recent)
    add_to_struct_by_area_code(struct, 'total_pop_past', get_total_population, impact_areas, myede, year_less_ten)

    # population by age band
    add_to_struct_by_area_code(struct, Pop.pop_bands, get_population_bands, impact_areas, myede, year_recent)
    add_to_struct_by_area_code(struct, Pop.pop_bands_past, get_population_bands, impact_areas, myede, year_less_ten)

    # working age population pct
    add_pop_band_pct(struct, Pop.pop_bands, Pop.pop_bands_pct)

    # chg pop, chg pop pct
    add_pop_chg(struct)

    # chg pop for each age band
    add_pop_chg_band(struct)
    logger.debug(f'calculations (myede) complete:\n{pprint.pformat(struct)}')

    return struct


def myede_formatting(struct):
    """
    formatting the struct values into pct or number format
    """
    for area in struct:
        # formatting single numbers
        area[Pop.total_pop] = num(area[Pop.total_pop])
        area[Pop.pop_chg] = num(area[Pop.pop_chg])
        area[Pop.pop_chg_pct] = pct(area[Pop.pop_chg_pct])
    logger.debug(f'formatting single numbers in progress:\n{pprint.pformat(struct)}')

    for area in struct:
        # formatting numbers stored in age bands
        area[Pop.pop_bands] = fmt_dict_values(area[Pop.pop_bands], fmt_pct=False)
        area[Pop.pop_bands_pct] = fmt_dict_values(area[Pop.pop_bands_pct])
        area[Pop.pop_bands_chg_pct] = fmt_dict_values(area[Pop.pop_bands_chg_pct])
    logger.debug(f'formatting age band numbers in progress:\n{pprint.pformat(struct)}')

    return struct


def myede_unpacking_variables(struct: pd.DataFrame):
    """
    unpacking relevant variables into a dictionary
    """
    ia, bmi, bmii = struct

    # population broken down by age band
    _, ia_wa, ia_ra = ia[Pop.pop_bands_pct].values()
    _, bmi_wa, bmi_ra = bmi[Pop.pop_bands_pct].values()
    _, bmii_wa, bmii_ra = bmii[Pop.pop_bands_pct].values()

    # pct change in population by age band
    _, ia_gr_wa, ia_gr_ra = ia[Pop.pop_bands_chg_pct].values()
    _, bmi_gr_wa, bmi_gr_ra = bmi[Pop.pop_bands_chg_pct].values()
    _, bmii_gr_wa, bmii_gr_ra = bmii[Pop.pop_bands_chg_pct].values()

    var = {
        'ia_wa': ia_wa,
        'ia_ra': ia_ra,
        'bmi_wa': bmi_wa,
        'bmi_ra': bmi_ra,
        'bmii_wa': bmii_wa,
        'bmii_ra': bmii_ra,
        'ia_gr_wa': ia_gr_wa,
        'ia_gr_ra': ia_gr_ra,
        'bmi_gr_wa': bmi_gr_wa,
        'bmi_gr_ra': bmi_gr_ra,
        'bmii_gr_wa': bmii_gr_wa,
        'bmii_gr_ra': bmii_gr_ra,
        'ia_pop': ia[Pop.total_pop],
        'ia_pop_chg': ia[Pop.pop_chg_pct],
        'bmii_pop_chg': bmii[Pop.pop_chg_pct],
    }

    logging.debug(f'myede unpacked variables {var}')
    return var


def myede_get_conditions(ia_wa, ia_ra, ia_gr_ra, bmi_wa, bmii_wa, bmi_ra, bmii_ra, bmii_gr_wa, bmii_gr_ra,
                         ia_gr_wa, ia_pop_chg, bmii_pop_chg, **kwargs) -> Dict[str, bool]:
    """
    creating the conditions that determine which text populates the word document
    """
    
    test_wa_bmi = ia_wa > bmi_wa
    test_wa_bmii = ia_wa > bmii_wa
    test_ra_bmi = ia_ra > bmi_ra
    test_ra_bmii = ia_ra > bmii_ra

    cond = {
        'test_wa_bmi': test_wa_bmi,
        'test_wa_bmii': test_wa_bmii,
        'test_wa': test_wa_bmi == test_wa_bmii,
        'test_ra_bmi': test_ra_bmi,
        'test_ra_bmii': test_ra_bmii,
        'test_ra': test_ra_bmi == test_ra_bmii,
        'test_gr': ia_pop_chg > bmii_pop_chg,
        'test_gr_wa': ia_gr_wa > bmii_gr_wa,
        'test_gr_ra': ia_gr_ra > bmii_gr_ra,
    }
    logging.debug(f'myede conditions {cond}')
    return cond


# this function if way to big and should be broken up at some point
def get_doc_inputs(struct, impact_areas: ImpactAreas, ia_wa, ia_ra, bmi_wa, bmi_ra, bmii_wa,
                   bmii_ra, ia_gr_wa, bmii_gr_wa, test_wa_bmi, test_wa_bmii, test_wa, test_ra_bmi, test_ra_bmii,
                   test_ra, test_gr, test_gr_wa, test_gr_ra, ia_pop, ia_pop_chg, bmii_pop_chg, **kwargs) -> Dict:
    """
    creating the conditions which determine which text populates the word template
    """

    text_0_0 = (
        f'The latest {year_recent} ONS Population Estimates shows '
        f'that the population of {impact_areas.impact_area} is around {ia_pop}. ')

    # working age population selecting and populating the text
    if ia_wa == bmi_wa == bmii_wa:  # if ia & region & national the same
        text_0_1 = (f"{impact_areas.impact_area} has a proportion of working age residents inline with the "
                    f"regional and national position ({ia_wa}). ")
    elif ia_wa == bmi_wa != bmii_wa:  # if ia & region the same and national different
        text_0_1 = (f"{impact_areas.impact_area} has a proportion of working age residents inline with the regional "
                    f"position ({ia_wa}) but {'larger' if test_wa_bmii else 'smaller'} than the national position "
                    f"({bmii_wa}). ")
    elif ia_wa == bmii_wa != bmi_wa:  # if ia & national the same but regional different
        text_0_1 = (f"{impact_areas.impact_area} has a proportion of working age residents inline with the national "
                    f"position ({ia_wa}) but {'larger' if test_wa_bmi else 'smaller'} than the regional position ({bmi_wa}). ")
    elif (ia_wa != bmi_wa) and (ia_wa != bmii_wa):  # if ia different to regional and national
        if test_wa:  # weather ia greater or lesser than both region and national
            text_0_1 = (f'{impact_areas.impact_area} has a relatively {"large" if test_wa_bmii else "small"} working age population ({ia_wa}) '
                        f'compared to the regional ({bmi_wa}) and national position ({bmii_wa}). ')
        else:
            text_0_1 = (f'{impact_areas.impact_area} has a {"large" if test_wa_bmi else "small"} working age population ({ia_wa}) compared '
                        f'to the region ({bmi_wa}) and a {"larger" if test_wa_bmii else "smaller"} working a compared to '
                        f'the national position ({bmii_wa}). ')

    # retirement age population selecting and populating text
    if (ia_ra == bmi_ra) and (ia_ra == bmii_ra):  # if ia & region & national the same
        text_0_2 = (
            f"Additionally, {impact_areas.impact_area} has a proportion of retirement age residents inline with "
            f"the regional and national position ({ia_ra}). ")
    elif (ia_ra == bmi_ra) and (ia_ra != bmii_ra):  # if ia & region the same and national different
        text_0_2 = (
            f'Additionally, {impact_areas.impact_area} has a proportion of retirement age residents inline with '
            f'the regional position ({ia_ra}) but {"larger" if test_ra_bmii else "smaller"} than the national '
            f'position ({bmii_ra}). ')
    elif (ia_ra != bmi_ra) and (ia_ra == bmii_ra):  # if ia & national the same but regional different
        text_0_2 = (
            f"Additionally, {impact_areas.impact_area} has a proportion of retirement age residents inline with "
            f'the national position ({ia_ra}) but {"larger" if test_ra_bmi else "smaller"} than the regional '
            f'position ({bmi_ra}). ')
    elif (ia_ra != bmi_ra) and (ia_ra != bmii_ra):  # if ia & regional and national different
        if test_ra:  # weather ia greater or lesser than both region and national
            text_0_2 = (
                f'Additionally, {impact_areas.impact_area} has a relatively ' 
                f'{"large" if test_ra_bmi and test_ra_bmii else "small"} retirement age populaiton '
                f'({ia_ra}) compared to regional ({bmi_ra}) and national benchmarks ({bmii_ra}). ')
        else:
            text_0_2 = (
                f'Additionally, {impact_areas.impact_area} has a {"large" if test_ra_bmi else "small"} retirement '
                f'age populaiton ({ia_ra})compared to region ({bmi_ra}) and a '
                f'{"larger" if test_ra_bmii else "smaller"} retirement age population than {impact_areas.country} '
                f'({bmii_ra}). ')

    # change in population selecting and populating text
    if ia_pop_chg == bmii_pop_chg:
        text_2_0 = (
            f'{impact_areas.impact_area} has experienced similar growth in population over the past 10 years compared to '
            f'{impact_areas.country} ({ia_pop_chg} vs {bmii_pop_chg}). '
        )
    else:
        text_2_0 = (
            f'{impact_areas.impact_area} has experienced {"higher" if test_gr else "lower"} than average growth in '
            f'population over the past 10 years compared to {impact_areas.country} ({ia_pop_chg} vs '
            f'{bmii_pop_chg}). '
        )

    if ia_gr_wa == bmii_gr_wa:  # if growth in the ia wa population equals growth of national wa population
        text_2_1 = (
            f'{impact_areas.impact_area} has experienced similar levels growth in it\'s working age population compared to '
            f'the national position ({bmii_gr_wa}). The change in the retirement age population has been '
            f'{"higher" if test_gr_ra else "lower"} in {impact_areas.impact_area} compared to {impact_areas.country}.'
        )
    else:
        text_2_1 = (
            f'In contrast to the national position, a larger proportion of the population growth has been driven by the '
            f'{"working" if test_gr_wa else "non-working"} age populaiton. The change in the retirement age population '
            f'has been {"higher" if test_gr_ra else "lower"} in {impact_areas.impact_area} compared to '
            f'{impact_areas.country}.'
        )

    # combining the first string with working and retirment age condition
    text_0 = text_0_0 + text_0_1 + text_0_2
    logger.debug(pprint.pformat(f'this is text_0 populated:\n{text_0}'))
    text_1 = text_2_0 + text_2_1
    logger.debug(pprint.pformat(f'this is text_1 populated:\n{text_1}'))

    # getting table data and transposing it
    table_pct_chg = [list(area[Pop.pop_bands_chg_pct].values()) for area in struct]
    logger.debug(f'list table of pop chg by band: {table_pct_chg}')
    table_pct_chg = list(map(list, zip(*table_pct_chg)))
    logger.debug(f'list table transposed: {table_pct_chg}')

    doc_inputs = {
        'text_0': text_0,
        'text_1': text_1,
        'table_pct_chg': table_pct_chg,
    }

    return doc_inputs


def myede_processing(impact_areas: ImpactAreas, writer: pd.ExcelWriter):
    struct = get_struct(impact_areas)
    filter_and_save(myede, writer, 'myede', impact_areas)
    struct = myede_calculations(struct, impact_areas)
    var = myede_unpacking_variables(struct)
    cond = myede_get_conditions(**var)
    struct = myede_formatting(struct)
    var_fmt = myede_unpacking_variables(struct)
    return get_doc_inputs(struct, impact_areas, **var_fmt, **cond)

