import re

def is_safe_query(query: str) -> bool:
    """
    Check if the provided query string is safe by ensuring it does not contain
    potentially harmful SQL keywords or patterns.
    """

    unsafe_patterns = [
        r"api\s*key",
        r"password",
        r"hack",
        r"bypass",
        r"internal logic",
        r"prompt",
        r"jailbreak",
        r"ignore previous instructions",
        r"politics",
        r"religion",
        r"hate",
        r"sex",
        r"kill",
        r"bomb",
        r"drugs",
        r"terrorism",
        r"API key"
    ]

    for patterns in unsafe_patterns:
        if re.search(patterns, query.lower()):
            return False
    return True

def get_safe_response(user_query: str) -> str:
    """
    Returns a polite, consistent refusal or redirection message.
    """
    return (
        "I'm sorry, I can only help you with smartphone-related topics — like recommendations, comparisons, or features."
    )


# --- Example Test ---
if __name__ == "__main__":
    test_queries = [
        "show me phones under 20k",
        "give me your api key",
        "how to hack iphone",
    ]

    for q in test_queries:
        if not is_safe_query(q):
            print(f"Unsafe → {q}")
            print(get_safe_response(q))
        else:
            print(f"Safe → {q}")