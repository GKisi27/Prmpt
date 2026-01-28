"""
Static Judge Service - Regex/Exact match validation for levels 1-10
"""
import re
from typing import Tuple


def judge_static(user_input: str, validation: dict) -> Tuple[bool, str, int]:
    """
    Judge user input against static validation rules.
    
    Returns:
        Tuple of (success, feedback, score)
    """
    validation_type = validation.get("type", "exact")
    expected = validation.get("expected", "")
    case_sensitive = validation.get("case_sensitive", True)
    
    # Normalize for case-insensitive comparison
    compare_input = user_input if case_sensitive else user_input.lower()
    compare_expected = expected if case_sensitive else expected.lower()
    
    if validation_type == "exact":
        # Exact match
        if compare_input.strip() == compare_expected.strip():
            return True, "Perfect! Exact match achieved! 🎉", 100
        else:
            return False, f"Not quite. Expected exactly: '{expected}'", 0
    
    elif validation_type == "contains":
        # Check if output contains expected string
        if compare_expected in compare_input:
            return True, "Great job! Your output contains the required content! ✨", 100
        else:
            return False, f"Your output should contain: '{expected}'", 0
    
    elif validation_type == "regex":
        # Regex pattern match
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            if re.search(expected, user_input, flags):
                return True, "Excellent! Pattern matched successfully! 🚀", 100
            else:
                return False, "The pattern doesn't match. Try a different approach.", 0
        except re.error:
            return False, "Internal error: Invalid validation pattern.", 0
    
    return False, "Unknown validation type.", 0
