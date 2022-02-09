import itertools

from abc import ABCMeta, abstractmethod
from typing import Dict, Sequence, Tuple
from modules.entities.comparison import Comparison
from modules.entities.package import Package, VersionTuple


class Comparator(metaclass=ABCMeta):
    """
    Base comparator class.

    Attributes:
        `packages: Sequence[Package]` - list of packages
        `source_branch_name: str` - branch name need to compare
    """

    def __init__(self, packages: Sequence[Package], source_branch_name: str):
        self.packages = packages
        self.source = sorted(
            [p for p in self.packages if p.branch_name == source_branch_name],
            key=lambda i: i.name
        )
        self.source_branch_name = source_branch_name

    @abstractmethod
    def compare(self) -> Comparison:
        """
        Method that performs specific comparison.
        Should be overrided for subclasses.

        Returns:
            `Comparison` - comparison result object.
        """
        pass


class ExistsOnlyComparator(Comparator):

    def compare(self) -> Comparison:
        source_names = {f"{p.name}:{p.arch}={p.version}" for p in self.source}
        all_names = {
            f"{s.name}:{s.arch}={s.version}" for s in self.packages
        }

        source_only_names = all_names - source_names

        source_only_packages = [
            p for p in self.packages
            if f"{p.name}:{p.arch}={p.version}" in source_only_names
        ]

        return Comparison(
            title="Packages exists in {source} only".format(
                source=self.source_branch_name
            ),
            packages=source_only_packages,
            count=len(source_only_packages)
        )


class BranchPackageVersionComparator(Comparator):

    def group_by_versions(self) -> Sequence[Dict]:
        all_packages = self.packages
        result = dict()
        for package_name, packages in itertools.groupby(
            all_packages, key=lambda i: i.name
        ):
            if package_name not in result:
                result[package_name] = dict(
                    name=package_name,
                    versions=dict(),
                    greatest=dict()
                )
            for branch, branch_packages in itertools.groupby(
                packages, key=lambda i: i.branch_name
            ):
                for package in branch_packages:
                    result[package_name]["versions"][branch] = package.parsed_version
        for package in result.values():
            if len(package['versions']) > 1:
                first, second = package['versions'].items()
                package.update(self.compare_versions(first, second))
        return list(result.values())

    def compare_versions(
        self,
        first_version: Tuple[str, VersionTuple],
        second_version: Tuple[str, VersionTuple]
    ):
        items = [first_version, second_version]
        first = tuple(i for i in first_version[1] if str(i).isdigit())
        second = tuple(i for i in second_version[1] if str(i).isdigit())
        greatest_index = 0
        if first < second:
            greatest_index = 1
        branch, version = items[greatest_index]
        return {
            'greatest': {branch: version}
        }

    def compare(self) -> Comparison:
        grouped_packages = self.group_by_versions()

        greatest_source_packages = [
            package
            for package in grouped_packages
            if all((
                len(package['versions']) > 1,
                'greatest' in package,
                self.source_branch_name in package['greatest']
            ))
        ]

        return Comparison(
            title="Packages with greatest version in {source} only".format(
                source=self.source_branch_name
            ),
            packages=greatest_source_packages,
            count=len(greatest_source_packages)
        )
