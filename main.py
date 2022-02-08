from argparse import ArgumentParser
from typing import Dict

from modules.fetcher import PackageListFetcher


def parse_args():
    parser = ArgumentParser("rdb-package-info")
    # parser.add_argument_group("list")
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser("list", help="list packages")
    list_parser.add_argument("branches", nargs='+', help="included branches")
    # Все пакеты, version которых больше в sisyphus
    list_parser.add_argument("--version")

    return parser.parse_args()

def list_packages(branch: Dict) -> None:
    print(f"Branch: {branch.get('branch_name')}")
    packages = branch.get('packages')
    if not packages:
        return
    for package in packages:
        print(f"{package.get('name')}:{package.get('arch')}={package.get('version')}")


def main():
    args = parse_args()

    fetcher = PackageListFetcher(
        branches=args.branches
    )
    for branch in fetcher.fetch():
        list_packages(branch=branch)


if __name__ == "__main__":
    main()
