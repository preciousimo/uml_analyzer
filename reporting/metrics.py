def calculate_precision(true_positives, false_positives):
    """
    Calculate precision: TP / (TP + FP)
    """
    return true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0

def calculate_recall(true_positives, false_negatives):
    """
    Calculate recall: TP / (TP + FN)
    """
    return true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

def calculate_f1_score(precision, recall):
    """
    Calculate F1 score: 2 * (precision * recall) / (precision + recall)
    """
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

def evaluate_performance(detected_errors, actual_errors):
    """
    Evaluate framework performance using precision, recall, and F1 score.
    """
    true_positives = len(set(detected_errors).intersection(set(actual_errors)))
    false_positives = len(set(detected_errors).difference(set(actual_errors)))
    false_negatives = len(set(actual_errors).difference(set(detected_errors)))

    precision = calculate_precision(true_positives, false_positives)
    recall = calculate_recall(true_positives, false_negatives)
    f1_score = calculate_f1_score(precision, recall)

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }