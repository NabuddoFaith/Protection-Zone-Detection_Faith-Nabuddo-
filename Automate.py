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
# 3. CREATE PROTECTION POLYGON
# ============================================================

protection_wkt = data["protection_zone_wkt"]

protection_polygon = wkt.loads(protection_wkt)

print("Protection geometry:",
      protection_polygon.geom_type)


# ============================================================
# 4. CREATE POINTS
# ============================================================

point_records = []

for pt in data["detected_points"]:

    geometry = Point(
        pt["lon"],
        pt["lat"]
    )

    point_records.append({
        "POINT_ID": pt["point_id"],
        "LON": pt["lon"],
        "LAT": pt["lat"],
        "DESC": pt["description"],
        "geometry": geometry
    })


# ============================================================
# 5. CREATE GEODATAFRAME
# ============================================================

# Do NOT pass CRS here because your PROJ installation
# is currently failing when it tries to resolve EPSG:4326.

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
# 7. STATUS
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
# 8. DISPLAY RESULTS
# ============================================================

print("")
print("============================================================")
print("POINT-IN-POLYGON RESULTS")
print("============================================================")

for _, row in points_gdf.iterrows():

    print(
        f"{row['POINT_ID']} | "
        f"{row['LON']} | "
        f"{row['LAT']} | "
        f"{row['STATUS']} | "
        f"{row['DESC']}"
    )


# ============================================================
# 9. FLAGGED RECORDS ONLY
# ============================================================

flagged = points_gdf[
    points_gdf["INSIDE_ZONE"] == True
].copy()


print("")
print("============================================================")
print("FLAGGED RECORDS")
print("============================================================")

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


# ============================================================
# 10. SAVE CSV
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
# 11. SAVE FLAGGED GEOJSON
# ============================================================

geojson_output = os.path.join(
    output_folder,
    "flagged_detected_points.geojson"
)

# Export geometry without requiring CRS transformation
flagged.to_file(
    geojson_output,
    driver="GeoJSON"
)


# ============================================================
# 12. SUMMARY
# ============================================================

print("")
print("============================================================")
print("SUMMARY")
print("============================================================")

print(
    "Total points:",
    len(points_gdf)
)

print(
    "Flagged points:",
    len(flagged)
)

print(
    "Outside points:",
    len(points_gdf) - len(flagged)
)

print("")
print("CSV:")
print(csv_output)

print("")
print("GeoJSON:")
print(geojson_output)