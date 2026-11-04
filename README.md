# Vertiport

Review of FAA draft AC 150/5390-4, *Vertical Flight Aircraft Infrastructure Design* (posted 10/22/2026, comments due 1/11/2027 to vertiports@faa.gov), and a planning tool built from it.

## Contents

| Path | What it is |
|---|---|
| `source/faa_draft_ac_150-5390-4/` | Draft AC PDF, FAA industry letter, comment matrix (.xlsx), and a text extract of the AC. Downloaded 2026-11-04 from faa.gov. |
| `tool/vertiport-surfaces.html` | Vertiport Surface Planner. Open it in a browser (it needs internet for map tiles). Place a pad, set D, RD, MTOW and approach courses, view the surfaces in 2D or 3D, export KML for Google Earth or GeoJSON for GIS. |

## Running it

Open `tool/vertiport-surfaces.html` directly, or serve the folder so other machines on the network can use it:

```
python3 -m http.server 8080 --bind 0.0.0.0 --directory tool
```

The 3D view uses CesiumJS with Esri imagery and terrain. A free Cesium ion token (ion.cesium.com, pasted into the panel) adds Cesium World Terrain and OpenStreetMap 3D buildings. The token stays in the browser's local storage and is not saved in the repo.

## What the tool draws, and from which paragraph

- TLOF: 1 RD + 10 ft; +20% if elevated with a non-load-bearing FATO (4.2.1.4)
- FATO: larger of 1.5 D and TLOF + 0.34 D each side; extra length above 1,000 ft MSL from Figure 4-4 (4.3.1.4)
- Safety area: 0.28 D, min 20 ft, +10 ft without the standard H (4.4.1.4)
- Heliport protection zone: 280 ft under each approach surface (4.5.1)
- Downwash/outwash caution area: 780 x 420 ft per path, only for aircraft 7,000 lb and under (4.6.1)
- Approach/departure surface: FATO width to 500 ft at 4,000 ft; 8:1 max for helicopters, 15:1 or shallower for powered lift (4.7.1.1)
- Transitional surfaces: 2:1 out to 250 ft from centerline, along the FATO and the approach surface (4.7.1.1)

Not modeled yet: curved approaches, hospital lateral extensions, taxiways and taxi DCA, parking.

The Figure 4-4 curve was read off the chart (about +/- 5 ft); the AC's example (3,200 ft adds 80 ft) is on it. Helicopter presets come from Appendix E, Table E-1. The AC has no powered-lift data table.

Coordinates are WGS84 (EPSG:4326). Surface altitudes in exports are meters MSL: ground elevation + deck height + surface height.
