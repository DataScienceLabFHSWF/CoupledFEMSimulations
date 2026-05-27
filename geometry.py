"""Pure helper to load a tool geometry from YAML.

Lives outside :mod:`extract_temps` so it can be unit-tested without
ABAQUS' ``odbAccess`` import. The ABAQUS-side script imports
:func:`resolve_geometry` and turns it into the flat ``nodelist`` /
``nodelabels`` pair the old code expected — but the *source of truth* is
now ``configs/geometry/{tool}.yaml``.

v1 hardcoded these indices as a literal Python list. v2 separates *mesh
identity* (origin + offset, per tool, in YAML) from *extraction logic*
(this module), so a re-mesh only requires editing the YAML.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

# Standard ABAQUS Python is 2.7-without-pip, so keep this module
# stdlib + PyYAML only. No type-only typing features beyond Optional.

CONFIG_ROOT = Path(__file__).resolve().parent / "configs" / "geometry"


@dataclass
class ToolGeometry:
    name: str
    nodelist: list  # list of int — absolute ABAQUS node indices, in CSV order
    nodelabels: list  # list of str — column headers, parallel to nodelist
    start_time_source: str  # "zero" | "previous"


def _detect_tool(filepath):
    # type: (str) -> str
    """Return the tool tag (``M1`` | ``M2`` | ``M3``) hidden in ``filepath``."""

    for tag in ("M1", "M2", "M3"):
        if tag in filepath:
            return tag
    raise ValueError("Cannot infer tool tag from path: " + str(filepath))


def load_geometry(tool):
    # type: (str) -> ToolGeometry
    path = CONFIG_ROOT / (tool + ".yaml")
    with open(str(path), "rb") as fh:
        raw = yaml.safe_load(fh)

    nodelist = []
    labels = []
    for group_name, group in raw["node_groups"].items():
        origin = int(group["origin"])
        for col in group["columns"]:
            nodelist.append(origin + int(col["offset"]))
            labels.append(str(col["label"]))

    return ToolGeometry(
        name=str(raw["name"]),
        nodelist=nodelist,
        nodelabels=labels,
        start_time_source=str(raw.get("start_time_source", "zero")),
    )


def resolve_geometry(filepath):
    # type: (str) -> ToolGeometry
    """Convenience: detect tool from ``filepath`` and load its geometry."""

    return load_geometry(_detect_tool(filepath))


def csv_header(geom):
    # type: (ToolGeometry) -> str
    """Return the CSV header line matching the v1 ``nodelabels`` format."""

    parts = ["'timestamp'"] + ["'" + lbl + "'" for lbl in geom.nodelabels]
    return ", ".join(parts)


__all__ = ["ToolGeometry", "load_geometry", "resolve_geometry", "csv_header"]
