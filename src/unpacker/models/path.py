from functools import cached_property
from typing import TypeVar

import superpathlib
<<<<<<< HEAD
=======
from simple_classproperty import classproperty
from typing_extensions import Self
>>>>>>> template

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
<<<<<<< HEAD
    @cached_property
    def with_clean_name(self: T) -> T:
        clean_stem = self.stem.split(" (")[0]
        return self.with_stem(clean_stem)
=======
    @classmethod
    @classproperty
    def source_root(cls) -> Self:
        return cls(__file__).parent.parent

    @classmethod
    @classproperty
    def assets(cls) -> Self:
        path = cls.script_assets / cls.source_root.name
        return cast("Self", path)

    @classmethod
    @classproperty
    def config(cls) -> Self:
        path = cls.assets / "config" / "config.yaml"
        return cast("Self", path)
>>>>>>> template
