import pytest

from rdb_package_info.modules.entities.package import Package
from rdb_package_info.modules.utils import parse_package_version


@pytest.fixture
def package_factory():
    def new(**params):
        package_info = dict(
            name="test_package",
            branch_name="test_branch",
            version="0.0.1",
            parsed_version=(0, 0, 1),
            release="alt1",
            arch="x86_64",
            disttag="dfsg1",
            buildtime=123456,
            source="test_package",
            epoch=0
        )
        package_info.update(params)
        package_info['parsed_version'] = parse_package_version(
            package_info['version']
        )
        return Package(**package_info)
    return new
