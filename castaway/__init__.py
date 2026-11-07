#!/usr/bin/env python3
"""Discover files outside your Homeshick castles."""

__version__ = "1.0"

from collections.abc import Callable, Iterable, Iterator
import os
import shlex
import subprocess
from pathlib import Path

from pathspec import GitIgnoreSpec


home = Path.home()
config_home = Path(os.environ.get("XDG_CONFIG_HOME", home/".config")).expanduser().resolve()

SEARCH_PATHS = (config_home, )  # you may also add home/".local/share"


def tracked_in(castle: Path|str) -> Iterator[str]:
    return (
        os.fsdecode(path).removeprefix("home/")
        for path in subprocess.run(
            ["git", "-C", str(castle), "ls-files", "-z", "--", "home/"],
            capture_output=True
        ).stdout.split(b"\0")
        if path
    )


def tracked_in_all(castles: Path) -> set[str]:
    return {
        path
        for castle in castles.iterdir()
        for path in tracked_in(castle)
    }


def untracked_in(
        folder: Path,
        tracked: set[str], ignored: Callable[[str], bool],
        max_depth: int) -> set[str]:
    return {
        file
        for file in regular_files(folder, max_depth)
        if file not in tracked and not ignored(file)
    }


def get_ignore_spec():
    ignore_file = config_home/"castaway.ignore"
    if ignore_file.exists():
        content = ignore_file.read_text()
    else:
        content = Path(__file__).with_name("default.ignore").read_text()
        ignore_file.write_text(content)
        
    return GitIgnoreSpec.from_lines(content.splitlines())


def untracked_in_all(folders: Iterable[Path]) -> list[str]:
    castles = home/".homesick/repos"
    tracked = tracked_in_all(castles)

    ignore_spec = get_ignore_spec()

    max_depth = int(os.environ.get('CASTAWAY_MAX_DEPTH', "3"))

    return sorted({
        file
        for folder in folders
        for file in untracked_in(
            folder, tracked, ignore_spec.match_file, max_depth
        )
    })


def regular_files(root: Path, max_depth: int) -> Iterator[str]:
    for current, dirs, files in root.walk(follow_symlinks=False):
        depth = len(current.relative_to(root).parts)
        if depth + 1 >= max_depth:
            dirs[:] = []
        for name in files:
            file = current/name
            if file.is_file(follow_symlinks=False):
                yield file.relative_to(home).as_posix()


def main():
    for path in untracked_in_all(SEARCH_PATHS):
        print(shlex.quote(path))


if __name__ == "__main__":
    main()
