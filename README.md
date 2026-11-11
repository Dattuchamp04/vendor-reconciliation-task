# Vendor Payment Reconciliation: an AI agent evaluation task

A small, realistic multi-file task for testing AI agents, with an automatic grader.
The agent gets a working directory containing a spreadsheet of invoices, a bank statement
and customer emails, and must produce a reconciliation report. A Python grader scores the
result: **1.0 if every row is correct, 0.0 otherwise.**

Built by Sridatta Khoday as a public demo of how I design evaluation tasks. It's
self-contained and needs only Python 3.10+ (standard library only).

## Run it

```bash
python run_demo.py
```

```
does nothing               reward = 0.0
trusts the emails          reward = 0.0
tampers with the inputs    reward = 0.0
reference solution         reward = 1.0
```

## What the agent sees

```
task/instruction.md       the instruction (clear and complete, no hints about the answer)
task/files/
  invoices.csv            8 invoices, amounts in Indian digit grouping ("1,25,000.00")
  bank_statement.csv      October credits and debits, the only source of truth
  emails/                 4 customer emails, some of them wrong
```

## Why it's hard (and fair)

Every trap follows from a rule stated in the instruction, so a careful human gets it right:

| Trap | What a careless agent does |
|---|---|
| Emails claim payments the bank never received (INV-1003, INV-1004) | Marks them PAID |
| Invoice references in mixed formats: `INV1001`, `inv-1002`, `INV 1002` | Misses payments |
| One payment split across two bank lines (INV-1002) | Sees only part of it |
| One bank credit covering two invoices (INV-1005 + INV-1007) | Gives it all to the first |
| A refund debit cancels a payment (INV-1008) | Ignores debits |
| An overpayment with an "advance" (INV-1006) | Calls it PAID |
| Indian digit grouping in the invoice file | Parses `1,25,000.00` wrong |
| Interest and bank charges with no invoice reference | Allocates them somewhere |

## Grader design

- **Answer key outside the workspace.** `grader/expected.csv` is never copied into the
  agent's directory, so rewriting the inputs can't change what "correct" means.
  `baselines/tamper_inputs.py` tries exactly that and still scores 0.0.
- **Strict, binary reward.** Exact header, row count and values. Partial credit would
  reward an agent that trusts the emails for getting some rows right by luck.
- **Clear failure messages.** The grader reports which invoice is wrong and how, which
  makes reviewing an agent's attempt fast.

## How I verified it

1. **Fail-to-pass:** an empty workspace scores 0.0; the reference solution scores 1.0.
2. **Plausible wrong approaches fail:** trusting emails, and tampering with inputs.
3. **Mutation testing:** I broke the reference solution in four realistic ways (ignoring
   refunds, no split allocation, strict reference matching only, calling overpayments
   PAID). The grader catches every one.

## Layout

```
task/            what the agent receives
grader/          grade.py + answer key (never shown to the agent)
solution/        reference solution
baselines/       wrong approaches used to test the grader
run_demo.py      runs all agents in fresh temporary workspaces
```
