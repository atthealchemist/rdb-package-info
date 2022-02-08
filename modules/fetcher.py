import requests

from typing import Dict, List
from modules.constants import API_EXPORT_PACKAGES_URL


class PackageListFetcher:

    def __init__(self, branches: List[str]) -> None:
        self.branches = branches
  
    def fetch_one(self, branch_name: str) -> Dict:
        response = requests.get(
            API_EXPORT_PACKAGES_URL.format(branch=branch_name)
        )
        if response.status_code == 200:
            return response.json()

    def fetch(self) -> List[Dict]:
        print("Fetching data from server...")
        for branch in self.branches:
            yield self.fetch_one(branch)
        print("Ok!")
