import requests
import json
import os

# -----------------------------
# Output folder
# -----------------------------
OUTPUT_DIR = "data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# VERIFIED MapDirect layers
# -----------------------------
MAPDIRECT_LAYERS = {
    "counties": {
        "url": "https://ca.dep.state.fl.us/arcgis/rest/services/Map_Direct/Boundaries/MapServer/1"
    },
    "rivers": {
        "url": "https://ca.dep.state.fl.us/arcgis/rest/services/Map_Direct/Environment/MapServer/33"
    },
    "waterbodies": {
        "url": "https://ca.dep.state.fl.us/arcgis/rest/services/Map_Direct/Environment/MapServer/35"
    }
}

def fetch_layer(layer_name, layer_url):
    print(f"\nFetching {layer_name}...")

    params = {
        "where": "1=1",
        "outFields": "*",
        "f": "geojson"
    }

    query_url = f"{layer_url}/query"

    response = requests.get(query_url, params=params)
    response.raise_for_status()

    geojson = response.json()

    output_path = os.path.join(OUTPUT_DIR, f"{layer_name}.geojson")
    with open(output_path, "w") as f:
        json.dump(geojson, f)

    print(f"Saved → {output_path}")

if __name__ == "__main__":
    for name, cfg in MAPDIRECT_LAYERS.items():
        fetch_layer(name, cfg["url"])

    print("\n✅ All MapDirect layers fetched successfully.")
