from functools import cached_property
from typing import TypeVar

import superpathlib

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @cached_property
    def with_clean_name(self: T) -> T:
        clean_stem = self.stem.split(" (")[0]
        return self.with_stem(clean_stem)
