import csv
import logging
from dataclasses import dataclass

from jobrunner.config import JobConfig
from jobrunner.validate import validate_row


@dataclass
class RunStats:
    total: int
    good: int
    rejected: int

    @property
    def error_rate(self) -> float:
        return self.rejected / self.total if self.total else 0.0


def run_job(config: JobConfig, logger: logging.Logger) -> RunStats:
    """Read the input CSV, write clean.csv and rejects.csv into the output dir."""
    config.output_dir.mkdir(parents=True, exist_ok=True)
    good = rejected = 0
    with config.input_path.open(newline="") as src:
        reader = csv.DictReader(src)
        fields = list(reader.fieldnames or [])
        with (config.output_dir / "clean.csv").open("w", newline="") as clean_f, \
                (config.output_dir / "rejects.csv").open("w", newline="") as rej_f:
            clean = csv.DictWriter(clean_f, fieldnames=fields)
            rej = csv.DictWriter(rej_f, fieldnames=fields + ["reason"])
            clean.writeheader()
            rej.writeheader()
            for row in reader:
                problems = validate_row(row)
                if problems:
                    rejected += 1
                    rej.writerow({**row, "reason": "; ".join(problems)})
                    logger.debug("rejected row %s: %s", row.get("order_id"), problems)
                else:
                    good += 1
                    clean.writerow(row)
    stats = RunStats(total=good + rejected, good=good, rejected=rejected)
    logger.info("processed %d rows: %d good, %d rejected", stats.total, good, rejected)
    return stats
