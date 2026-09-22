import re


COMMON_PASSWORDS = {
    "123456", "123456789", "qwerty", "password", "12345",
    "12345678", "111111", "1234567", "sunshine", "iloveyou",
    "admin", "welcome", "monkey", "login", "abc123",
    "starwars", "123123", "dragon", "passw0rd", "master",
    "hello", "freedom", "whatever", "qazwsx", "trustno1",
    "letmein", "football", "baseball", "superman", "michael",
    "shadow", "princess", "ninja", "mustang", "access",
    "flower", "hottie", "loveme", "jordan", "harley",
}
SEQUENTIAL_PATTERNS = [
    "0123456789",
    "abcdefghijklmnopqrstuvwxyz",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]
 
def check_length(password):
    
    length = len(password)

    if length >=12:
        return 2, True, "Good password length(12+ characters)"
    elif length >= 8:
        return 1, True, "Acceptable password length(8-11 characters)"
    else:
        return 0, False, "too short(less than 8 characters)"


def check_uppercase(password):
    
    has_upper = any(char.isupper() for char in password)
    if has_upper:
        return 1, True, "Contains uppercase letter(s)"
    else:
        return 0, False, "Missing uppercase letter(s)"

def check_lowercase(password):
    
    has_lower = any(char.islower() for char in password)
    if has_lower:
        return 1, True, "Contains lowercase letter(s)"
    else:
        return 0, False, "Missing lowercase letter(s)"

def check_numbers(password):
    
    has_number = any(char.isdigit() for char in password)
    if has_number:
        return 1, True, "Contains number(s)"
    else:
        return 0, False, "Missing number(s)"

def check_special_characters(password):
    
    has_special = bool(re.search(r"[^a-zA-Z0-9]", password))
    if has_special:
        return 1, True, "Contains special character(s)"
    else:
        return 0, False, "Missing special character(s)"

def check_common_password(password):
    if password.lower() in COMMON_PASSWORDS:
        return 0, False, "This is a very common password. Please choose a more unique one."
    else: 
        return 2, True, "Not found in common passwords list"

def check_repeated_characters(password):
    pattern = re.compile(r"(.)\1\1")

    if pattern.search(password):
        return 0, False, "Contains repeated characters (3 or more in a row)"
    else:
        return 1, True, "No obvious repeated characters"

def check_sequential_patterns(password):
    lowered = password.lower()
    for pattern in SEQUENTIAL_PATTERNS:
        for start in range(len(pattern) - 2):
            chunk = pattern[start:start + 3]
            if chunk in lowered:
                return 0, False, f"Contains a predictable sequential pattern: {chunk}"
    return 1, True, "No obvious sequential patterns"

def run_all_checks(password):
    check_functions = [
        ("length", check_length),
        ("uppercase", check_uppercase),
        ("lowercase", check_lowercase),
        ("numbers", check_numbers),
        ("special_characters", check_special_characters),
        ("common_password", check_common_password),
        ("repeated_characters", check_repeated_characters),
        ("sequential_patterns", check_sequential_patterns)
    ]

    results = []
    for name, func in check_functions:
        points, passed, message = func(password)
        results.append({
            "name": name,
            "points": points,
            "passed": passed,
            "message": message
        })

    return results

def calculate_total_score(check_results):
    return sum(result["points"] for result in check_results)

RATING_ORDER = [
    "Very Weak",
     "Weak",
     "Moderate",
    "Strong",
     "Very Strong"
]

def get_strength_rating(score, password, check_results):
    if len(password) < 6:
        return "Very Weak"

    checks_by_name = {c["name"]: c["passed"] for c in check_results}

    if not checks_by_name.get("common_password", True):
        return "Very Weak"

    if score <= 2:
        return " Very Weak"
    elif score <= 4:
        return "Weak"
    elif score <= 6:
        return "Moderate"
    elif score <= 8:
        return "Strong"
    else:
        return "Very Strong"

    has_