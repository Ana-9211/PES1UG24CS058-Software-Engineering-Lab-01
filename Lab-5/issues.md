# Issues found in library_system.py

Line numbers refer to the original file. Tool reports are in `*_before.txt`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on rule string | Security (Bandit B307, Pylint W0123) | 45 | `fine_from_rule` passes a caller-supplied string to `eval`, allowing arbitrary code execution. | Parse with `ast` and evaluate only numbers, `days` and `+ - * /`. |
| Mutable default argument | Bug (Pylint W0102) | 9, 12 | `dates=[]` is shared across all calls, so the "loan dates on record" count grew across different students (1, 2, 3). | Remove the parameter; keep per-student dates in a `loan_dates` dict. |
| Bare `except: pass` | Bug / Security (Bandit B110, Flake8 E722, Pylint W0702) | 21-22 | Hides every error, including a return of a book that was never borrowed. | Catch `KeyError`/`ValueError` and print a message. |
| Renewal changes the global fine rate | Logic bug (not flagged by tools) | 27-30 | Renewing for more than 14 days raised `FINE_PER_DAY` for everyone, so "Fine for 5 days" printed 15 instead of 10. | Renewal no longer touches the rate; `global` removed. |
| Negative fine | Logic bug (not flagged) | 24-25 | `calculate_fine(-3)` returned -9. | Clamp days at 0 with `max`. |
| Invalid book id accepted | Logic bug (not flagged) | 56 | Integer id 4521 was stored; the code's own comment says it must be a string. Empty student id was dropped silently. | Validate input, print a rejection message, return a bool. |
| Crash on non-numeric input | Bug (not flagged) | 63 | `int(days)` raises `ValueError` on input like `abc`. | Catch `ValueError` and print a message. |
| Files opened without `with`/encoding | Quality (Pylint R1732, W1514) | 34, 40 | Handles leak if an error occurs; encoding is platform dependent. | `with open(..., encoding="utf-8")`, `json.load`/`json.dump`. |
| `global loans` reassigned | Quality (Pylint W0603) | 35 | Rebinding a global in `load_records`. | `loans.clear()` then `loans.update(...)`. |
| `renewBook` naming | Style (Pylint C0103) | 27 | Not snake_case. | Renamed `renew_book`. |
| Missing docstrings | Style (Pylint C0114, C0116) | all | No module/function docstrings. | Added. |
| `%` formatting, `+` concatenation | Style (Pylint C0209) | 14, 31 | Old-style string building. | f-strings. |
| Unused `import os` | Style (Pylint W0611, Flake8 F401) | 2 | Dead import. | Removed. |
| Blank lines / long lines | Style (Flake8 E302, E305, E501) | many | PEP 8 spacing and >79-char lines. | Two blank lines between defs; long lines rewrapped via f-string split. |
| `main()` runs on import | Quality | 68 | Importing the module runs the demo. | `if __name__ == "__main__":` guard. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.07/10 | 10.00/10 |
| Bandit | 2 issues (1 medium, 1 low) | 0 |
| Flake8 | 14 findings | 0 |
