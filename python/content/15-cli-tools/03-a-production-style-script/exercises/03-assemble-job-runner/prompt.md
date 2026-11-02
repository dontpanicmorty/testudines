This is a small package, `jobrunner`, that cleans an orders export. `logs.py` and `runner.py` are finished. Implement the three TODOs:

**`jobrunner/validate.py`** `validate_row(row) -> list[str]`: returns problems (empty list when fine), one string per problem, each starting with the field name and a colon:
- `order_id` must be a positive integer (`"order_id: ..."`);
- `amount` must parse as a float and be `>= 0` (`"amount: ..."`);
- `status`, after `.strip().lower()`, must be one of `open`, `shipped`, `cancelled` (`"status: ..."`).
Missing keys count as invalid.

**`jobrunner/config.py`** `load_config(env) -> JobConfig` reads `JOB_INPUT` (required), `JOB_OUTPUT_DIR` (required), `JOB_MAX_ERROR_RATE` (default `0.1`, must be a number in `0..1`) and `JOB_LOG_LEVEL` (default `INFO`; one of DEBUG/INFO/WARNING/ERROR, case-insensitive, stored upper-case). `input_path` and `output_dir` are `Path`s. If anything is wrong raise `ConfigError` whose message mentions **every** offending variable name.

**`jobrunner/cli.py`** `main(argv=None, env=None) -> int` with options `--input`, `--output-dir`, `--max-error-rate`, `-v/--verbose`. Command-line values override the matching `JOB_*` variables; `env` defaults to `os.environ`. Then:
1. configure logging (`setup_logging`), 2. `run_job(config, logger)`, 3. print `total=<n> good=<n> rejected=<n>` to **stdout**, 4. decide the exit code.

Exit codes: `0` success; `1` empty input or error rate above `max_error_rate` (print the reason to stderr, outputs are still written); `2` bad configuration (`error: ...` on stderr); `3` input file not found (`error: ...` on stderr). Argparse keeps its usual exit 2 for bad usage.
