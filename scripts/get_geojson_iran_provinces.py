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


def create_short_name(name):
    """Create a short version by removing common words and extra spaces."""
    if not name:
        return name

    # Remove common Persian words that might be redundant
    persian_common_words = ["استان", "شهرستان", "بخش", "دهستان", "روستا", "شهر"]

    # Remove common English words
    english_common_words = ["province", "state", "county", "district", "region", "area"]

    cleaned = name.strip()

    # Remove Persian common words
    for word in persian_common_words:
        cleaned = re.sub(rf"\b{re.escape(word)}\b\s*", "", cleaned, flags=re.IGNORECASE)

    # Remove English common words
    for word in english_common_words:
        cleaned = re.sub(rf"\b{re.escape(word)}\b\s*", "", cleaned, flags=re.IGNORECASE)

    # Remove extra spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def process_provinces_data(geojson_data):
    """Process the provinces GeoJSON data and create cleaned versions."""

    # Process each feature to clean the names
    cleaned_features = []
    short_features = []

    for feature in geojson_data.get("features", []):
        properties = feature.get("properties", {})
        tags = properties.get("tags", {})

        # Create cleaned tags with only Persian and English names
        cleaned_tags = {}
        short_tags = {}

        # Keep essential properties
        for key in [
            "ISO3166-2",
            "admin_level",
            "boundary",
            "is_in:country",
            "is_in:country_code",
        ]:
            if key in tags:
                cleaned_tags[key] = tags[key]
                short_tags[key] = tags[key]

        # Clean and add Persian name
        persian_name = tags.get("name:fa") or tags.get("name", "")
        if persian_name:
            clean_persian = clean_persian_name(persian_name)
            if clean_persian:
                cleaned_tags["name"] = clean_persian
                cleaned_tags["name:fa"] = clean_persian
                short_tags["name"] = create_short_name(clean_persian)
                short_tags["name:fa"] = create_short_name(clean_persian)

        # Clean and add English name
        english_name = tags.get("name:en", "")
        if english_name:
            clean_english = clean_english_name(english_name)
            if clean_english:
                cleaned_tags["name:en"] = clean_english
                short_tags["name:en"] = create_short_name(clean_english)

        # Create cleaned feature
        cleaned_feature = {
            "type": feature.get("type"),
            "properties": {
                "type": properties.get("type"),
                "id": properties.get("id"),
                "tags": cleaned_tags,
            },
            "geometry": feature.get("geometry"),
        }

        # Create short feature
        short_feature = {
            "type": feature.get("type"),
            "properties": {
                "type": properties.get("type"),
                "id": properties.get("id"),
                "tags": short_tags,
            },
            "geometry": feature.get("geometry"),
        }

        # Only add if we have at least one cleaned name
        if cleaned_tags.get("name") or cleaned_tags.get("name:en"):
            cleaned_features.append(cleaned_feature)
            short_features.append(short_feature)

    return cleaned_features, short_features


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


def save_geojson_files(geojson_data, output_dir):
    """Save GeoJSON data in different formats."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process the data
    cleaned_features, short_features = process_provinces_data(geojson_data)

    # Create different versions
    versions = {
        "provinces.all.geojson": {
            "type": "FeatureCollection",
            "features": geojson_data.get("features", []),
        },
        "provinces.all.min.geojson": {
            "type": "FeatureCollection",
            "features": geojson_data.get("features", []),
        },
        "provinces.short.geojson": {
            "type": "FeatureCollection",
            "features": cleaned_features,
        },
        "provinces.short.min.geojson": {
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

    print(f"\nProcessed {len(cleaned_features)} provinces")
    return cleaned_features


def main():
    """Main function to download and process provinces data."""

    # Define paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_dir = project_root / "data" / "provinces"

    try:
        # Download data
        geojson_data = download_provinces_data()

        # Process and save
        features = save_geojson_files(geojson_data, output_dir)

        # Print sample of processed data
        print("\nSample processed provinces:")
        for i, feature in enumerate(features[:3]):
            tags = feature.get("properties", {}).get("tags", {})
            iso_code = tags.get("ISO3166-2", "N/A")
            persian_name = tags.get("name", "")
            english_name = tags.get("name:en", "")

            print(f"\n{i + 1}. {iso_code}")
            print(f"   Persian: {persian_name}")
            print(f"   English: {english_name}")

    except Exception as e:
        print(f"Error processing data: {e}")


if __name__ == "__main__":
    main()
