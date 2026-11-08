#!/usr/bin/env python3
"""Build tool/data/asos-stations.js from Iowa Environmental Mesonet station lists.

Usage: python3 scripts/build_asos_stations.py <folder of <ST>_ASOS.geojson files> <download date>

The folder lives in the shared data store:
~/Hovecon/data/aam/weather/iem_asos_stations_<date>/
Each row is [id, name, lat, lon, first year of record, last year (null if still reporting)].
"""
import json, os, sys

src, date = sys.argv[1], sys.argv[2]
rows = []
for fn in sorted(os.listdir(src)):
    if not fn.endswith("_ASOS.geojson"):
        continue
    for f in json.load(open(os.path.join(src, fn))).get("features", []):
        p, g = f["properties"], f.get("geometry")
        if not g or not p.get("archive_begin"):
            continue
        lon, lat = g["coordinates"][:2]
        end = p.get("archive_end")
        rows.append([p["sid"], (p.get("sname") or "").strip(), round(lat, 4), round(lon, 4),
                     int(p["archive_begin"][:4]), int(end[:4]) if end else None])
out = os.path.join(os.path.dirname(__file__), "..", "tool", "data", "asos-stations.js")
with open(out, "w") as fh:
    fh.write("// ASOS/AWOS stations from the Iowa Environmental Mesonet, downloaded %s.\n" % date)
    fh.write("// [id, name, lat, lon, first year of record, last year or null if still reporting]\n")
    fh.write("window.ASOS_STATIONS = {date: %s, rows: %s};\n" % (json.dumps(date), json.dumps(rows, separators=(",", ":"))))
print(len(rows), "stations ->", out)
