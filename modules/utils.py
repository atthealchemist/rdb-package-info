import requests

from typing import Dict, List, Optional, Tuple, Union
from string import ascii_letters, punctuation

from modules.constants import API_BRANCHES_LIST_URL


def parse_package_version(version: str) -> Tuple[Union[int, str], ...]:
    """
    Method used for parsing package version to more convenient tuple
    of strings and ints.

    Allows us to compare package versions.

    Args:
        `version: str` - string version of package
    Returns:
        `VersionTuple` - tuple contains integers and strings of version.

    Example:
        "4.1b" -> (4, 1, 'b')
    """
    replacements = version.maketrans(punctuation, "." * len(punctuation))
    version = version.translate(replacements)

    result_version = []
    for index in version.split('.'):
        if any(letter for letter in ascii_letters if letter in index):
            result_version.extend(index)
        else:
            result_version.append(int(index))

    return tuple(map(lambda i: int(i) if str(i).isdigit() else i, result_version))


def get_available_branches() -> List[Optional[str]]:
    """
    Method used for fetching existings branches from web api.

    Returns:
        `List[str]` - lists of branches names, if got response from web api.
        Otherwise empty list.
    """
    branches = []
    response = requests.get(API_BRANCHES_LIST_URL)
    if response.status_code == 200:
        response_dict = response.json()
        branches = [
            entry.get('branch')
            for entry in response_dict.get('branches')
        ]
    return branches


def check_existing_branches(branches: List[str]) -> Dict[str, bool]:
    """
    Method used for checking branches on availability from web api.

    Args:
        `branches: List[str]` - list of supposed branch names

    Returns:
        `Dict[str, bool]` - dictionary contains name of branch and it
        availability (`True` by default)
    """
    available_branches = get_available_branches()
    check_results = {
        branch: branch in available_branches
        for branch in branches
    }
    return check_results
