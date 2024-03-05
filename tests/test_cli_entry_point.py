from package_dev_utils.tests.args import no_cli_args
from unpacker import cli


@no_cli_args
def test_entry_point(working_directory: None) -> None:
    cli.entry_point()
