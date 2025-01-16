from typing import Dict, List
from ..parsers.uml_parser import UseCaseParser, ClassParser

class CrossDiagramValidator:
    def __init__(self, use_case_parser: UseCaseParser, class_parser: ClassParser):
        self.use_case_parser = use_case_parser
        self.class_parser = class_parser
        
    def validate_traceability(self) -> List[Dict]:
        """Validate traceability between use cases and classes."""
        violations = []
        
        # Check if each use case has implementing classes
        for use_case_id, use_case in self.use_case_parser.use_cases.items():
            implementing_classes = self._find_implementing_classes(use_case)
            
            if not implementing_classes:
                violations.append({
                    'rule': 'use_case_implementation',
                    'element': use_case.name,
                    'message': f"Use case '{use_case.name}' has no implementing classes"
                })
        
        return violations

    def validate_actor_method_mapping(self) -> List[Dict]:
        """Validate mapping between actor interactions and class methods."""
        violations = []
        
        for actor_id, actor in self.use_case_parser.actors.items():
            # Get all use cases connected to this actor
            actor_use_cases = self._get_actor_use_cases(actor)
            
            for use_case in actor_use_cases:
                # Find implementing classes for the use case
                implementing_classes = self._find_implementing_classes(use_case)
                
                # Check if methods exist in implementing classes
                if not self._verify_method_existence(use_case, implementing_classes):
                    violations.append({
                        'rule': 'actor_method_mapping',
                        'element': f"{actor.name} - {use_case.name}",
                        'message': f"No corresponding methods found for actor '{actor.name}' interaction in use case '{use_case.name}'"
                    })
        
        return violations

    def _find_implementing_classes(self, use_case: 'UMLElement') -> List['ClassElement']:
        """Find classes that implement a use case."""
        implementing_classes = []
        
        # This is a simplified implementation. In practice, you would need more
        # sophisticated logic to determine implementing classes based on naming,
        # dependencies, or explicit traceability links.
        for class_id, class_elem in self.class_parser.classes.items():
            if self._is_implementing_class(use_case, class_elem):
                implementing_classes.append(class_elem)
        
        return implementing_classes

    def _is_implementing_class(self, use_case: 'UMLElement', class_elem: 'ClassElement') -> bool:
        """Determine if a class implements a use case."""
        # This is a simplified check. In practice, you would need more sophisticated
        # logic to determine if a class implements a use case.
        use_case_words = set(use_case.name.lower().split())
        class_words = set(class_elem.name.lower().split())
        
        return len(use_case_words.intersection(class_words)) > 0

    def _get_actor_use_cases(self, actor: 'UMLElement') -> List['UMLElement']:
        """Get all use cases connected to an actor."""
        use_cases = []
        
        for relationship in self.use_case_parser.relationships:
            if relationship.source_id == actor.id:
                target_use_case = self.use_case_parser.use_cases.get(relationship.target_id)
                if target_use_case:
                    use_cases.append(target_use_case)
        
        return use_cases

    def _verify_method_existence(self, use_case: 'UMLElement', implementing_classes: List['ClassElement']) -> bool:
        """Verify that appropriate methods exist in implementing classes."""
        # This is a simplified check. In practice, you would need more sophisticated
        # logic to verify method existence and compatibility.
        use_case_action = use_case.name.lower()
        
        for class_elem in implementing_classes:
            for method in class_elem.methods:
                if method['name'].lower() in use_case_action:
                    return True
        
        return False

# Main usage example
def main():
    # Initialize parsers
    use_case_parser = UseCaseParser()
    class_parser = ClassParser()
    
    # Parse XMI content (example)
    use_case_xmi = """<?xml version="1.0" encoding="UTF-8"?>
    <uml:Model>
        <!-- Use Case diagram content -->
    </uml:Model>"""
    
    class_xmi = """<?xml version="1.0" encoding="UTF-8"?>
    <uml:Model>
        <!-- Class diagram content -->
    </uml:Model>"""
    
    use_case_parser.parse_xmi(use_case_xmi)
    class_parser.parse_xmi(class_xmi)
    
    # Initialize validators
    use_case_validator = UseCaseValidationRules()
    class_validator = ClassValidationRules()
    cross_validator = CrossDiagramValidator(use_case_parser, class_parser)
    
    # Perform validation
    violations = []
    
    # Validate use case elements
    for actor_id, actor in use_case_parser.actors.items():
        violations.extend(use_case_validator.validate_actor_name(actor.name))
    
    for use_case_id, use_case in use_case_parser.use_cases.items():
        violations.extend(use_case_validator.validate_use_case_name(use_case.name))
    
    # Validate class elements
    for class_id, class_elem in class_parser.classes.items():
        violations.extend(class_validator.validate_class_name(class_elem.name))
        for method in class_elem.methods:
            violations.extend(class_validator.validate_method_name(method['name']))
    
    # Perform cross-diagram validation
    violations.extend(cross_validator.validate_traceability())
    violations.extend(cross_validator.validate_actor_method_mapping())
    
    return violations