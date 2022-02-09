import sys
import ijson

from urllib.request import urlopen

from typing import Iterable, List, Optional
from modules.constants import API_EXPORT_PACKAGES_URL
from modules.entities.package import Package
from modules.utils import check_existing_branches


class PackageFetcher:

    def check_branches(self, branches: List[str]) -> List[str]:
        """
        Method used for checking branches from web.

        Prevents us to request branch with incorrect name.

        Args:
            `branches: List[str]` - list of branches names

        Returns:
            `List[str]` - list of filtered correct and existed branches names from web
        """
        result_branches = []
        for br, exists in check_existing_branches(branches).items():
            if not exists:
                print(
                    f"Specified branch ({br}) is not found on repository, skipping\n")
                continue
            result_branches.append(br)

        if not result_branches:
            print("No branches found, exiting...")
            sys.exit()

        return result_branches

    def fetch(self, branches: Optional[List[str]] = None) -> Iterable[Package]:
        """
        Method used to fetch packages for specified branches from web.

        Args:
            `branches: List[str]` - list of branch names to fetch

        Returns: `Generator[Package]` - generator of fetched packages
        """
        if not branches:
            branches = []
        branches = self.check_branches(branches)
        for branch in branches:
            for idx, package in enumerate(
                ijson.items(
                    urlopen(API_EXPORT_PACKAGES_URL.format(branch=branch)),
                    'packages.item'
                )
            ):
                print(
                    f"[{idx + 1} packages] Fetching branch ({branch}) from web...",
                    end="\r")
                package = Package.from_dict(package)
                package.branch_name = branch
                yield package
            print("\nOk!")
