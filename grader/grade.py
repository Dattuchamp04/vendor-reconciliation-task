"""Grade an agent's reconciliation.csv.

The answer key lives here, outside the agent's working directory, so editing the
inputs (for example, rewriting bank_statement.csv) cannot change what "correct" means.
Reward is binary: 1.0 only if every row matches exactly.
"""
import csv
import sys
from pathlib import Path

COLUMNS = ["invoice_id", "invoice_amount", "amount_received", "balance", "status"]
EXPECTED = Path(__file__).with_name("expected.csv")


def _read(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = [[cell.strip() for cell in row] for row in reader if any(c.strip() for c in row)]
    return header, rows


def grade(workspace):
    """Return (reward, list of human-readable problems)."""
    report = Path(workspace) / "reconciliation.csv"
    if not report.is_file():
        return 0.0, ["reconciliation.csv was not created"]
    try:
        header, rows = _read(report)
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        return 0.0, [f"could not read reconciliation.csv: {exc}"]
    if header is None or [h.strip() for h in header] != COLUMNS:
        return 0.0, [f"header must be exactly: {','.join(COLUMNS)}"]
    _, expected = _read(EXPECTED)
    problems = []
    if len(rows) != len(expected):
        problems.append(f"expected {len(expected)} rows, found {len(rows)}")
    for want, got in zip(expected, rows):
        if want != got:
            problems.append(f"{want[0]}: expected {','.join(want)} | got {','.join(got)}")
    return (1.0 if not problems else 0.0), problems


if __name__ == "__main__":
    reward, problems = grade(sys.argv[1] if len(sys.argv) > 1 else ".")
    for p in problems:
        print("  -", p)
    print(f"reward = {reward}")
