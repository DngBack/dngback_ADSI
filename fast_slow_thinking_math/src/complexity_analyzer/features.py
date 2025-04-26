"""
Feature extraction utilities for the Complexity Analyzer.
"""

import re
import nltk
from nltk.tokenize import word_tokenize
import sympy
import config

# Download necessary NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class FeatureExtractor:
    """
    Extracts features from mathematical problems for complexity analysis.
    """
    
    def __init__(self):
        """Initialize the feature extractor with configuration settings."""
        self.domain_complexity = config.COMPLEXITY_ANALYZER['DOMAIN_COMPLEXITY']
        self.operation_complexity = config.COMPLEXITY_ANALYZER['OPERATION_COMPLEXITY']
        
        # Compile regex patterns for feature extraction
        self.variable_pattern = re.compile(r'[a-zA-Z](?!\w)')
        self.operation_patterns = {
            'addition': re.compile(r'[+]|\bplus\b|\badd\b|\bsum\b|\btotal\b'),
            'subtraction': re.compile(r'[-]|\bminus\b|\bsubtract\b|\bdifference\b'),
            'multiplication': re.compile(r'[*×]|\btimes\b|\bmultiply\b|\bproduct\b'),
            'division': re.compile(r'[/÷]|\bdivide\b|\bquotient\b|\bratio\b'),
            'exponentiation': re.compile(r'[\^]|\bpower\b|\bsquared\b|\bcubed\b|\bexponent\b'),
            'root': re.compile(r'\broot\b|\bsquare root\b|\bcube root\b|\b\sqrt\b'),
            'logarithm': re.compile(r'\blog\b|\bln\b|\blogarithm\b'),
            'trigonometric': re.compile(r'\bsin\b|\bcos\b|\btan\b|\bsine\b|\bcosine\b|\btangent\b'),
            'derivative': re.compile(r'\bderivative\b|\bdifferentiate\b|\bd/dx\b'),
            'integral': re.compile(r'\bintegral\b|\bintegrate\b|\b∫\b'),
            'limit': re.compile(r'\blimit\b|\blim\b'),
            'summation': re.compile(r'\bsummation\b|\bsum of\b|\b∑\b'),
            'product': re.compile(r'\bproduct of\b|\b∏\b'),
        }
        
        self.domain_keywords = {
            'arithmetic': ['add', 'subtract', 'multiply', 'divide', 'plus', 'minus', 'times'],
            'algebra': ['equation', 'solve', 'variable', 'expression', 'polynomial', 'factor', 'simplify'],
            'geometry': ['angle', 'triangle', 'circle', 'square', 'rectangle', 'polygon', 'area', 'volume', 'perimeter'],
            'calculus': ['derivative', 'integral', 'limit', 'differentiate', 'integrate', 'rate of change'],
            'statistics': ['probability', 'mean', 'median', 'mode', 'standard deviation', 'variance', 'distribution'],
            'number_theory': ['prime', 'divisor', 'factor', 'remainder', 'modulo', 'congruence'],
            'combinatorics': ['combination', 'permutation', 'factorial', 'choose', 'arrangement'],
        }
    
    def extract_features(self, problem_text):
        """
        Extract features from a mathematical problem text.
        
        Args:
            problem_text (str): The text of the mathematical problem.
            
        Returns:
            dict: A dictionary of extracted features.
        """
        # Normalize text
        normalized_text = problem_text.lower()
        
        # Tokenize text - using simple split instead of NLTK tokenizer to avoid dependency issues
        tokens = normalized_text.split()
        
        # Extract features
        features = {
            'length': self._extract_length_feature(normalized_text),
            'sentence_structure': self._extract_sentence_structure_feature(normalized_text),
            'variables': self._extract_variables_feature(normalized_text),
            'keywords': self._extract_keywords_feature(normalized_text, tokens),
            'domain': self._extract_domain_feature(normalized_text, tokens),
            'operations': self._extract_operations_feature(normalized_text),
        }
        
        return features
    
    def _extract_length_feature(self, text):
        """Extract feature based on the length of the problem."""
        # Normalize length to a 0-1 scale
        # Assuming problems longer than 200 characters are very complex
        length = len(text)
        normalized_length = min(1.0, length / 200.0)
        return normalized_length
    
    def _extract_sentence_structure_feature(self, text):
        """Extract feature based on the sentence structure complexity."""
        # Count the number of clauses (approximated by counting commas and conjunctions)
        clause_markers = [',', ' and ', ' or ', ' but ', ' because ', ' if ', ' then ', ' when ', ' while ']
        clause_count = sum(text.count(marker) for marker in clause_markers) + 1  # +1 for the base clause
        
        # Normalize to a 0-1 scale
        # Assuming more than 5 clauses indicates a very complex structure
        normalized_structure = min(1.0, clause_count / 5.0)
        return normalized_structure
    
    def _extract_variables_feature(self, text):
        """Extract feature based on the number and complexity of variables."""
        # Count unique variables
        variables = set(re.findall(self.variable_pattern, text))
        variable_count = len(variables)
        
        # Normalize to a 0-1 scale
        # Assuming more than 4 variables indicates a very complex problem
        normalized_variables = min(1.0, variable_count / 4.0)
        return normalized_variables
    
    def _extract_keywords_feature(self, text, tokens):
        """Extract feature based on mathematical keywords."""
        # Count mathematical keywords
        math_keywords = ['solve', 'find', 'calculate', 'determine', 'evaluate', 'simplify', 'factor', 'expand']
        keyword_count = sum(token in math_keywords for token in tokens)
        
        # Normalize to a 0-1 scale
        # Assuming more than 3 keywords indicates a very complex problem
        normalized_keywords = min(1.0, keyword_count / 3.0)
        return normalized_keywords
    
    def _extract_domain_feature(self, text, tokens):
        """Extract feature based on the mathematical domain."""
        # Determine the domain based on keywords
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(keyword in text for keyword in keywords)
            if score > 0:
                domain_scores[domain] = score
        
        # If no domain is detected, default to arithmetic (simplest)
        if not domain_scores:
            return self.domain_complexity['arithmetic']
        
        # Get the domain with the highest score
        primary_domain = max(domain_scores, key=domain_scores.get)
        return self.domain_complexity[primary_domain]
    
    def _extract_operations_feature(self, text):
        """Extract feature based on mathematical operations."""
        # Detect operations
        operation_scores = {}
        for operation, pattern in self.operation_patterns.items():
            matches = pattern.findall(text)
            if matches:
                operation_scores[operation] = len(matches) * self.operation_complexity[operation]
        
        # If no operations are detected, default to addition (simplest)
        if not operation_scores:
            return self.operation_complexity['addition']
        
        # Calculate the average complexity of detected operations
        total_complexity = sum(operation_scores.values())
        total_operations = sum(len(pattern.findall(text)) for pattern in self.operation_patterns.values())
        
        # Normalize to ensure it's between 0 and 1
        if total_operations == 0:
            return 0.1  # Default to a low complexity if no operations detected
        
        normalized_operations = min(1.0, total_complexity / total_operations)
        return normalized_operations
