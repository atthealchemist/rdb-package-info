import attr

from typing import Dict, Sequence, Union
from rdb_package_info.modules.entities.package import Package


@attr.s(auto_attribs=True)
class Comparison:
    """
    Comparison result object.
    Used for grouping result of comparison.

    Attributes:
        `title: str` - title of comparison result. Simple user-defined label.
        `packages: Sequence[Package | Dict]` - list of resulted packages
        `count: int` - count of resulted packages
    """
    title: str
    packages: Sequence[Union[Package, Dict]]
    count: int

    def as_dict(self) -> Dict:
        """
        Converts result object to dict representation.

        Returns:
            `Dict` - dict representation of result object.
        """
        return dict(
            title=self.title,
            count=self.count,
            packages=[
                p if isinstance(p, dict) else p.as_dict()
                for p in self.packages
            ]
        )
