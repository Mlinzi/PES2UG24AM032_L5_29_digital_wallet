# Lab 5: Static Code Analysis — Digital Wallet & Payment Tracker

## Completed lab: PES2UG24AM032 — Ashrit Nair

The cleaned program reads credentials from the environment. To run on Windows
PowerShell (the values below are for the local classroom demo only):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
$env:WALLET_PIN = "4321"
$env:GATEWAY_SECRET = "local-demo-key"
.\.venv\Scripts\python.exe digital_wallet.py
```

Run the final analysis with:

```powershell
.\.venv\Scripts\python.exe -m pylint --persistent=n digital_wallet.py
.\.venv\Scripts\python.exe -m bandit -r digital_wallet.py
.\.venv\Scripts\python.exe -m flake8 digital_wallet.py
```

Before-and-after reports are under `reports/before/` and `reports/after/`.
An empty Flake8 report means no findings; see `reports/after/verification.txt`
for execution-check results. The demo preserves the original output except for
the random OTP: final balance is 1900.0 and total credits are 2500.
`issues.md` documents fixes. `reflection.md` contains draft reflections because
the supplied handout omits the four questions mentioned below.

The original assignment instructions follow.

**Your file:** `digital_wallet.py`

Follow the lab handout for the full instructions.

## About the program

A simple payment wallet. It sends a one-time password, tops up the balance, pays merchants after a PIN check and a daily limit, prints a mini statement, works out cashback and verifies a payment-gateway key.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:

   ```
   python digital_wallet.py
   ```

   It runs a short demonstration and needs no input. Note what it prints, so you can check that it still behaves the same after your fixes.

2. **Install the tools:**

   ```
   python -m pip install pylint bandit flake8
   ```

3. **Run the analysis and save the reports:**

   ```
   python -m pylint digital_wallet.py > pylint_report.txt
   python -m bandit -r digital_wallet.py > bandit_report.txt
   python -m flake8 digital_wallet.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ...   | ...  | ...     | ...         | ...          |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

- `digital_wallet.py`: your cleaned version, with at least 4 issues fixed.
- `issues.md`: the completed issue table.
- `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.
