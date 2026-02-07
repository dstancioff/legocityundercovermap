LEGO City Undercover Map
========================

You can use this map for finding all secrets in Lego City Undercover, different types can be filtered using the legend and you can mark secrets as completed to hide them.

The map can be visited at:
https://meeuw.github.io/legocityundercovermap/

I've used several online guides to complete the map and made corrections, feel free to use my changes. It's also enspired on the "breath-of-the-wild-interactive-map".

The map isn't complete and I can use your help! Please report an issue if you'd like to have something changed or, even better, change it yourself and create a pull request!

All markers are defined in markers.json. District outlines are defined in districts.json. To find the coordinates you can add ?debug=1 to the url and click on the map, a popup will appear with the coordinates. With debug enabled the popup for a marker will contain the coordinates.

District format in ``districts.json``::

    {
      "districts": [
        {
          "id": "auburn-bay",
          "title": {"en": "Auburn Bay"},
          "tiles": "main",
          "path": [[-10.0, -20.0], [-12.0, -24.0], [-8.0, -28.0], [-6.0, -22.0]],
          "style": {"color": "#1f5fbf", "fillColor": "#1f5fbf", "weight": 2}
        }
      ]
    }

``path`` should be a closed district boundary shape (at least 3 points). ``tiles`` defaults to ``main`` if omitted.

District point index
--------------------

Use ``generate_district_points.py`` to build ``district-points.json`` from ``markers.json`` and ``districts.json``::

    python3 generate_district_points.py

The generated file contains:

- ``districts``: list of districts with ``point_ids`` and ``point_count`` (points grouped by district)
- ``points``: every marker point with ``district_ids`` (for per-point district lookup)
- ``validation.unassigned_point_ids``: points that do not fall in any district
- ``validation.ambiguous_points``: points that fall in more than one district

This dataset is intended for:

- sidebar grouping by district
- district validation (unassigned/ambiguous points)
- comparing district point lists against external sources

This map is created using the open source LeafletJS library (many thanks!), I've created the tiles by screenshotting the map on a Nintendo Switch and shared the pictures on Facebook, removed the HUD using Imagemagick and glued them back together using GIMP. This way I've created a baselayer which I've aligned to the top left and cropped at 4096x4096 pixels. This image was cropped and scaled to tiles using crop.png.

The completion data is stored as localeStorage in your browser, as the markers are still being updated the completion data might get garbled. Please make sure you've forked the map to make sure your completion data will not be corrupted.
