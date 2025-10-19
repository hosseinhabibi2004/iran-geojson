# Iran GeoJSON

GeoJSON boundaries of Iran map, downloaded from OpenStreetMap APIs (via <http://overpass-api.de>).

## About

This project provides GeoJSON files for Iran's administrative divisions, including provinces and counties. The data is sourced from OpenStreetMap and organized for easy use in mapping applications.

**Original Source**: This project is based on the original work from [mokazemi/iran-geojson](https://codeberg.org/mokazemi/iran-geojson) on Codeberg.

## Project Structure

```
iran-geojson/
├── data/
│   ├── provinces/
│   │   └── iran_provinces_geo.json    # All 31 provinces of Iran
│   └── counties/
│       ├── IR-00_geo.json            # Markazī counties
│       ├── IR-01_geo.json            # Gīlān counties
│       └── ...                       # Other provinces' counties
├── scripts/
│   ├── get_geojson_iran_provinces.py # Download provinces data
│   └── get_geojson_iran_counties.py  # Download counties data
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

**Download provinces data:**

```bash
python scripts/get_geojson_iran_provinces.py
```

**Download counties data:**

```bash
python scripts/get_geojson_iran_counties.py
```

### Using the Data

The GeoJSON files can be used in various mapping libraries and applications:

- **JavaScript**: Leaflet, Mapbox GL JS, OpenLayers
- **Python**: GeoPandas, Folium, Plotly
- **R**: leaflet, mapview
- **QGIS**: Direct import of GeoJSON files

## Data Description

### Provinces (استان‌ها)

The `iran_provinces_geo.json` file contains boundaries of all 31 provinces of Iran.

### Counties (شهرستان‌ها)

Individual county files are stored in `data/counties/` with naming convention `IR-XX_geo.json` where XX is the ISO 3166-2 code of the province.

## ISO 3166-2:IR Province Codes

| Code  | Subdivision name (fa)      | English Name |
|-------|----------------------------|--------------|
| IR-00 | Markazī                    | Markazi      |
| IR-01 | Gīlān                      | Gilan        |
| IR-02 | Māzandarān                 | Mazandaran   |
| IR-03 | Āz̄ārbāyjān-e Shārqī        | East Azerbaijan |
| IR-04 | Āz̄ārbāyjān-e Ghārbī        | West Azerbaijan |
| IR-05 | Kermānshāh                 | Kermanshah   |
| IR-06 | Khūzestān                  | Khuzestan    |
| IR-07 | Fārs                       | Fars         |
| IR-08 | Kermān                     | Kerman       |
| IR-09 | Khorāsān-e Raẕavī          | Razavi Khorasan |
| IR-10 | Eşfahān                    | Isfahan      |
| IR-11 | Sīstān va Balūchestān      | Sistan and Baluchestan |
| IR-12 | Kordestān                  | Kurdistan    |
| IR-13 | Hamadān                    | Hamadan      |
| IR-14 | Chahār Maḩāl va Bakhtīārī  | Chaharmahal and Bakhtiari |
| IR-15 | Lorestān                   | Lorestan     |
| IR-16 | Īlām                       | Ilam         |
| IR-17 | Kohgīlūyeh va Bowyer Aḩmad | Kohgiluyeh and Boyer-Ahmad |
| IR-18 | Būshehr                    | Bushehr      |
| IR-19 | Zanjān                     | Zanjan       |
| IR-20 | Semnān                     | Semnan       |
| IR-21 | Yazd                       | Yazd         |
| IR-22 | Hormozgān                  | Hormozgan    |
| IR-23 | Tehrān                     | Tehran       |
| IR-24 | Ardabīl                    | Ardabil      |
| IR-25 | Qom                        | Qom          |
| IR-26 | Qazvīn                     | Qazvin       |
| IR-27 | Golestān                   | Golestan     |
| IR-28 | Khorāsān-e Shomālī         | North Khorasan |
| IR-29 | Khorāsān-e Jonūbī          | South Khorasan |
| IR-30 | Alborz                     | Alborz       |

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
