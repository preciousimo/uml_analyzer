from typing import Dict, List, Set
import networkx as nx
from ..linguistic.analyzer import LinguisticAnalyzer

class SemanticAnalyzer:
    def __init__(self):
        self.analyzer = LinguisticAnalyzer()
        self.similarity_threshold = 0.75

    def analyze_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts."""
        doc1 = self.analyzer.nlp(text1)
        doc2 = self.analyzer.nlp(text2)
        return doc1.similarity(doc2)

    def build_semantic_graph(self, elements: List[Dict]) -> nx.Graph:
        """Build a graph representing semantic relationships between elements."""
        graph = nx.Graph()
        
        # Add nodes
        for element in elements:
            graph.add_node(element['id'], 
                         name=element['name'], 
                         type=element['type'],
                         semantic_props=self.extract_semantic_properties(element['name']))
        
        # Add edges based on semantic similarity
        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                similarity = self.analyze_semantic_similarity(elem1['name'], elem2['name'])
                if similarity >= self.similarity_threshold:
                    graph.add_edge(elem1['id'], elem2['id'], weight=similarity)
        
        return graph

    def extract_semantic_properties(self, text: str) -> Dict:
        """Extract semantic properties from text."""
        analysis = self.analyzer.analyze_text(text)
        return {
            'nouns': [token for token, pos in analysis['pos_tags'] if pos in ['NOUN', 'PROPN']],
            'verbs': [token for token, pos in analysis['pos_tags'] if pos == 'VERB'],
            'entities': analysis['entities']
        }

class CrossDiagramAnalyzer:
    def __init__(self, semantic_analyzer: SemanticAnalyzer):
        self.semantic_analyzer = semantic_analyzer
        self.traceability_matrix = {}

    def analyze_traceability(self, use_cases: Dict, classes: Dict) -> Dict:
        """Generate traceability matrix between use cases and classes."""
        matrix = {}
        
        for uc_id, use_case in use_cases.items():
            matrix[use_case.name] = {}
            for class_id, class_elem in classes.items():
                similarity = self.semantic_analyzer.analyze_semantic_similarity(
                    use_case.name, 
                    class_elem.name
                )
                matrix[use_case.name][class_elem.name] = similarity
        
        self.traceability_matrix = matrix
        return matrix

    def identify_semantic_clusters(self, graph: nx.Graph) -> List[Set]:
        """Identify clusters of semantically related elements."""
        # Use community detection to find clusters
        communities = nx.community.louvain_communities(graph)
        return communities

    def analyze_semantic_coverage(self, use_cases: Dict, classes: Dict) -> Dict:
        """Analyze semantic coverage between use cases and implementing classes."""
        coverage = {}
        
        for uc_id, use_case in use_cases.items():
            coverage[use_case.name] = {
                'implementing_classes': [],
                'missing_functionality': [],
                'semantic_overlap': []
            }
            
            # Find potential implementing classes
            for class_id, class_elem in classes.items():
                similarity = self.semantic_analyzer.analyze_semantic_similarity(
                    use_case.name,
                    class_elem.name
                )
                
                if similarity >= self.semantic_analyzer.similarity_threshold:
                    coverage[use_case.name]['implementing_classes'].append({
                        'class_name': class_elem.name,
                        'similarity_score': similarity
                    })
                
                # Check for method coverage
                missing_functionality = self.identify_missing_functionality(
                    use_case, 
                    class_elem
                )
                if missing_functionality:
                    coverage[use_case.name]['missing_functionality'].extend(missing_functionality)
        
        return coverage

    def identify_missing_functionality(self, use_case: 'UMLElement', class_elem: 'ClassElement') -> List[str]:
        """Identify missing functionality in implementing classes."""
        missing = []
        use_case_semantics = self.semantic_analyzer.extract_semantic_properties(use_case.name)
        
        # Check if all actions (verbs) in use case have corresponding methods
        for verb in use_case_semantics['verbs']:
            method_found = False
            for method in class_elem.methods:
                method_semantics = self.semantic_analyzer.extract_semantic_properties(method['name'])
                if verb in method_semantics['verbs']:
                    method_found = True
                    break
            
            if not method_found:
                missing.append(f"Action '{verb}' not implemented in class '{class_elem.name}'")
        
        return missing