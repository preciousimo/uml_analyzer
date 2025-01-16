from typing import List, Dict
import json
import matplotlib.pyplot as plt
import seaborn as sns

class ReportGenerator:
    def __init__(self):
        self.report_data = {}

    def generate_validation_report(self, violations: List[Dict]) -> str:
        """Generate a detailed validation report."""
        report = {
            'summary': self._generate_summary(violations),
            'detailed_violations': self._categorize_violations(violations),
            'recommendations': self._generate_recommendations(violations)
        }
        
        self.report_data = report
        return json.dumps(report, indent=2)

    def _generate_summary(self, violations: List[Dict]) -> Dict:
        """Generate summary statistics of violations."""
        violation_types = {}
        for violation in violations:
            rule_type = violation['rule']
            violation_types[rule_type] = violation_types.get(rule_type, 0) + 1
        
        return {
            'total_violations': len(violations),
            'violation_types': violation_types
        }

    def _categorize_violations(self, violations: List[Dict]) -> Dict:
        """Categorize violations by type and severity."""
        categories = {
            'naming': [],
            'semantic': [],
            'relationship': [],
            'cross_diagram': []
        }
        
        for violation in violations:
            if 'name' in violation['rule']:
                categories['naming'].append(violation)
            elif 'semantic' in violation['rule']:
                categories['semantic'].append(violation)
            elif 'relationship' in violation['rule']:
                categories['relationship'].append(violation)
            else:
                categories['cross_diagram'].append(violation)
        
        return categories

    def _generate_recommendations(self, violations: List[Dict]) -> List[str]:
        """Generate improvement recommendations based on violations."""
        recommendations = []
        violation_patterns = self._analyze_violation_patterns(violations)
        
        for pattern, count in violation_patterns.items():
            if count > 1:
                recommendations.append(self._get_recommendation_for_pattern(pattern))
        
        return recommendations

    def _analyze_violation_patterns(self, violations: List[Dict]) -> Dict:
        """Analyze patterns in violations."""
        patterns = {}
        for violation in violations:
            pattern = violation['rule']
            patterns[pattern] = patterns.get(pattern, 0) + 1
        return patterns

    def _get_recommendation_for_pattern(self, pattern: str) -> str:
        """Get specific recommendation for a violation pattern."""
        recommendations = {
            'actor_name_noun': "Ensure all actor names are nouns or noun phrases describing roles",
            'use_case_name_verb': "Use verb phrases for use case names to clearly indicate actions",
            'class_name_noun': "Use singular nouns for class names following Pascal case convention",
            'method_name_verb': "Start method names with verbs following camelCase convention",
            'use_case_implementation': "Ensure all use cases have corresponding implementing classes",
            'actor_method_mapping': "Verify that actor interactions are properly mapped to class methods"
        }
        return recommendations.get(pattern, "Review and refine the model according to UML best practices")

    def generate_visualization(self, type: str) -> None:
        """Generate visualization of validation results."""
        if type == 'violation_summary':
            self._plot_violation_summary()
        elif type == 'semantic_coverage':
            self._plot_semantic_coverage()

    def _plot_violation_summary(self) -> None:
        """Plot summary of violations."""
        summary = self.report_data['summary']['violation_types']
        
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(summary.keys()), y=list(summary.values()))
        plt.title('Validation Violations by Type')
        plt.xticks(rotation=45)
        plt.ylabel('Number of Violations')
        plt.tight_layout()
        plt.savefig('validation_summary.png')
        plt.close()

# Example usage
if __name__ == "__main__":
    # Initialize components
    use_case_parser = UseCaseParser()
    class_parser = ClassParser()
    semantic_analyzer = SemanticAnalyzer()
    cross_analyzer = CrossDiagramAnalyzer(semantic_analyzer)
    report_generator = ReportGenerator()
    
    # Parse diagrams and perform analysis
    # (example code from previous implementation)
    
    # Generate and display report
    violations = []  # Collect violations from validation
    report = report_generator.generate_validation_report(violations)
    print(report)
    
    # Generate visualizations
    report_generator.generate_visualization('violation_summary')