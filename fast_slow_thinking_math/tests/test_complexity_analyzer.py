"""
Test module for the Complexity Analyzer.
"""

import unittest
from src.complexity_analyzer.analyzer import ComplexityAnalyzer

class TestComplexityAnalyzer(unittest.TestCase):
    """Test cases for the Complexity Analyzer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ComplexityAnalyzer()
        
    def test_simple_problem(self):
        """Test analysis of a simple problem."""
        problem = "What is 25 × 4?"
        analysis = self.analyzer.analyze(problem)
        
        self.assertLessEqual(analysis['complexity_score'], 0.3)
        self.assertEqual(analysis['complexity_level'], 'Simple')
        self.assertEqual(self.analyzer.get_recommended_strategy(analysis['complexity_level']), 'FAST')
        
    def test_medium_problem(self):
        """Test analysis of a medium complexity problem."""
        problem = "Solve the equation 2x² + 5x - 3 = 0 for x."
        analysis = self.analyzer.analyze(problem)
        
        self.assertTrue(0.3 < analysis['complexity_score'] <= 0.6)
        self.assertEqual(analysis['complexity_level'], 'Medium')
        self.assertEqual(self.analyzer.get_recommended_strategy(analysis['complexity_level']), 'FAST_THEN_SLOW')
        
    def test_complex_problem(self):
        """Test analysis of a complex problem."""
        problem = """
        Find the volume of the solid obtained by rotating the region bounded by 
        y = x², y = 0, and x = 2 about the y-axis using the method of cylindrical shells.
        """
        analysis = self.analyzer.analyze(problem)
        
        self.assertGreater(analysis['complexity_score'], 0.6)
        self.assertEqual(analysis['complexity_level'], 'Complex')
        self.assertEqual(self.analyzer.get_recommended_strategy(analysis['complexity_level']), 'SLOW')
        
    def test_feature_extraction(self):
        """Test feature extraction from a problem."""
        problem = "Solve for x: 3x + 2 = 14"
        analysis = self.analyzer.analyze(problem)
        
        self.assertIn('features', analysis)
        self.assertIn('length', analysis['features'])
        self.assertIn('variables', analysis['features'])
        self.assertIn('operations', analysis['features'])
        
    def test_feature_contributions(self):
        """Test calculation of feature contributions."""
        problem = "Find the derivative of f(x) = x³ + 2x² - 5x + 3"
        analysis = self.analyzer.analyze(problem)
        
        self.assertIn('feature_contributions', analysis)
        for feature in analysis['features']:
            self.assertIn(feature, analysis['feature_contributions'])

if __name__ == '__main__':
    unittest.main()
