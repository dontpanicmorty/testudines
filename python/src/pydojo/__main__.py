from __future__ import annotations

import argparse


def main() -> None:
    ap = argparse.ArgumentParser(prog="pydojo", description="Offline Python training for data practitioners")
    ap.add_argument("command", nargs="?", default="app", choices=["app", "validate", "selftest"])
    a = ap.parse_args()
    if a.command == "validate":
        from .validate import main as vmain
        raise SystemExit(vmain())
    if a.command == "selftest":
        from .selftest import main as smain
        raise SystemExit(smain())
    from .app import run
    raise SystemExit(run())


if __name__ == "__main__":
    main()
