from semantic_analysis.use_case_validation import validate_use_case_semantics
from semantic_analysis.class_validation import validate_class_semantics
from semantic_analysis.cross_diagram import semantic_similarity

def detect_errors(uml_elements):
    """
    Identify and highlight inconsistencies in UML diagrams.
    """
    errors = []

    # Validate Use Case Diagrams
    for use_case in uml_elements["use_cases"]:
        is_valid, message = validate_use_case_semantics(use_case)
        if not is_valid:
            errors.append(f"Use Case Error: {use_case['name']} - {message}")

    # Validate Class Diagrams
    for cls in uml_elements["classes"]:
        is_valid, message = validate_class_semantics(cls)
        if not is_valid:
            errors.append(f"Class Error: {cls['name']} - {message}")

    # Cross-Diagram Validation
    for use_case in uml_elements["use_cases"]:
        for cls in uml_elements["classes"]:
            similarity = semantic_similarity(use_case["name"], cls["name"])
            if similarity < 0.5:  # Threshold for semantic alignment
                errors.append(f"Cross-Diagram Error: Use case '{use_case['name']}' and class '{cls['name']}' are not semantically aligned.")

    return errors