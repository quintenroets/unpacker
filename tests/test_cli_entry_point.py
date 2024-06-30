import pytest
from package_dev_utils.tests.args import no_cli_args
from unpacker import cli


@no_cli_args
@pytest.mark.usefixtures("_working_directory")
def test_entry_point() -> None:
    cli.entry_point()
