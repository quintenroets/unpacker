import os
from collections.abc import Iterator

import pytest

from unpacker.models import Path


@pytest.fixture
def folder_on_disk() -> Iterator[Path]:
    path = Path.tempdir(in_memory=False)
    with path:
        yield path


@pytest.fixture
def folder() -> Iterator[Path]:
    path = Path.tempdir()
    with path:
        yield path


@pytest.fixture
def _working_directory(folder: Path) -> Iterator[None]:
    cwd = Path.cwd()
    os.chdir(folder)
    yield
    os.chdir(cwd)
