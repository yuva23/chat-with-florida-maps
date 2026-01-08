import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INTENT_PROMPT = """
You are a GIS intent parser.

Return ONLY valid JSON in this format:
{
  "layers": ["rivers","counties"],
  "operation": "visualize",
  "location": "Florida"
}

Rules:
- layers can only be rivers, counties, waterbodies
- operation: visualize
- NO explanations
"""

def ask_ai(question):
    # Heuristic: map vs knowledge
    map_keywords = ["map", "show", "display", "visualize", "counties", "rivers"]

    if any(k in question.lower() for k in map_keywords):
        # MAP MODE
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": INTENT_PROMPT},
                {"role": "user", "content": question}
            ]
        )

        intent = json.loads(response.choices[0].message.content)
        return {"type": "map", "intent": intent}

    # KNOWLEDGE MODE
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": "You are a GIS expert. Answer clearly."},
            {"role": "user", "content": question}
        ]
    )

    return {
        "type": "text",
        "answer": response.choices[0].message.content
    }
