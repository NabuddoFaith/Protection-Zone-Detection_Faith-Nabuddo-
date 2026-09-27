Protection Zone Detection
This project checks whether detected points fall inside a protected polygon and exports the flagged results as GIS-friendly outputs.

Overview
The script reads a JSON payload from input.txt, parses the protection polygon from WKT, evaluates each detected point using a point-in-polygon test, and then exports:

flagged records as CSV
flagged records as GeoJSON
the protection polygon as GeoJSON
The workflow is designed for monitoring activities inside a restricted or protected area, such as construction, encroachment, or site activity checks.

Project Files
Automate.py – main processing script
input.txt – input data in JSON format
flagged_detected_points.csv – flagged point records exported to CSV
flagged_detected_points.geojson – flagged points exported as GeoJSON
protection_zone.geojson – protection polygon exported as GeoJSON
Requirements
Install the required Python packages:

pip install geopandas shapely

Depending on your system, you may also need supporting geospatial dependencies such as fiona, pyogrio, or pyproj.

Input Data Format
The script expects a JSON structure like this in input.txt:

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

Field descriptions
protection_zone_wkt: boundary of the protected area in Well-Known Text format
protection_zone_crs: optional CRS metadata, default is EPSG:4326
detected_points: list of spatial observations
point_id: unique identifier for each point
lon: longitude
lat: latitude
description: descriptive note about the observation
How the Script Works
Reads the JSON from input.txt
Loads the protection polygon from WKT
Reads the configured CRS value, defaulting to EPSG:4326
Converts each detected point into a Shapely Point
Performs a point-in-polygon check
Marks each point as either:
FLAGGED - INSIDE PROTECTION ZONE
OUTSIDE PROTECTION ZONE
Displays all results and flagged records in the terminal
Exports the flagged points to CSV and GeoJSON
Exports the protection polygon to GeoJSON
Run the Script
From the project folder, run:

python Automate.py

The script prints:

protection zone details
CRS information
point-by-point results
flagged records
a message when no points fall inside the zone
output file paths
Output Files
CSV output
Example:

POINT_ID,LON,LAT,DESC,STATUS
LOC_001,32.59,0.33,Foundation excavation observed,FLAGGED - INSIDE PROTECTION ZONE

GeoJSON output
The script creates:

flagged_detected_points.geojson for the flagged points
protection_zone.geojson for the protected polygon boundary
Notes
The project uses longitude/latitude coordinates, which are appropriate for EPSG:4326-style geographic data.
CRS is not assigned to the GeoDataFrame because the current local PROJ installation has an EPSG database issue; the script still performs the spatial check correctly using the provided coordinates.
The protection polygon is exported as a standalone GeoJSON feature collection to preserve the spatial boundary even when CRS assignment is limited in the environment.
Typical Use Cases
This workflow is useful for:

protected-area monitoring
site encroachment detection
infrastructure restriction checks
alerting when activities enter a restricted zone
License
This project is provided as-is for project-specific GIS processing and monitoring tasks.
