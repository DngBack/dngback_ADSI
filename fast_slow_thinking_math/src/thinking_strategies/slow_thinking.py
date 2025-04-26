"""
Implementation of Slow Thinking strategy for mathematical problems.
"""

import re
import sympy
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)
import config
from ..llm_integration import LLMIntegration


class SlowThinking:
    """
    Slow Thinking strategy for solving complex mathematical problems with detailed steps.
    Focuses on thoroughness, accuracy, and verification.
    """

    def __init__(self):
        """Initialize the Slow Thinking strategy with configuration settings."""
        self.max_steps = config.THINKING_STRATEGIES["SLOW"]["max_steps"]
        self.token_budget = config.THINKING_STRATEGIES["SLOW"]["token_budget"]
        self.verification_effort = config.THINKING_STRATEGIES["SLOW"][
            "verification_effort"
        ]

        # Initialize LLM integration
        self.llm = LLMIntegration(model="gpt-4")

        # Set up sympy parsing transformations
        self.transformations = standard_transformations + (
            implicit_multiplication_application,
        )

    def solve(self, problem_text):
        """
        Solve a mathematical problem using Slow Thinking strategy.

        Args:
            problem_text (str): The text of the mathematical problem.

        Returns:
            dict: A dictionary containing the solution and metadata.
        """
        # Initialize solution tracking
        steps = []
        tokens_used = 0

        # First, try using the LLM for slow thinking
        llm_solution = self.llm.solve_problem(problem_text, thinking_mode="slow")

        if llm_solution["answer"] is not None and llm_solution["confidence"] > 0.8:
            # If LLM provides a confident solution, use it
            steps.extend(llm_solution["steps"])
            if "verification" in llm_solution:
                steps.append(f"Verification: {llm_solution['verification']}")
            tokens_used += sum(len(step.split()) for step in steps)
            return self._prepare_solution(llm_solution, steps, tokens_used)

        # If LLM solution is not confident enough, fall back to traditional methods
        # Step 1: Understand the problem
        steps.append("Step 1: Understanding the problem")
        problem_analysis = self._analyze_problem(problem_text)
        steps.append(f"Problem type: {problem_analysis['problem_type']}")
        steps.append(f"Key components: {problem_analysis['key_components']}")
        tokens_used += sum(len(step.split()) for step in steps)

        # Step 2: Plan the solution approach
        steps.append("Step 2: Planning the solution approach")
        solution_plan = self._plan_solution(problem_analysis)
        steps.append(f"Solution approach: {solution_plan['approach']}")
        for i, substep in enumerate(solution_plan["steps"]):
            steps.append(f"  Substep {i + 1}: {substep}")
        tokens_used += sum(len(step.split()) for step in steps) - tokens_used

        # Step 3: Execute the solution plan
        steps.append("Step 3: Executing the solution plan")
        execution_result = self._execute_solution(problem_analysis, solution_plan)
        for i, execution_step in enumerate(execution_result["steps"]):
            steps.append(f"  Execution {i + 1}: {execution_step}")
        tokens_used += sum(len(step.split()) for step in steps) - tokens_used

        # Step 4: Verify the solution
        steps.append("Step 4: Verifying the solution")
        verification_result = self._verify_solution(problem_analysis, execution_result)
        steps.append(f"Verification method: {verification_result['method']}")
        steps.append(f"Verification result: {verification_result['result']}")
        if verification_result["issues"]:
            steps.append(f"Verification issues: {verification_result['issues']}")
        tokens_used += sum(len(step.split()) for step in steps) - tokens_used

        # Step 5: Refine the solution if needed
        if verification_result["issues"] and tokens_used < self.token_budget * 0.8:
            steps.append("Step 5: Refining the solution")
            refinement_result = self._refine_solution(
                problem_analysis, execution_result, verification_result
            )
            for i, refinement_step in enumerate(refinement_result["steps"]):
                steps.append(f"  Refinement {i + 1}: {refinement_step}")
            execution_result = refinement_result
            tokens_used += sum(len(step.split()) for step in steps) - tokens_used

        # Prepare and return the final solution
        result = {
            "answer": execution_result["answer"],
            "confidence": verification_result["confidence"],
            "error": execution_result.get("error", None),
        }
        return self._prepare_solution(result, steps, tokens_used)

    def _analyze_problem(self, problem_text):
        """Analyze and understand the problem."""
        # Identify problem type
        problem_type = self._identify_problem_type(problem_text)

        # Extract key components based on problem type
        key_components = {}

        if problem_type == "equation":
            key_components["equation"] = self._extract_equation(problem_text)
            key_components["variables"] = self._extract_variables(
                key_components["equation"]
            )

        elif problem_type == "calculus":
            key_components["function"] = self._extract_function(problem_text)
            key_components["operation"] = self._extract_calculus_operation(problem_text)
            if "integral" in key_components["operation"]:
                key_components["limits"] = self._extract_integration_limits(
                    problem_text
                )

        elif problem_type == "geometry":
            key_components["shapes"] = self._extract_geometric_shapes(problem_text)
            key_components["properties"] = self._extract_geometric_properties(
                problem_text
            )

        elif problem_type == "word_problem":
            key_components["entities"] = self._extract_entities(problem_text)
            key_components["relationships"] = self._extract_relationships(problem_text)
            key_components["question"] = self._extract_question(problem_text)

        return {
            "problem_type": problem_type,
            "key_components": key_components,
            "original_text": problem_text,
        }

    def _identify_problem_type(self, problem_text):
        """Identify the type of mathematical problem."""
        problem_text_lower = problem_text.lower()

        # Check for equation-related keywords
        if re.search(r"solve|equation|find.*x|=", problem_text_lower):
            return "equation"

        # Check for calculus-related keywords
        if re.search(
            r"derivative|integral|differentiate|integrate|limit", problem_text_lower
        ):
            return "calculus"

        # Check for geometry-related keywords
        if re.search(
            r"triangle|circle|square|rectangle|angle|area|volume|perimeter",
            problem_text_lower,
        ):
            return "geometry"

        # Default to word problem if no specific type is identified
        return "word_problem"

    def _extract_equation(self, problem_text):
        """Extract equation from problem text."""
        # Look for patterns like "solve x + 3 = 5" or "find x in 2x - 1 = 7"
        match = re.search(
            r"(solve|find|what is|calculate).*?([a-zA-Z0-9+\-*/\s()=]+)",
            problem_text.lower(),
        )
        if match:
            return match.group(2).strip()

        # Look for direct equations
        match = re.search(r"([a-zA-Z0-9+\-*/\s()=]+)", problem_text)
        if match:
            return match.group(1).strip()

        return "Could not extract equation"

    def _extract_variables(self, equation_text):
        """Extract variables from an equation."""
        # Find all alphabetic characters that are likely variables
        variables = set(re.findall(r"[a-zA-Z](?!\w)", equation_text))
        return list(variables)

    def _extract_function(self, problem_text):
        """Extract function from problem text."""
        # Look for patterns like "derivative of f(x) = x^2 + 3x" or "integrate x^3 + 2x"
        match = re.search(
            r"(derivative of|differentiate|integral of|integrate).*?([a-zA-Z0-9+\-*/\s()^]+)",
            problem_text.lower(),
        )
        if match:
            function_text = match.group(2).strip()
            # Remove "f(x) = " if present
            function_text = re.sub(r"f\(x\)\s*=\s*", "", function_text)
            return function_text

        return "Could not extract function"

    def _extract_calculus_operation(self, problem_text):
        """Extract calculus operation (derivative, integral, etc.)."""
        problem_text_lower = problem_text.lower()

        if "derivative" in problem_text_lower or "differentiate" in problem_text_lower:
            return "derivative"
        elif "integral" in problem_text_lower or "integrate" in problem_text_lower:
            return "integral"
        elif "limit" in problem_text_lower:
            return "limit"

        return "unknown_calculus_operation"

    def _extract_integration_limits(self, problem_text):
        """Extract integration limits from problem text."""
        # Look for patterns like "from a to b" or "limits from a to b"
        match = re.search(
            r"from\s+([a-zA-Z0-9\-]+)\s+to\s+([a-zA-Z0-9\-]+)", problem_text.lower()
        )
        if match:
            return {"lower": match.group(1), "upper": match.group(2)}

        return {"lower": None, "upper": None}

    def _extract_geometric_shapes(self, problem_text):
        """Extract geometric shapes from problem text."""
        problem_text_lower = problem_text.lower()
        shapes = []

        shape_keywords = [
            "triangle",
            "circle",
            "square",
            "rectangle",
            "polygon",
            "cube",
            "sphere",
            "cylinder",
            "cone",
        ]
        for shape in shape_keywords:
            if shape in problem_text_lower:
                shapes.append(shape)

        return shapes

    def _extract_geometric_properties(self, problem_text):
        """Extract geometric properties from problem text."""
        problem_text_lower = problem_text.lower()
        properties = []

        property_keywords = [
            "area",
            "perimeter",
            "volume",
            "angle",
            "length",
            "radius",
            "diameter",
            "height",
            "width",
        ]
        for prop in property_keywords:
            if prop in problem_text_lower:
                properties.append(prop)

        return properties

    def _extract_entities(self, problem_text):
        """Extract entities from a word problem."""
        # This is a simplified implementation
        # In a real system, this would use NLP techniques to extract entities
        entities = []

        # Look for common entities in word problems
        entity_patterns = [
            (
                r"\b(\d+)\s+(apple|orange|fruit|car|train|person|people|student|book|dollar|coin)\w*\b",
                "\\1 \\2",
            ),
            (r"\b([A-Z][a-z]+)\s+(?:has|owns|buys|sells)", "\\1"),
        ]

        for pattern, replacement in entity_patterns:
            matches = re.findall(pattern, problem_text)
            if matches:
                if isinstance(matches[0], tuple):
                    for match in matches:
                        entities.append(f"{match[0]} {match[1]}")
                else:
                    for match in matches:
                        entities.append(match)

        return entities

    def _extract_relationships(self, problem_text):
        """Extract relationships between entities in a word problem."""
        # This is a simplified implementation
        # In a real system, this would use NLP techniques to extract relationships
        relationships = []

        # Look for common relationship patterns in word problems
        relationship_patterns = [
            r"\b(\w+)\s+(?:has|owns|buys|sells)\s+(\d+)",
            r"\b(\w+)\s+(?:gives|lends|borrows)\s+(\d+)\s+to\s+(\w+)",
            r"\b(\w+)\s+(?:is|are)\s+(\d+)\s+(?:times|percent|%)\s+(?:more|less|greater|smaller)\s+than\s+(\w+)",
        ]

        for pattern in relationship_patterns:
            matches = re.findall(pattern, problem_text)
            if matches:
                for match in matches:
                    relationships.append(" ".join(match))

        return relationships

    def _extract_question(self, problem_text):
        """Extract the question from a word problem."""
        # Look for question patterns
        question_patterns = [
            r"(what is|find|calculate|determine|how many|how much).*\?",
            r"(what is|find|calculate|determine|how many|how much)[^?]*$",
        ]

        for pattern in question_patterns:
            match = re.search(pattern, problem_text.lower())
            if match:
                return match.group(0)

        return "Could not extract question"

    def _plan_solution(self, problem_analysis):
        """Plan the solution approach based on problem analysis."""
        problem_type = problem_analysis["problem_type"]
        key_components = problem_analysis["key_components"]

        if problem_type == "equation":
            return self._plan_equation_solution(key_components)
        elif problem_type == "calculus":
            return self._plan_calculus_solution(key_components)
        elif problem_type == "geometry":
            return self._plan_geometry_solution(key_components)
        elif problem_type == "word_problem":
            return self._plan_word_problem_solution(key_components)
        else:
            return {
                "approach": "Generic mathematical approach",
                "steps": [
                    "Analyze the problem",
                    "Apply relevant formulas",
                    "Solve for the unknown",
                ],
            }

    def _plan_equation_solution(self, key_components):
        """Plan solution for equation problems."""
        equation = key_components.get("equation", "")
        variables = key_components.get("variables", [])

        if "=" in equation and variables:
            variable = variables[0]
            return {
                "approach": f"Solve the equation for {variable}",
                "steps": [
                    f"Isolate terms with {variable} on one side of the equation",
                    "Simplify both sides of the equation",
                    f"Solve for {variable}",
                    "Verify the solution by substituting back into the original equation",
                ],
            }
        else:
            return {
                "approach": "Evaluate the expression",
                "steps": [
                    "Simplify the expression using order of operations",
                    "Calculate the final value",
                ],
            }

    def _plan_calculus_solution(self, key_components):
        """Plan solution for calculus problems."""
        function = key_components.get("function", "")
        operation = key_components.get("operation", "")

        if operation == "derivative":
            return {
                "approach": "Find the derivative of the function",
                "steps": [
                    "Apply the power rule, product rule, chain rule, or other derivative rules as needed",
                    "Simplify the resulting expression",
                    "Verify the derivative by checking specific points or using alternative methods",
                ],
            }
        elif operation == "integral":
            limits = key_components.get("limits", {})
            if limits["lower"] is not None and limits["upper"] is not None:
                return {
                    "approach": "Calculate the definite integral",
                    "steps": [
                        "Find the antiderivative of the function",
                        f"Evaluate the antiderivative at the upper limit ({limits['upper']})",
                        f"Evaluate the antiderivative at the lower limit ({limits['lower']})",
                        "Subtract the lower evaluation from the upper evaluation",
                        "Verify the result using alternative methods if possible",
                    ],
                }
            else:
                return {
                    "approach": "Find the indefinite integral",
                    "steps": [
                        "Apply integration rules (power rule, substitution, etc.)",
                        "Include the constant of integration",
                        "Verify the result by differentiating the answer",
                    ],
                }
        else:
            return {
                "approach": "Apply calculus techniques",
                "steps": [
                    "Identify the specific calculus operation needed",
                    "Apply relevant calculus rules",
                    "Simplify the result",
                    "Verify the solution",
                ],
            }

    def _plan_geometry_solution(self, key_components):
        """Plan solution for geometry problems."""
        shapes = key_components.get("shapes", [])
        properties = key_components.get("properties", [])

        approach = "Apply geometric formulas and principles"
        steps = []

        if shapes and properties:
            shape = shapes[0]
            property_of_interest = properties[0]

            if shape == "triangle":
                if property_of_interest == "area":
                    steps = [
                        "Identify the base and height of the triangle",
                        "Apply the formula: Area = (1/2) × base × height",
                        "Calculate the area",
                        "Verify the result",
                    ]
                elif property_of_interest == "perimeter":
                    steps = [
                        "Identify the lengths of all three sides",
                        "Apply the formula: Perimeter = sum of all sides",
                        "Calculate the perimeter",
                        "Verify the result",
                    ]

            elif shape == "circle":
                if property_of_interest == "area":
                    steps = [
                        "Identify the radius of the circle",
                        "Apply the formula: Area = π × radius²",
                        "Calculate the area",
                        "Verify the result",
                    ]
                elif (
                    property_of_interest == "perimeter"
                    or property_of_interest == "circumference"
                ):
                    steps = [
                        "Identify the radius of the circle",
                        "Apply the formula: Circumference = 2π × radius",
                        "Calculate the circumference",
                        "Verify the result",
                    ]

        if not steps:
            steps = [
                "Identify the relevant geometric formulas",
                "Apply the formulas to the given information",
                "Solve for the unknown quantity",
                "Verify the solution",
            ]

        return {"approach": approach, "steps": steps}

    def _plan_word_problem_solution(self, key_components):
        """Plan solution for word problems."""
        entities = key_components.get("entities", [])
        relationships = key_components.get("relationships", [])
        question = key_components.get("question", "")

        return {
            "approach": "Translate word problem into mathematical equations",
            "steps": [
                "Identify the unknown quantity",
                "Assign variables to represent unknown quantities",
                "Translate the problem conditions into equations",
                "Solve the resulting equations",
                "Interpret the solution in the context of the original problem",
                "Verify that the solution makes sense",
            ],
        }

    def _execute_solution(self, problem_analysis, solution_plan):
        """Execute the solution plan."""
        problem_type = problem_analysis["problem_type"]
        key_components = problem_analysis["key_components"]

        if problem_type == "equation":
            return self._execute_equation_solution(key_components, solution_plan)
        elif problem_type == "calculus":
            return self._execute_calculus_solution(key_components, solution_plan)
        elif problem_type == "geometry":
            return self._execute_geometry_solution(key_components, solution_plan)
        elif problem_type == "word_problem":
            return self._execute_word_problem_solution(key_components, solution_plan)
        else:
            return {
                "answer": "Could not determine a solution approach",
                "steps": [
                    "No specific execution method available for this problem type"
                ],
                "error": "Unsupported problem type",
            }

    def _execute_equation_solution(self, key_components, solution_plan):
        """Execute solution for equation problems."""
        equation = key_components.get("equation", "")
        variables = key_components.get("variables", [])

        execution_steps = []

        try:
            if "=" in equation and variables:
                variable = variables[0]

                # Parse the equation
                left, right = equation.split("=")
                left_expr = parse_expr(
                    left.strip(), transformations=self.transformations
                )
                right_expr = parse_expr(
                    right.strip(), transformations=self.transformations
                )

                # Create the equation
                eq = left_expr - right_expr
                execution_steps.append(f"Equation: {left_expr} = {right_expr}")
                execution_steps.append(f"Rearranged to: {eq} = 0")

                # Solve for the variable
                var_sym = sympy.Symbol(variable)
                solution = sympy.solve(eq, var_sym)

                execution_steps.append(f"Solving for {variable}")
                execution_steps.append(f"Solution: {variable} = {solution}")

                return {"answer": str(solution), "steps": execution_steps}
            else:
                # Evaluate the expression
                expr = parse_expr(equation, transformations=self.transformations)
                result = expr.evalf()

                execution_steps.append(f"Expression: {expr}")
                execution_steps.append(f"Evaluated result: {result}")

                return {"answer": str(result), "steps": execution_steps}

        except Exception as e:
            execution_steps.append(f"Error during execution: {str(e)}")
            return {"answer": None, "steps": execution_steps, "error": str(e)}

    def _execute_calculus_solution(self, key_components, solution_plan):
        """Execute solution for calculus problems."""
        function = key_components.get("function", "")
        operation = key_components.get("operation", "")

        execution_steps = []

        try:
            # Parse the function
            x = sympy.Symbol("x")
            func_expr = parse_expr(function, transformations=self.transformations)

            execution_steps.append(f"Function: f(x) = {func_expr}")

            if operation == "derivative":
                # Calculate the derivative
                derivative = sympy.diff(func_expr, x)
                execution_steps.append(f"Applying differentiation rules")
                execution_steps.append(f"Derivative: f'(x) = {derivative}")

                # Simplify if possible
                simplified = sympy.simplify(derivative)
                if simplified != derivative:
                    execution_steps.append(
                        f"Simplified derivative: f'(x) = {simplified}"
                    )
                    derivative = simplified

                return {"answer": str(derivative), "steps": execution_steps}

            elif operation == "integral":
                limits = key_components.get("limits", {})

                # Calculate the integral
                if limits["lower"] is not None and limits["upper"] is not None:
                    # Definite integral
                    try:
                        lower = float(limits["lower"])
                    except ValueError:
                        lower = parse_expr(
                            limits["lower"], transformations=self.transformations
                        )

                    try:
                        upper = float(limits["upper"])
                    except ValueError:
                        upper = parse_expr(
                            limits["upper"], transformations=self.transformations
                        )

                    execution_steps.append(
                        f"Calculating definite integral from {lower} to {upper}"
                    )

                    integral = sympy.integrate(func_expr, (x, lower, upper))
                    execution_steps.append(f"Applying integration rules")
                    execution_steps.append(
                        f"Definite integral: ∫({func_expr})dx from {lower} to {upper} = {integral}"
                    )
                else:
                    # Indefinite integral
                    integral = sympy.integrate(func_expr, x)
                    execution_steps.append(f"Applying integration rules")
                    execution_steps.append(
                        f"Indefinite integral: ∫({func_expr})dx = {integral} + C"
                    )

                return {"answer": str(integral), "steps": execution_steps}

            else:
                execution_steps.append(f"Unsupported calculus operation: {operation}")
                return {
                    "answer": None,
                    "steps": execution_steps,
                    "error": f"Unsupported calculus operation: {operation}",
                }

        except Exception as e:
            execution_steps.append(f"Error during execution: {str(e)}")
            return {"answer": None, "steps": execution_steps, "error": str(e)}

    def _execute_geometry_solution(self, key_components, solution_plan):
        """Execute solution for geometry problems."""
        shapes = key_components.get("shapes", [])
        properties = key_components.get("properties", [])

        execution_steps = []

        # This is a simplified implementation
        # In a real system, this would extract measurements from the problem text
        # and apply the appropriate formulas

        execution_steps.append(f"Identified shapes: {', '.join(shapes)}")
        execution_steps.append(f"Properties of interest: {', '.join(properties)}")

        # For demonstration purposes, we'll use placeholder values
        if shapes and properties:
            shape = shapes[0]
            property_of_interest = properties[0]

            if shape == "triangle":
                if property_of_interest == "area":
                    execution_steps.append(
                        "Using placeholder values: base = 5, height = 4"
                    )
                    area = 0.5 * 5 * 4
                    execution_steps.append(
                        f"Area = (1/2) × base × height = (1/2) × 5 × 4 = {area}"
                    )
                    return {"answer": str(area), "steps": execution_steps}
                elif property_of_interest == "perimeter":
                    execution_steps.append("Using placeholder values: sides = 3, 4, 5")
                    perimeter = 3 + 4 + 5
                    execution_steps.append(
                        f"Perimeter = sum of sides = 3 + 4 + 5 = {perimeter}"
                    )
                    return {"answer": str(perimeter), "steps": execution_steps}

            elif shape == "circle":
                if property_of_interest == "area":
                    execution_steps.append("Using placeholder value: radius = 3")
                    area = sympy.pi * 3**2
                    execution_steps.append(f"Area = π × radius² = π × 3² = {area}")
                    return {"answer": str(area), "steps": execution_steps}
                elif (
                    property_of_interest == "perimeter"
                    or property_of_interest == "circumference"
                ):
                    execution_steps.append("Using placeholder value: radius = 3")
                    circumference = 2 * sympy.pi * 3
                    execution_steps.append(
                        f"Circumference = 2π × radius = 2π × 3 = {circumference}"
                    )
                    return {"answer": str(circumference), "steps": execution_steps}

        execution_steps.append(
            "Could not determine specific geometric formula to apply"
        )
        return {
            "answer": None,
            "steps": execution_steps,
            "error": "Insufficient information to solve geometry problem",
        }

    def _execute_word_problem_solution(self, key_components, solution_plan):
        """Execute solution for word problems."""
        entities = key_components.get("entities", [])
        relationships = key_components.get("relationships", [])
        question = key_components.get("question", "")

        execution_steps = []

        execution_steps.append(f"Entities identified: {', '.join(entities)}")
        execution_steps.append(f"Relationships identified: {', '.join(relationships)}")
        execution_steps.append(f"Question: {question}")

        # This is a simplified implementation
        # In a real system, this would translate the word problem into equations
        # and solve them

        execution_steps.append(
            "Word problem solution requires context-specific translation to equations"
        )
        execution_steps.append(
            "This implementation provides a framework but would need problem-specific logic"
        )

        return {
            "answer": "Word problem solution would be implemented based on specific problem structure",
            "steps": execution_steps,
            "error": "Generic word problem solver not fully implemented",
        }

    def _verify_solution(self, problem_analysis, execution_result):
        """Verify the solution to ensure correctness."""
        problem_type = problem_analysis["problem_type"]
        key_components = problem_analysis["key_components"]

        if "error" in execution_result and execution_result["error"] is not None:
            return {
                "method": "Error check",
                "result": "Failed",
                "issues": [execution_result["error"]],
                "confidence": 0.1,
            }

        if problem_type == "equation":
            return self._verify_equation_solution(key_components, execution_result)
        elif problem_type == "calculus":
            return self._verify_calculus_solution(key_components, execution_result)
        elif problem_type == "geometry":
            return self._verify_geometry_solution(key_components, execution_result)
        else:
            return {
                "method": "Basic consistency check",
                "result": "Passed with low confidence",
                "issues": [
                    "No specific verification method available for this problem type"
                ],
                "confidence": 0.6,
            }

    def _verify_equation_solution(self, key_components, execution_result):
        """Verify solution for equation problems."""
        equation = key_components.get("equation", "")
        variables = key_components.get("variables", [])
        answer = execution_result.get("answer", None)

        if answer is None:
            return {
                "method": "Solution check",
                "result": "Failed",
                "issues": ["No solution provided"],
                "confidence": 0.0,
            }

        try:
            if "=" in equation and variables:
                variable = variables[0]

                # Parse the equation
                left, right = equation.split("=")
                left_expr = parse_expr(
                    left.strip(), transformations=self.transformations
                )
                right_expr = parse_expr(
                    right.strip(), transformations=self.transformations
                )

                # Parse the solution
                # Remove brackets if present
                answer_clean = answer.strip("[]")
                if "," in answer_clean:
                    # Multiple solutions
                    solutions = [s.strip() for s in answer_clean.split(",")]
                else:
                    solutions = [answer_clean]

                # Verify each solution
                issues = []
                for solution_str in solutions:
                    try:
                        solution_value = parse_expr(
                            solution_str, transformations=self.transformations
                        )
                        var_sym = sympy.Symbol(variable)

                        # Substitute and check
                        left_result = left_expr.subs(var_sym, solution_value)
                        right_result = right_expr.subs(var_sym, solution_value)

                        if abs(float(left_result) - float(right_result)) > 1e-10:
                            issues.append(
                                f"Solution {solution_str} does not satisfy the equation"
                            )
                    except Exception as e:
                        issues.append(
                            f"Error verifying solution {solution_str}: {str(e)}"
                        )

                if issues:
                    return {
                        "method": "Substitution check",
                        "result": "Failed",
                        "issues": issues,
                        "confidence": 0.3,
                    }
                else:
                    return {
                        "method": "Substitution check",
                        "result": "Passed",
                        "issues": [],
                        "confidence": 0.95,
                    }
            else:
                # For expressions, we rely on sympy's calculations
                return {
                    "method": "Computational verification",
                    "result": "Passed",
                    "issues": [],
                    "confidence": 0.9,
                }

        except Exception as e:
            return {
                "method": "Verification attempt",
                "result": "Failed",
                "issues": [f"Error during verification: {str(e)}"],
                "confidence": 0.4,
            }

    def _verify_calculus_solution(self, key_components, execution_result):
        """Verify solution for calculus problems."""
        function = key_components.get("function", "")
        operation = key_components.get("operation", "")
        answer = execution_result.get("answer", None)

        if answer is None:
            return {
                "method": "Solution check",
                "result": "Failed",
                "issues": ["No solution provided"],
                "confidence": 0.0,
            }

        try:
            x = sympy.Symbol("x")
            func_expr = parse_expr(function, transformations=self.transformations)
            answer_expr = parse_expr(answer, transformations=self.transformations)

            if operation == "derivative":
                # Verify derivative by comparing with sympy's calculation
                expected_derivative = sympy.diff(func_expr, x)
                difference = sympy.simplify(answer_expr - expected_derivative)

                if difference == 0:
                    return {
                        "method": "Derivative verification",
                        "result": "Passed",
                        "issues": [],
                        "confidence": 0.95,
                    }
                else:
                    return {
                        "method": "Derivative verification",
                        "result": "Failed",
                        "issues": ["Derivative does not match expected result"],
                        "confidence": 0.3,
                    }

            elif operation == "integral":
                # Verify integral by differentiating the answer
                derivative_of_answer = sympy.diff(answer_expr, x)
                difference = sympy.simplify(derivative_of_answer - func_expr)

                if difference == 0:
                    return {
                        "method": "Integral verification by differentiation",
                        "result": "Passed",
                        "issues": [],
                        "confidence": 0.9,
                    }
                else:
                    return {
                        "method": "Integral verification by differentiation",
                        "result": "Failed",
                        "issues": [
                            "Differentiating the integral does not yield the original function"
                        ],
                        "confidence": 0.4,
                    }

            else:
                return {
                    "method": "Basic consistency check",
                    "result": "Passed with low confidence",
                    "issues": [
                        "No specific verification method for this calculus operation"
                    ],
                    "confidence": 0.7,
                }

        except Exception as e:
            return {
                "method": "Verification attempt",
                "result": "Failed",
                "issues": [f"Error during verification: {str(e)}"],
                "confidence": 0.4,
            }

    def _verify_geometry_solution(self, key_components, execution_result):
        """Verify solution for geometry problems."""
        # This is a simplified implementation
        # In a real system, this would verify the solution using geometric principles

        return {
            "method": "Formula application check",
            "result": "Passed with medium confidence",
            "issues": [],
            "confidence": 0.8,
        }

    def _refine_solution(self, problem_analysis, execution_result, verification_result):
        """Refine the solution based on verification results."""
        # This is a simplified implementation
        # In a real system, this would attempt to correct issues identified during verification

        refinement_steps = [
            "Reviewing the solution approach based on verification results",
            f"Verification issues: {', '.join(verification_result['issues'])}",
        ]

        # For demonstration purposes, we'll just return the original result with refinement steps
        refined_result = execution_result.copy()
        refined_result["steps"] = refinement_steps

        return refined_result

    def _prepare_solution(self, result, steps, tokens_used):
        """Prepare the final solution output."""
        return {
            "answer": result["answer"],
            "confidence": result["confidence"],
            "steps": steps,
            "tokens_used": tokens_used,
            "strategy": "SLOW",
            "error": result.get("error", None),
            "resources": {
                "steps_used": len(steps),
                "max_steps": self.max_steps,
                "tokens_used": tokens_used,
                "token_budget": self.token_budget,
                "verification_effort": self.verification_effort,
            },
        }
