import requests
import json
import osm2geojson

# Define the Overpass API query
overpass_url = "http://overpass-api.de/api/interpreter"

for i in range(0, 31):
    overpass_query = f'''
    [out:json];
    area["ISO3166-2"="IR-{i:02d}"]->.province;
    rel["admin_level"="5"](area.province);
    out body;
    >;
    out skel qt;
    '''

    # Send the query to the Overpass API
    response = requests.get(overpass_url, params={'data': overpass_query})

    # Parse the response
    data = json.loads(response.text)

    # Convert the data to GeoJSON format
    geojson = osm2geojson.json2geojson(data)

    # Save the GeoJSON data to a file with UTF-8 encoding
    print(f'Downloading IR-{i:02d}')

    with open(f'IR-{i:02d}_geo.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(geojson, ensure_ascii=False, indent=2))
