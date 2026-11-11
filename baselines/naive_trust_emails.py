"""A plausible but wrong approach: believe the customers' emails.

It marks every invoice mentioned in an email as fully PAID. The grader should give it 0.0.
"""
import csv
import re
import sys
from pathlib import Path


def run(workdir):
    workdir = Path(workdir)
    claimed = set()
    for mail in (workdir / "emails").glob("*.txt"):
        claimed.update(re.findall(r"INV-\d{4}", mail.read_text(encoding="utf-8")))
    with open(workdir / "invoices.csv", newline="", encoding="utf-8") as f:
        invoices = list(csv.DictReader(f))
    with open(workdir / "reconciliation.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["invoice_id", "invoice_amount", "amount_received", "balance", "status"])
        for row in sorted(invoices, key=lambda r: r["invoice_id"]):
            amount = float(row["amount_inr"].replace(",", ""))
            paid = row["invoice_id"] in claimed
            got = amount if paid else 0.0
            w.writerow([row["invoice_id"], f"{amount:.2f}", f"{got:.2f}", f"{amount - got:.2f}",
                        "PAID" if paid else "UNPAID"])


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else ".")
