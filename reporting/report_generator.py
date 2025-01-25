from .metrics import evaluate_performance

def generate_report(detected_errors, actual_errors):
    """
    Generate a detailed report with performance metrics.
    """
    report = "Semantic Validation Report\n"
    report += "========================\n"

    if not detected_errors:
        report += "No errors found. The UML diagrams are semantically coherent.\n"
    else:
        for error in detected_errors:
            report += f"- {error}\n"

    # Calculate performance metrics
    metrics = evaluate_performance(detected_errors, actual_errors)
    report += "\nPerformance Metrics\n"
    report += "===================\n"
    report += f"Precision: {metrics['precision']:.2f}\n"
    report += f"Recall: {metrics['recall']:.2f}\n"
    report += f"F1 Score: {metrics['f1_score']:.2f}\n"
    report += f"True Positives: {metrics['true_positives']}\n"
    report += f"False Positives: {metrics['false_positives']}\n"
    report += f"False Negatives: {metrics['false_negatives']}\n"

    return report