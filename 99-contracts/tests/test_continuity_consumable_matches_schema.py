"""Gate: the consumable `pact_contracts.continuity` vocabulary == the locked schema.

PACT owns the continuity contract; `contracts_py/pact_contracts/continuity.py` is
its importable Python form (downstream repos consume it instead of hand-mirroring).
This gate pins that consumable to the canonical
`99-contracts/schemas/continuity_findings_packet.schema.json` so the two can never
silently diverge — a schema enum change fails here until the consumable is updated,
and that one update then propagates to every importer.

Run: cd 99-contracts && python3 -m pytest tests/test_continuity_consumable_matches_schema.py -v
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_CONTRACTS_PY = Path(__file__).resolve().parents[2] / "contracts_py"
_SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "continuity_findings_packet.schema.json"

if str(_CONTRACTS_PY) not in sys.path:
    sys.path.insert(0, str(_CONTRACTS_PY))

from pact_contracts import continuity  # noqa: E402  (after sys.path insert)


def _finding_props() -> dict:
    schema = json.loads(_SCHEMA.read_text(encoding="utf-8"))
    for sub in schema.get("allOf", []):
        props = sub.get("properties", {})
        if "candidate_findings" in props:
            return props["candidate_findings"]["items"]["properties"]
    raise AssertionError("candidate_findings shape not found in schema (fail closed)")


_FINDING = _finding_props()


def _schema_enum(*path: str) -> set[str]:
    node = _FINDING
    for key in path:
        node = node[key]
    values = set(node["enum"])
    assert values, f"schema enum at {path} is empty (fail closed)"
    return values


# (consumable frozenset, schema enum path within a finding)
_CASES = [
    ("FINDING_TYPES", continuity.FINDING_TYPES, ("finding_type",)),
    ("SCOPE_TYPES", continuity.SCOPE_TYPES, ("scope_type",)),
    ("SPAN_ROLES", continuity.SPAN_ROLES, ("evidence_spans", "items", "properties", "span_role")),
    ("CONFIDENCES", continuity.CONFIDENCES, ("confidence",)),
    ("CANDIDATE_STATES", continuity.CANDIDATE_STATES, ("candidate_state",)),
    ("SEVERITY_HINTS", continuity.SEVERITY_HINTS, ("severity_hint",)),
]


@pytest.mark.parametrize("name,consumable,path", _CASES, ids=[c[0] for c in _CASES])
def test_consumable_matches_canonical_schema(name, consumable, path):
    assert consumable, f"pact_contracts.continuity.{name} is empty (fail closed)"
    schema_set = _schema_enum(*path)
    assert set(consumable) == schema_set, (
        f"{name} drift vs continuity_findings_packet.schema.json:\n"
        f"  consumable={sorted(consumable)}\n  schema    ={sorted(schema_set)}"
    )


def test_consumable_exports_all_six_enums():
    # Fail-closed completeness: all six finding enums are exposed + non-empty.
    for name, consumable, _ in _CASES:
        assert isinstance(consumable, frozenset) and consumable, f"{name} missing/empty"
