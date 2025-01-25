import unittest
from semantic_analysis.use_case_validation import validate_use_case_semantics
from semantic_analysis.class_validation import validate_class_semantics

class TestSemanticAnalysis(unittest.TestCase):
    def test_validate_use_case_semantics(self):
        use_case = {"name": "Login", "description": "User logs into the system."}
        is_valid, message = validate_use_case_semantics(use_case)
        self.assertTrue(is_valid)

    def test_validate_class_semantics(self):
        cls = {"name": "UserManager", "methods": ["authenticateUser"]}
        is_valid, message = validate_class_semantics(cls)
        self.assertTrue(is_valid)

if __name__ == "__main__":
    unittest.main()