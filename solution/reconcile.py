"""Reference solution: reconcile invoices against the bank statement only."""
import csv
import re
import sys
from decimal import Decimal
from pathlib import Path

REF = re.compile(r"INV[ -]?(\d{4})", re.IGNORECASE)
CENT = Decimal("0.01")


def money(text):
    text = (text or "").replace(",", "").strip()
    return Decimal(text) if text else Decimal("0")


def reconcile(workdir):
    workdir = Path(workdir)
    with open(workdir / "invoices.csv", newline="", encoding="utf-8") as f:
        invoices = {row["invoice_id"]: money(row["amount_inr"]) for row in csv.DictReader(f)}
    received = {inv: Decimal("0") for inv in invoices}

    with open(workdir / "bank_statement.csv", newline="", encoding="utf-8") as f:
        for line in csv.DictReader(f):
            refs = [f"INV-{n}" for n in REF.findall(line["description"])]
            refs = [r for r in refs if r in invoices]
            if not refs:
                continue
            credit, debit = money(line["credit_inr"]), money(line["debit_inr"])
            if debit:
                received[refs[0]] -= debit
            remaining = credit
            for i, inv in enumerate(refs):
                if i == len(refs) - 1:
                    share = remaining
                else:
                    share = min(remaining, max(invoices[inv] - received[inv], Decimal("0")))
                received[inv] += share
                remaining -= share

    rows = []
    for inv in sorted(invoices):
        amount, got = invoices[inv], received[inv]
        if got <= 0:
            status = "UNPAID"
        elif got < amount:
            status = "PARTIAL"
        elif got == amount:
            status = "PAID"
        else:
            status = "OVERPAID"
        rows.append([inv, amount, got, amount - got, status])

    with open(workdir / "reconciliation.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["invoice_id", "invoice_amount", "amount_received", "balance", "status"])
        for inv, amount, got, bal, status in rows:
            writer.writerow([inv, f"{amount.quantize(CENT)}", f"{got.quantize(CENT)}",
                             f"{bal.quantize(CENT)}", status])


if __name__ == "__main__":
    reconcile(sys.argv[1] if len(sys.argv) > 1 else ".")
