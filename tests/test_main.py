import io
import string
import zipfile
from unittest.mock import MagicMock, patch

from hypothesis import HealthCheck, given, settings, strategies
from unpacker.main.main import Unpacker
from unpacker.models import Path

disable_function_scoped_fixture_check = settings(
    suppress_health_check=(HealthCheck.function_scoped_fixture,)
)


def test_main(folder: Path) -> None:
    unpacker = Unpacker(folder)
    unpacker.run()


@patch("cli.run")
@disable_function_scoped_fixture_check
@given(name=strategies.text(alphabet=string.ascii_letters))
def test_remove_duplicates(_: MagicMock, folder: Path, name: str) -> None:
    create_duplicates(folder, name)
    unpacker = Unpacker(folder)
    unpacker.run()


def create_duplicates(folder: Path, name: str) -> None:
    path = folder / name
    path.touch()
    for _ in range(2):
        duplicate_path = path.with_nonexistent_name()
        duplicate_path.touch()


@disable_function_scoped_fixture_check
@given(
    content=strategies.binary(),
    name=strategies.text(alphabet=string.ascii_letters, min_size=1),
)
def test_unpack_archive(folder_on_disk: Path, name: str, content: bytes) -> None:
    create_zipfile(folder_on_disk, name, content)
    unpacker = Unpacker(folder_on_disk)
    unpacker.run()


def create_zipfile(folder: Path, name: str, content: bytes) -> None:
    content = create_zipped_content(name, content)
    path = folder / name
    path = path.with_suffix(".zip")
    path.byte_content = content


def create_zipped_content(name: str, content: bytes) -> bytes:
    file_object = io.BytesIO()
    zip_object = zipfile.ZipFile(file_object, "w")
    with zip_object:
        zip_object.writestr(name, content)
    file_object.seek(0)
    return file_object.getvalue()


@disable_function_scoped_fixture_check
@given(name=strategies.text(alphabet=string.ascii_letters, min_size=1))
def test_pdf_conversion(folder: Path, name: str) -> None:
    path = folder / name
    path = path.with_suffix(".docx")
    path.touch()
    unpacker = Unpacker(folder)
    with patch("cli.run") as mock_run:
        unpacker.run()
    mock_run.assert_called_once()
