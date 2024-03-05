import sys
import typing
from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cached_property

import cli

from ..models import Path


@dataclass
class DuplicatedPaths:
    path: Path
    paths: list[Path] = field(default_factory=list)

    @cached_property
    def sorted_paths(self) -> list[Path]:
        return sorted(self.paths, key=lambda path: -path.mtime)

    def remove_duplicates(self) -> None:
        self.sorted_paths[0].rename(self.path)
        for path in self.sorted_paths[1:]:
            cli.run("gio trash", path)


@dataclass
class UnpackAction:
    command: str
    suffices: list[str]

    def run(self, path: Path) -> None:
        new_parent = path.parent / path.stem
        new_parent.mkdir(parents=True, exist_ok=True)
        new_path = new_parent / path.name
        path = path.rename(new_path)
        cli.run(self.command, path, cwd=new_parent)
        path.unlink()

    def check(self, path: Path) -> None:
        if path.suffix in self.suffices:
            self.run(path)


def extract_path() -> Path:
    return Path.cwd() if sys.stdin.isatty() else typing.cast(Path, Path.docs)


@dataclass
class Unpacker:
    folder: Path = field(default_factory=extract_path)

    def run(self) -> None:
        """
        Clean up working directory.
        """
        self.unpack_files()
        self.remove_duplicate_files()

    def unpack_files(self) -> None:
        unpack_actions = [
            UnpackAction("7za e", [".7z"]),
            UnpackAction("unoconv -f pdf", [".pptx", ".docx"]),
        ]
        for path in self.generate_files():
            path.unpack_if_archive()
            for unpack_action in unpack_actions:
                unpack_action.check(path)

    def remove_duplicate_files(self) -> None:
        paths_per_clean_path = self.calculate_paths_per_clean_path()
        for duplicated_paths in paths_per_clean_path.values():
            duplicated_paths.remove_duplicates()

    def calculate_paths_per_clean_path(self) -> dict[Path, DuplicatedPaths]:
        paths_per_clean_path = {}
        for path in self.generate_files():
            clean_path = path.with_clean_name
            if clean_path not in paths_per_clean_path:
                paths_per_clean_path[clean_path] = DuplicatedPaths(path.with_clean_name)
            paths_per_clean_path[clean_path].paths.append(path)
        return paths_per_clean_path

    def generate_files(self) -> Iterator[Path]:
        for path in self.folder.iterdir():
            if path.is_file():
                yield path
