from __future__ import annotations

import argparse


def main() -> None:
    ap = argparse.ArgumentParser(prog="testudines", description="Offline SQL and Python practice")
    ap.add_argument("command", nargs="?", default="app", choices=["app", "validate", "selftest"])
    ap.add_argument("section", nargs="?", choices=["sql", "python"],
                    help="validate only this section's curriculum (default: both)")
    ap.add_argument("only", nargs="?", help="python only: check just the path or module whose id contains this")
    a = ap.parse_args()
    if a.command == "validate":
        from .validate import main as vmain
        raise SystemExit(vmain(a.section, a.only))
    if a.command == "selftest":
        from .selftest import main as smain
        raise SystemExit(smain())
    from .app import run
    raise SystemExit(run())


if __name__ == "__main__":
    main()
