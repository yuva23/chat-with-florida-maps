import geopandas as gpd
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


counties = gpd.read_file(DATA_DIR / "counties.geojson")
rivers = gpd.read_file(DATA_DIR / "rivers.geojson")

# Ensure CRS is projected (meters)
if counties.crs.is_geographic:
    counties = counties.to_crs(epsg=3857)

if rivers.crs.is_geographic:
    rivers = rivers.to_crs(epsg=3857)


print("Buffering rivers (1000 meters)...")
rivers_buffer = rivers.buffer(1000)

rivers_buffer_gdf = gpd.GeoDataFrame(
    geometry=rivers_buffer,
    crs=rivers.crs
)

print("Intersecting buffered rivers with counties...")
affected_counties = gpd.overlay(
    counties,
    rivers_buffer_gdf,
    how="intersection"
)


output_file = OUTPUT_DIR / "counties_near_rivers.geojson"
affected_counties.to_file(output_file, driver="GeoJSON")

print(f"✅ Spatial analysis complete.")
print(f"Saved → {output_file}")
