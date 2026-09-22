import getpass

from password_analyzer.analyzer import analyze_password

PASS_MARK = "\u2713"
FAIL_MARK = "\u2717"

def print_banner():
    print("=" *50)
    print("        PASSWORD STRENGTH ANALYZER")
    print("=" *50)
    print("Your password is analyzed locally and is never")
    print("stored, logged, or displayed on screen")
    print("-" *50)

def print_report(result):
    print()
    print(f"Password length: {result['password_length']} characters")
    print(f"Password Strength: {result['rating']}" 
          f"({result['score']}/{result['max_score']} points)")
    print()

    print("Checks:")
    for check in result['checks']:
        mark = PASS_MARK if check['passed'] else FAIL_MARK
        print(f"  {mark} {check['message']}")

    print()
    print("Recommendations:")
    for tip in result['recommendations']:
        print(f"  - {tip}")
    print()

def main():
    print_banner()

    try:
        password = getpass.getpass("Enter your password to analyze: ")
    except (EOFError, KeyboardInterrupt):
        print("\nNo password entered. Exiting.")
        return

    result = analyze_password(password)

    password = None

    print_report(result)

if __name__ == "__main__":
    main()

        
