# Task: Reconcile October vendor payments

Your working directory contains our October receivables:

- `invoices.csv`: invoices we issued (amounts use Indian digit grouping, e.g. `1,25,000.00`)
- `bank_statement.csv`: every credit and debit on our account in October
- `emails/`: messages from customers about their payments

Create `reconciliation.csv` in the working directory with one row per invoice, sorted by
`invoice_id`, and exactly these columns:

`invoice_id,invoice_amount,amount_received,balance,status`

Rules:

1. **The bank statement is the only source of truth.** Emails may be wrong or incomplete;
   never count a payment that does not appear on the statement.
2. A statement line refers to an invoice when its description contains `INV` (any case),
   optionally followed by a space or hyphen, then the 4-digit invoice number
   (`INV1001`, `inv-1002`, `INV 1002` all refer to `INV-1002`-style IDs).
   Lines that refer to no invoice are ignored.
3. Credits add to an invoice's amount received; debits (refunds) subtract from it.
4. A single credit that refers to several invoices is allocated to them in the order they
   appear in the description, each receiving up to its remaining unpaid amount; anything
   left over goes to the last invoice listed.
5. `balance` = `invoice_amount` - `amount_received` (negative when overpaid).
6. `status` is `PAID` (received equals amount), `PARTIAL` (more than zero but less),
   `UNPAID` (zero or less) or `OVERPAID` (more than the amount).
7. Write money as plain numbers with exactly 2 decimals and no thousands separators
   (`125000.00`, `-5000.00`). Do not modify the input files.
