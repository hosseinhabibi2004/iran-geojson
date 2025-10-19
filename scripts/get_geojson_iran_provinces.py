import requests
import json
import osm2geojson

# Define the Overpass API query
overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:json];
(
 relation["ISO3166-2"~"^IR-"]["admin_level"="4"];
 way["ISO3166-2"~"^IR-"]["admin_level"="4"];
 node["ISO3166-2"~"^IR-"]["admin_level"="4"];
);
out geom;
"""

# Send the query to the Overpass API
response = requests.get(overpass_url, params={"data": overpass_query})

# Parse the response
data = json.loads(response.text)

# Convert the data to GeoJSON format
geojson = osm2geojson.json2geojson(data)

# Save the GeoJSON data to a file with UTF-8 encoding
with open("../data/provinces/iran_provinces_geo.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(geojson, ensure_ascii=False, indent=2))
