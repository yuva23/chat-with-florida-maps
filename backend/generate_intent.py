import os
import json
from openai import OpenAI

# -----------------------------
# OpenAI client
# -----------------------------
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# -----------------------------
# System prompt (VERY IMPORTANT)
# -----------------------------
SYSTEM_PROMPT = """
You are a GIS intent parser.

Convert a user question into a strict JSON object with this schema ONLY:

{
  "layers": ["rivers", "waterbodies", "counties"],
  "operation": "visualize | buffer_intersection",
  "location": "Florida or county name"
}

Rules:
- Use only layer names from: rivers, waterbodies, counties
- Return ONLY valid JSON
- No explanations
"""

def generate_intent(user_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)

if __name__ == "__main__":
    user_query = input("Ask a GIS question: ")

    intent = generate_intent(user_query)

    with open("backend/intent.json", "w") as f:
        json.dump(intent, f, indent=2)

    print("\n✅ intent.json generated:")
    print(json.dumps(intent, indent=2))
