"""Handles all interactions with the external Google Gemini API."""

import google.generativeai as genai
from flask import current_app
import numpy as np


def generate_code_from_prompt(prompt_text):
    """
    Generates code from a text prompt using the Gemini API.

    Args:
        prompt_text (str): The user's natural language prompt.

    Returns:
        str: The generated code block as a string, or an error message.
    """
    try:
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }
        model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                                      generation_config=generation_config)
        full_prompt = (
            "You are a code generation expert. "
            "Based on the following prompt, generate only the code block requested. "
            "Do not include any explanation, preamble, or markdown formatting. "
            "Just return the raw code.\n\n"
            f"PROMPT: \"{prompt_text}\""
        )
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        current_app.logger.error(f"Gemini API error (generation): {e}")
        return "Error: Could not generate code. Please check the API key and server logs."


def explain_code(code_to_explain):
    """
    Generates an explanation for a block of code using the Gemini API.

    Args:
        code_to_explain (str): The block of code to be explained.

    Returns:
        str: The AI-generated explanation in Markdown format, or an error message.
    """
    try:
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        prompt = (
            "You are a code explanation expert. Provide a detailed, "
            "line-by-line explanation of the following code. "
            "Use Markdown for formatting, including bullet points and bold text. "
            "Do not wrap the entire response in a code block.\n\n"
            "CODE:\n"
            f"```\n{code_to_explain}\n```"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        current_app.logger.error(f"Gemini API error (explanation): {e}")
        return "Error: Could not generate explanation."


def suggest_tags_for_code(code_to_analyze):
    """
    Generates suggested tags for a block of code using the Gemini API.

    Args:
        code_to_analyze (str): The block of code to be analyzed.

    Returns:
        str: A comma-separated string of tags, or an error message.
    """
    try:
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        prompt = (
            "You are a code analysis expert. Analyze the following code and generate a "
            "comma-separated list of 3 to 5 relevant, lowercase tags. "
            "Do not include any explanation, markdown, or other text. "
            "Example output: python,flask,sqlalchemy,database\n\n"
            "CODE:\n"
            f"```\n{code_to_analyze}\n```"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        current_app.logger.error(f"Gemini API error (tagging): {e}")
        return "Error: Could not suggest tags."


def generate_embedding(text_to_embed, task_type="RETRIEVAL_DOCUMENT"):
    """
    Generates a vector embedding for a block of text using the Gemini API.

    Args:
        text_to_embed (str): The text to create an embedding for.
        task_type (str): The type of task ('RETRIEVAL_DOCUMENT' for storing,
                         'RETRIEVAL_QUERY' for searching).

    Returns:
        list: A list of floats representing the vector embedding, or None on error.
    """
    try:
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text_to_embed,
            task_type=task_type
        )
        return result['embedding']
    except Exception as e:
        current_app.logger.error(f"Gemini API error (embedding): {e}")
        return None


def generate_leetcode_solution(problem_title, problem_description, language):
    try:
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }
        model = genai.GenerativeModel(model_name="gemini-2.5-flash",
                                      generation_config=generation_config)
        full_prompt = (
            f"You are an expert LeetCode solution generator. "
            f"Generate a complete, correct, and efficient solution in {language} for the following LeetCode problem. "
            f"Provide only the code, without any explanation, preamble, or markdown formatting. "
            f"Problem Title: {problem_title}\n"
            f"Problem Description: {problem_description}\n\n"
            f"SOLUTION ({language}):"
        )
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        current_app.logger.error(f"Gemini API error (solution generation): {e}")
        return "Error: Could not generate solution. Please check the API key and server logs."


def explain_leetcode_solution(solution_code, problem_title, language):
    try:
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        prompt = (
            f"You are an expert at explaining LeetCode solutions. "
            f"Provide a concise but educative explanation for the following {language} solution to the problem '{problem_title}'. "
            f"Your explanation should cover:\n"
            f"1.  **Code Explanation**: A clear breakdown of the solution's logic.\n"
            f"2.  **Pattern Identification**: Identify any common algorithmic patterns or data structures used (e.g., Two Pointers, Dynamic Programming, Hash Map).\n"
            f"3.  **Time Complexity**: Analyze and state the time complexity of the solution.\n"
            f"4.  **Space Complexity**: Analyze and state the space complexity of the solution.\n"
            f"Use Markdown for formatting, including bullet points, code blocks, and bold text. "
            f"Do not wrap the entire response in a code block.\n\n"
            f"SOLUTION ({language}):\n"
            f"```\n{solution_code}\n```"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        current_app.logger.error(f"Gemini API error (explanation): {e}")
        return "Error: Could not generate explanation."


def classify_leetcode_solution(solution_code, problem_description):
    try:
        genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        prompt = (
            "You are an expert in LeetCode problem classification. "
            "Analyze the following problem description and its solution. "
            "Generate a comma-separated list of 3 to 5 relevant classifications "
            "(e.g., 'Dynamic Programming', 'Two Pointers', 'BFS', 'Array', 'Hash Table'). "
            "Do not include any explanation, markdown, or other text. "
            "Example output: Dynamic Programming,Array,Hash Table\n\n"
            f"PROBLEM DESCRIPTION:\n{problem_description}\n\n"
            f"SOLUTION CODE:\n```\n{solution_code}\n```"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        current_app.logger.error(f"Gemini API error (classification): {e}")
        return "Error: Could not classify solution."


def cosine_similarity(v1, v2):
    """
    Calculates the cosine similarity between two vectors.

    Args:
        v1 (np.array): The first vector.
        v2 (np.array): The second vector.

    Returns:
        float: The cosine similarity between v1 and v2, or 0.0 if a norm is zero.
    """
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return np.dot(v1, v2) / (norm_v1 * norm_v2)
