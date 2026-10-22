# Reflection draft

Student: Ashrit Nair (PES2UG24AM032)

The supplied three-page handout does not contain the four reflection questions
mentioned in the repository README. The four topics below are draft reflections,
not a reproduction of missing assignment questions. Review these answers in your
own words and replace the prompts if your instructor supplies the questions.

## What did each tool contribute?

Pylint reported maintainability and correctness concerns, including a shared
mutable default, global reassignment, unused arguments, naming, and missing
docstrings. Bandit found security concerns in PIN hashing, temporary-file creation,
OTP generation, and a hardcoded credential. Flake8 identified formatting problems.
Using all three gave a broader review than any single tool.

## Which findings deserved attention first?

The high-severity SHA-1 finding and medium-severity temporary-file finding took
priority. PBKDF2 slows PIN guessing, while securely creating the receipt file
removes the unsafe gap between choosing a name and creating a file. Low-severity
findings still mattered: OTPs need a cryptographic random generator and
credentials should be configured outside the source code.

## How were the fixes verified?

The original reports were saved before editing. After the fixes, all three tools
were rerun without suppressing findings. Pylint reached 10.00/10, Bandit reported
no issues, and Flake8 produced no findings. The demo was checked against its
original output except for the random OTP. Its balance remained 1900.0 and total
credits remained 2500. Additional checks covered rejected payments, explicit logs,
gateway verification, statement counts, and receipt-file creation.

## What are the limits of static analysis?

The tools cannot prove the business rules are correct or replace execution checks
and code review. Inspection found that a negative payment could increase the
balance even though it was not flagged by these scans. The program also checks
its named daily limit per transaction, not cumulatively across a day. The final
score measures the checks performed, not production readiness or complete security.
