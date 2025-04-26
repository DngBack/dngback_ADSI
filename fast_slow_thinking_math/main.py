"""
Main application file for the Fast-Slow Thinking Math system.
"""

import json
import time
import logging
import os
from src.complexity_analyzer.analyzer import ComplexityAnalyzer
from src.thinking_strategies.fast_thinking import FastThinking
from src.thinking_strategies.slow_thinking import SlowThinking
from src.thinking_strategies.combined import FastThenSlow
from src.switching_mechanism.switcher import ThinkingSwitcher
from src.switching_mechanism.monitor import ReasoningMonitor
from src.resource_allocator.allocator import ResourceAllocator
import config

# Configure logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format=config.LOGGING['FORMAT'],
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(config.LOGGING['FILE'], mode='w')
    ]
)
logger = logging.getLogger(__name__)

class FastSlowThinkingMath:
    """
    Main application class for the Fast-Slow Thinking Math system.
    """
    
    def __init__(self):
        """Initialize the Fast-Slow Thinking Math system."""
        logger.info("Initializing Fast-Slow Thinking Math system")
        
        # Initialize components
        self.analyzer = ComplexityAnalyzer()
        self.fast_strategy = FastThinking()
        self.slow_strategy = SlowThinking()
        self.combined_strategy = FastThenSlow(self.fast_strategy, self.slow_strategy)
        self.resource_allocator = ResourceAllocator()
        self.switcher = ThinkingSwitcher(
            analyzer=self.analyzer,
            fast_strategy=self.fast_strategy,
            slow_strategy=self.slow_strategy,
            combined_strategy=self.combined_strategy,
            resource_allocator=self.resource_allocator
        )
        self.monitor = ReasoningMonitor()
        
        logger.info("System initialization complete")
    
    def load_problems(self, file_path):
        """
        Load mathematical problems from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file.
            
        Returns:
            list: List of problem dictionaries.
        """
        logger.info(f"Loading problems from {file_path}")
        try:
            with open(file_path, 'r') as f:
                problems = json.load(f)
            logger.info(f"Loaded {len(problems)} problems")
            return problems
        except Exception as e:
            logger.error(f"Error loading problems: {str(e)}")
            return []
    
    def solve_problem(self, problem_text):
        """
        Solve a mathematical problem using the Fast-Slow Thinking system.
        
        Args:
            problem_text (str): The text of the mathematical problem.
            
        Returns:
            dict: Solution results.
        """
        logger.info(f"Solving problem: {problem_text}")
        
        # Measure solution time
        start_time = time.time()
        
        # Solve the problem using the switching mechanism
        solution = self.switcher.solve(problem_text)
        
        # Calculate solution time
        solution_time = time.time() - start_time
        solution['solution_time'] = solution_time
        
        # Monitor the solution
        monitoring_feedback = self.monitor.monitor_solution(solution)
        solution['monitoring_feedback'] = monitoring_feedback
        
        logger.info(f"Problem solved in {solution_time:.2f} seconds with strategy {solution['strategy']}")
        logger.info(f"Solution confidence: {solution['confidence']:.2f}")
        
        return solution
    
    def evaluate_problems(self, problems):
        """
        Evaluate a list of mathematical problems.
        
        Args:
            problems (list): List of problem dictionaries.
            
        Returns:
            dict: Evaluation results.
        """
        logger.info(f"Evaluating {len(problems)} problems")
        
        results = []
        metrics = {
            'total_problems': len(problems),
            'total_time': 0,
            'avg_time': 0,
            'strategy_counts': {'FAST': 0, 'SLOW': 0, 'FAST_THEN_SLOW': 0},
            'complexity_counts': {'Simple': 0, 'Medium': 0, 'Complex': 0},
            'avg_confidence': 0,
            'correct_answers': 0
        }
        
        for problem in problems:
            problem_id = problem.get('id', 'unknown')
            problem_text = problem.get('problem', '')
            expected_answer = problem.get('answer', '')
            complexity_level = problem.get('complexity_level', 'unknown')
            
            logger.info(f"Evaluating problem {problem_id}: {problem_text}")
            
            # Solve the problem
            solution = self.solve_problem(problem_text)
            
            # Update metrics
            metrics['total_time'] += solution['solution_time']
            metrics['strategy_counts'][solution['strategy']] += 1
            
            if complexity_level in metrics['complexity_counts']:
                metrics['complexity_counts'][complexity_level] += 1
            
            metrics['avg_confidence'] += solution['confidence']
            
            # Check if answer is correct (simplified check)
            is_correct = self._check_answer(solution['answer'], expected_answer)
            if is_correct:
                metrics['correct_answers'] += 1
            
            # Store result
            result = {
                'problem_id': problem_id,
                'problem_text': problem_text,
                'complexity_level': complexity_level,
                'expected_answer': expected_answer,
                'actual_answer': solution['answer'],
                'is_correct': is_correct,
                'strategy_used': solution['strategy'],
                'confidence': solution['confidence'],
                'solution_time': solution['solution_time']
            }
            results.append(result)
            
            logger.info(f"Problem {problem_id} evaluation complete. Correct: {is_correct}")
        
        # Calculate averages
        if len(problems) > 0:
            metrics['avg_time'] = metrics['total_time'] / len(problems)
            metrics['avg_confidence'] = metrics['avg_confidence'] / len(problems)
        
        # Calculate accuracy
        metrics['accuracy'] = metrics['correct_answers'] / len(problems) if len(problems) > 0 else 0
        
        logger.info(f"Evaluation complete. Accuracy: {metrics['accuracy']:.2f}, Avg time: {metrics['avg_time']:.2f}s")
        
        return {
            'results': results,
            'metrics': metrics
        }
    
    def _check_answer(self, actual_answer, expected_answer):
        """
        Check if the actual answer matches the expected answer.
        This is a simplified check that could be improved for a real system.
        
        Args:
            actual_answer (str): Actual answer from the system.
            expected_answer (str): Expected correct answer.
            
        Returns:
            bool: True if answers match, False otherwise.
        """
        if actual_answer is None:
            return False
        
        # Convert to strings and normalize
        actual_str = str(actual_answer).lower().replace(' ', '').replace('*', '')
        expected_str = str(expected_answer).lower().replace(' ', '').replace('*', '')
        
        # Direct match
        if actual_str == expected_str:
            return True
        
        # Check for multiple solutions in different order
        if ',' in actual_str and ',' in expected_str:
            actual_parts = sorted([p.strip() for p in actual_str.split(',')])
            expected_parts = sorted([p.strip() for p in expected_str.split(',')])
            return actual_parts == expected_parts
        
        # Check for equations with variable names
        if '=' in actual_str and '=' in expected_str:
            # Extract the value part after the equals sign
            actual_value = actual_str.split('=')[1].strip()
            expected_value = expected_str.split('=')[1].strip()
            return actual_value == expected_value
        
        # Check for numerical equivalence
        try:
            # Try to convert to float for numerical comparison
            actual_float = float(actual_str)
            expected_float = float(expected_str)
            return abs(actual_float - expected_float) < 1e-6
        except (ValueError, TypeError):
            pass
        
        # More sophisticated checks could be added here
        
        return False

