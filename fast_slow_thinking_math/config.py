"""
Configuration settings for the Fast-Slow Thinking Math system.
"""

# Complexity Analyzer settings
COMPLEXITY_ANALYZER = {
    # Thresholds for complexity classification
    'SIMPLE_THRESHOLD': 0.3,      # Problems with score <= 0.3 are classified as Simple
    'MEDIUM_THRESHOLD': 0.6,      # Problems with score <= 0.6 are classified as Medium
                                  # Problems with score > 0.6 are classified as Complex
    
    # Feature weights for complexity scoring
    'FEATURE_WEIGHTS': {
        'length': 0.15,            # Weight for problem length
        'sentence_structure': 0.1, # Weight for sentence structure complexity
        'variables': 0.2,          # Weight for number of variables
        'keywords': 0.15,          # Weight for mathematical keywords
        'domain': 0.15,            # Weight for mathematical domain
        'operations': 0.25,        # Weight for mathematical operations
    },
    
    # Mathematical domains and their complexity scores
    'DOMAIN_COMPLEXITY': {
        'arithmetic': 0.2,
        'algebra': 0.4,
        'geometry': 0.5,
        'calculus': 0.7,
        'statistics': 0.6,
        'number_theory': 0.8,
        'combinatorics': 0.7,
    },
    
    # Mathematical operations and their complexity scores
    'OPERATION_COMPLEXITY': {
        'addition': 0.1,
        'subtraction': 0.1,
        'multiplication': 0.2,
        'division': 0.3,
        'exponentiation': 0.4,
        'root': 0.5,
        'logarithm': 0.6,
        'trigonometric': 0.6,
        'derivative': 0.7,
        'integral': 0.8,
        'limit': 0.7,
        'summation': 0.6,
        'product': 0.6,
    },
}

# Thinking Strategy settings
THINKING_STRATEGIES = {
    # Fast Thinking settings
    'FAST': {
        'max_steps': 3,           # Maximum number of reasoning steps
        'token_budget': 100,      # Maximum number of tokens to use
        'verification_effort': 0.2, # Effort spent on verification (0.0 to 1.0)
    },
    
    # Slow Thinking settings
    'SLOW': {
        'max_steps': 10,          # Maximum number of reasoning steps
        'token_budget': 500,      # Maximum number of tokens to use
        'verification_effort': 0.8, # Effort spent on verification (0.0 to 1.0)
    },
    
    # Fast-then-Slow settings
    'FAST_THEN_SLOW': {
        'confidence_threshold': 0.7, # Threshold for switching from Fast to Slow
        'max_fast_steps': 2,      # Maximum steps in Fast mode before considering switch
    },
}

# Switching Mechanism settings
SWITCHING_MECHANISM = {
    # Default strategy mapping based on complexity
    'STRATEGY_MAPPING': {
        'Simple': 'FAST',
        'Medium': 'FAST_THEN_SLOW',
        'Complex': 'SLOW',
    },
    
    # Dynamic switching settings
    'CONFIDENCE_THRESHOLD': 0.7,  # Confidence threshold for dynamic switching
    'ERROR_DETECTION_THRESHOLD': 0.3, # Threshold for error detection
}

# Resource Allocator settings
RESOURCE_ALLOCATOR = {
    'BASE_TOKEN_BUDGET': 100,     # Base token budget
    'STEP_TOKEN_COST': 10,        # Token cost per reasoning step
    'VERIFICATION_TOKEN_COST': 20, # Token cost for verification
}

# Data settings
DATA = {
    'MATH_PROBLEMS_FILE': 'data/math_problems.json',
}

# Logging settings
LOGGING = {
    'LEVEL': 'INFO',              # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'FILE': 'logs/fast_slow_thinking.log',
}
