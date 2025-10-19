# Iran GeoJSON

GeoJSON boundaries of Iran map, downloaded from OpenStreetMap APIs (via <http://overpass-api.de>).

## About

This project provides GeoJSON files for Iran's administrative divisions, including provinces and counties. The data is sourced from OpenStreetMap and organized for easy use in mapping applications. The project includes both full data with all language names and cleaned versions with only Persian and English names.

**Original Source**: This project is based on the original work from [mokazemi/iran-geojson](https://codeberg.org/mokazemi/iran-geojson) on Codeberg.

## Project Structure

```text
iran-geojson/
├── data/
│   ├── provinces/
│   │   ├── provinces.all.geojson      # All 31 provinces (full data with cleaned names)
│   │   ├── provinces.all.min.geojson  # All 31 provinces (minified)
│   │   ├── provinces.geojson          # Short version (only name:fa and name:en)
│   │   └── provinces.min.geojson      # Short version (minified)
│   └── counties/
│       ├── IR-00/
│       │   ├── IR-00.all.geojson      # Markazī counties (full data)
│       │   └── IR-00.all.min.geojson  # Markazī counties (minified)
│       ├── IR-01/
│       │   ├── IR-01.all.geojson      # Gīlān counties (full data)
│       │   └── IR-01.all.min.geojson  # Gīlān counties (minified)
│       └── ...                       # Other provinces' counties
├── scripts/
│   ├── get_geojson_iran_provinces.py # Download and process provinces data
│   └── get_geojson_iran_counties.py  # Download and process counties data
├── requirements.txt                   # Python dependencies
├── README.md                         # This file
└── LICENSE                           # MIT License
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/iran-geojson.git
cd iran-geojson
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Downloading Data

To download the latest GeoJSON data from OpenStreetMap:

**Download and process provinces data:**

```bash
python scripts/get_geojson_iran_provinces.py
```

This will create 4 files:

- `provinces.all.geojson` - Full data with all original tags + cleaned name values
- `provinces.all.min.geojson` - Full data (minified)
- `provinces.geojson` - Short version (only name:fa and name:en in properties)
- `provinces.min.geojson` - Short version (minified)

**Download and process counties data:**

```bash
python scripts/get_geojson_iran_counties.py
```

This will create county files for each province (IR-00 to IR-30) with both full and minified versions.

### Name Cleaning Features

The scripts automatically clean and process names:

**Persian Names:**

- Removes "استان" prefix (e.g., "استان تهران" → "تهران")
- Removes extra spaces and common administrative terms

**English Names:**

- Removes "Province" suffix (e.g., "Tehran Province" → "Tehran")
- Removes extra spaces and common administrative terms

**Data Structure:**

- **`.all` versions**: Keep all original tags and properties, only clean the name values
- **Short versions**: Remove tags completely, keep only `name:fa` and `name:en` in properties
- **Metabase optimized**: `name:fa` and `name:en` are directly accessible in properties

### Using the Data

The GeoJSON files can be used in various mapping libraries and applications:

- **JavaScript**: Leaflet, Mapbox GL JS, OpenLayers
- **Python**: GeoPandas, Folium, Plotly
- **R**: leaflet, mapview
- **QGIS**: Direct import of GeoJSON files

### Using with Metabase

You can use these GeoJSON files as custom region maps in [Metabase](https://www.metabase.com/). This allows you to create interactive maps of Iran's provinces in your Metabase dashboards.

#### Setting up Custom Region Maps

1. **Access Map Settings**:
   - Go to **Admin Settings** > **Settings** > **Maps**
   - Click on **Custom Maps** tab

2. **Add Iran Map**:
   - Click **Add a Map**
   - **Name**: "Iran"
   - **URL**: Use the direct URL to `provinces.min.geojson` (copy the link from [here](https://raw.githubusercontent.com/hosseinhabibi2004/iran-geojson/refs/heads/master/data/provinces/provinces.min.geojson))
   - **Region's identifier**: `name:en` (English names) or `name:fa` (Persian names)
   - **Region's display name**: `name:en` (English names) or `name:fa` (Persian names)

#### Data Requirements for Metabase

- **File size**: Must be less than 5 MB (the provided file is optimized for this)
- **Accessibility**: Must be accessible via public URL
- **Format**: Must contain polygon features (not just points)
- **Coordinates**: Must use geographic coordinates (latitude/longitude)

#### Environment Variable Setup

To pre-load the maps when Metabase starts, you can use the environment variable:

```bash
MB_CUSTOM_GEOJSON='[
  {
    "name": "Iran",
    "url": "https://raw.githubusercontent.com/hosseinhabibi2004/iran-geojson/refs/heads/master/data/provinces/provinces.min.geojson",
    "region_key": "name:en",
    "region_name": "name:en"
  }
]'
```

#### Creating Maps in Metabase

Once configured, you can create region maps in Metabase by:

1. Creating a new question
2. Selecting your data source
3. Choosing **Visualization** > **Map** > **Region map**
4. Selecting "Iran" from the region dropdown
5. Mapping your data's region identifier column to the GeoJSON's name field (name:en or name:fa)

For more details, see the [Metabase Custom Maps documentation](https://www.metabase.com/docs/latest/configuring-metabase/custom-maps#custom-region-maps).

## Data Description

### File Types

- **`.all.geojson`** - Full data with all original tags + cleaned name values
- **`.all.min.geojson`** - Full data (minified for smaller file size)
- **`.geojson`** - Short version with only `name:fa` and `name:en` in properties
- **`.min.geojson`** - Short version (minified)

### Provinces (استان‌ها)

The provinces data contains boundaries of all 31 provinces of Iran in multiple formats:

- `provinces.all.geojson` - Full data with all original tags + cleaned name values
- `provinces.geojson` - Short version with only `name:fa` and `name:en` in properties

### Counties (شهرستان‌ها)

Individual county files are organized by province in `data/counties/IR-XX/` folders where XX is the ISO 3166-2 code. Each province folder contains:

- `IR-XX.all.geojson` - Full county data for that province
- `IR-XX.all.min.geojson` - Minified version

## ISO 3166-2:IR Province Codes

| Code  | Persian Name | English Name |
|-------|--------------|--------------|
| IR-00 | مرکزی        | Markazi      |
| IR-01 | گیلان         | Gilan        |
| IR-02 | مازندران     | Mazandaran   |
| IR-03 | آذربایجان شرقی | East Azerbaijan |
| IR-04 | آذربایجان غربی | West Azerbaijan |
| IR-05 | کرمانشاه     | Kermanshah   |
| IR-06 | خوزستان      | Khuzestan    |
| IR-07 | فارس         | Fars         |
| IR-08 | کرمان        | Kerman       |
| IR-09 | خراسان رضوی  | Razavi Khorasan |
| IR-10 | اصفهان       | Isfahan      |
| IR-11 | سیستان و بلوچستان    | Sistan and Baluchestan |
| IR-12 | کردستان      | Kurdistan    |
| IR-13 | همدان        | Hamadan      |
| IR-14 | چهارمحال و بختیاری | Chaharmahal and Bakhtiyari |
| IR-15 | لرستان       | Lorestan     |
| IR-16 | ایلام         | Ilam         |
| IR-17 | کهگیلویه و بویر احمد | Kohgiluye and Buyer Ahmad |
| IR-18 | بوشهر        | Bushehr      |
| IR-19 | زنجان        | Zanjan       |
| IR-20 | سمنان        | Semnan       |
| IR-21 | یزد          | Yazd         |
| IR-22 | هرمزگان      | Hormozgan    |
| IR-23 | تهران        | Tehran       |
| IR-24 | اردبیل       | Ardabil      |
| IR-25 | قم           | Qom  |
| IR-26 | قزوین        | Qazvin       |
| IR-27 | گلستان       | Golestan     |
| IR-28 | خراسان شمالی | North Khorasan |
| IR-29 | خراسان جنوبی | South Khorasan |
| IR-30 | البرز        | Alborz       |

## Data Source

- **OpenStreetMap**: [https://www.openstreetmap.org/](https://www.openstreetmap.org/)
- **Overpass API**: [http://overpass-api.de/](http://overpass-api.de/)
- **Original Project**: [https://codeberg.org/mokazemi/iran-geojson](https://codeberg.org/mokazemi/iran-geojson)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Original project by [mokazemi](https://codeberg.org/mokazemi) on Codeberg
- OpenStreetMap contributors for the geographic data
- Overpass API for providing the data access interface
