import attr
from typing import Optional
from enum import Enum


class Architectures(Enum):
    """
    Available package architectures.

    Attrubutes:
        `aarch64` - ARM 64-bit architecture.

        `i586` - PC 32-bit (x86) architecture. Also could be named as i386.

        `x86_64` - PC 64-bit (x64) architecture. Also could be named as amd64.

        `ppc64le` - PowerPC 64-bit architecture (little-endian)

        `noarch` - No (or universal) architecture. Used when package could not be bounded to specific architecture.

    """

    AARCH64 = "aarch64"
    I586 = "i586"
    X86_64 = "x86_64"
    PPC64LE = "ppc64le"
    NOARCH = "noarch"
    ARMH = "armh"

    @classmethod
    def from_string(cls, source: str) -> Optional["Architectures"]:
        """
        Class method that sets up architecture enum from it value.
        """
        return cls[source.upper()] or None

    def __str__(self) -> str:
        """
        String representation of enum.
        Simply returns a value.
        """
        return self.value


@attr.s(auto_attribs=True)
class Architecture:
    target: Optional[Architectures]
    additional: Optional[Architectures] = None

    @classmethod
    def from_string(cls, src: str) -> "Architecture":
        """
        Class method that creates architecture object from string

        Returns:
            `Architecture` - architecture object.
        """
        if '-' in src:
            target, additional = src.split('-')
            return cls(
                target=Architectures.from_string(target),
                additional=Architectures.from_string(additional)
            )
        return cls(target=Architectures.from_string(src))

    def __str__(self) -> str:
        """
        String representation of architecture object.
        """
        if self.additional:
            return f"{self.target}-{self.additional}"
        return str(self.target)
