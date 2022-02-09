import attr

from typing import Dict, Tuple, Union
from typing_extensions import TypeAlias

from modules.entities.architecture import Architecture
from modules.utils import parse_package_version

VersionTuple: TypeAlias = Tuple[Union[str, int], ...]


@attr.s(auto_attribs=True)
class Package:
    """
    Base package structure.
    Contains information about package.

    Attrubutes:
        `name: str` - package name, as it should be named in repository
        `branch_name: str` - branch of specific package
            (they're could be slightly different for branches imo)
        `epoch: int` - package generation (maybe?). 0 by default.
        `version: str` - package version
        `parsed_version: VersionTuple` - package version parsed to tuple
            (for comparing)
        `release: str` - specific release distro version
        `arch: Architecture` - package architecture
        `disttag: str` - specific subversion for concrete distro
        `buildtime: int` - package build time
        `source: str` - package parent. Same as name if package have no parent.
    """
    name: str
    version: str
    parsed_version: VersionTuple
    release: str
    arch: Architecture
    disttag: str
    buildtime: int
    source: str
    epoch: int = 0
    branch_name: str = ""

    @classmethod
    def from_dict(cls, package: Dict) -> "Package":
        """
        Class method creates package object from json response item

        Args:
            `package: Dict` - json response item of package.

        Returns:
            `Package` - constructed package object.
        """
        try:
            version = package.get('version', "")
            if version:
                package['parsed_version'] = parse_package_version(version)
        except ValueError:
            print("Can't parse version of package, skipping...")
            package['parsed_version'] = (0, 0, 0)
        return cls(**package)

    def as_dict(self) -> Dict:
        """
        Dict representation of package object.

        Returns: `Dict`
        """
        return attr.asdict(self)

    def __str__(self) -> str:
        """
        String representation of package.
        """
        package_repr = f"{self.name}:{self.arch}={self.version}"
        if self.disttag:
            package_repr += f" ({self.disttag})"
        if self.source and self.source != self.name:
            package_repr += f" [parent: {self.source}]"
        return package_repr
