import argparse
import sys
from enum import Enum


class Numbering(Enum):
    NONE = 0
    ALL = 1
    NONEMPTY = 2


def print_numbered_line(line, line_number, pad=6):
    print(f"{line_number:{pad}}\t{line}", end="")


def cat(filepath, numbering, start_line):
    line_number = start_line

    try:
        with open(filepath) as file:
            for line in file:
                should_number = (
                    numbering == Numbering.ALL
                    or (
                        numbering == Numbering.NONEMPTY
                        and line.strip("\n")
                    )
                )

                if should_number:
                    print_numbered_line(line, line_number)
                    line_number += 1
                else:
                    print(line, end="")

    except FileNotFoundError:
        print(
            f"cat: {filepath}: No such file or directory",
            file=sys.stderr,
        )
        return line_number, False

    except IsADirectoryError:
        print(
            f"cat: {filepath}: Is a directory",
            file=sys.stderr,
        )
        return line_number, False

    except PermissionError:
        print(
            f"cat: {filepath}: Permission denied",
            file=sys.stderr,
        )
        return line_number, False

    return line_number, True


def main():
    parser = argparse.ArgumentParser(
        description="Concatenate files and print on the standard output."
    )

    parser.add_argument(
        "-n",
        action="store_true",
        help="number all output lines",
    )

    parser.add_argument(
        "-b",
        action="store_true",
        help="number non-empty output lines",
    )

    parser.add_argument(
        "files",
        nargs="+",
        help="files to concatenate",
    )

    args = parser.parse_args()

    if args.n and args.b:
        parser.error("options -n and -b are mutually exclusive")
    elif args.n:
        numbering = Numbering.ALL
    elif args.b:
        numbering = Numbering.NONEMPTY
    else:
        numbering = Numbering.NONE

    line_number = 1
    success = True

    for filepath in args.files:
        line_number, file_success = cat(
            filepath,
            numbering=numbering,
            start_line=line_number,
        )
        success = success and file_success

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())