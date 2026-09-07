import argparse
import sys


def wc(path):
    try:
        with open(path, "rb") as file:
            content = file.read()

        line_count = content.count(b"\n")
        word_count = len(content.split())
        byte_count = len(content)

        return line_count, word_count, byte_count

    except FileNotFoundError:
        print(
            f"wc: {path}: No such file or directory",
            file=sys.stderr,
        )
    except IsADirectoryError:
        print(
            f"wc: {path}: Is a directory",
            file=sys.stderr,
        )
    except PermissionError:
        print(
            f"wc: {path}: Permission denied",
            file=sys.stderr,
        )
    except OSError as error:
        print(
            f"wc: {path}: {error}",
            file=sys.stderr,
        )

    return None


def print_stats(
    line_count,
    word_count,
    byte_count,
    filename,
    show_lines,
    show_words,
    show_bytes,
):
    parts = []

    if show_lines:
        parts.append(f"{line_count:7d}")

    if show_words:
        parts.append(f"{word_count:7d}")

    if show_bytes:
        parts.append(f"{byte_count:7d}")

    print("".join(parts), filename)


def main():
    parser = argparse.ArgumentParser(
        description="Print newline, word, and byte counts for files."
    )

    parser.add_argument(
        "-l",
        action="store_true",
        help="print the newline count",
    )

    parser.add_argument(
        "-w",
        action="store_true",
        help="print the word count",
    )

    parser.add_argument(
        "-c",
        action="store_true",
        help="print the byte count",
    )

    parser.add_argument(
        "paths",
        nargs="+",
        help="files to count",
    )

    args = parser.parse_args()

    # If no options are supplied, wc prints all three counts.
    show_lines = args.l
    show_words = args.w
    show_bytes = args.c

    if not any((show_lines, show_words, show_bytes)):
        show_lines = True
        show_words = True
        show_bytes = True

    total_lines = 0
    total_words = 0
    total_bytes = 0
    successful_files = 0

    for path in args.paths:
        counts = wc(path)

        if counts is None:
            continue

        line_count, word_count, byte_count = counts

        total_lines += line_count
        total_words += word_count
        total_bytes += byte_count
        successful_files += 1

        print_stats(
            line_count,
            word_count,
            byte_count,
            path,
            show_lines,
            show_words,
            show_bytes,
        )

    if len(args.paths) > 1 and successful_files > 0:
        print_stats(
            total_lines,
            total_words,
            total_bytes,
            "total",
            show_lines,
            show_words,
            show_bytes,
        )

    return 0 if successful_files == len(args.paths) else 1


if __name__ == "__main__":
    sys.exit(main())