import os
from path import Path
import sys

from libs.cli import Cli
from libs.errorhandler import ErrorHandler
from libs.progressbar import ProgressBar

commands = {
    "unzip -q -o": ["zip"],
    "7za e": ["7z"],
    "tar -xf": ["gz", "tgz", "tar"],
    "unoconv -f pdf": ["pptx", "docx"]
}

def unpack(folder):
    command_mapper = {ext: cmd for cmd, exts in commands.items() for ext in exts}
    
    for path in folder.iterdir():
        if path.is_file():
            command = command_mapper.get(path.suffix[1:])
            if command:
                with ProgressBar("Unpacking.."):
                    new_parent = path.parent / path.stem
                    new_parent.mkdir(parents=True, exist_ok=True)
                    path = path.rename(new_parent / path.name)
                    Cli.run(f"{command} '{path}'", pwd=new_parent)
                    path.unlink()

def map_to_unique(path: Path):
    return path.stem.split(" (")[0] + path.suffix

def undouble(folder: Path):
    name_mapper = {}
    
    for path in folder.iterdir():
        if path.is_file():
            key = map_to_unique(path)
            name_mapper[key] = name_mapper.get(key, []) + [path]

    for unique, paths in name_mapper.items():
        paths = sorted(paths, key=lambda path: -path.stat().st_mtime)
        Cli.run(f'gio trash "{p}"' for p in paths[1:])

        paths[0].rename(folder / unique)

def main():
    with ErrorHandler():
        folder = Path(os.getcwd()) if sys.stdin.isatty() else Path.docs
        unpack(folder)
        undouble(folder)

if __name__ == "__main__":
    main()
