import json
import os

import geopandas as gpd
from shapely import wkt
from shapely.geometry import Point


# ============================================================
# 1. INPUT TXT FILE
# ============================================================

txt_file = r"D:\Tolo work\Personal\GIS JOB\Python\input.txt"

output_folder = os.path.dirname(txt_file)


# ============================================================
# 2. READ TXT JSON
# ============================================================

with open(txt_file, "r", encoding="utf-8") as f:
    data = json.load(f)


# ============================================================
# 3. READ PROTECTION ZONE
# ============================================================

protection_wkt = data["protection_zone_wkt"]

protection_crs = data.get(
    "protection_zone_crs",
    "EPSG:4326"
)

protection_polygon = wkt.loads(
    protection_wkt
)

print("")
print("============================================================")
print("PROTECTION ZONE")
print("============================================================")

print(
    "Protection CRS:",
    protection_crs
)

print(
    "Protection geometry:",
    protection_polygon.geom_type
)


# ============================================================
# 4. CREATE DETECTED POINTS
# ============================================================

point_records = []

for pt in data["detected_points"]:

    point_geometry = Point(
        pt["lon"],
        pt["lat"]
    )

    point_records.append({
        "POINT_ID": pt["point_id"],
        "LON": pt["lon"],
        "LAT": pt["lat"],
        "DESC": pt["description"],
        "geometry": point_geometry
    })


# ============================================================
# 5. CREATE GEODATAFRAME
# ============================================================

# CRS is intentionally not assigned here because the current
# PROJ installation has an EPSG database issue.
#
# Both the protection polygon and detected points are already
# provided in longitude/latitude coordinates (EPSG:4326).

points_gdf = gpd.GeoDataFrame(
    point_records,
    geometry="geometry"
)


# ============================================================
# 6. POINT-IN-POLYGON TEST
# ============================================================

points_gdf["INSIDE_ZONE"] = (
    points_gdf.geometry.within(
        protection_polygon
    )
)


# ============================================================
# 7. CREATE STATUS FIELD
# ============================================================

points_gdf["STATUS"] = points_gdf[
    "INSIDE_ZONE"
].apply(
    lambda x:
        "FLAGGED - INSIDE PROTECTION ZONE"
        if x
        else "OUTSIDE PROTECTION ZONE"
)


# ============================================================
# 8. DISPLAY ALL RESULTS
# ============================================================

print("")
print("============================================================")
print("POINT-IN-POLYGON RESULTS")
print("============================================================")

for _, row in points_gdf.iterrows():

    print(
        f"{row['POINT_ID']} | "
        f"Longitude: {row['LON']} | "
        f"Latitude: {row['LAT']} | "
        f"{row['STATUS']} | "
        f"{row['DESC']}"
    )


# ============================================================
# 9. SELECT FLAGGED RECORDS
# ============================================================

flagged = points_gdf[
    points_gdf["INSIDE_ZONE"] == True
].copy()


# ============================================================
# 10. DISPLAY FLAGGED RECORDS
# ============================================================

print("")
print("============================================================")
print("FLAGGED RECORDS")
print("============================================================")

if len(flagged) > 0:

    print(
        flagged[
            [
                "POINT_ID",
                "LON",
                "LAT",
                "DESC",
                "STATUS"
            ]
        ].to_string(index=False)
    )

else:

    print(
        "No detected points fall inside the protection zone."
    )


# ============================================================
# 11. SAVE FLAGGED POINTS AS CSV
# ============================================================

csv_output = os.path.join(
    output_folder,
    "flagged_detected_points.csv"
)

flagged.drop(
    columns="geometry"
).to_csv(
    csv_output,
    index=False
)


# ============================================================
# 12. SAVE FLAGGED POINTS AS GEOJSON
# ============================================================

geojson_output = os.path.join(
    output_folder,
    "flagged_detected_points.geojson"
)

# Export without CRS transformation because the coordinates
# are already longitude/latitude in EPSG:4326.

flagged.to_file(
    geojson_output,
    driver="GeoJSON"
)


# ============================================================
# 13. SAVE PROTECTION ZONE AS GEOJSON
# ============================================================

protection_geojson_output = os.path.join(
    output_folder,
    "protection_zone.geojson"
)

# Use Shapely's GeoJSON geometry representation directly.
# This avoids the current PROJ/EPSG database problem.

protection_feature = {
    "type": "Feature",
    "properties": {
        "ZONE_ID": "PROTECTION_ZONE",
        "CRS": protection_crs
    },
    "geometry": protection_polygon.__geo_interface__
}


# Create FeatureCollection

protection_geojson = {
    "type": "FeatureCollection",
    "features": [
        protection_feature
    ]
}


# Write protection-zone GeoJSON

with open(
    protection_geojson_output,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        protection_geojson,
        f,
        indent=4
    )


# ============================================================
# 14. SUMMARY
# ============================================================

total_points = len(points_gdf)

flagged_points = len(flagged)

outside_points = (
    total_points - flagged_points
)


print("")
print("============================================================")
print("SUMMARY")
print("============================================================")

print(
    "Total detected points:",
    total_points
)

print(
    "Flagged points inside protection zone:",
    flagged_points
)

print(
    "Points outside protection zone:",
    outside_points
)


# ============================================================
# 15. OUTPUT FILES
# ============================================================

print("")
print("============================================================")
print("OUTPUT FILES")
print("============================================================")

print("")
print("1. Flagged Points CSV:")
print(csv_output)

print("")
print("2. Flagged Points GeoJSON:")
print(geojson_output)

print("")
print("3. Protection Zone GeoJSON:")
print(protection_geojson_output)


# ============================================================
# 16. EXPECTED RESULT FOR THE SAMPLE DATA
# ============================================================

print("")
print("============================================================")
print("EXPECTED SAMPLE RESULT")
print("============================================================")

print(
    "LOC_001 -> INSIDE PROTECTION ZONE"
)

print(
    "LOC_002 -> OUTSIDE PROTECTION ZONE"
)

print(
    "LOC_003 -> INSIDE PROTECTION ZONE"
)

print(
    "LOC_004 -> OUTSIDE PROTECTION ZONE"
)

print(
    "LOC_005 -> INSIDE PROTECTION ZONE"
)

print("")
print("Processing completed successfully.")
