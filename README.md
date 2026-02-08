# LEGO City Undercover Map (dstancioff fork)

Personal fork of [meeuw/legocityundercovermap](https://github.com/meeuw/legocityundercovermap), used for my own LEGO City Undercover playthrough and map tweaks.

- Upstream: <https://github.com/meeuw/legocityundercovermap>
- This fork: <https://github.com/dstancioff/legocityundercovermap>
- Live map: <https://dstancioff.github.io/legocityundercovermap>

## Fork Changes

- Sidebar UI for browsing points.
- District-based data model and boundaries (`districts.json`).
- Generated district point index (`district-points.json`) plus generator script (`generate_district_points.py`).
- District validation outputs (`unassigned-analysis.json`) to track unassigned and ambiguous points.
- Grouping mode updates in the sidebar (category mode and district mode).
- District focus controls and follow-up refinements.
- Label/control polish and icon/logo display improvements.
- Fork banner updates and project-specific UX adjustments.
- Additional zoom levels

## What The Map Does

Use this map to track collectibles and secrets in LEGO City Undercover. Marker types can be filtered, and points can be marked completed.

Current map behavior includes:

- Persisted completion state in browser `localStorage`.
- Optional district overlays.
- Cursor coordinate overlay on the map.
- District-aware grouping/focus tools in the sidebar.

## Data Files

- `markers.json`: all map points/markers.
- `districts.json`: district boundaries as simple map polygons.
- `district-points.json`: generated lookup/index that maps points to districts and includes validation data.

To find coordinates while editing map data, use `?debug=1` in the URL and click the map. Marker popups include coordinates in debug mode.

District format in `districts.json`:

```json
{
  "districts": [
    {
      "id": "auburn-bay",
      "title": { "en": "Auburn Bay" },
      "tiles": "main",
      "path": [[-10.0, -20.0], [-12.0, -24.0], [-8.0, -28.0], [-6.0, -22.0]],
      "style": { "color": "#1f5fbf", "fillColor": "#1f5fbf", "weight": 2 }
    }
  ]
}
```

`path` should be a closed district boundary shape (at least 3 points). `tiles` defaults to `main` if omitted.

## District Point Index

Generate `district-points.json` from `markers.json` and `districts.json`:

```bash
python3 generate_district_points.py
```

Generated data includes:

- `districts`: districts with `point_ids` and `point_count`.
- `points`: every marker point with `district_ids`.
- `validation.unassigned_point_ids`: points in no district.
- `validation.ambiguous_points`: points in multiple districts.

Intended uses:

- Group sidebar points by district.
- Validate district coverage quality.
- Compare local district assignments against external reference lists.

## Technical Notes

This map is built with [LeafletJS](https://leafletjs.com/). The base map tiles were assembled from Nintendo Switch screenshots, HUD cleanup, and stitching/cropping to a 4096x4096 base image, then tiled with `crop.py`.

Completion data is stored in browser `localStorage`. If marker data changes, old completion data can become stale.
