# Static Code Analysis — Issues and Fixes

The line numbers below refer to the original `hospital_patient_system.py` uploaded for review. Line numbers may change after edits.

| Issue | Type / Tool | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe `eval()` | Security — Bandit B307 / Pylint W0123 | 38–40 | Evaluating a supplied string as Python can execute arbitrary code. | Replaced `eval()` with an AST-based evaluator that permits only numeric constants, `base_bill`, and basic arithmetic operators. |
| Shell command built from a filename | Security — Bandit B605 | 52–56 | `os.system()` launches a shell command using a value that may contain shell metacharacters. | Removed shell execution. The program reports the exported path with Python's `print()`. |
| Weak MD5 hash | Security — Bandit B324 | 44–45 | MD5 is not appropriate when a modern cryptographic digest is expected. | Replaced MD5 with SHA-256. A hash of an ID is not encryption or anonymization. |
| Non-cryptographic random token | Security — Bandit B311 | 48–49 | `random` is not intended for security-sensitive tokens. | Replaced it with `secrets.randbelow()` for a four-digit token. |
| Bare `except` that silently ignores errors | Reliability/style — Bandit B110, Flake8 E722, Pylint W0702 | 21–25 | All exceptions are swallowed, hiding unexpected bugs and failures. | Used an explicit lookup and return value for unknown patient IDs. |
| Mutable default argument | Code quality — Pylint W0102 | 13 | `intake_log=[]` shares the same list across calls. | Changed the default to `None` and creates a new list inside the function. |
| Unused imports and variables | Code quality/style — Pylint W0611/W0612, Flake8 F401/F841 | 4, 29, 39, 61 | `math`, `bed_charge`, `base_bill` in the old function, and loop variable `p` are unused. | Removed unused items and simplified the ward count. |
| Comparison with `None` using `==` | Style — Pylint C0121, Flake8 E711 | 30 | `== None` is not the recommended identity check. | Uses `is None` through a retrieved patient record. |
| File opened without context manager/encoding | Reliability/style — Pylint W1514/R1732 | 52–55 | The file may not close if an error occurs, and encoding depends on platform defaults. | Uses `Path.open(..., encoding="utf-8")` in a `with` block. |
| Missing docstrings, naming and formatting | Style — Pylint/Flake8 | Multiple | Several functions lack docstrings; `admitPatient` is not snake_case; some lines are too long. | Added docstrings, renamed to `admit_patient`, and formatted the code consistently. |
| Hard-coded access key | Security practice | 68, 77 | A credential is embedded in source and printed to output. | Removed the hard-coded key and its print statement. Secrets should be supplied through a secure configuration mechanism when needed. |
| Plain-text-like `str(dict)` export | Maintainability/data format | 53–54 | The output is Python representation rather than a standard structured data format. | Exports JSON with indentation and UTF-8 encoding. |
