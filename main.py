from preprocessing.parser import parse_xmi
from preprocessing.tokenizer import preprocess_text
from error_detection.detector import detect_errors
from reporting.report_generator import generate_report

def main():
    # Step 1: Parse UML diagram
    uml_elements = parse_xmi("uml_diagram.xmi")

    # Step 2: Preprocess text
    for use_case in uml_elements["use_cases"]:
        use_case["description"] = preprocess_text(use_case["description"])

    # Step 3: Detect errors
    detected_errors = detect_errors(uml_elements)

    # Step 4: Define actual errors (ground truth)
    actual_errors = [
        "Use Case Error: Login - Use case name should be a verb or verbal phrase.",
        "Cross-Diagram Error: Use case 'Login' and class 'UserManager' are not semantically aligned."
    ]

    # Step 5: Generate report with performance metrics
    report = generate_report(detected_errors, actual_errors)
    print(report)

if __name__ == "__main__":
    main()