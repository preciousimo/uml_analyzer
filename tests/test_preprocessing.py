import unittest
from preprocessing.parser import parse_xmi
from preprocessing.tokenizer import preprocess_text

class TestPreprocessing(unittest.TestCase):
    def test_parse_xmi(self):
        uml_elements = parse_xmi("uml_diagram.xmi")
        self.assertIn("use_cases", uml_elements)
        self.assertIn("actors", uml_elements)
        self.assertIn("classes", uml_elements)

    def test_preprocess_text(self):
        tokens = preprocess_text("User logs into the system.")
        self.assertIn("logs", tokens)
        self.assertNotIn("the", tokens)

if __name__ == "__main__":
    unittest.main()