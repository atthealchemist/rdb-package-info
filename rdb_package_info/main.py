from rdb_package_info.modules.commands.compare import CompareBranchesCommand


def main():
    command = CompareBranchesCommand()
    command.process(args=[])


if __name__ == "__main__":
    main()
