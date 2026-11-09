import subprocess
import sys


def test_imports_as_package():
    r = subprocess.run(
        [sys.executable, "-c", "from mylib.transform import normalize_rows"],
        capture_output=True, text=True, timeout=20,
    )
    assert r.returncode == 0, r.stderr[-400:]


def test_normalize_rows():
    from mylib.transform import normalize_rows

    rows = [{"name": " ada ", "email": "ADA@X.COM"}, {"name": "GRACE  hopper", "email": " g@y.org "}]
    assert normalize_rows(rows) == [
        {"name": "Ada", "email": "ada@x.com"},
        {"name": "Grace Hopper", "email": "g@y.org"},
    ]


def test_cleaning_is_still_a_sibling_module():
    import mylib.cleaning
    from mylib import transform

    assert transform.clean_name is mylib.cleaning.clean_name
