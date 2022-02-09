from modules.entities.architecture import Architectures
from modules.entities.comparison import Comparison
from modules.comparator import ExistsOnlyComparator, BranchPackageVersionComparator


class TestComparators:

    def test_exist_only_comparator(self, package_factory):
        all_packages = (
            package_factory(name="p1", arch=Architectures.I586,
                            branch_name="p10"),
            package_factory(name="p2", branch_name="p10"),
            package_factory(name="s1", branch_name="p10"),
            package_factory(name="s2", branch_name="p10"),
            package_factory(name="s1", branch_name="sisyphus"),
            package_factory(name="s2", branch_name="sisyphus"),
            package_factory(name="p3", branch_name="sisyphus"),
        )

        comparator = ExistsOnlyComparator(
            packages=all_packages,
            source_branch_name="p10"
        )

        compare_result = comparator.compare()
        assert compare_result
        assert compare_result.count == 1

    def test_version_comparator(self, package_factory):
        all_packages = (
            package_factory(name="p1", version="1.0.1", arch=Architectures.I586,
                            branch_name="p10"),
            package_factory(name="p2", version="1.0.0", branch_name="p10"),
            package_factory(name="s1", version="1.1.1", branch_name="p10"),
            package_factory(name="s2", version="1.2.1", branch_name="p10"),
            package_factory(name="s1", version="1.1.2",
                            branch_name="sisyphus"),
            package_factory(name="s2", version="1.2.0",
                            branch_name="sisyphus"),
            package_factory(name="p3", version="1.2.2",
                            branch_name="sisyphus"),
        )

        comparator = BranchPackageVersionComparator(
            packages=all_packages,
            source_branch_name="sisyphus"
        )

        compare_result = comparator.compare()
        assert compare_result.count == 1

        # p10_names = {f"{p.name}:{p.arch}={p.version}" for p in all_packages if p.branch_name == "p10"}
        # sisyphus_names = {f"{s.name}:{s.arch}={s.version}" for s in all_packages if s.branch_name == "sisyphus"}

        # packages_in_p10_only = p10_names - sisyphus_names
        # packages_in_s_only = sisyphus_names - p10_names

        # p10_only_packages = [
        #     p for p in all_packages
        #     if f"{p.name}:{p.arch}={p.version}" in packages_in_p10_only
        # ]

        # p10_only_comparison = Comparison(
        #     title="Packages exists in p10 only",
        #     packages=p10_only_packages,
        #     count=len(p10_only_packages)
        # )

        # assert p10_only_comparison.count == 2

        # s_only_packages = [
        #     p for p in all_packages
        #     if f"{p.name}:{p.arch}={p.version}" in packages_in_s_only
        # ]
        # s_only_comparison = Comparison(
        #     title="Packages exists in p10 only",
        #     packages=s_only_packages,
        #     count=len(s_only_packages)
        # )

        # assert s_only_comparison.count == 1
