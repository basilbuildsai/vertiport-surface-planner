"""Build tool/data/facilities.js from an FAA NASR 28-day subscription CSV zip.

    python3 scripts/build_facilities.py <DD_Mon_YYYY_CSV.zip> <cycle date, e.g. 2026-10-29>

The zip comes from https://www.faa.gov/air_traffic/flight_info/aeronav/aero_data/NASR_Subscription/
Reads APT_BASE.csv and keeps operational facilities of every type: airports, heliports, seaplane
bases, gliderports, ultralight parks and balloonports. Writes a script that sets window.FACILITIES.
"""
import csv, io, json, sys, zipfile
from pathlib import Path

src, cycle = sys.argv[1], sys.argv[2]
out = Path(__file__).resolve().parent.parent / "tool" / "data" / "facilities.js"
with zipfile.ZipFile(src) as z:
    name = next(n for n in z.namelist() if n.endswith("APT_BASE.csv"))
    rows = list(csv.DictReader(io.TextIOWrapper(z.open(name), encoding="latin-1")))
keep = []
for r in rows:
    if r["ARPT_STATUS"] != "O":
        continue
    keep.append([r["ARPT_ID"], r["ARPT_NAME"].strip(), r["CITY"].strip(), r["STATE_CODE"],
                 round(float(r["LAT_DECIMAL"]), 5), round(float(r["LONG_DECIMAL"]), 5),
                 round(float(r["ELEV"] or 0)), r["SITE_TYPE_CODE"], r["FACILITY_USE_CODE"],
                 1 if r["TWR_TYPE_CODE"].startswith("ATCT") else 0])
payload = {"cycle": cycle, "source": "FAA NASR 28-day subscription, APT_BASE.csv",
           "fields": ["id", "name", "city", "state", "lat", "lon", "elev", "type", "use", "tower"], "rows": keep}
out.write_text("window.FACILITIES=" + json.dumps(payload, separators=(",", ":")) + ";\n")
print(f"{len(keep)} facilities, {out.stat().st_size / 1e6:.1f} MB -> {out}")
