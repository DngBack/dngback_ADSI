"""
Implementation of the Resource Allocator for the Fast-Slow Thinking system.
"""

import config

class ResourceAllocator:
    """
    Allocates computational resources based on problem complexity and selected strategy.
    """
    
    def __init__(self):
        """Initialize the Resource Allocator with configuration settings."""
        self.base_token_budget = config.RESOURCE_ALLOCATOR['BASE_TOKEN_BUDGET']
        self.step_token_cost = config.RESOURCE_ALLOCATOR['STEP_TOKEN_COST']
        self.verification_token_cost = config.RESOURCE_ALLOCATOR['VERIFICATION_TOKEN_COST']
    
    def allocate(self, complexity_analysis):
        """
        Allocate resources based on problem complexity.
        
        Args:
            complexity_analysis (dict): Complexity analysis results.
            
        Returns:
            dict: Resource allocation information.
        """
        complexity_score = complexity_analysis['complexity_score']
        complexity_level = complexity_analysis['complexity_level']
        
        # Calculate token budget based on complexity
        token_budget = self._calculate_token_budget(complexity_score)
        
        # Calculate maximum reasoning steps based on complexity
        max_steps = self._calculate_max_steps(complexity_score)
        
        # Calculate verification effort based on complexity
        verification_effort = self._calculate_verification_effort(complexity_score)
        
        # Prepare resource allocation
        allocation = {
            'token_budget': token_budget,
            'max_steps': max_steps,
            'verification_effort': verification_effort,
            'complexity_level': complexity_level,
            'complexity_score': complexity_score
        }
        
        return allocation
    
    def _calculate_token_budget(self, complexity_score):
        """
        Calculate token budget based on complexity score.
        
        Args:
            complexity_score (float): Complexity score between 0.0 and 1.0.
            
        Returns:
            int: Token budget.
        """
        # Scale token budget based on complexity
        # Simple problems get base budget, complex problems get up to 5x base budget
        scaling_factor = 1 + 4 * complexity_score
        token_budget = int(self.base_token_budget * scaling_factor)
        
        return token_budget
    
    def _calculate_max_steps(self, complexity_score):
        """
        Calculate maximum reasoning steps based on complexity score.
        
        Args:
            complexity_score (float): Complexity score between 0.0 and 1.0.
            
        Returns:
            int: Maximum reasoning steps.
        """
        # Simple problems need fewer steps, complex problems need more
        # Range from 3 steps (simplest) to 15 steps (most complex)
        min_steps = 3
        max_steps = 15
        steps_range = max_steps - min_steps
        
        max_steps = min_steps + int(steps_range * complexity_score)
        
        return max_steps
    
    def _calculate_verification_effort(self, complexity_score):
        """
        Calculate verification effort based on complexity score.
        
        Args:
            complexity_score (float): Complexity score between 0.0 and 1.0.
            
        Returns:
            float: Verification effort between 0.0 and 1.0.
        """
        # Simple problems need less verification, complex problems need more
        # Range from 0.2 (simplest) to 0.8 (most complex)
        min_effort = 0.2
        max_effort = 0.8
        effort_range = max_effort - min_effort
        
        verification_effort = min_effort + (effort_range * complexity_score)
        
        # Round to 2 decimal places
        verification_effort = round(verification_effort, 2)
        
        return verification_effort
    
    def allocate_for_strategy(self, complexity_analysis, strategy):
        """
        Allocate resources based on problem complexity and selected strategy.
        
        Args:
            complexity_analysis (dict): Complexity analysis results.
            strategy (str): Selected strategy ('FAST', 'SLOW', or 'FAST_THEN_SLOW').
            
        Returns:
            dict: Strategy-specific resource allocation.
        """
        # Get base allocation
        base_allocation = self.allocate(complexity_analysis)
        
        # Adjust based on strategy
        if strategy == 'FAST':
            # Fast thinking uses fewer resources
            return {
                'token_budget': int(base_allocation['token_budget'] * 0.5),
                'max_steps': min(3, base_allocation['max_steps']),
                'verification_effort': min(0.3, base_allocation['verification_effort']),
                'complexity_level': base_allocation['complexity_level'],
                'complexity_score': base_allocation['complexity_score']
            }
        
        elif strategy == 'SLOW':
            # Slow thinking uses more resources
            return {
                'token_budget': int(base_allocation['token_budget'] * 1.5),
                'max_steps': max(10, base_allocation['max_steps']),
                'verification_effort': max(0.7, base_allocation['verification_effort']),
                'complexity_level': base_allocation['complexity_level'],
                'complexity_score': base_allocation['complexity_score']
            }
        
        elif strategy == 'FAST_THEN_SLOW':
            # Combined strategy gets combined resources
            return {
                'token_budget': int(base_allocation['token_budget'] * 1.2),
                'max_steps': base_allocation['max_steps'] + 2,
                'verification_effort': base_allocation['verification_effort'] + 0.1,
                'complexity_level': base_allocation['complexity_level'],
                'complexity_score': base_allocation['complexity_score']
            }
        
        else:
            # Default to base allocation
            return base_allocation
