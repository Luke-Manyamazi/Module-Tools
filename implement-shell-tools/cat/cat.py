import argparse
import sys
from enum import Enum

class Numbering(Enum):
    NONE = 0
    ALL = 1
    NONEMPTY = 2

def print_numbered_line(line, line_number, pad=6):
    print(f"{line_number:{pad}}\t{line}", end='')
    return line_number + 1

def cat(filepath, numbering, start_line):
    line_number = start_line
    try:
        with open(filepath) as f:
            for line in f:
                if numbering == Numbering.NONEMPTY:
                    if line.strip():
                        line_number = print_numbered_line(line, line_number)
                    else:
                        print(line, end='')
                elif numbering == Numbering.ALL:
                    line_number = print_numbered_line(line, line_number)
                else:
                    print(line, end='')
    except FileNotFoundError:
        print(
            f"cat: {filepath}: No such file or directory",
            file=sys.stderr
        )
    return line_number

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate files and print on the standard output."
    )
    parser.add_argument('-n', action='store_true', help='number all output lines')
    parser.add_argument('-b', action='store_true', help='number non-empty output lines')
    parser.add_argument('files', nargs='+', help='files to concatenate')
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

    for file in args.files:
        line_number = cat(file, numbering=numbering, start_line=line_number)

if __name__ == "__main__":
    main()
