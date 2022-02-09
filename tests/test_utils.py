from modules.utils import parse_package_version


class TestUtils:

    def test_parse_package_version(self):
        assert parse_package_version("1.2.3") == (1, 2, 3)
        assert parse_package_version("0.165") == (0, 165)
        assert parse_package_version("0.12_62") == (0, 12, 62)
