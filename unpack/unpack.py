import cli
import sys
from plib import Path


from libs.progressbar import ProgressBar


def unpack(folder):
    commands = {
        "unzip -q -o": ["zip"],
        "7za e": ["7z"],
        "tar -xf": ["gz", "tgz", "tar"],
        "unoconv -f pdf": ["pptx", "docx"]
    }
    command_mapper = {ext: cmd for cmd, exts in commands.items() for ext in exts}
    
    for path in folder.iterdir():
        if path.is_file():
            command = command_mapper.get(path.suffix[1:])
            if command:
                with ProgressBar("Unpacking.."):
                    new_parent = path.parent / path.stem
                    new_parent.mkdir(parents=True, exist_ok=True)
                    path = path.rename(new_parent / path.name)
                    cli.run(command, path, cwd=new_parent)
                    path.unlink()


def undouble(folder: Path):
    name_mapper = {}
    
    for path in folder.iterdir():
        if path.is_file():
            key = path.stem.split(" (")[0] + path.suffix
            name_mapper[key] = name_mapper.get(key, []) + [path]

    for unique, paths in name_mapper.items():
        paths = sorted(paths, key=lambda path: -path.mtime)
        for path in paths[1:]:
            cli.run('gio trash', path)

        paths[0].rename(folder / unique)


def main():
    with cli.errorhandler():
        folder = Path.cwd() if sys.stdin.isatty() else Path.docs
        unpack(folder)
        undouble(folder)


if __name__ == "__main__":
    main()
