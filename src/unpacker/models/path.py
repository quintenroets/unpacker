from functools import cached_property
from typing import Self

import superpathlib


class Path(superpathlib.Path):
    @cached_property
    def with_clean_name(self) -> Self:
        clean_stem = self.stem.split(" (")[0]
        return self.with_stem(clean_stem)
