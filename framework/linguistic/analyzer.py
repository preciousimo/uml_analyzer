import spacy
from typing import Dict, List, Tuple

class LinguisticAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        
    def analyze_text(self, text: str) -> Dict:
        """Perform linguistic analysis on text."""
        doc = self.nlp(text)
        return {
            'pos_tags': self.extract_pos_tags(doc),
            'entities': self.extract_entities(doc),
            'dependencies': self.extract_dependencies(doc),
            'noun_phrases': self.extract_noun_phrases(doc),
            'verb_phrases': self.extract_verb_phrases(doc)
        }

    def extract_pos_tags(self, doc) -> List[Tuple[str, str]]:
        """Extract part-of-speech tags."""
        return [(token.text, token.pos_) for token in doc]

    def extract_entities(self, doc) -> List[Tuple[str, str]]:
        """Extract named entities."""
        return [(ent.text, ent.label_) for ent in doc.ents]

    def extract_dependencies(self, doc) -> List[Tuple[str, str, str]]:
        """Extract syntactic dependencies."""
        return [(token.text, token.dep_, token.head.text) for token in doc]

    def extract_noun_phrases(self, doc) -> List[str]:
        """Extract noun phrases."""
        return [chunk.text for chunk in doc.noun_chunks]

    def extract_verb_phrases(self, doc) -> List[str]:
        """Extract verb phrases."""
        return [token.text for token in doc if token.pos_ == "VERB"]

class SemanticRoleLabeler:
    def __init__(self):
        self.analyzer = LinguisticAnalyzer()

    def label_roles(self, sentence: str) -> Dict:
        """Label semantic roles in a sentence."""
        analysis = self.analyzer.analyze_text(sentence)
        
        # Identify subject (typically actor)
        subject = self._find_subject(analysis['dependencies'])
        
        # Identify action (verb phrase)
        action = self._find_main_verb(analysis['dependencies'])
        
        # Identify object (typically system or component)
        object_ = self._find_object(analysis['dependencies'])
        
        return {
            'subject': subject,
            'action': action,
            'object': object_
        }

    def _find_subject(self, dependencies: List[Tuple[str, str, str]]) -> str:
        """Find the subject in dependencies."""
        for word, dep, head in dependencies:
            if dep in ['nsubj', 'nsubjpass']:
                return word
        return ""

    def _find_main_verb(self, dependencies: List[Tuple[str, str, str]]) -> str:
        """Find the main verb in dependencies."""
        for word, dep, head in dependencies:
            if dep == 'ROOT' and word.lower() not in ['is', 'are', 'was', 'were']:
                return word
        return ""

    def _find_object(self, dependencies: List[Tuple[str, str, str]]) -> str:
        """Find the object in dependencies."""
        for word, dep, head in dependencies:
            if dep in ['dobj', 'pobj']:
                return word
        return ""