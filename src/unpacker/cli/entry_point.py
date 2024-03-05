from package_utils.cli import create_entry_point

from unpacker.main.main import Unpacker

entry_point = create_entry_point(Unpacker.run, Unpacker)
