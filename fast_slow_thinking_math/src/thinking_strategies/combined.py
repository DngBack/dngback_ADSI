"""
Implementation of Fast-then-Slow Thinking strategy for mathematical problems.
"""

import config
from .fast_thinking import FastThinking
from .slow_thinking import SlowThinking

class FastThenSlow:
    """
    Fast-then-Slow Thinking strategy that starts with Fast Thinking and switches to
    Slow Thinking if needed based on confidence and complexity.
    """
    
    def __init__(self, fast_thinking=None, slow_thinking=None):
        """
        Initialize the Fast-then-Slow Thinking strategy with configuration settings.
        
        Args:
            fast_thinking (FastThinking, optional): Fast Thinking strategy instance.
            slow_thinking (SlowThinking, optional): Slow Thinking strategy instance.
        """
        self.confidence_threshold = config.THINKING_STRATEGIES['FAST_THEN_SLOW']['confidence_threshold']
        self.max_fast_steps = config.THINKING_STRATEGIES['FAST_THEN_SLOW']['max_fast_steps']
        
        # Initialize thinking strategies
        self.fast_thinking = fast_thinking if fast_thinking else FastThinking()
        self.slow_thinking = slow_thinking if slow_thinking else SlowThinking()
    
    def solve(self, problem_text):
        """
        Solve a mathematical problem using Fast-then-Slow Thinking strategy.
        
        Args:
            problem_text (str): The text of the mathematical problem.
            
        Returns:
            dict: A dictionary containing the solution and metadata.
        """
        # Initialize solution tracking
        steps = []
        tokens_used = 0
        
        # Step 1: Try Fast Thinking first
        steps.append("Starting with Fast Thinking approach")
        fast_result = self.fast_thinking.solve(problem_text)
        
        # Add Fast Thinking steps to our steps
        for i, fast_step in enumerate(fast_result['steps']):
            steps.append(f"Fast Thinking {i+1}: {fast_step}")
        
        tokens_used += fast_result['tokens_used']
        
        # Step 2: Evaluate if we need to switch to Slow Thinking
        switch_decision = self._evaluate_switch_decision(fast_result)
        steps.append(f"Switch decision: {switch_decision['decision']} - {switch_decision['reason']}")
        tokens_used += len(steps[-1].split())
        
        # Step 3: If needed, switch to Slow Thinking
        if switch_decision['decision'] == 'switch':
            steps.append("Switching to Slow Thinking approach")
            
            # Pass relevant information from Fast Thinking to Slow Thinking
            context_for_slow = self._prepare_context_for_slow(problem_text, fast_result)
            
            # Solve with Slow Thinking
            slow_result = self.slow_thinking.solve(context_for_slow)
            
            # Add Slow Thinking steps to our steps
            for i, slow_step in enumerate(slow_result['steps']):
                steps.append(f"Slow Thinking {i+1}: {slow_step}")
            
            tokens_used += slow_result['tokens_used']
            
            # Prepare final result based on Slow Thinking
            result = {
                'answer': slow_result['answer'],
                'confidence': slow_result['confidence'],
                'error': slow_result.get('error', None),
                'fast_result': fast_result,
                'slow_result': slow_result,
                'switch_decision': switch_decision
            }
        else:
            # Use Fast Thinking result
            steps.append("Continuing with Fast Thinking approach")
            
            # Prepare final result based on Fast Thinking
            result = {
                'answer': fast_result['answer'],
                'confidence': fast_result['confidence'],
                'error': fast_result.get('error', None),
                'fast_result': fast_result,
                'switch_decision': switch_decision
            }
        
        # Prepare and return the final solution
        return self._prepare_solution(result, steps, tokens_used)
    
    def _evaluate_switch_decision(self, fast_result):
        """
        Evaluate whether to switch from Fast to Slow Thinking.
        
        Args:
            fast_result (dict): Result from Fast Thinking.
            
        Returns:
            dict: Decision information.
        """
        # Check confidence
        if fast_result['confidence'] < self.confidence_threshold:
            return {
                'decision': 'switch',
                'reason': f"Low confidence ({fast_result['confidence']:.2f} < {self.confidence_threshold})"
            }
        
        # Check for errors
        if fast_result.get('error', None) is not None:
            return {
                'decision': 'switch',
                'reason': f"Error in Fast Thinking: {fast_result['error']}"
            }
        
        # Check number of steps used
        if len(fast_result['steps']) >= self.max_fast_steps:
            return {
                'decision': 'switch',
                'reason': f"Reached maximum Fast Thinking steps ({len(fast_result['steps'])} >= {self.max_fast_steps})"
            }
        
        # Check token usage
        if fast_result['tokens_used'] >= fast_result['resources']['token_budget'] * 0.9:
            return {
                'decision': 'switch',
                'reason': f"High token usage ({fast_result['tokens_used']} tokens)"
            }
        
        # No need to switch
        return {
            'decision': 'continue',
            'reason': f"Fast Thinking successful with high confidence ({fast_result['confidence']:.2f})"
        }
    
    def _prepare_context_for_slow(self, problem_text, fast_result):
        """
        Prepare context information from Fast Thinking to pass to Slow Thinking.
        
        Args:
            problem_text (str): Original problem text.
            fast_result (dict): Result from Fast Thinking.
            
        Returns:
            str: Enhanced problem text with context for Slow Thinking.
        """
        # For simple implementation, we just pass the original problem
        # In a more sophisticated system, we could include insights from Fast Thinking
        
        # If Fast Thinking found an answer but with low confidence, include it as a hint
        if fast_result['answer'] is not None and fast_result['confidence'] > 0.3:
            context = (
                f"{problem_text}\n\n"
                f"Initial analysis suggests the answer might be {fast_result['answer']} "
                f"but this needs verification."
            )
            return context
        
        return problem_text
    
    def _prepare_solution(self, result, steps, tokens_used):
        """Prepare the final solution output."""
        # Calculate total resources used
        if 'slow_result' in result:
            # Combined resources from both strategies
            resources = {
                'steps_used': len(steps),
                'max_steps': self.slow_thinking.max_steps + self.fast_thinking.max_steps,
                'tokens_used': tokens_used,
                'token_budget': self.fast_thinking.token_budget + self.slow_thinking.token_budget,
                'verification_effort': max(
                    self.fast_thinking.verification_effort,
                    self.slow_thinking.verification_effort
                )
            }
        else:
            # Only Fast Thinking resources
            resources = {
                'steps_used': len(steps),
                'max_steps': self.fast_thinking.max_steps,
                'tokens_used': tokens_used,
                'token_budget': self.fast_thinking.token_budget,
                'verification_effort': self.fast_thinking.verification_effort
            }
        
        return {
            'answer': result['answer'],
            'confidence': result['confidence'],
            'steps': steps,
            'tokens_used': tokens_used,
            'strategy': 'FAST_THEN_SLOW',
            'error': result.get('error', None),
            'resources': resources,
            'switch_decision': result['switch_decision']
        }
