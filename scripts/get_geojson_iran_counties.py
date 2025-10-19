#!/usr/bin/env python3

import requests
import json
import osm2geojson
from pathlib import Path


def download_county_data(province_code):
    """Download county data for a specific province."""
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
[out:json];
area["ISO3166-2"="{province_code}"]->.province;
rel["admin_level"="5"](area.province);
out body;
>;
out skel qt;
"""

    # Send the query to the Overpass API
    response = requests.get(overpass_url, params={"data": overpass_query})
    data = json.loads(response.text)
    geojson = osm2geojson.json2geojson(data)

    return geojson


def save_county_files(geojson_data, province_code, output_dir):
    """Save county data in different formats."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create different versions
    versions = {
        f"{province_code}.all.geojson": geojson_data,
        f"{province_code}.all.min.geojson": geojson_data,
    }

    for filename, data in versions.items():
        filepath = output_dir / filename

        if "min" in filename:
            # Minified version
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        else:
            # Formatted version
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Created: {filepath}")


def main():
    """Main function to download and process counties data."""

    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    base_output_dir = project_root / "data" / "counties"

    print("Downloading counties data from Overpass API...")

    for i in range(0, 31):
        province_code = f"IR-{i:02d}"
        output_dir = base_output_dir / province_code

        try:
            print(f"Downloading {province_code}...")

            # Download data
            geojson_data = download_county_data(province_code)

            # Process and save
            save_county_files(geojson_data, province_code, output_dir)

            print(f"Completed {province_code}")

        except Exception as e:
            print(f"Error processing {province_code}: {e}")

    print("\nAll counties processing completed!")


if __name__ == "__main__":
    main()
