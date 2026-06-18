import os
import sys
import argparse

def ls(path, one_column, show_hidden):
    """List files in a directory, optionally in one column or including hidden files."""
    try:
        if os.path.isfile(path):
            print(os.path.basename(path))
            return

        files = os.listdir(path)

        if show_hidden:
            files = ['.', '..'] + files
        else:
            files = [f for f in files if not f.startswith('.')]

        files.sort()

        if one_column:
            print(*files, sep='\n')
        else:
            print(*files)

    except FileNotFoundError:
        print(
            f"ls: cannot access '{path}': No such file or directory",
            file=sys.stderr
        )
    except NotADirectoryError:
        print(
            f"ls: cannot access '{path}': Not a directory",
            file=sys.stderr
        )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-1', dest='one_column', action='store_true', help='list one file per line')
    parser.add_argument('-a', action='store_true', help='show hidden files')
    parser.add_argument('path', nargs='?', default='.', help='directory to list')
    args = parser.parse_args()

    ls(args.path, args.one_column, args.a)

if __name__ == "__main__":
    main()
