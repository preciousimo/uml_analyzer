from typing import List, Dict
from ..linguistic.analyzer import LinguisticAnalyzer

class ValidationRule:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def validate(self, element) -> List[Dict]:
        """Base validation method to be implemented by specific rules."""
        raise NotImplementedError

class UseCaseValidationRules:
    def __init__(self):
        self.analyzer = LinguisticAnalyzer()

    def validate_actor_name(self, actor_name: str) -> List[Dict]:
        """Validate that actor names are nouns or noun phrases."""
        analysis = self.analyzer.analyze_text(actor_name)
        violations = []
        
        if not any(tag[1] in ['NOUN', 'PROPN'] for tag in analysis['pos_tags']):
            violations.append({
                'rule': 'actor_name_noun',
                'element': actor_name,
                'message': f"Actor name '{actor_name}' should be a noun or noun phrase"
            })
        
        return violations

    def validate_use_case_name(self, use_case_name: str) -> List[Dict]:
        """Validate that use case names contain verbs."""
        analysis = self.analyzer.analyze_text(use_case_name)
        violations = []
        
        if not any(tag[1] == 'VERB' for tag in analysis['pos_tags']):
            violations.append({
                'rule': 'use_case_name_verb',
                'element': use_case_name,
                'message': f"Use case name '{use_case_name}' should contain a verb"
            })
        
        return violations

class ClassValidationRules:
    def __init__(self):
        self.analyzer = LinguisticAnalyzer()

    def validate_class_name(self, class_name: str) -> List[Dict]:
        """Validate that class names are nouns."""
        analysis = self.analyzer.analyze_text(class_name)
        violations = []
        
        if not any(tag[1] in ['NOUN', 'PROPN'] for tag in analysis['pos_tags']):
            violations.append({
                'rule': 'class_name_noun',
                'element': class_name,
                'message': f"Class name '{class_name}' should be a noun"
            })
        
        return violations

    def validate_method_name(self, method_name: str) -> List[Dict]:
        """Validate that method names are verbs or verb phrases."""
        analysis = self.analyzer.analyze_text(method_name)
        violations = []
        
        if not any(tag[1] == 'VERB' for tag in analysis['pos_tags']):
            violations.append({
                'rule': 'method_name_verb',
                'element': method_name,
                'message': f"Method name '{method_name}' should contain a verb"
            })
        
        return violations