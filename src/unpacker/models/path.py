from functools import cached_property
from typing import TypeVar

import superpathlib
from typing_extensions import Self

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @cached_property
    def with_clean_name(self) -> Self:
        clean_stem = self.stem.split(" (")[0]
        return self.with_stem(clean_stem)
