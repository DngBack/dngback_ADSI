"""
LLM Integration module for the Fast-Slow Thinking Math system.
"""

import os
from dotenv import load_dotenv
import openai
import json
import logging

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class LLMIntegration:
    """
    Integration with OpenAI's GPT models for mathematical problem solving.
    """

    def __init__(self, model="gpt-4"):
        """
        Initialize the LLM integration.

        Args:
            model (str): The OpenAI model to use (default: gpt-4)
        """
        self.model = model
        self.logger = logging.getLogger(__name__)

    def solve_problem(self, problem_text, thinking_mode="fast"):
        """
        Solve a mathematical problem using the LLM.

        Args:
            problem_text (str): The text of the mathematical problem
            thinking_mode (str): Either "fast" or "slow" thinking mode

        Returns:
            dict: Solution and metadata
        """
        try:
            # Prepare the prompt based on thinking mode
            if thinking_mode == "fast":
                prompt = self._create_fast_thinking_prompt(problem_text)
            else:
                prompt = self._create_slow_thinking_prompt(problem_text)

            # Call the OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a mathematical problem solver. Provide clear, step-by-step solutions.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3 if thinking_mode == "fast" else 0.7,
                max_tokens=1000 if thinking_mode == "fast" else 2000,
            )

            # Extract and parse the response
            solution_text = response.choices[0].message.content
            return self._parse_solution(solution_text, thinking_mode)

        except Exception as e:
            self.logger.error(f"Error in LLM problem solving: {str(e)}")
            return {
                "answer": None,
                "confidence": 0.0,
                "error": str(e),
                "steps": ["Error occurred during LLM processing"],
            }

    def _create_fast_thinking_prompt(self, problem_text):
        """Create a prompt for fast thinking mode."""
        return f"""Solve this mathematical problem quickly and efficiently:
{problem_text}

Provide:
1. The answer
2. A brief explanation
3. Confidence level (0-1)

Format your response as JSON:
{{
    "answer": "your answer",
    "explanation": "brief explanation",
    "confidence": confidence_value
}}"""

    def _create_slow_thinking_prompt(self, problem_text):
        """Create a prompt for slow thinking mode."""
        return f"""Solve this mathematical problem thoroughly and carefully:
{problem_text}

Provide:
1. Problem analysis
2. Step-by-step solution
3. Verification steps
4. The final answer
5. Confidence level (0-1)

Format your response as JSON:
{{
    "analysis": "problem analysis",
    "steps": ["step 1", "step 2", ...],
    "verification": "verification steps",
    "answer": "final answer",
    "confidence": confidence_value
}}"""

    def _parse_solution(self, solution_text, thinking_mode):
        """Parse the LLM's solution into a structured format."""
        try:
            # Extract JSON from the response
            json_str = solution_text[
                solution_text.find("{") : solution_text.rfind("}") + 1
            ]
            solution_data = json.loads(json_str)

            if thinking_mode == "fast":
                return {
                    "answer": solution_data.get("answer"),
                    "confidence": solution_data.get("confidence", 0.0),
                    "steps": [
                        solution_data.get("explanation", "No explanation provided")
                    ],
                    "error": None,
                }
            else:
                return {
                    "answer": solution_data.get("answer"),
                    "confidence": solution_data.get("confidence", 0.0),
                    "steps": solution_data.get("steps", []),
                    "verification": solution_data.get("verification", ""),
                    "error": None,
                }

        except json.JSONDecodeError:
            self.logger.error("Failed to parse LLM response as JSON")
            return {
                "answer": None,
                "confidence": 0.0,
                "error": "Failed to parse LLM response",
                "steps": ["Error parsing response"],
            }
