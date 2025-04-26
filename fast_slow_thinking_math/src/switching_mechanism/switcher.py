"""
Implementation of the Switching Mechanism for the Fast-Slow Thinking system.
"""

import config
from src.complexity_analyzer.analyzer import ComplexityAnalyzer
from src.thinking_strategies.fast_thinking import FastThinking
from src.thinking_strategies.slow_thinking import SlowThinking
from src.thinking_strategies.combined import FastThenSlow

class ThinkingSwitcher:
    """
    Switching Mechanism that selects the appropriate thinking strategy based on
    problem complexity and monitors the reasoning process.
    """
    
    def __init__(self, analyzer=None, fast_strategy=None, slow_strategy=None, combined_strategy=None, resource_allocator=None):
        """
        Initialize the Thinking Switcher with components and configuration settings.
        
        Args:
            analyzer (ComplexityAnalyzer, optional): Complexity analyzer instance.
            fast_strategy (FastThinking, optional): Fast thinking strategy instance.
            slow_strategy (SlowThinking, optional): Slow thinking strategy instance.
            combined_strategy (FastThenSlow, optional): Combined thinking strategy instance.
            resource_allocator (ResourceAllocator, optional): Resource allocator instance.
        """
        # Initialize components
        self.analyzer = analyzer if analyzer else ComplexityAnalyzer()
        self.fast_strategy = fast_strategy if fast_strategy else FastThinking()
        self.slow_strategy = slow_strategy if slow_strategy else SlowThinking()
        self.combined_strategy = combined_strategy if combined_strategy else FastThenSlow(self.fast_strategy, self.slow_strategy)
        self.resource_allocator = resource_allocator
        
        # Load configuration
        self.strategy_mapping = config.SWITCHING_MECHANISM['STRATEGY_MAPPING']
        self.confidence_threshold = config.SWITCHING_MECHANISM['CONFIDENCE_THRESHOLD']
        self.error_detection_threshold = config.SWITCHING_MECHANISM['ERROR_DETECTION_THRESHOLD']
    
    def solve(self, problem_text):
        """
        Solve a mathematical problem by selecting the appropriate thinking strategy.
        
        Args:
            problem_text (str): The text of the mathematical problem.
            
        Returns:
            dict: A dictionary containing the solution and metadata.
        """
        # Step 1: Analyze problem complexity
        complexity_analysis = self.analyzer.analyze(problem_text)
        
        # Step 2: Select initial strategy based on complexity
        initial_strategy = self._select_initial_strategy(complexity_analysis)
        
        # Step 3: Allocate resources if resource allocator is available
        if self.resource_allocator:
            resource_allocation = self.resource_allocator.allocate(complexity_analysis)
        else:
            resource_allocation = None
        
        # Step 4: Solve the problem with the selected strategy
        solution = self._solve_with_strategy(problem_text, initial_strategy, complexity_analysis, resource_allocation)
        
        # Step 5: Add metadata to the solution
        solution['complexity_analysis'] = complexity_analysis
        solution['initial_strategy'] = initial_strategy
        
        return solution
    
    def _select_initial_strategy(self, complexity_analysis):
        """
        Select the initial thinking strategy based on complexity analysis.
        
        Args:
            complexity_analysis (dict): Complexity analysis results.
            
        Returns:
            str: Selected strategy ('FAST', 'SLOW', or 'FAST_THEN_SLOW').
        """
        complexity_level = complexity_analysis['complexity_level']
        return self.strategy_mapping.get(complexity_level, 'FAST_THEN_SLOW')
    
    def _solve_with_strategy(self, problem_text, strategy, complexity_analysis, resource_allocation=None):
        """
        Solve the problem using the selected strategy.
        
        Args:
            problem_text (str): The text of the mathematical problem.
            strategy (str): Selected strategy ('FAST', 'SLOW', or 'FAST_THEN_SLOW').
            complexity_analysis (dict): Complexity analysis results.
            resource_allocation (dict, optional): Resource allocation information.
            
        Returns:
            dict: Solution results.
        """
        # Apply resource allocation if available
        if resource_allocation:
            # In a real implementation, we would configure the strategies with the allocated resources
            pass
        
        # Solve with the selected strategy
        if strategy == 'FAST':
            solution = self.fast_strategy.solve(problem_text)
            
            # Check if we need to switch to a more complex strategy
            if self._should_switch_to_more_complex(solution):
                return self._handle_strategy_switch(problem_text, 'FAST', 'FAST_THEN_SLOW', solution)
            
            return solution
            
        elif strategy == 'SLOW':
            return self.slow_strategy.solve(problem_text)
            
        elif strategy == 'FAST_THEN_SLOW':
            return self.combined_strategy.solve(problem_text)
            
        else:
            # Default to Fast-then-Slow if strategy is not recognized
            return self.combined_strategy.solve(problem_text)
    
    def _should_switch_to_more_complex(self, solution):
        """
        Determine if we should switch to a more complex strategy based on solution results.
        
        Args:
            solution (dict): Solution results from the current strategy.
            
        Returns:
            bool: True if we should switch, False otherwise.
        """
        # Check confidence
        if solution['confidence'] < self.confidence_threshold:
            return True
        
        # Check for errors
        if solution.get('error', None) is not None:
            return True
        
        # Check resource usage
        if solution['resources']['steps_used'] >= solution['resources']['max_steps']:
            return True
        
        return False
    
    def _handle_strategy_switch(self, problem_text, from_strategy, to_strategy, current_solution):
        """
        Handle switching from one strategy to another.
        
        Args:
            problem_text (str): The text of the mathematical problem.
            from_strategy (str): Current strategy.
            to_strategy (str): Target strategy.
            current_solution (dict): Solution results from the current strategy.
            
        Returns:
            dict: Solution results from the new strategy.
        """
        # Log the switch
        switch_reason = self._determine_switch_reason(current_solution)
        
        # Solve with the new strategy
        if to_strategy == 'FAST_THEN_SLOW':
            new_solution = self.combined_strategy.solve(problem_text)
        elif to_strategy == 'SLOW':
            new_solution = self.slow_strategy.solve(problem_text)
        else:
            new_solution = self.fast_strategy.solve(problem_text)
        
        # Add switch information to the solution
        new_solution['strategy_switch'] = {
            'from_strategy': from_strategy,
            'to_strategy': to_strategy,
            'reason': switch_reason,
            'original_solution': current_solution
        }
        
        return new_solution
    
    def _determine_switch_reason(self, solution):
        """
        Determine the reason for switching strategies.
        
        Args:
            solution (dict): Solution results from the current strategy.
            
        Returns:
            str: Reason for switching.
        """
        if solution.get('error', None) is not None:
            return f"Error in current strategy: {solution['error']}"
        
        if solution['confidence'] < self.confidence_threshold:
            return f"Low confidence: {solution['confidence']:.2f} < {self.confidence_threshold}"
        
        if solution['resources']['steps_used'] >= solution['resources']['max_steps']:
            return f"Resource limit reached: {solution['resources']['steps_used']} steps used"
        
        return "Unknown reason"
