import fmtkit
import fmtkit.core as core


def test_top_level_imports():
    from fmtkit import clean_name, parse_amount
    assert clean_name("  ada   LOVELACE ") == "Ada Lovelace"
    assert parse_amount("$1,234.50") == 1234.5


def test_dunder_all():
    assert sorted(fmtkit.__all__) == ["clean_name", "parse_amount"]


def test_star_import_exposes_only_public():
    ns = {}
    exec("from fmtkit import *", ns)
    public = {k for k in ns if not k.startswith("__")}
    assert public == {"clean_name", "parse_amount"}, public


def test_helper_is_private():
    assert hasattr(core, "_normalize"), "rename normalize to _normalize"
    assert not hasattr(core, "normalize"), "public normalize must be gone"
