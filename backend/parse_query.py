import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("backend/prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read()

def parse_user_query(user_query):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ],
        temperature=0
    )
    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    query = "Show flood-prone areas near rivers in Leon County"
    print(json.dumps(parse_user_query(query), indent=2))
