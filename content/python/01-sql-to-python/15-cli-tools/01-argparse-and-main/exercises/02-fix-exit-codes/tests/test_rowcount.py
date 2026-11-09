import subprocess
import sys
from pathlib import Path

from solution import main


def test_success(tmp_path, capsys):
    f = tmp_path / "a.csv"
    f.write_text("id\n1\n\n2\n")
    assert main([str(f)]) == 0
    out = capsys.readouterr()
    assert out.out.strip() == "3" and out.err == ""


def test_skip_header(tmp_path, capsys):
    f = tmp_path / "a.csv"
    f.write_text("id\n1\n2\n")
    assert main([str(f), "--skip-header"]) == 0
    assert capsys.readouterr().out.strip() == "2"


def test_missing_file_goes_to_stderr_and_returns_1(tmp_path, capsys):
    rc = main([str(tmp_path / "nope.csv")])
    out = capsys.readouterr()
    assert rc == 1, f"expected exit code 1, got {rc}"
    assert out.out == "", f"nothing may reach stdout, got {out.out!r}"
    assert out.err.startswith("error:")


def test_script_exit_code(tmp_path):
    script = Path(__file__).with_name("solution.py")
    r = subprocess.run([sys.executable, str(script), str(tmp_path / "nope.csv")], capture_output=True, text=True)
    assert r.returncode == 1
    assert r.stdout == "" and r.stderr.startswith("error:")
