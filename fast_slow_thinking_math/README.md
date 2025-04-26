# Fast-Slow Thinking for Mathematical Problems

This project implements a Fast-Slow Thinking system for mathematical problems, which automatically determines the complexity of math problems and applies appropriate thinking strategies to optimize the balance between performance and resource efficiency.

## Project Structure

```
fast_slow_thinking_math/
├── data/                      # Data directory
│   ├── math_problems.json     # Sample math problems dataset
│   └── README.md              # Data documentation
├── src/                       # Source code
│   ├── __init__.py            # Package initialization
│   ├── complexity_analyzer/   # Complexity analysis module
│   │   ├── __init__.py
│   │   ├── analyzer.py        # Main analyzer implementation
│   │   └── features.py        # Feature extraction utilities
│   ├── thinking_strategies/   # Thinking strategies module
│   │   ├── __init__.py
│   │   ├── fast_thinking.py   # Fast thinking implementation
│   │   ├── slow_thinking.py   # Slow thinking implementation
│   │   └── combined.py        # Fast-then-Slow implementation
│   ├── switching_mechanism/   # Switching mechanism module
│   │   ├── __init__.py
│   │   ├── switcher.py        # Main switcher implementation
│   │   └── monitor.py         # Reasoning process monitor
│   └── resource_allocator/    # Resource allocation module
│       ├── __init__.py
│       └── allocator.py       # Resource allocator implementation
├── tests/                     # Test directory
│   ├── __init__.py
│   ├── test_complexity_analyzer.py
│   ├── test_thinking_strategies.py
│   └── test_switching_mechanism.py
├── notebooks/                 # Jupyter notebooks for exploration and visualization
│   ├── complexity_analysis.ipynb
│   └── performance_evaluation.ipynb
├── main.py                    # Main entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fast_slow_thinking_math.git
cd fast_slow_thinking_math

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from src.complexity_analyzer.analyzer import ComplexityAnalyzer
from src.thinking_strategies.fast_thinking import FastThinking
from src.thinking_strategies.slow_thinking import SlowThinking
from src.thinking_strategies.combined import FastThenSlow
from src.switching_mechanism.switcher import ThinkingSwitcher
from src.resource_allocator.allocator import ResourceAllocator

# Initialize components
analyzer = ComplexityAnalyzer()
fast_thinking = FastThinking()
slow_thinking = SlowThinking()
fast_then_slow = FastThenSlow(fast_thinking, slow_thinking)
resource_allocator = ResourceAllocator()
switcher = ThinkingSwitcher(
    analyzer=analyzer,
    fast_strategy=fast_thinking,
    slow_strategy=slow_thinking,
    combined_strategy=fast_then_slow,
    resource_allocator=resource_allocator
)

# Solve a math problem
problem = "Solve for x: 2x + 3 = 7"
result = switcher.solve(problem)
print(f"Solution: {result.answer}")
print(f"Strategy used: {result.strategy}")
print(f"Resources used: {result.resources}")
```

## Components

### Complexity Analyzer

The Complexity Analyzer evaluates the complexity of mathematical problems based on various features such as length, structure, variables, mathematical keywords, etc. It assigns a complexity score from 0.0 to 1.0 and classifies problems into different complexity levels.

### Thinking Strategies

- **Fast Thinking**: A strategy for simple problems, focusing on speed and efficiency.
- **Slow Thinking**: A strategy for complex problems, focusing on accuracy and detail.
- **Fast-then-Slow**: A combined strategy that starts with Fast Thinking and switches to Slow Thinking if needed.

### Switching Mechanism

The Switching Mechanism decides which thinking strategy to use based on the complexity assessment and monitors the reasoning process to adjust the strategy if necessary.

### Resource Allocator

The Resource Allocator manages computational resources based on the selected thinking strategy, adjusting the number of tokens, reasoning steps, and verification effort.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
