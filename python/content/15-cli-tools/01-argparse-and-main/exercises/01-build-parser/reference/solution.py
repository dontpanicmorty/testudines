import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="export_orders")
    parser.add_argument("input")
    parser.add_argument("-o", "--output", default="-")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--env", choices=["dev", "prod"], default="dev")
    parser.add_argument("--dry-run", action="store_true")
    return parser
