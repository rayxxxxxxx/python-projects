import os
import argparse
from pathlib import Path
import re


def change_names_style(dirpath: Path, styler: object, rename_all: bool):
    dir_content = os.listdir(dirpath)
    names_map = {}

    for name in dir_content:
        if os.path.isfile(Path(dirpath, name)) or rename_all:
            names_map[name] = styler(name)

    for old_name, new_name in names_map.items():
        os.rename(
            Path(dirpath, old_name),
            Path(dirpath, new_name)
        )
        print(f"{old_name}  -->  {new_name}")


class NameStyler:

    def __init__(self) -> None:
        self.style_map = {
            'camel-case': self.to_camel_case,
            'snake-case': self.to_snake_case
        }

    def to_camel_case(self, fname: str):
        words = re.split(r"[\s\-\_]", fname)

        if len(words) <= 1:
            return fname

        for i, w in enumerate(words):
            words[i] = w[0].upper() + w[1:].lower()
        words[0] = words[0].lower()

        return ''.join(words)

    def to_snake_case(self, fname: str):
        words = re.split(r"[\s\-\_]", fname)
        return '_'.join(words)


def main():

    styler = NameStyler()

    parser = argparse.ArgumentParser(
        description='Files and directories renamer')

    parser.add_argument(
        'dirpath',
        type=Path,
        help='path, in which you want rename files'
    )

    parser.add_argument(
        'style',
        type=str,
        choices=styler.style_map.keys(),
        help='type of name style'
    )

    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        dest='rename_all',
        help='rename files AND directories'
    )

    args = parser.parse_args()

    change_names_style(
        args.dirpath,
        styler.style_map[args.style],
        args.rename_all
    )


if __name__ == '__main__':
    main()
