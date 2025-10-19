#!/usr/bin/env python3

import requests
import json
import osm2geojson
import re
from pathlib import Path


def clean_persian_name(name):
    """Remove 'استان' prefix and extra spaces from Persian names."""
    if not name:
        return name

    # Remove 'استان' prefix
    cleaned = re.sub(r"^استان\s*", "", name.strip())

    # Remove extra spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Specific corrections
    if cleaned == "کهگیلویه و بویر احمد":
        cleaned = "کهگیلویه و بویراحمد"

    return cleaned


def clean_english_name(name):
    """Remove 'Province' suffix and extra spaces from English names."""
    if not name:
        return name

    # Remove 'Province' suffix (case insensitive)
    cleaned = re.sub(r"\s*province\s*$", "", name.strip(), flags=re.IGNORECASE)

    # Remove extra spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def process_provinces_data(geojson_data):
    """Process the provinces GeoJSON data and create cleaned versions."""

    # Process each feature to clean the names
    all_features = []
    short_features = []

    for feature in geojson_data.get("features", []):
        properties = feature.get("properties", {})
        tags = properties.get("tags", {})

        # Clean names
        persian_name = tags.get("name:fa") or tags.get("name", "")
        clean_persian = clean_persian_name(persian_name)

        english_name = tags.get("name:en", "")
        clean_english = clean_english_name(english_name)

        # Create all feature (original structure + cleaned name values)
        all_properties = properties.copy()
        all_tags = tags.copy()
        if clean_persian:
            all_tags["name:fa"] = clean_persian
        if clean_english:
            all_tags["name:en"] = clean_english
        all_properties["tags"] = all_tags

        all_feature = {
            "type": feature.get("type"),
            "properties": all_properties,
            "geometry": feature.get("geometry"),
        }

        # Create short properties (only name:fa and name:en)
        short_properties = {}
        if clean_persian:
            short_properties["name:fa"] = clean_persian
        if clean_english:
            short_properties["name:en"] = clean_english

        # Create short feature (no tags, no id, only names)
        short_feature = {
            "type": feature.get("type"),
            "properties": short_properties,
            "geometry": feature.get("geometry"),
        }

        # Only add if we have at least one cleaned name
        if clean_persian or clean_english:
            all_features.append(all_feature)
            short_features.append(short_feature)

    return all_features, short_features


def download_provinces_data():
    """Download provinces data from Overpass API."""
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

    print("Downloading provinces data from Overpass API...")
    response = requests.get(overpass_url, params={"data": overpass_query})
    data = json.loads(response.text)
    geojson = osm2geojson.json2geojson(data)

    return geojson


def save_geojson_files(all_features, short_features, output_dir):
    """Save GeoJSON data in different formats."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create different versions
    versions = {
        "provinces.all.geojson": {
            "type": "FeatureCollection",
            "features": all_features,
        },
        "provinces.all.min.geojson": {
            "type": "FeatureCollection",
            "features": all_features,
        },
        "provinces.geojson": {
            "type": "FeatureCollection",
            "features": short_features,
        },
        "provinces.min.geojson": {
            "type": "FeatureCollection",
            "features": short_features,
        },
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

    print(f"\nProcessed {len(all_features)} provinces")


def main():
    """Main function to download and process provinces data."""

    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_dir = project_root / "data" / "provinces"

    try:
        # Download data
        geojson_data = download_provinces_data()

        # Process data
        all_features, short_features = process_provinces_data(geojson_data)

        # Save files
        save_geojson_files(all_features, short_features, output_dir)

        # Print sample of processed data
        print("\nSample processed provinces:")
        for i, feature in enumerate(all_features[:3]):
            properties = feature.get("properties", {})
            tags = properties.get("tags", {})
            iso_code = tags.get("ISO3166-2", "N/A")
            persian_name = tags.get("name:fa", "")
            english_name = tags.get("name:en", "")

            print(f"\n{i + 1}. {iso_code}")
            print(f"   Persian: {persian_name}")
            print(f"   English: {english_name}")

    except Exception as e:
        print(f"Error processing data: {e}")


if __name__ == "__main__":
    main()
