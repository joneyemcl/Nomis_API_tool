"""
Asks the users impact area of interest.
"""
import logging
from typing import List, Dict

from definitions import LookUp
from definitions import receptors
from impact_areas import load_lookup

logger = logging.getLogger(__name__)


def df_col_to_list_lower(col: str) -> List:
    logger.debug('reading csv into dataframe')
    df = load_lookup()
    ls = df[col].tolist()
    logger.debug('returning lower case list')
    return [item.lower() for item in ls]


def list_match_first_char(text: str, items: List) -> List[str]:
    """
    returns list of items where the first character matches the first character of a string
    """
    logger.debug('returning a list with first char match')
    return sorted([item.lower() for item in items if item[0] == text[0]])


def user_impact_area(area_criteria: List) -> str:
    """
    getting a valid local authority district from the user.
    """
    user_area: str = input('Please enter the name of a local authority: ')

    while user_area.lower() not in area_criteria:
        logger.debug(f'user entered invalid area {user_area}')
        print(f'\n{user_area} is not a valid local authority, did you mean any of the following?')
        for area in list_match_first_char(user_area, area_criteria):
            print(area)
        user_area = input('Please try again: ')

    print(f'\nYou selected {user_area}.')
    logger.debug(f'user successfully selected {user_area}')
    return user_area


def get_user_impact_area() -> str:
    lads_lower = df_col_to_list_lower(LookUp.LAD_NM)
    return user_impact_area(lads_lower)


def get_user_receptors() -> Dict:
    logging.debug('asking user which receptors to include')
    print('\nAvailable indicators will now be listed, to include an indicator enter "y" to exclude enter "n".')
    for k, v in receptors.items():
        user_choice = input(f'Do you want to include {v[0]}? ')
        while user_choice not in ['y', 'n']:
            logging.debug(f'incorrect choice entered {user_choice}')
            user_choice = input(f'Sorry {user_choice} is an invalid choice please enter "y" or "n"... ')
        receptors[k].append(user_choice)
        logging.debug(f'user selected {receptors[k]}')
    return receptors
