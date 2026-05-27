"""Tests for the v2-publication geometry loader.

These tests do NOT import ``extract_temps`` (which imports ABAQUS'
``odbAccess``). They only exercise the pure helper in ``geometry.py``.

Regression baseline — the v1 hardcoded literals were::

    M1/M3 nodelist = [5208+5, 5208+344, 2672+304, 2672+327, 2672+397,
                      8, 9, 271, 238, 569]
    M2    nodelist = [5656+5, 5656+344, 2296+304, 2296+327, 2296+397,
                      8, 9, 271, 238, 569]

Both must reproduce after the YAML refactor.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from geometry import csv_header, load_geometry  # noqa: E402


@pytest.mark.parametrize(
    "tool, expected_nodelist",
    [
        (
            "M1",
            [5208 + 5, 5208 + 344, 2672 + 304, 2672 + 327, 2672 + 397,
             8, 9, 271, 238, 569],
        ),
        (
            "M2",
            [5656 + 5, 5656 + 344, 2296 + 304, 2296 + 327, 2296 + 397,
             8, 9, 271, 238, 569],
        ),
        (
            "M3",
            [5208 + 5, 5208 + 344, 2672 + 304, 2672 + 327, 2672 + 397,
             8, 9, 271, 238, 569],
        ),
    ],
)
def test_loaded_nodelist_matches_v1_literals(tool, expected_nodelist):
    geom = load_geometry(tool)
    assert geom.nodelist == expected_nodelist


def test_start_time_source_per_tool():
    assert load_geometry("M1").start_time_source == "zero"
    assert load_geometry("M2").start_time_source == "previous"
    assert load_geometry("M3").start_time_source == "previous"


def test_csv_header_starts_with_timestamp():
    header = csv_header(load_geometry("M1"))
    assert header.startswith("'timestamp'")
    assert "Stempel_innen_mitte" in header
    assert header.count(",") == 10  # timestamp + 10 columns => 10 commas
