"""Build tool/data/facilities.js from an FAA NASR 28-day subscription CSV zip.

    python3 scripts/build_facilities.py <DD_Mon_YYYY_CSV.zip> <cycle date, e.g. 2026-10-29>

The zip comes from https://www.faa.gov/air_traffic/flight_info/aeronav/aero_data/NASR_Subscription/
Reads APT_BASE.csv and keeps operational facilities of every type: airports, heliports, seaplane
bases, gliderports, ultralight parks and balloonports. Writes a script that sets window.FACILITIES.
Also reads APT_RWY.csv and APT_RWY_END.csv for open public-use airports and writes
tool/data/runways.js (window.RUNWAYS), the input for the 14 CFR Part 77 imaginary surfaces.
"""
import csv, io, json, sys, zipfile
from pathlib import Path

src, cycle = sys.argv[1], sys.argv[2]
out = Path(__file__).resolve().parent.parent / "tool" / "data" / "facilities.js"
def read(z, suffix):
    name = next(n for n in z.namelist() if n.endswith(suffix))
    return list(csv.DictReader(io.TextIOWrapper(z.open(name), encoding="latin-1")))

with zipfile.ZipFile(src) as z:
    rows, rwys, ends = read(z, "APT_BASE.csv"), read(z, "APT_RWY.csv"), read(z, "APT_RWY_END.csv")
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

# Runways for Part 77: open, public-use airports (site type A), both ends with coordinates.
PAVED = ("ASPH", "CONC", "PEM", "BRICK", "TRTD")
base = {r["SITE_NO"]: r for r in rows if r["ARPT_STATUS"] == "O" and r["SITE_TYPE_CODE"] == "A" and r["FACILITY_USE_CODE"] == "PU"}
end_by = {}
for e in ends:
    end_by.setdefault((e["SITE_NO"], e["RWY_ID"]), []).append(e)
airports = {}
for r in rwys:
    a = base.get(r["SITE_NO"])
    es = end_by.get((r["SITE_NO"], r["RWY_ID"]), [])
    if not a or len(es) != 2 or not all(e["LAT_DECIMAL"] and e["LONG_DECIMAL"] for e in es):
        continue
    def end(e):
        return [e["RWY_END_ID"], round(float(e["LAT_DECIMAL"]), 6), round(float(e["LONG_DECIMAL"]), 6),
                round(float(e["RWY_END_ELEV"] or a["ELEV"] or 0), 1), e["FAR_PART_77_CODE"]]
    paved = 1 if any(t in r["SURFACE_TYPE_CODE"] for t in PAVED) else 0
    ap = airports.setdefault(r["SITE_NO"], [a["ARPT_ID"], a["ARPT_NAME"].strip(), round(float(a["LAT_DECIMAL"]), 5),
                                            round(float(a["LONG_DECIMAL"]), 5), round(float(a["ELEV"] or 0), 1), []])
    ap[5].append([r["RWY_ID"], paved] + [end(e) for e in es])
rw_out = out.parent / "runways.js"
payload = {"cycle": cycle, "source": "FAA NASR 28-day subscription, APT_BASE, APT_RWY and APT_RWY_END",
           "fields": ["id", "name", "lat", "lon", "elev", "runways: [id, paved, [end, lat, lon, elev, part77 code] x2]"],
           "airports": list(airports.values())}
rw_out.write_text("window.RUNWAYS=" + json.dumps(payload, separators=(",", ":")) + ";\n")
print(f"{len(airports)} public-use airports with runways, {rw_out.stat().st_size / 1e6:.1f} MB -> {rw_out}")
