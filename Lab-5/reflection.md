# Reflection

**1. Which tool was most helpful, and why?**
Pylint. It caught the most real problems (mutable default, bare except, globals, unclosed files) and gave the biggest score change, 6.07 to 10.00. Bandit was shortest but flagged the most serious issue, `eval`.

**2. What kinds of issues did the tools miss?**
Logic bugs: negative fines, renewals silently raising the fine rate for everyone, an integer book id that the code's own comment says is invalid, and a crash on non-numeric input. These only showed up by running the program and reading its output.

**3. Did any fix change program behaviour? Were any warnings false positives?**
Yes, intentionally: "Fine for 5 days" went from 15 to 10 because renewals no longer inflate the rate, negative fines are now 0, and the invalid loans are rejected with a message. No warning was a true false positive, but the "unused import" and "missing docstring" findings are low value next to the logic bugs.

**4. How would you integrate static analysis into a team workflow?**
Run Flake8, Pylint and Bandit in a pre-commit hook and in CI on every pull request, failing the build on any Bandit finding and on a Pylint score below a set threshold (e.g. 9.5). Pair this with tests and code review, because the tools cannot judge whether the program's behaviour is correct.
