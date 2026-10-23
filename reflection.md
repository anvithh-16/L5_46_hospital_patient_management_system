# Static Code Analysis — Reflection

> Note: The exact four reflection questions were not included in the readable portion of the supplied handout. These are draft reflections on the lab's stated learning outcomes; map them to the instructor's exact questions if their wording differs.

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without running the program. Pylint focuses on code quality and likely programming mistakes, Flake8 checks style and formatting, and Bandit looks for common security risks. Using all three provides different perspectives on the same code.

## 2. Which findings were most important, and why?

The unsafe use of `eval()` and the shell command constructed for `os.system()` were important because they could allow unintended code or command execution. The weak MD5 digest and use of the ordinary `random` module for a token were also security concerns. The mutable default list and bare exception handler were important correctness and maintainability issues.

## 3. How were the issues fixed and verified?

The fixes included replacing `eval()` with a restricted arithmetic-expression evaluator, removing shell execution, using SHA-256 and `secrets`, replacing the mutable default with `None`, handling unknown patient IDs explicitly, and using a context manager for file output. After applying the changes, the program should be run and Pylint, Bandit, and Flake8 should all be rerun. The final reports should be saved and compared with the baseline reports to verify the findings are resolved.

## 4. What did you learn, and what are the limitations of static analysis?

I learned that code can run and still contain security risks, hidden bugs, and style problems. Static-analysis tools help identify likely issues early, but their warnings need human review: not every warning has the same impact, and tools cannot prove that the program's behavior is correct. Runtime tests and careful review are still necessary.
