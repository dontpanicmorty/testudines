import subprocess
import sys
from pathlib import Path

HERE = str(Path(__file__).parent)

BLOCKED = f"""
import sys
sys.path.insert(0, {HERE!r})
sys.modules['pandas'] = None          # makes 'import pandas' raise ImportError
import pricing
assert pricing.net_price(120.0, 0.2) == 100.0
assert 'pandas' not in [k for k, v in sys.modules.items() if v is not None]
print('ok')
"""


def test_import_and_core_work_without_pandas():
    r = subprocess.run([sys.executable, "-c", BLOCKED], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "ok" in r.stdout


def test_to_frame_still_works_with_pandas():
    sys.path.insert(0, HERE)
    import pricing

    df = pricing.to_frame([("a", 120.0, 0.2), ("b", 11.0, 0.1)])
    assert list(df.columns) == ["sku", "gross", "net"]
    assert df["net"].tolist() == [100.0, 10.0]


def test_public_names():
    sys.path.insert(0, HERE)
    import pricing

    assert sorted(pricing.__all__) == ["net_price", "to_frame"]
