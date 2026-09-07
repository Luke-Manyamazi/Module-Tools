import argparse
import os
import sys


def ls(path, one_column, show_hidden):
    try:
        if os.path.isfile(path):
            print(os.path.basename(path))
            return True

        files = os.listdir(path)

        if show_hidden:
            files = [".", ".."] + files
        else:
            files = [file for file in files if not file.startswith(".")]

        files.sort()

        separator = "\n" if one_column else "\t"
        print(*files, sep=separator)

        return True

    except FileNotFoundError:
        print(
            f"ls: cannot access '{path}': No such file or directory",
            file=sys.stderr,
        )
    except NotADirectoryError:
        print(
            f"ls: cannot access '{path}': Not a directory",
            file=sys.stderr,
        )
    except PermissionError:
        print(
            f"ls: cannot open directory '{path}': Permission denied",
            file=sys.stderr,
        )

    return False


def main():
    parser = argparse.ArgumentParser(
        description="List directory contents."
    )

    parser.add_argument(
        "-1",
        dest="one_column",
        action="store_true",
        help="list one file per line",
    )

    parser.add_argument(
        "-a",
        action="store_true",
        help="show hidden files",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="directory to list",
    )

    args = parser.parse_args()

    success = ls(
        path=args.path,
        one_column=args.one_column,
        show_hidden=args.a,
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())