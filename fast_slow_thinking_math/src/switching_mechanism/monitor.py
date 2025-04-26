"""
Implementation of the reasoning process monitor for the Switching Mechanism.
"""

import config

class ReasoningMonitor:
    """
    Monitors the reasoning process during problem-solving and provides
    feedback for potential strategy adjustments.
    """
    
    def __init__(self):
        """Initialize the Reasoning Monitor with configuration settings."""
        self.confidence_threshold = config.SWITCHING_MECHANISM['CONFIDENCE_THRESHOLD']
        self.error_detection_threshold = config.SWITCHING_MECHANISM['ERROR_DETECTION_THRESHOLD']
    
    def monitor_step(self, step_info):
        """
        Monitor a single reasoning step and provide feedback.
        
        Args:
            step_info (dict): Information about the current reasoning step.
            
        Returns:
            dict: Monitoring feedback.
        """
        # Extract information from the step
        step_content = step_info.get('content', '')
        step_confidence = step_info.get('confidence', 1.0)
        step_strategy = step_info.get('strategy', 'unknown')
        
        # Check for potential issues
        issues = self._detect_issues(step_content, step_confidence)
        
        # Determine if strategy adjustment is needed
        adjustment_needed = self._needs_adjustment(issues, step_confidence, step_strategy)
        
        # Prepare monitoring feedback
        feedback = {
            'issues': issues,
            'adjustment_needed': adjustment_needed,
            'confidence_assessment': self._assess_confidence(step_confidence),
            'recommendations': self._generate_recommendations(issues, step_confidence, step_strategy)
        }
        
        return feedback
    
    def monitor_solution(self, solution):
        """
        Monitor the complete solution and provide overall feedback.
        
        Args:
            solution (dict): The complete solution information.
            
        Returns:
            dict: Overall monitoring feedback.
        """
        # Extract information from the solution
        steps = solution.get('steps', [])
        confidence = solution.get('confidence', 1.0)
        strategy = solution.get('strategy', 'unknown')
        error = solution.get('error', None)
        
        # Collect issues from all steps
        all_issues = []
        for step in steps:
            if isinstance(step, dict) and 'content' in step:
                step_issues = self._detect_issues(step['content'], step.get('confidence', 1.0))
                all_issues.extend(step_issues)
            else:
                step_issues = self._detect_issues(str(step), 1.0)
                all_issues.extend(step_issues)
        
        # Add error as an issue if present
        if error:
            all_issues.append(f"Error in solution: {error}")
        
        # Determine if strategy adjustment is needed for future similar problems
        future_adjustment = self._recommend_future_adjustment(all_issues, confidence, strategy)
        
        # Prepare overall feedback
        feedback = {
            'issues': all_issues,
            'overall_confidence': confidence,
            'future_adjustment': future_adjustment,
            'quality_assessment': self._assess_solution_quality(confidence, all_issues),
            'recommendations': self._generate_overall_recommendations(all_issues, confidence, strategy)
        }
        
        return feedback
    
    def _detect_issues(self, content, confidence):
        """
        Detect potential issues in a reasoning step.
        
        Args:
            content (str): Content of the reasoning step.
            confidence (float): Confidence level for the step.
            
        Returns:
            list: Detected issues.
        """
        issues = []
        
        # Check for uncertainty indicators
        uncertainty_indicators = ['maybe', 'perhaps', 'possibly', 'not sure', 'uncertain', 'might be']
        for indicator in uncertainty_indicators:
            if indicator in content.lower():
                issues.append(f"Uncertainty detected: '{indicator}'")
        
        # Check for error indicators
        error_indicators = ['error', 'mistake', 'incorrect', 'wrong', 'invalid', 'failed']
        for indicator in error_indicators:
            if indicator in content.lower():
                issues.append(f"Potential error detected: '{indicator}'")
        
        # Check for low confidence
        if confidence < self.error_detection_threshold:
            issues.append(f"Very low confidence: {confidence:.2f}")
        
        return issues
    
    def _needs_adjustment(self, issues, confidence, strategy):
        """
        Determine if strategy adjustment is needed based on detected issues.
        
        Args:
            issues (list): Detected issues.
            confidence (float): Confidence level.
            strategy (str): Current strategy.
            
        Returns:
            bool: True if adjustment is needed, False otherwise.
        """
        # If there are any issues, consider adjustment
        if issues:
            return True
        
        # If confidence is below threshold, consider adjustment
        if confidence < self.confidence_threshold:
            return True
        
        # If using Fast strategy with borderline confidence, consider adjustment
        if strategy == 'FAST' and confidence < self.confidence_threshold + 0.1:
            return True
        
        return False
    
    def _assess_confidence(self, confidence):
        """
        Assess the confidence level.
        
        Args:
            confidence (float): Confidence level.
            
        Returns:
            str: Confidence assessment.
        """
        if confidence < self.error_detection_threshold:
            return "Very Low"
        elif confidence < self.confidence_threshold:
            return "Low"
        elif confidence < 0.8:
            return "Moderate"
        elif confidence < 0.95:
            return "High"
        else:
            return "Very High"
    
    def _generate_recommendations(self, issues, confidence, strategy):
        """
        Generate recommendations based on detected issues.
        
        Args:
            issues (list): Detected issues.
            confidence (float): Confidence level.
            strategy (str): Current strategy.
            
        Returns:
            list: Recommendations.
        """
        recommendations = []
        
        if issues:
            if strategy == 'FAST':
                recommendations.append("Consider switching to a more thorough strategy")
            elif strategy == 'FAST_THEN_SLOW':
                recommendations.append("Proceed to Slow Thinking phase")
            else:
                recommendations.append("Increase verification effort")
        
        if confidence < self.confidence_threshold:
            recommendations.append("Verify intermediate results")
            recommendations.append("Consider alternative approaches")
        
        if not recommendations:
            recommendations.append("Continue with current strategy")
        
        return recommendations
    
    def _recommend_future_adjustment(self, issues, confidence, strategy):
        """
        Recommend strategy adjustment for future similar problems.
        
        Args:
            issues (list): Detected issues.
            confidence (float): Overall confidence.
            strategy (str): Strategy used.
            
        Returns:
            dict: Recommendation for future adjustment.
        """
        if not issues and confidence > 0.9:
            if strategy == 'SLOW':
                return {
                    'adjust': True,
                    'recommendation': 'FAST',
                    'reason': 'High confidence solution achieved with Slow Thinking, suggesting simpler strategy may be sufficient'
                }
            elif strategy == 'FAST_THEN_SLOW':
                return {
                    'adjust': True,
                    'recommendation': 'FAST',
                    'reason': 'High confidence solution achieved with Fast-then-Slow, but may be solvable with just Fast Thinking'
                }
            else:
                return {
                    'adjust': False,
                    'recommendation': strategy,
                    'reason': 'Current strategy is appropriate'
                }
        
        if len(issues) > 3 or confidence < self.error_detection_threshold:
            if strategy == 'FAST':
                return {
                    'adjust': True,
                    'recommendation': 'SLOW',
                    'reason': 'Multiple issues or very low confidence with Fast Thinking'
                }
            elif strategy == 'FAST_THEN_SLOW':
                return {
                    'adjust': True,
                    'recommendation': 'SLOW',
                    'reason': 'Multiple issues or very low confidence with Fast-then-Slow'
                }
            else:
                return {
                    'adjust': False,
                    'recommendation': strategy,
                    'reason': 'Already using most thorough strategy'
                }
        
        return {
            'adjust': False,
            'recommendation': strategy,
            'reason': 'Current strategy appears appropriate'
        }
    
    def _assess_solution_quality(self, confidence, issues):
        """
        Assess the overall quality of the solution.
        
        Args:
            confidence (float): Overall confidence.
            issues (list): Detected issues.
            
        Returns:
            str: Quality assessment.
        """
        if confidence > 0.9 and not issues:
            return "Excellent"
        elif confidence > 0.8 and len(issues) <= 1:
            return "Good"
        elif confidence > 0.6 and len(issues) <= 2:
            return "Satisfactory"
        elif confidence > 0.4:
            return "Questionable"
        else:
            return "Poor"
    
    def _generate_overall_recommendations(self, issues, confidence, strategy):
        """
        Generate overall recommendations based on solution quality.
        
        Args:
            issues (list): Detected issues.
            confidence (float): Overall confidence.
            strategy (str): Strategy used.
            
        Returns:
            list: Overall recommendations.
        """
        recommendations = []
        
        if len(issues) > 2:
            recommendations.append("Review solution for errors")
        
        if confidence < self.confidence_threshold:
            recommendations.append("Consider alternative solution approaches")
            
            if strategy == 'FAST':
                recommendations.append("Try solving with Slow Thinking strategy")
            elif strategy == 'FAST_THEN_SLOW':
                recommendations.append("Try solving directly with Slow Thinking strategy")
        
        if not recommendations:
            recommendations.append("Solution appears reliable")
        
        return recommendations
