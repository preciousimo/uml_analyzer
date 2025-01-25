import spacy

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

def validate_use_case_semantics(use_case):
    """
    Validate actor roles and use case names using POS tagging.
    """
    doc = nlp(use_case["name"])
    # Check if use case name is a verb or verbal phrase
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    if not verbs:
        return False, "Use case name should be a verb or verbal phrase."
    return True, ""