import argparse
import sys

def wc(path, count_lines, count_words, count_bytes):
    """Count lines, words, and bytes for a single file."""
    try:
        with open(path, 'r') as f:
            content = f.read()

        lines = content.splitlines()
        words = content.split()

        line_count = len(lines)
        word_count = len(words)
        byte_count = len(content.encode('utf-8'))

        if not any([count_lines, count_words, count_bytes]):
            count_lines = True
            count_words = True
            count_bytes = True

        parts = []

        if count_lines:
            parts.append(str(line_count))

        if count_words:
            parts.append(str(word_count))

        if count_bytes:
            parts.append(str(byte_count))

        print(' '.join(parts), path)

        return line_count, word_count, byte_count

    except FileNotFoundError:
        print(
            f"wc: {path}: No such file or directory",
            file=sys.stderr
        )
        return (0, 0, 0)

    except IsADirectoryError:
        print(
            f"wc: {path}: Is a directory",
            file=sys.stderr
        )
        return (0, 0, 0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', action='store_true', help='Count lines')
    parser.add_argument('-w', action='store_true', help='Count words')
    parser.add_argument('-c', action='store_true', help='Count bytes')
    parser.add_argument('paths', nargs='+', help='Files to count')
    args = parser.parse_args()

    total_lines = 0
    total_words = 0
    total_bytes = 0

    multiple_files = len(args.paths) > 1
    show_all = not any([args.l, args.w, args.c])

    for path in args.paths:
        l, w, b = wc(path, args.l, args.w, args.c)
        total_lines += l
        total_words += w
        total_bytes += b

    if multiple_files:
        parts = []

        if args.l or show_all:
            parts.append(str(total_lines))

        if args.w or show_all:
            parts.append(str(total_words))

        if args.c or show_all:
            parts.append(str(total_bytes))

        print(' '.join(parts), 'total')

if __name__ == "__main__":
    main()
