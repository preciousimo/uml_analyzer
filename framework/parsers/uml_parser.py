import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

class UMLElement:
    def __init__(self, id: str, name: str, element_type: str):
        self.id = id
        self.name = name
        self.element_type = element_type
        self.relationships: List['UMLRelationship'] = []

class UMLRelationship:
    def __init__(self, source_id: str, target_id: str, relationship_type: str):
        self.source_id = source_id
        self.target_id = target_id
        self.relationship_type = relationship_type

class UseCaseParser:
    def __init__(self):
        self.actors: Dict[str, UMLElement] = {}
        self.use_cases: Dict[str, UMLElement] = {}
        self.relationships: List[UMLRelationship] = []

    def parse_xmi(self, xmi_content: str) -> None:
        """Parse XMI content containing Use Case diagram elements."""
        root = ET.fromstring(xmi_content)
        
        # Parse actors
        for actor in root.findall(".//actor"):
            actor_id = actor.get('id')
            actor_name = actor.get('name')
            self.actors[actor_id] = UMLElement(actor_id, actor_name, 'actor')

        # Parse use cases
        for use_case in root.findall(".//useCase"):
            use_case_id = use_case.get('id')
            use_case_name = use_case.get('name')
            self.use_cases[use_case_id] = UMLElement(use_case_id, use_case_name, 'useCase')

        # Parse relationships
        for relation in root.findall(".//relationship"):
            source_id = relation.get('source')
            target_id = relation.get('target')
            rel_type = relation.get('type')
            relationship = UMLRelationship(source_id, target_id, rel_type)
            self.relationships.append(relationship)

class ClassParser:
    def __init__(self):
        self.classes: Dict[str, 'ClassElement'] = {}
        self.relationships: List[UMLRelationship] = []

    def parse_xmi(self, xmi_content: str) -> None:
        """Parse XMI content containing Class diagram elements."""
        root = ET.fromstring(xmi_content)
        
        # Parse classes
        for class_elem in root.findall(".//class"):
            class_id = class_elem.get('id')
            class_name = class_elem.get('name')
            
            # Parse attributes
            attributes = []
            for attr in class_elem.findall(".//attribute"):
                attributes.append({
                    'name': attr.get('name'),
                    'type': attr.get('type'),
                    'visibility': attr.get('visibility')
                })

            # Parse methods
            methods = []
            for method in class_elem.findall(".//method"):
                methods.append({
                    'name': method.get('name'),
                    'return_type': method.get('returnType'),
                    'parameters': method.findall(".//parameter")
                })

            self.classes[class_id] = ClassElement(class_id, class_name, attributes, methods)

        # Parse relationships
        for relation in root.findall(".//relationship"):
            source_id = relation.get('source')
            target_id = relation.get('target')
            rel_type = relation.get('type')
            self.relationships.append(UMLRelationship(source_id, target_id, rel_type))

class ClassElement(UMLElement):
    def __init__(self, id: str, name: str, attributes: List[Dict], methods: List[Dict]):
        super().__init__(id, name, 'class')
        self.attributes = attributes
        self.methods = methods