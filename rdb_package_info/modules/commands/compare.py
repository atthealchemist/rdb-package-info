import json
from typing import Dict, List, Sequence
from rdb_package_info.modules.commands.base import BaseCommand
from rdb_package_info.modules.comparator import (
    ExistsOnlyComparator, BranchPackageVersionComparator
)

from rdb_package_info.modules.fetcher import PackageFetcher


class CompareBranchesCommand(BaseCommand):
    """
    Comparing branches command.
    """

    def print_comparisons(self, comparisons: Sequence[Dict]):
        """
        Method prints comparison results to console.

        Args:
            `comparisons: Sequence[Dict]` - list of comparison results
        """
        print("Performed next comparisons: ")
        for idx, comp in enumerate(comparisons):
            print(
                f"{idx + 1}. {comp.get('title')} -> {comp.get('count')} pkgs"
            )

    def write_file(self,
                   comparisons: Sequence[Dict],
                   filename: str = "result.rdb-comparison.json"):
        """
        Method writes comparison results to json file.

        Args:
            `comparisons: Sequence[Dict]` - list of comparison results
            `filename: str` - filename of result file
        """
        with open(filename, "w") as json_file:
            json_file.write(json.dumps(comparisons))
            print(f"Writed comparisons result @ {filename}")

    def process(self, args: List[str]) -> None:
        """
        Method performs next checks
        and writes results in `result.rdb-comparison.json` file:
            - packages only in p10
            - packages only in sisyphus
            - packages with greatest version in sisyphus
        """
        all_packages = list(PackageFetcher().fetch(
            branches=['p10', 'sisyphus']
        ))

        comparisons = (
            ExistsOnlyComparator(
                packages=all_packages,
                source_branch_name="p10"
            ).compare().as_dict(),
            ExistsOnlyComparator(
                packages=all_packages,
                source_branch_name="sisyphus"
            ).compare().as_dict(),
            BranchPackageVersionComparator(
                packages=all_packages,
                source_branch_name="sisyphus"
            ).compare().as_dict()
        )

        self.print_comparisons(comparisons)
        self.write_file(comparisons)
