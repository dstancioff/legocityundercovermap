#!/usr/bin/env python3
"""Build a district-to-points index from markers.json + districts.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
MARKERS_PATH = ROOT / "markers.json"
DISTRICTS_PATH = ROOT / "districts.json"
OUTPUT_PATH = ROOT / "district-points.json"


def district_bbox(path: list[list[float]]) -> dict[str, float]:
    lats = [point[0] for point in path]
    lngs = [point[1] for point in path]
    return {
        "lat_min": min(lats),
        "lat_max": max(lats),
        "lng_min": min(lngs),
        "lng_max": max(lngs),
    }


def marker_title_text(marker: dict[str, Any]) -> str:
    title = marker.get("title")
    if isinstance(title, dict):
        return title.get("en") or title.get("nl") or ""
    if isinstance(title, str):
        return title
    return ""


def marker_tiles(marker: dict[str, Any]) -> str:
    return marker.get("tiles") or "main"


def contains(district: dict[str, Any], coords: list[float], marker_tile: str) -> bool:
    district_tile = district.get("tiles") or "main"
    if district_tile != marker_tile:
        return False
    bbox = district["_bbox"]
    lat, lng = float(coords[0]), float(coords[1])
    return (
        bbox["lat_min"] <= lat <= bbox["lat_max"]
        and bbox["lng_min"] <= lng <= bbox["lng_max"]
    )


def main() -> None:
    markers = json.loads(MARKERS_PATH.read_text())
    districts_doc = json.loads(DISTRICTS_PATH.read_text())
    districts = districts_doc.get("districts", [])

    for district in districts:
        district["_bbox"] = district_bbox(district["path"])

    points: list[dict[str, Any]] = []
    for marker_type in sorted(markers.keys()):
        category = markers[marker_type]
        marker_list = category.get("markers", [])
        for marker_i, marker in enumerate(marker_list):
            coords = marker.get("coords")
            if not isinstance(coords, list) or len(coords) != 2:
                continue

            tile = marker_tiles(marker)
            district_matches = [d["id"] for d in districts if contains(d, coords, tile)]

            point = {
                "id": f"{marker_type}:{marker_i}",
                "marker_type": marker_type,
                "marker_index": marker_i,
                "title": marker_title_text(marker),
                "coords": [float(coords[0]), float(coords[1])],
                "tiles": tile,
                "district_ids": district_matches,
            }
            points.append(point)

    points.sort(key=lambda point: point["id"])

    by_district: dict[str, dict[str, Any]] = {}
    district_ids = {district["id"] for district in districts}
    for district in districts:
        by_district[district["id"]] = {
            "id": district["id"],
            "title": district.get("title", {}),
            "tiles": district.get("tiles") or "main",
            "point_count": 0,
            "point_ids": [],
        }

    unassigned: list[str] = []
    ambiguous: list[dict[str, Any]] = []
    unknown_district_refs: list[dict[str, Any]] = []

    for point in points:
        district_matches = point["district_ids"]
        if len(district_matches) == 0:
            unassigned.append(point["id"])
            continue

        if len(district_matches) > 1:
            ambiguous.append(
                {
                    "point_id": point["id"],
                    "district_ids": district_matches,
                }
            )

        for district_id in district_matches:
            if district_id not in district_ids:
                unknown_district_refs.append(
                    {"point_id": point["id"], "district_id": district_id}
                )
                continue
            by_district[district_id]["point_count"] += 1
            by_district[district_id]["point_ids"].append(point["id"])

    for district_data in by_district.values():
        district_data["point_ids"].sort()

    output = {
        "meta": {
            "source_markers": MARKERS_PATH.name,
            "source_districts": DISTRICTS_PATH.name,
            "total_points": len(points),
            "district_count": len(districts),
            "assigned_point_count": len(points) - len(unassigned),
            "unassigned_point_count": len(unassigned),
            "ambiguous_point_count": len(ambiguous),
        },
        "districts": [by_district[district["id"]] for district in districts],
        "points": points,
        "validation": {
            "unassigned_point_ids": sorted(unassigned),
            "ambiguous_points": ambiguous,
            "unknown_district_refs": unknown_district_refs,
        },
    }

    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=False) + "\n")
    print(
        f"Wrote {OUTPUT_PATH.name} "
        f"({output['meta']['total_points']} points, "
        f"{output['meta']['unassigned_point_count']} unassigned, "
        f"{output['meta']['ambiguous_point_count']} ambiguous)"
    )


if __name__ == "__main__":
    main()
