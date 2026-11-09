"""dedupe: print unique lines, preserving order."""
import argparse
import sys


def main(argv=None, *, stdin=None, stdout=None, stderr=None) -> int:
    stdin = stdin if stdin is not None else sys.stdin
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr

    parser = argparse.ArgumentParser(prog="dedupe")
    parser.add_argument("path", nargs="?", default="-")
    parser.add_argument("--ignore-case", action="store_true")
    parser.add_argument("--count", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.path == "-":
            text = stdin.read()
        else:
            with open(args.path, encoding="utf-8") as f:
                text = f.read()
    except OSError as exc:
        print(f"error: cannot read {args.path}: {exc.strerror}", file=stderr)
        return 1

    seen: dict[str, list] = {}
    for line in text.splitlines():
        if not line:
            continue
        key = line.lower() if args.ignore_case else line
        if key in seen:
            seen[key][1] += 1
        else:
            seen[key] = [line, 1]
    for line, count in seen.values():
        print(f"{count}\t{line}" if args.count else line, file=stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
