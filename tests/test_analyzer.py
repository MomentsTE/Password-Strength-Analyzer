import unittest
from password_analyzer.analyzer import (
    analyze_password,
    check_length,
    check_uppercase,
    check_lowercase,
    check_numbers,
    check_special_characters,
    check_common_password,
    check_repeated_characters,
    check_sequential_patterns
)

class TestIndividualChecks(unittest.TestCase):
   
    def test_check_length_too_short(self):
        points, passed, _ = check_length("abc")
        self.assertFalse(passed)
        self.assertEqual(points, 0)
 
    def test_check_length_acceptable(self):
        points, passed, _ = check_length("abcdefgh")  # 8 characters
        self.assertTrue(passed)
        self.assertEqual(points, 1)
 
    def test_check_length_good(self):
        points, passed, _ = check_length("abcdefghijkl")  # 12 characters
        self.assertTrue(passed)
        self.assertEqual(points, 2)
 
    def test_check_uppercase_missing(self):
        _, passed, _ = check_uppercase("alllowercase")
        self.assertFalse(passed)
 
    def test_check_uppercase_present(self):
        _, passed, _ = check_uppercase("HasAnUpper")
        self.assertTrue(passed)
 
    def test_check_lowercase_missing(self):
        _, passed, _ = check_lowercase("ALLUPPERCASE")
        self.assertFalse(passed)
 
    def test_check_lowercase_present(self):
        _, passed, _ = check_lowercase("hasLower")
        self.assertTrue(passed)
 
    def test_check_numbers_missing(self):
        _, passed, _ = check_numbers("NoNumbersHere")
        self.assertFalse(passed)
 
    def test_check_numbers_present(self):
        _, passed, _ = check_numbers("Number1Here")
        self.assertTrue(passed)
 
    def test_check_special_characters_missing(self):
        _, passed, _ = check_special_characters("NoSpecials123")
        self.assertFalse(passed)
 
    def test_check_special_characters_present(self):
        _, passed, _ = check_special_characters("Special!123")
        self.assertTrue(passed)
 
    def test_check_common_password_is_flagged(self):
        _, passed, _ = check_common_password("password")
        self.assertFalse(passed)
 
    def test_check_common_password_is_case_insensitive(self):
        # "Password" should still be caught even with a capital P
        _, passed, _ = check_common_password("Password")
        self.assertFalse(passed)
 
    def test_check_common_password_not_flagged(self):
        _, passed, _ = check_common_password("Xk9#mQ2vL7pZ")
        self.assertTrue(passed)
 
    def test_check_repeated_characters_detected(self):
        _, passed, _ = check_repeated_characters("Paaassword111")
        self.assertFalse(passed)
 
    def test_check_repeated_characters_not_detected(self):
        _, passed, _ = check_repeated_characters("NormalPassword1")
        self.assertTrue(passed)
 
    def test_check_sequential_patterns_detected_numbers(self):
        _, passed, _ = check_sequential_patterns("MyPass123!")
        self.assertFalse(passed)
 
    def test_check_sequential_patterns_detected_letters(self):
        _, passed, _ = check_sequential_patterns("abcDoor99!")
        self.assertFalse(passed)
 
    def test_check_sequential_patterns_detected_keyboard_walk(self):
        _, passed, _ = check_sequential_patterns("qwerty99!")
        self.assertFalse(passed)
 
    def test_check_sequential_patterns_not_detected(self):
        _, passed, _ = check_sequential_patterns("Xk9#mQ2vL7pZ")
        self.assertTrue(passed)

class TestAnalyzePassword(unittest.TestCase): 
    def test_empty_password(self):
        result = analyze_password("")
        self.assertEqual(result["rating"], "Very Weak")
        self.assertEqual(result["score"], 0)
 
    def test_very_short_password(self):
        result = analyze_password("ab1")
        self.assertEqual(result["rating"], "Very Weak")
 
    def test_only_lowercase_password(self):
        result = analyze_password("abcdefghijkl")
        # Long, but missing uppercase/numbers/special characters
        self.assertIn(result["rating"], ["Weak", "Moderate"])
 
    def test_common_password_rated_very_weak(self):
        result = analyze_password("password")
        self.assertEqual(result["rating"], "Very Weak")
 
    def test_password_with_repeated_pattern(self):
        result = analyze_password("aaaaaaaa")
        # Repeated characters should cap the rating at "Weak" at best,
        # even though the password is 8 characters long.
        self.assertIn(result["rating"], ["Very Weak", "Weak"])
 
    def test_uppercase_and_lowercase_password(self):
        result = analyze_password("HelloWorldPassword")
        # Has upper/lower and is long, but no numbers/specials
        self.assertIn(result["rating"], ["Weak", "Moderate", "Strong"])
 
    def test_password_with_numbers(self):
        result = analyze_password("Hello12345World")
        checks_by_name = {c["name"]: c["passed"] for c in result["checks"]}
        self.assertTrue(checks_by_name["numbers"])
 
    def test_password_with_special_characters(self):
        result = analyze_password("Hello!World#123")
        checks_by_name = {c["name"]: c["passed"] for c in result["checks"]}
        self.assertTrue(checks_by_name["special_characters"])
 
    def test_strong_password(self):
        result = analyze_password("Tr0ub4dor&Zebra")
        self.assertIn(result["rating"], ["Strong", "Very Strong"])
 
    def test_very_strong_password(self):
        result = analyze_password("Xk9#mQ2vL7pZ!nR4")
        self.assertEqual(result["rating"], "Very Strong")
 
    def test_result_contains_recommendations(self):
        result = analyze_password("weak")
        self.assertTrue(len(result["recommendations"]) > 0)
 
    def test_result_contains_all_check_names(self):
        result = analyze_password("SomePassword123!")
        expected_names = {
            "length", "uppercase", "lowercase", "numbers",
            "special_characters", "common_password",
            "repeated_characters", "sequential_patterns",
        }
        actual_names = {c["name"] for c in result["checks"]}
        self.assertEqual(expected_names, actual_names)
 
 
if __name__ == "__main__":
    unittest.main()