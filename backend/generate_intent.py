from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a GIS intent parser.
Return ONLY valid JSON in this schema:

{
  "layers": ["rivers", "counties"],
  "operation": "visualize",
  "location": "Florida"
}

Rules:
- Allowed layers: rivers, counties
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
