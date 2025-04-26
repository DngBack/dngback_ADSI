"""
Main implementation of the Complexity Analyzer for mathematical problems.
"""

import re
import numpy as np
from .features import FeatureExtractor
import config

class ComplexityAnalyzer:
    """
    Analyzes the complexity of mathematical problems and classifies them
    into different complexity levels.
    """
    
    def __init__(self):
        """Initialize the complexity analyzer with configuration settings."""
        self.feature_extractor = FeatureExtractor()
        self.feature_weights = config.COMPLEXITY_ANALYZER['FEATURE_WEIGHTS']
        self.simple_threshold = config.COMPLEXITY_ANALYZER['SIMPLE_THRESHOLD']
        self.medium_threshold = config.COMPLEXITY_ANALYZER['MEDIUM_THRESHOLD']
    
    def analyze(self, problem_text):
        """
        Analyze the complexity of a mathematical problem.
        
        Args:
            problem_text (str): The text of the mathematical problem.
            
        Returns:
            dict: A dictionary containing the complexity analysis results.
        """
        # Extract features
        features = self.feature_extractor.extract_features(problem_text)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(features)
        
        # Classify complexity level
        complexity_level = self._classify_complexity(complexity_score)
        
        # Prepare detailed analysis
        analysis = {
            'problem': problem_text,
            'complexity_score': complexity_score,
            'complexity_level': complexity_level,
            'features': features,
            'feature_contributions': self._calculate_feature_contributions(features),
        }
        
        return analysis
    
    def _calculate_complexity_score(self, features):
        """
        Calculate the overall complexity score based on extracted features.
        
        Args:
            features (dict): Dictionary of extracted features.
            
        Returns:
            float: Complexity score between 0.0 and 1.0.
        """
        # Calculate weighted sum of features
        weighted_sum = sum(
            features[feature] * weight
            for feature, weight in self.feature_weights.items()
        )
        
        # Normalize to ensure it's between 0 and 1
        normalized_score = min(1.0, max(0.0, weighted_sum))
        
        # Round to 2 decimal places for readability
        return round(normalized_score, 2)
    
    def _classify_complexity(self, complexity_score):
        """
        Classify the complexity level based on the complexity score.
        
        Args:
            complexity_score (float): Complexity score between 0.0 and 1.0.
            
        Returns:
            str: Complexity level ('Simple', 'Medium', or 'Complex').
        """
        if complexity_score <= self.simple_threshold:
            return 'Simple'
        elif complexity_score <= self.medium_threshold:
            return 'Medium'
        else:
            return 'Complex'
    
    def _calculate_feature_contributions(self, features):
        """
        Calculate the contribution of each feature to the overall complexity score.
        
        Args:
            features (dict): Dictionary of extracted features.
            
        Returns:
            dict: Dictionary of feature contributions.
        """
        feature_contributions = {}
        for feature, value in features.items():
            contribution = value * self.feature_weights[feature]
            feature_contributions[feature] = round(contribution, 2)
        
        return feature_contributions
    
    def get_recommended_strategy(self, complexity_level):
        """
        Get the recommended thinking strategy based on the complexity level.
        
        Args:
            complexity_level (str): Complexity level ('Simple', 'Medium', or 'Complex').
            
        Returns:
            str: Recommended thinking strategy ('FAST', 'FAST_THEN_SLOW', or 'SLOW').
        """
        strategy_mapping = config.SWITCHING_MECHANISM['STRATEGY_MAPPING']
        return strategy_mapping.get(complexity_level, 'FAST_THEN_SLOW')  # Default to FAST_THEN_SLOW if not found
