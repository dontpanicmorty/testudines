import csv

from jobrunner.cli import main

HEADER = "order_id,amount,status\n"


def write_input(tmp_path, rows):
    f = tmp_path / "orders.csv"
    f.write_text(HEADER + "".join(rows))
    return f


def read(path):
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def test_success_end_to_end(tmp_path, capsys):
    src = write_input(tmp_path, ["1,10.5,open\n", "2,3,SHIPPED\n", "3,x,open\n", "4,5,open\n",
                                 "5,1,open\n", "6,1,open\n", "7,1,open\n", "8,1,open\n",
                                 "9,1,open\n", "10,1,open\n", "11,1,open\n", "12,1,open\n",
                                 "13,1,open\n", "14,1,open\n", "15,1,open\n", "16,1,open\n",
                                 "17,1,open\n", "18,1,open\n", "19,1,open\n", "20,1,open\n"])
    out = tmp_path / "out"
    rc = main(["--input", str(src), "--output-dir", str(out), "--max-error-rate", "0.1"], env={})
    captured = capsys.readouterr()
    assert rc == 0, captured.err
    assert captured.out.strip() == "total=20 good=19 rejected=1"
    assert len(read(out / "clean.csv")) == 19
    rejects = read(out / "rejects.csv")
    assert [r["order_id"] for r in rejects] == ["3"] and "amount" in rejects[0]["reason"]


def test_env_vars_are_used(tmp_path, capsys):
    src = write_input(tmp_path, ["1,1,open\n"])
    rc = main([], env={"JOB_INPUT": str(src), "JOB_OUTPUT_DIR": str(tmp_path / "o")})
    assert rc == 0
    assert capsys.readouterr().out.strip() == "total=1 good=1 rejected=0"


def test_cli_overrides_env(tmp_path, capsys):
    a = write_input(tmp_path, ["1,1,open\n"])
    b = tmp_path / "b.csv"
    b.write_text(HEADER + "1,1,open\n2,1,open\n")
    rc = main(["--input", str(b)], env={"JOB_INPUT": str(a), "JOB_OUTPUT_DIR": str(tmp_path / "o")})
    assert rc == 0 and "total=2" in capsys.readouterr().out


def test_error_budget_exceeded_returns_1_but_writes_outputs(tmp_path, capsys):
    src = write_input(tmp_path, ["1,1,open\n", "x,1,open\n", "y,1,open\n"])
    out = tmp_path / "out"
    rc = main(["--input", str(src), "--output-dir", str(out)], env={})
    captured = capsys.readouterr()
    assert rc == 1
    assert captured.out.strip() == "total=3 good=1 rejected=2"
    assert "error rate" in captured.err
    assert (out / "rejects.csv").exists()


def test_empty_input_returns_1(tmp_path, capsys):
    src = write_input(tmp_path, [])
    assert main(["--input", str(src), "--output-dir", str(tmp_path / "o")], env={}) == 1
    assert "no input rows" in capsys.readouterr().err


def test_bad_config_returns_2(tmp_path, capsys):
    rc = main([], env={})
    err = capsys.readouterr().err
    assert rc == 2
    assert err.startswith("error:") and "JOB_INPUT" in err


def test_missing_input_returns_3(tmp_path, capsys):
    rc = main(["--input", str(tmp_path / "nope.csv"), "--output-dir", str(tmp_path / "o")], env={})
    captured = capsys.readouterr()
    assert rc == 3
    assert captured.err.startswith("error:") and captured.out == ""


def test_verbose_logs_debug_to_stderr(tmp_path, capsys):
    src = write_input(tmp_path, ["bad,1,open\n"])
    main(["--input", str(src), "--output-dir", str(tmp_path / "o"), "-v", "--max-error-rate", "1"], env={})
    captured = capsys.readouterr()
    assert "DEBUG" in captured.err
    assert "DEBUG" not in captured.out