def main():
    """Main function to run the Fast-Slow Thinking Math system."""
    # Initialize the system
    system = FastSlowThinkingMath()
    
    # Load problems
    problems = system.load_problems(config.DATA['MATH_PROBLEMS_FILE'])
    
    # Evaluate problems
    evaluation = system.evaluate_problems(problems)
    
    # Save evaluation results
    with open('evaluation_results.json', 'w') as f:
        json.dump(evaluation, f, indent=2)
    
    # Print summary
    print("\nEvaluation Summary:")
    print(f"Total problems: {evaluation['metrics']['total_problems']}")
    print(f"Accuracy: {evaluation['metrics']['accuracy']:.2f}")
    print(f"Average solution time: {evaluation['metrics']['avg_time']:.2f} seconds")
    print(f"Average confidence: {evaluation['metrics']['avg_confidence']:.2f}")
    print("\nStrategy usage:")
    for strategy, count in evaluation['metrics']['strategy_counts'].items():
        print(f"  {strategy}: {count} problems")
    
    print("\nComplexity distribution:")
    for level, count in evaluation['metrics']['complexity_counts'].items():
        print(f"  {level}: {count} problems")
    
    # Print detailed results for each problem
    print("\nDetailed Results:")
    for result in evaluation['results']:
        print(f"\nProblem: {result['problem_text']}")
        print(f"Expected: {result['expected_answer']}")
        print(f"Actual: {result['actual_answer']}")
        print(f"Correct: {result['is_correct']}")
        print(f"Strategy: {result['strategy_used']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Time: {result['solution_time']:.2f}s")

if __name__ == "__main__":
    main()
