# Password Strength Analyzer

A beginner-friendly, command-line tool written in Python that analyzes a password and reports how strong it is — along with a clear, human-readable explanation of *why*.

## Description

Password Strength Analyzer asks the user for a password (input is hidden as it's typed) and checks it against a set of common security criteria: length, character variety, use of common/breached passwords, repeated characters, and predictable sequences like `123` or `qwerty`. It then returns a rating from **Very Weak** to **Very Strong**, along with a breakdown of exactly which checks passed or failed and practical recommendations for improvement.

This is a small, self-contained learning project — not a production security product. See [Limitations](#limitations) and [Disclaimer](#disclaimer) below.

## Why I Built This Project

I'm transitioning into software engineering and building a genuine interest in cybersecurity alongside it. Rather than just reading about password security theory, I wanted to build something that forced me to actually apply it: writing testable logic for real security checks, handling sensitive user input responsibly, and documenting my reasoning the way a security-minded engineer would. This project is my first step toward a portfolio that shows I can build, test, and explain small security-related tools — not just describe them.

## Cybersecurity Concepts Demonstrated

- **Password entropy basics** — why length and character variety matter for resisting brute-force attacks
- **Common password / dictionary attacks** — why checking against known weak passwords matters more than pattern rules alone
- **Predictable pattern detection** — recognizing keyboard walks (`qwerty`) and sequences (`123`, `abc`) attackers try early
- **Secure handling of sensitive input** — using `getpass` so passwords aren't displayed, and never logging, printing, or persisting the raw password
- **Defense-in-depth thinking** — combining multiple independent checks rather than relying on one rule
- **Test-driven development** — writing tests that define expected security behavior before trusting the implementation

## Features

- Rates passwords from **Very Weak** to **Very Strong**
- Explains *why* a password received its rating, check by check
- Detects missing uppercase, lowercase, numbers, and special characters
- Flags common/breached-style passwords (e.g. `password`, `123456`)
- Detects repeated characters (`aaaa`) and predictable sequences (`123`, `qwerty`)
- Gives specific, actionable recommendations
- Hides password input in the terminal using `getpass`
- Fully covered by unit tests (32 tests)

## Technologies Used

- **Python 3** (standard library only — no third-party dependencies)
- `re` — pattern matching for special characters and sequences
- `getpass` — secure, non-echoing password input
- `unittest` — Python's built-in testing framework

## Project Structure

```
password-strength-analyzer/
├── README.md
├── requirements.txt
├── main.py                       # CLI entry point (handles input/output)
├── password_analyzer/
│   ├── __init__.py
│   └── analyzer.py               # All analysis/scoring logic (no I/O)
└── tests/
    ├── __init__.py
    └── test_analyzer.py          # Unit tests for analyzer.py
```

**Why this structure?** The analysis logic (`analyzer.py`) is kept completely separate from the command-line interface (`main.py`). `analyzer.py` never calls `print()` or `input()` — it only takes a string in and returns a dictionary out. This separation is a common real-world pattern because it means:

1. The "brain" of the program can be tested directly, without needing to simulate terminal input.
2. The same logic could later be reused in a different interface (e.g. a web form or API) without any changes.

## How the Analyzer Works

The password is run through eight independent checks, each worth a number of points:

| Check | Points | What it looks for |
|---|---|---|
| Length | 0–2 | 12+ chars = 2 pts, 8–11 chars = 1 pt, under 8 = 0 pts |
| Uppercase letters | 0–1 | At least one `A-Z` |
| Lowercase letters | 0–1 | At least one `a-z` |
| Numbers | 0–1 | At least one digit |
| Special characters | 0–1 | Anything that isn't a letter or digit |
| Not a common password | 0–2 | Not found in a small list of known weak passwords |
| No repeated characters | 0–1 | No character repeated 3+ times in a row (e.g. `aaa`) |
| No sequential patterns | 0–1 | No `123`, `abc`, `qwerty`-style sequences |

The points are added up (out of a maximum of 10) and mapped to a rating. Two situations override the score entirely, because they matter more than raw math:

- **Under 6 characters** → always **Very Weak** (trivially brute-forceable regardless of variety)
- **Matches a known common password** → always **Very Weak** (an attacker will try it first, no matter how "varied" it looks)

Repeated characters or predictable sequences also **cap** the rating at "Weak" at best, since they make a password far less random than its raw length suggests.

## How to Install / Run It

No installation required beyond Python 3 itself.

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd password-strength-analyzer

# 2. Run the analyzer
python3 main.py
```

You'll be prompted to enter a password. Your typing will not be shown on screen.

## How to Run the Tests

```bash
python3 -m unittest discover tests -v
```

This runs all 32 tests and prints each one's name and result (`ok` or `FAIL`). You can also run just the test file directly:

```bash
python3 -m unittest tests.test_analyzer -v
```

## Example Usage / Output

```
==================================================
        PASSWORD STRENGTH ANALYZER
==================================================
Your password is analyzed locally and is never
stored, logged, or displayed on screen.
--------------------------------------------------

Enter a password to analyze: 

Password length: 15 characters
Password Strength: Very Strong (10/10 points)

Checks:
  ✓ Good password length (12+ characters)
  ✓ Contains uppercase letters
  ✓ Contains lowercase letters
  ✓ Contains numbers
  ✓ Contains special characters
  ✓ Not found in common password list
  ✓ No obvious repeated characters
  ✓ No obvious sequential patterns

Recommendations:
  - Avoid using personal information (names, birthdays, etc.)
  - Consider using a passphrase (multiple random words)
```

Example for a weak password (e.g. `password123`):

```
Password Strength: Very Weak (5/10 points)

Checks:
  ✓ Good password length (12+ characters)
  ✗ Missing uppercase letters
  ✓ Contains lowercase letters
  ✓ Contains numbers
  ✗ Missing special characters
  ✗ This is a very common password - easy to guess
  ✓ No obvious repeated characters
  ✓ No obvious sequential patterns

Recommendations:
  - Add at least one uppercase letter
  - Add at least one special character (e.g. !, @, #, $)
  - Avoid common passwords found in known password lists
  - Avoid using personal information (names, birthdays, etc.)
  - Consider using a passphrase (multiple random words)
```

## Security and Privacy Considerations

- The password is **never stored, logged, printed, or written to disk** at any point. It exists only in memory for the duration of the analysis.
- User input is collected with `getpass.getpass()` instead of `input()`, so the password is not echoed to the terminal screen or saved in shell history the way a typed command might be.
- The analyzer does not connect to the internet or any external service — everything runs locally, so the password never leaves the machine it's typed on.
- The common-password list used here is intentionally small and for demonstration purposes. A production tool would check against a much larger breached-password dataset (e.g. via a k-anonymity API such as Have I Been Pwned), which this project deliberately does not attempt.

## What I Learned

- How to break a problem into small, independently testable functions instead of one large script
- Why **rules-based** strength checking (length + character variety) is useful but incomplete on its own — a "complex-looking" but common password is still weak
- The practical difference between checking a password's *strength* (this project) and *hashing/storing* a password securely (a related but separate concept — see below)
- How to use Python's `unittest` framework to write tests before/alongside implementation, and how a failing test can reveal a flaw in the *logic*, not just the code
- How to think about a small piece of sensitive data (a password) as something to minimize exposure to, even in a simple local script

## Limitations

- This tool checks password **strength**, not whether a password has actually appeared in a real data breach (that would require checking against a breach database).
- The common-password and pattern lists are small and for educational purposes — they are not exhaustive.
- It does not check for context-specific weaknesses, like a password containing the user's own name or the service name, since it has no knowledge of the user.
- Scoring is rule-based, not a true entropy calculation — it's a helpful approximation, not a cryptographic measurement.

## Future Improvements

- Add an entropy-based scoring option (bits of entropy) alongside the rule-based score
- Integrate with the Have I Been Pwned API (using k-anonymity, so the real password is never sent) to check for known breached passwords
- Add a simple GUI or web front-end using the existing `analyzer.py` logic unchanged
- Allow the user to check a password against a custom "personal information" list (e.g. their own name/birth year) without storing it
- Expand the common-password and pattern lists, or load them from an external file

## Disclaimer

This is a learning/portfolio project built to demonstrate foundational cybersecurity and Python concepts. It is **not** an enterprise-grade password security tool, has not been audited, and should not be relied on as the sole safeguard for any real account or system. For production use cases, rely on established, audited libraries and services.
