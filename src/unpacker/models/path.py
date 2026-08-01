<<<<<<< HEAD
from functools import cached_property
from typing import TypeVar

import superpathlib
from typing_extensions import Self

T = TypeVar("T", bound="Path")
=======
from typing import Self, cast

import superpathlib
from simple_classproperty import classproperty
>>>>>>> template


class Path(superpathlib.Path):
    @cached_property
    def with_clean_name(self) -> Self:
        clean_stem = self.stem.split(" (")[0]
        return self.with_stem(clean_stem)
