# Protection Zone Detection

This project checks whether detected geographic points fall inside a protected polygon and exports only the flagged records.

## Overview

The script reads a JSON payload from `input.txt`, builds a polygon from a WKT string, tests each detected point against that polygon, and then writes the flagged results to:

- `flagged_detected_points.csv`
- `flagged_detected_points.geojson`

It is designed for GIS monitoring workflows such as identifying construction or activity points inside a restricted or protected zone.

## Project Files

- `Automate.py` – main processing script
- `input.txt` – input data in JSON format
- `flagged_detected_points.csv` – flagged points exported as CSV
- `flagged_detected_points.geojson` – flagged points exported as GeoJSON

## Requirements

Install the required Python packages:

```bash
pip install geopandas shapely
```

If needed, also install supporting geospatial dependencies for your environment, especially if `geopandas` requires `fiona`, `pyogrio`, or `pyproj` based on your operating system.

## Input Data Format

The script expects a JSON structure similar to this in `input.txt`:

```json
{
  "protection_zone_wkt": "POLYGON ((32.5800 0.3200, 32.6000 0.3200, 32.6000 0.3400, 32.5800 0.3400, 32.5800 0.3200))",
  "protection_zone_crs": "EPSG:4326",
  "detected_points": [
    {
      "point_id": "LOC_001",
      "lon": 32.5900,
      "lat": 0.3300,
      "description": "Foundation excavation observed"
    }
  ]
}
```

### Field descriptions

- `protection_zone_wkt`: boundary of the protected area in Well-Known Text format
- `protection_zone_crs`: optional CRS metadata
- `detected_points`: list of point observations
  - `point_id`: unique identifier
  - `lon`: longitude
  - `lat`: latitude
  - `description`: textual description of the observation

## How the Script Works

1. Reads the JSON from `input.txt`
2. Parses the protection polygon using WKT
3. Converts each detected point into a Shapely `Point`
4. Performs a point-in-polygon test
5. Classifies each point as:
   - `FLAGGED - INSIDE PROTECTION ZONE`
   - `OUTSIDE PROTECTION ZONE`
6. Exports only the flagged points to CSV and GeoJSON

## Run the Script

From the project folder, run:

```bash
python Automate.py
```

The script prints:

- protection geometry type
- point-by-point results
- flagged records
- summary counts
- output file paths

## Output Example

The CSV output contains records such as:

```csv
POINT_ID,LON,LAT,DESC,STATUS
LOC_001,32.59,0.33,Foundation excavation observed,FLAGGED - INSIDE PROTECTION ZONE
```

The GeoJSON output contains the same flagged points as spatial features.

## Notes

- The project uses longitude/latitude values, consistent with WGS84-style coordinates.
- The script intentionally avoids assigning a CRS during GeoDataFrame creation because the local PROJ setup in this environment was failing on `EPSG:4326` resolution.
- The output geometry is still exported successfully as GeoJSON without explicit CRS assignment.

## Typical Use Case

This workflow is useful for:

- land protection monitoring
- infrastructure restriction checks
- site surveillance around restricted zones
- alert generation for points that enter protected boundaries

## License

This project is provided as-is for internal or project-specific GIS processing tasks.
