import spacy

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

def validate_class_semantics(cls):
    """
    Validate class names, attributes, and methods using linguistic rules.
    """
    # Check if class name is a singular noun
    doc = nlp(cls["name"])
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    if not nouns:
        return False, "Class name should be a singular noun."
    # Check method naming conventions
    for method in cls["methods"]:
        if not method[0].islower():
            return False, f"Method name '{method}' should be in camelCase."
    return True, ""