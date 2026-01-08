from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

LAYER_CATALOG = {
    "counties": {
        "type": "mapserver",
        "url": "https://ca.dep.state.fl.us/arcgis/rest/services/Boundaries/Florida_County_Boundaries/MapServer/0"
    },
    "rivers": {
        "type": "mapserver",
        "url": "https://ca.dep.state.fl.us/arcgis/rest/services/Hydrography/Florida_Rivers/MapServer/0"
    },
    "waterbodies": {
        "type": "mapserver",
        "url": "https://ca.dep.state.fl.us/arcgis/rest/services/Hydrography/Florida_Waterbodies/MapServer/0"
    }
}


LOCATION_ZOOMS = {
    "florida": { "center": [27.8, -81.7], "zoom": 7 },
    "orlando": { "center": [28.5383, -81.3792], "zoom": 10 },
    "miami": { "center": [25.7617, -80.1918], "zoom": 10 },
    "tampa": { "center": [27.9506, -82.4572], "zoom": 10 }
}


@app.route("/ask-gis", methods=["POST"])
def ask_gis():
    q = request.json.get("question")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": q}],
        temperature=0.2
    )

    return jsonify({
        "type": "text",
        "answer": response.choices[0].message.content
    })



@app.route("/map-command", methods=["POST"])
def map_command():
    q = request.json.get("question")

    system_prompt = """
You are a GIS intent parser.
Return ONLY valid JSON in this format:

{
  "layer": "counties | rivers | waterbodies",
  "location": "Florida | Orlando | Miami | Tampa"
}

Rules:
- Choose the best matching layer
- Choose the most relevant location
- No explanations
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": q}
        ],
        temperature=0
    )

    intent = json.loads(response.choices[0].message.content)

    layer_key = intent["layer"].lower()
    location_key = intent["location"].lower()

    return jsonify({
        "type": "map",
        "layer": LAYER_CATALOG[layer_key],
        "zoom": LOCATION_ZOOMS.get(location_key, LOCATION_ZOOMS["florida"]),
        "intent": intent
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
