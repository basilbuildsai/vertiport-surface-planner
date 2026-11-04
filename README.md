# Vertiport Surface Planner

A browser tool that lays out vertiport and heliport surfaces from the FAA's draft Advisory Circular 150/5390-4, *Vertical Flight Aircraft Infrastructure Design*. Place a pad on a map, enter the design aircraft and approach courses, and the planner draws the TLOF, FATO, safety area, protection zones, downwash caution area, and the approach and transitional surfaces. View them in 2D or 3D, then export to Google Earth (KML) or GIS (GeoJSON).

Free for noncommercial use. Commercial use needs a license; see [License](#license).

The draft AC was posted October 22, 2026. The FAA takes comments until January 11, 2027 at vertiports@faa.gov. The planner follows the draft and will need updating when the final AC is published.

## Running it

Open `tool/vertiport-surfaces.html` in a browser. It needs an internet connection for map tiles, elevation lookups and the 3D engine.

To share it with other machines on your network:

```
python3 -m http.server 8080 --bind 0.0.0.0 --directory tool
```

The 3D view uses CesiumJS with Esri imagery and terrain. A free Cesium ion token (from ion.cesium.com, pasted into the panel) adds Cesium World Terrain and OpenStreetMap 3D buildings. The token is kept in your browser's local storage and is never written to the repo.

## What it draws, and from which paragraph

| Element | Rule | Draft AC |
|---|---|---|
| TLOF | 1 RD + 10 ft; +20% if elevated with a non-load-bearing FATO | 4.2.1.4 |
| FATO | Larger of 1.5 D and TLOF + 0.34 D on each side; extra length above 1,000 ft MSL | 4.3.1.4, Figure 4-4 |
| Safety area | 0.28 D, at least 20 ft; +10 ft without the standard H | 4.4.1.4 |
| Heliport protection zone | 280 ft under each approach surface | 4.5.1 |
| Downwash/outwash caution area | 780 x 420 ft per path, aircraft 7,000 lb and under only | 4.6.1 |
| Approach/departure surface | FATO width to 500 ft at 4,000 ft; 8:1 max for helicopters, 15:1 or shallower for powered lift | 4.7.1.1 |
| Transitional surfaces | 2:1 out to 250 ft from centerline | 4.7.1.1 |

Not modeled yet: curved approaches, hospital lateral extensions, taxiways and the taxi caution area, and parking.

The Figure 4-4 curve was read off the chart and is good to about 5 ft; the AC's worked example (3,200 ft adds 80 ft) falls on it. Helicopter presets come from Appendix E, Table E-1. The AC has no powered-lift data, so powered-lift dimensions must come from the manufacturer.

Exports use WGS84 (EPSG:4326). Surface altitudes are meters MSL: ground elevation + deck height + surface height.

This is a planning sketch. It is not an FAA airspace determination or a design approval.

## Repository layout

| Path | Contents |
|---|---|
| `tool/vertiport-surfaces.html` | The planner, a single HTML file |
| `source/faa_draft_ac_150-5390-4/` | Draft AC PDF, FAA industry letter, comment matrix, and a text extract of the AC, downloaded 2026-11-04 from faa.gov |

## License

The planner is source-available under the [PolyForm Noncommercial License 1.0.0](LICENSE.md). It is not "open source" in the OSI sense, because commercial use is not allowed.

You may use, change and share it for any noncommercial purpose: personal study, research, teaching, hobby projects. The license also lets charities, schools, public research organizations, public safety and health organizations, and government institutions use it, whatever their funding.

Commercial use needs a separate license. That includes using the planner in paid consulting or engineering work, in a commercial product, or inside a for-profit company. To ask about a commercial license, email github.com/basilbuildsai.

The files in `source/` are U.S. government works published by the FAA and are not covered by this license. The planner loads third-party libraries and services at runtime (Leaflet, CesiumJS, Esri imagery and terrain, CARTO basemaps, OpenStreetMap data, USGS and Open-Meteo elevation, Photon geocoding), each under its own terms.

Required Notice: Copyright 2026 Basil Yap (https://github.com/basilbuildsai)
