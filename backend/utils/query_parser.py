import json
from transformers import pipeline
from huggingface_hub import login

# Login to HF Hub
login(token="hf_your_token_here")

model_name = "Qwen/Qwen2.5-3B-Instruct"

# Use pipeline for chat-like models
llm = pipeline(
    "text-generation",
    model=model_name,
    torch_dtype="auto",
    device_map="auto",
    return_full_text=False
)

# -----------------------------
# LOAD PHONE DATABASE
# -----------------------------
with open("/Users/nirzarshah/Documents/AI-shopping chat agent/dataset/phones.json", "r") as f:
    PHONE_DB = json.load(f)      # <-- This is a LIST, not a dict


# -----------------------------
# PARSER: EXTRACT INTENT + PHONES
# -----------------------------
def parse_query(user_query):
    """
    Uses LLM to extract:
    - intent
    - phones_to_compare (1 or more models)
    - brand, budget, features (optional)
    """

    prompt = f"""
You are a strict JSON parser.

Extract smartphone information from this query:
"{user_query}"

Rules:
1. Detect complete PHONE MODEL names (e.g., "iPhone 15 Pro", "Samsung Galaxy S23 Ultra").
2. phones_to_compare MUST be an array of model names.
3. If 2 or more phones detected → intent = "comparison".
4. If 1 phone detected → intent = "explanation".
5. If the user asks for suggestions → intent = "recommendation".
6. brand and budget may remain empty.
7. DO NOT output anything except valid JSON.

Return this JSON ONLY:

{{
  "intent": "",
  "brand": "",
  "budget": "",
  "features": [],
  "phones_to_compare": []
}}
"""

    result = llm(
        prompt,
        max_new_tokens=200,
        temperature=0.0,
        do_sample=False
    )

    response_text = result[0]["generated_text"]

    # Extract JSON substring safely
    try:
        start = response_text.index("{")
        end = response_text.rindex("}") + 1
        json_str = response_text[start:end]
        parsed = json.loads(json_str)
        return parsed

    except Exception:
        return {
            "intent": "irrelevant",
            "brand": "",
            "budget": "",
            "features": [],
            "phones_to_compare": []
        }



# -----------------------------
# FETCH PHONE INFO FROM phones.json
# -----------------------------
def get_phone_data(phone_name: str):
    """
    Retrieve info from phones.json (which is a LIST, not DICT).
    Matches by partial name.
    """

    if not phone_name:
        return None

    phone_name = phone_name.lower().strip()

    for item in PHONE_DB:
        if phone_name in item["name"].lower():
            return item

    return None



# -----------------------------
# SUMMARIZE PHONE SPECIFICATIONS
# -----------------------------
def summarize_phone(phone_name: str):
    """
    Fetch raw phone data + generate natural-language summary.
    """

    data = get_phone_data(phone_name)

    if not data:
        return f"Sorry, I couldn't find details for '{phone_name}'."

    # Convert phone object to formatted text for LLM
    raw_text = "\n".join([f"{k}: {v}" for k, v in data.items()])

    prompt = f"""
Summarize the following smartphone specifications in simple, clear English.
Avoid marketing language. Highlight strengths and weaknesses.

Phone name: {data.get("name")}

Specifications:
{raw_text}

Write a friendly, helpful summary:
"""

    result = llm(
        prompt,
        max_new_tokens=250,
        temperature=0.3,
        do_sample=True
    )

    return result[0]["generated_text"]



# -----------------------------
# HELPER: Pick the phone name from parsed query
# -----------------------------
def get_first_phone(parsed):
    """
    Return:
    - first phone in phones_to_compare, or
    - fallback to brand if user mentions "Samsung", etc.
    """

    if parsed.get("phones_to_compare"):
        return parsed["phones_to_compare"][0]

    if parsed.get("brand"):
        return parsed["brand"]

    return None



# -----------------------------
# TEST (Run this file directly)
# -----------------------------
if __name__ == "__main__":

    query = "Tell me about Apple iphone"
    parsed = parse_query(query)

    print("\nParsed:")
    print(json.dumps(parsed, indent=2))

    phone = get_first_phone(parsed)

    if phone:
        print("\nSummary:\n")
        print(summarize_phone(phone))
    else:
        print("No phone detected.")
