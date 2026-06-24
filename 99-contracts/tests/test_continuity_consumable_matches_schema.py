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


def _finding_item() -> dict:
    schema = json.loads(_SCHEMA.read_text(encoding="utf-8"))
    for sub in schema.get("allOf", []):
        props = sub.get("properties", {})
        if "candidate_findings" in props:
            return props["candidate_findings"]["items"]
    raise AssertionError("candidate_findings shape not found in schema (fail closed)")


_FINDING_ITEM = _finding_item()
_FINDING = _FINDING_ITEM["properties"]
_SPAN = _FINDING["evidence_spans"]["items"]["properties"]


def _packet_base_props() -> dict:
    base_path = _SCHEMA.parent / "packet_base.schema.json"
    return json.loads(base_path.read_text(encoding="utf-8"))["properties"]


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


# --------------------------------------------------------------------------- #
# Structural key vocabulary (consumed by the producer-side packet builder).
# These are the allowed property keys under additionalProperties:false, so the
# producer projects onto exactly these. Compared as SETS (the keys are the
# contract; the tuple order is only a deterministic-output convenience).
# --------------------------------------------------------------------------- #
def test_finding_keys_match_schema_allowed_keys():
    assert continuity.FINDING_KEYS, "FINDING_KEYS empty (fail closed)"
    assert len(continuity.FINDING_KEYS) == len(set(continuity.FINDING_KEYS)), (
        "FINDING_KEYS has duplicate entries"
    )
    assert set(continuity.FINDING_KEYS) == set(_FINDING.keys()), (
        "FINDING_KEYS drift vs schema finding properties:\n"
        f"  consumable={sorted(continuity.FINDING_KEYS)}\n"
        f"  schema    ={sorted(_FINDING.keys())}"
    )


def test_span_keys_match_schema_allowed_keys():
    assert continuity.SPAN_KEYS, "SPAN_KEYS empty (fail closed)"
    assert len(continuity.SPAN_KEYS) == len(set(continuity.SPAN_KEYS)), (
        "SPAN_KEYS has duplicate entries"
    )
    assert set(continuity.SPAN_KEYS) == set(_SPAN.keys()), (
        "SPAN_KEYS drift vs schema evidence-span properties:\n"
        f"  consumable={sorted(continuity.SPAN_KEYS)}\n"
        f"  schema    ={sorted(_SPAN.keys())}"
    )


def test_lineage_keys_match_packet_base():
    base_props = _packet_base_props()
    assert continuity.LINEAGE_KEYS, "LINEAGE_KEYS empty (fail closed)"
    for key in continuity.LINEAGE_KEYS:
        assert key in base_props, f"lineage key {key!r} absent from packet_base schema"
    # The triple is exactly these three context-handle fields.
    assert set(continuity.LINEAGE_KEYS) == {
        "task_intent_id",
        "context_bundle_id",
        "context_bundle_hash",
    }, f"LINEAGE_KEYS drift: {sorted(continuity.LINEAGE_KEYS)}"


def test_candidate_unreviewed_is_a_valid_candidate_state():
    assert continuity.CANDIDATE_UNREVIEWED == "candidate_unreviewed"
    assert continuity.CANDIDATE_UNREVIEWED in continuity.CANDIDATE_STATES, (
        "CANDIDATE_UNREVIEWED is not a member of the canonical candidate_state enum"
    )
