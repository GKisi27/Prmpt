"""
Level definitions for Prmpt
Levels 1-10: Static validation (regex/exact match)
Levels 11+: LLM-based validation
"""

LEVELS = [
    {
        "id": 1,
        "title": "Hello, World!",
        "description": "Your first prompt! Make the AI greet the world.",
        "goal": "Write a prompt that makes the AI output exactly: Hello, World!",
        "mode": "static",
        "validation": {
            "type": "exact",
            "expected": "Hello, World!",
            "case_sensitive": True
        },
        "difficulty": "beginner"
    },
    {
        "id": 2,
        "title": "Count to Five",
        "description": "Numbers are fundamental. Can you count?",
        "goal": "Write a prompt that outputs the numbers 1 through 5, separated by commas.",
        "mode": "static",
        "validation": {
            "type": "exact",
            "expected": "1, 2, 3, 4, 5",
            "case_sensitive": True
        },
        "difficulty": "beginner"
    },
    {
        "id": 3,
        "title": "Reverse It",
        "description": "Sometimes you need to think backwards.",
        "goal": "Write a prompt that outputs 'desserts' (stressed spelled backwards).",
        "mode": "static",
        "validation": {
            "type": "exact",
            "expected": "desserts",
            "case_sensitive": False
        },
        "difficulty": "beginner"
    },
    {
        "id": 4,
        "title": "JSON Basics",
        "description": "Structured data is powerful. Start with JSON.",
        "goal": "Output a valid JSON object with keys 'name' and 'age'.",
        "mode": "static",
        "validation": {
            "type": "contains",
            "expected": '"name"',
            "case_sensitive": True
        },
        "difficulty": "beginner"
    },
    {
        "id": 5,
        "title": "The Polite AI",
        "description": "Manners matter, even for AI.",
        "goal": "Make the AI say 'Please' and 'Thank you' in the same response.",
        "mode": "static",
        "validation": {
            "type": "regex",
            "expected": "(?i)please.*thank you|thank you.*please",
            "case_sensitive": False
        },
        "difficulty": "intermediate"
    },
]


def get_all_levels():
    """Return all available levels"""
    return LEVELS


def get_level_by_id(level_id: int):
    """Get a specific level by ID"""
    for level in LEVELS:
        if level["id"] == level_id:
            return level
    return None
