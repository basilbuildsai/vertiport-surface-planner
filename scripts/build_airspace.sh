#!/bin/zsh
# Build tool/data/airspace-bcd.js from an FAA NASR 28-day subscription cycle.
#
#   scripts/build_airspace.sh <class_airspace_shape_files.zip> <cycle date, e.g. 2026-10-29>
#
# The zip comes from https://www.faa.gov/air_traffic/flight_info/aeronav/aero_data/NASR_Subscription/
# (Additional Data, Class Airspace shapefile). Keeps Class B, C and D, drops Z, simplifies to about
# 10 m and writes a script that sets window.AIRSPACE, so the planner works offline and from file://.
# Needs GDAL; on Basil's Mac it comes through ~/Files/Work/GIS/scripts/qgis.sh.
set -e
zip=${1:?zip}; cycle=${2:?cycle date}
OGR=${OGR2OGR:-"$HOME/Files/Work/GIS/scripts/qgis.sh ogr2ogr"}
here=${0:A:h}/..; tmp=$(mktemp -d)
unzip -q "$zip" -d "$tmp"
shp=$(find "$tmp" -name 'Class_Airspace.shp' | head -1)
${=OGR} -f GeoJSON "$tmp/bcd.geojson" "$shp" -dim XY -t_srs EPSG:4326 \
  -where "CLASS IN ('B','C','D')" -simplify 0.0001 \
  -select IDENT,NAME,CLASS,LOWER_VAL,LOWER_CODE,UPPER_VAL,UPPER_CODE \
  -lco COORDINATE_PRECISION=5 -lco RFC7946=YES
{ print -n "window.AIRSPACE={cycle:\"$cycle\",source:\"FAA NASR 28-day subscription, Class Airspace shapefile\",data:"
  python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));d.pop("name",None);d.pop("crs",None);print(json.dumps(d,separators=(",",":")),end="")' "$tmp/bcd.geojson"
  print "};"; } > "$here/tool/data/airspace-bcd.js"
rm -rf "$tmp"
ls -lh "$here/tool/data/airspace-bcd.js"
