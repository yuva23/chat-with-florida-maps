import json
import subprocess
from pathlib import Path


INTENT_FILE = "backend/intent.json"
LAYER_CATALOG = "backend/layer_catalog.json"

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def load_intent():
    with open(INTENT_FILE, "r") as f:
        return json.load(f)

def load_catalog():
    with open(LAYER_CATALOG, "r") as f:
        return json.load(f)

def fetch_layer(layer_key):
    print(f"→ Fetching layer: {layer_key}")
    subprocess.run(
        ["python", "backend/fetch_mapdirect.py"],
        check=True
    )

if __name__ == "__main__":
    intent = load_intent()
    catalog = load_catalog()

    requested_layers = intent.get("layers", [])

    print("\nAI requested layers:")
    for lyr in requested_layers:
        print(f" - {lyr}")

    for layer_key in requested_layers:
        if layer_key in catalog:
            fetch_layer(layer_key)
        else:
            print(f"⚠️ Layer '{layer_key}' not found in catalog")

    print("\n✅ Dynamic GIS fetch complete.")
