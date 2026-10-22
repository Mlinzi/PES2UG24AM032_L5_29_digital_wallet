# Static analysis issue table

Student: Ashrit Nair (PES2UG24AM032)

Line numbers below refer to the original file in the initial commit (`0d188e2`).
Reports are in `reports/before/` and `reports/after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Bandit B324: weak SHA-1 | Security, High | 14 | SHA-1 is unsuitable for protecting PINs. | Use PBKDF2-HMAC-SHA256 with 600,000 iterations and a random process-local salt; compare hashes with `hmac.compare_digest`. |
| Bandit B306: insecure temporary path | Security, Medium | 60 | `mktemp` returns a path without securely creating the file, allowing a race. | Create the file atomically with `NamedTemporaryFile`; close it before returning its name. The caller owns deletion. |
| Bandit B105: hardcoded gateway secret | Security, Low | 6 | A credential is embedded in source control. | Read the gateway secret and wallet PIN from environment variables; require configuration for the demo. |
| Bandit B311: predictable OTP generator | Security, Low | 64 | The ordinary random generator is unsuitable for OTPs. | Use `secrets.randbelow(900000) + 100000`. |
| Pylint W0102: mutable default | Bug | 17, 23 | The default log list is shared between calls. | Default to `None` and append only when a caller supplies a log. |
| Pylint W0603: global reassignment | Maintainability | 28-29 | Updating a module variable through `global` makes state harder to follow. | Store the limit with the wallet balance and update that dictionary. |
| Pylint W0613: unused argument | Maintainability | 50 | The cashback calculation ignores merchant type. | Remove the unused argument and update its call; preserve the uniform 2% cashback. |
| Pylint C0103: naming | Style | 9, 13-58, 78 | Function, parameter, and local names violate naming conventions. | Use snake_case names and keep the limit inside wallet state. |
| Pylint C0114/C0116: missing documentation | Documentation | 1, 13-63 | The module and functions lack descriptions. | Add module and function docstrings. |
| Flake8 E261/E225/E231/E305 | Style | 76, 78-80 | Inline comment spacing, assignment spacing, comma spacing, and blank lines are incorrect. | Apply the reported PEP 8 formatting corrections. |

Additional inspection fixes: reject zero/negative payments and nonpositive limits,
make nonpositive statement counts print nothing, and guard the demo with
`if __name__ == "__main__"` so importing the module has no payment side effects.

This remains a teaching demo: the limit is checked per payment rather than
tracking cumulative daily spending. PIN salt and wallet state live only for the
current process, and the demo prints the OTP. A clean static scan does not turn
this into a production payment system.
