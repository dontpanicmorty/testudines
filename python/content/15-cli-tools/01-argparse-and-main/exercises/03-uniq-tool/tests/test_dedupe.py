import io

import pytest

from solution import main


def run(argv, text=""):
    out, err = io.StringIO(), io.StringIO()
    rc = main(argv, stdin=io.StringIO(text), stdout=out, stderr=err)
    return rc, out.getvalue(), err.getvalue()


def test_stdin_default_preserves_order_and_skips_blank():
    assert run([], "b\na\n\nb\nc\na\n") == (0, "b\na\nc\n", "")


def test_dash_means_stdin():
    assert run(["-"], "x\nx\n")[1] == "x\n"


def test_ignore_case_keeps_first_spelling():
    assert run(["--ignore-case"], "Apple\napple\nBANANA\n")[1] == "Apple\nBANANA\n"


def test_case_sensitive_by_default():
    assert run([], "a\nA\n")[1] == "a\nA\n"


def test_count():
    assert run(["--count"], "a\nb\na\n")[1] == "2\ta\n1\tb\n"
    assert run(["--count", "--ignore-case"], "a\nA\n")[1] == "2\ta\n"


def test_file_path(tmp_path):
    f = tmp_path / "in.txt"
    f.write_text("q\nq\nr\n")
    assert run([str(f)])[:2] == (0, "q\nr\n")


def test_missing_file(tmp_path):
    rc, out, err = run([str(tmp_path / "nope.txt")])
    assert rc == 1 and out == "" and err.startswith("error:")


def test_bad_usage_exit_2():
    with pytest.raises(SystemExit) as info:
        run(["--bogus"])
    assert info.value.code == 2
