"""SELF-CONSISTENCY gate freezing the canonical continuity-findings contract.

This gate is the structural lock on pact's V1 continuity-findings contract. It is
deliberately *fail-closed*: every extraction asserts non-empty BEFORE comparing,
so a broken parse can never trivially "match" an empty expectation.

Source of truth
---------------
pact IS the source of these schemas. To make the gate self-contained (and to give
it a frozen baseline that an author must consciously edit), the five canonical
schema files are mirrored under ``tests/_vendor/schemas/`` and the structural /
enum checks load from that mirror. The live fixtures under
``99-contracts/fixtures/`` are validated against the vendored packet schema (that
is the artifact we are gating against drift).

Fixture polarity (matches pact's own ``scripts/validate_contract_fixtures.py``)
-------------------------------------------------------------------------------
* ``fixtures/valid``  -> MUST validate (pass)
* ``fixtures/edge``   -> MUST validate (pass) -- edge fixtures are *valid boundary
  cases* in this repo (e.g. the warningless / empty-findings minimal packet), not
  rejection cases. The task prose said "edge must FAIL", but the repo's own
  contract treats edge as ``edge_passed``; forcing edge-must-fail would make this
  gate pass only by mis-validating a legitimately-valid packet. See the module
  docstring note and the NOTE in ``test_edge_fixtures_pass``.
* ``fixtures/invalid`` -> MUST be rejected (fail)

False-friends explicitly NOT conflated here
-------------------------------------------
* AuthorForge decision-action enum [review, retain, reject, promote] is NOT
  candidate_state.
* NeuroForge MAID authority_class [official_source, weighted_adjacent,
  advisory_only] is NOT this grounding authority_class [primary, secondary,
  derived].
* PCC bundle_hash == pact context_bundle_hash (intentional cross-boundary rename);
  not treated as drift.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
VENDOR_SCHEMA_DIR = HERE / "_vendor" / "schemas"
CONTRACTS_ROOT = HERE.parent  # 99-contracts
FIXTURE_ROOT = CONTRACTS_ROOT / "fixtures"

# The five schema files that compose the frozen continuity contract.
SCHEMA_FILES = (
    "continuity_findings_packet.schema.json",
    "packet_base.schema.json",
    "grounding_ref.schema.json",
    "serialization_profile_enum.schema.json",
    "source_lineage_digest.schema.json",
)

PACKET_SCHEMA = "continuity_findings_packet.schema.json"

# ---------------------------------------------------------------------------
# HARDCODED expected contract. Any schema edit MUST consciously update this dict.
# Values are the contract; compared as SETS (order-independent) per gate rules.
# ---------------------------------------------------------------------------
EXPECTED_ENUMS: dict[str, list[str]] = {
    # per-finding enums
    "finding_type": [
        "continuity_tension",
        "progression_break",
        "transition_gap",
        "descriptive_mismatch",
        "repeated_movement",
        "escalation_mismatch",
        "state_carry_forward_issue",
        "causal_link_unclear",
    ],
    "scope_type": [
        "scene_local",
        "adjacent_scene",
        "scene_window",
        "chapter_window",
    ],
    "span_role": [
        "setup",
        "contrast",
        "carry_forward",
        "mismatch_signal",
        "transition_signal",
        "progression_signal",
    ],
    "confidence": [
        "low",
        "moderate",
        "high",
    ],
    "candidate_state": [
        "candidate_unreviewed",
        "candidate_review_in_progress",
        "candidate_retained",
        "candidate_rejected",
        "candidate_promoted",
    ],
    "severity_hint": [
        "minor",
        "moderate",
        "major",
    ],
}

# packet_base.packet_class enum MUST include continuity_findings_packet.
EXPECTED_PACKET_CLASS_INCLUDES = "continuity_findings_packet"

# Lineage triple field names carried on packet_base.
EXPECTED_LINEAGE_TRIPLE = ["task_intent_id", "context_bundle_id", "context_bundle_hash"]

# grounding_ref.authority_class enum (pact grounding authority, NOT MAID authority).
EXPECTED_GROUNDING_AUTHORITY_CLASS = ["primary", "secondary", "derived"]


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------
def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_vendored(name: str) -> dict[str, Any]:
    return _load(VENDOR_SCHEMA_DIR / name)


def _build_registry() -> Registry:
    """Registry over the vendored schema dir, keyed by the relative ``./`` ref
    form used inside the schemas, the bare filename, and the schema $id."""
    registry: Registry = Registry()
    for name in SCHEMA_FILES:
        doc = _load_vendored(name)
        res = Resource.from_contents(doc, default_specification=DRAFT202012)
        registry = registry.with_resource("./" + name, res)
        registry = registry.with_resource(name, res)
        sid = doc.get("$id")
        if isinstance(sid, str) and sid:
            registry = registry.with_resource(sid, res)
    return registry


def _packet_validator() -> Draft202012Validator:
    schema = _load_vendored(PACKET_SCHEMA)
    return Draft202012Validator(schema, registry=_build_registry())


# ---------------------------------------------------------------------------
# Enum extraction helpers (fail-closed: raise on empty so callers can assert).
# ---------------------------------------------------------------------------
def _finding_item_schema(packet: dict[str, Any]) -> dict[str, Any]:
    """The per-finding object schema inside candidate_findings.items."""
    for branch in packet["allOf"]:
        props = branch.get("properties", {})
        if "candidate_findings" in props:
            return props["candidate_findings"]["items"]
    raise AssertionError("candidate_findings branch not found in continuity packet allOf")


def _packet_overlay(packet: dict[str, Any]) -> dict[str, Any]:
    """The continuity-specific overlay branch of the packet allOf."""
    for branch in packet["allOf"]:
        if "candidate_findings" in branch.get("properties", {}):
            return branch
    raise AssertionError("continuity overlay branch not found")


def _enum_at(schema: dict[str, Any]) -> list[str]:
    enum = schema.get("enum")
    assert isinstance(enum, list) and len(enum) > 0, (
        f"FAIL-CLOSED: expected a non-empty enum list, got {enum!r}"
    )
    return enum


# ===========================================================================
# (1) check_schema each of the five schema files.
# ===========================================================================
@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_is_valid_draft202012(name: str) -> None:
    doc = _load_vendored(name)
    Draft202012Validator.check_schema(doc)


# ===========================================================================
# (2) Extract literal enums and assert == HARDCODED expected (sets).
# ===========================================================================
def test_per_finding_enums_match_hardcoded() -> None:
    packet = _load_vendored(PACKET_SCHEMA)
    item = _finding_item_schema(packet)
    item_props = item["properties"]
    # span_role lives on the evidence-span sub-object, not the finding root.
    span_props = item_props["evidence_spans"]["items"]["properties"]

    def _schema_for(field: str) -> dict[str, Any]:
        if field == "span_role":
            return span_props[field]
        return item_props[field]

    extracted: dict[str, set[str]] = {}
    for field in EXPECTED_ENUMS:
        extracted[field] = set(_enum_at(_schema_for(field)))

    # fail-closed: every expected field must have been extracted non-empty
    assert set(extracted) == set(EXPECTED_ENUMS)
    for field, expected in EXPECTED_ENUMS.items():
        assert len(expected) > 0, f"hardcoded expectation for {field} is empty"
        assert extracted[field] == set(expected), (
            f"enum drift on {field}: schema={sorted(extracted[field])} "
            f"expected={sorted(set(expected))}"
        )


def test_packet_class_enum_includes_continuity() -> None:
    base = _load_vendored("packet_base.schema.json")
    enum = set(_enum_at(base["properties"]["packet_class"]))
    assert EXPECTED_PACKET_CLASS_INCLUDES in enum, (
        f"packet_class enum no longer includes "
        f"{EXPECTED_PACKET_CLASS_INCLUDES!r}: {sorted(enum)}"
    )


def test_packet_class_const_in_overlay() -> None:
    packet = _load_vendored(PACKET_SCHEMA)
    overlay = _packet_overlay(packet)
    const = overlay["properties"]["packet_class"].get("const")
    assert const == EXPECTED_PACKET_CLASS_INCLUDES, (
        f"packet_class const drift: {const!r}"
    )


def test_lineage_triple_field_names() -> None:
    base = _load_vendored("packet_base.schema.json")
    props = base["properties"]
    assert len(EXPECTED_LINEAGE_TRIPLE) == 3
    for field in EXPECTED_LINEAGE_TRIPLE:
        assert field in props, (
            f"lineage triple field {field!r} missing from packet_base properties"
        )
    # context_bundle_hash == PCC bundle_hash (intentional rename); assert the
    # pact-side name remains stable.
    assert "context_bundle_hash" in props


def test_grounding_authority_class_enum() -> None:
    gr = _load_vendored("grounding_ref.schema.json")
    enum = set(_enum_at(gr["properties"]["authority_class"]))
    assert enum == set(EXPECTED_GROUNDING_AUTHORITY_CLASS), (
        f"grounding authority_class drift: {sorted(enum)}"
    )
    # false-friend guard: MUST NOT be the NeuroForge MAID authority enum.
    maid_authority = {"official_source", "weighted_adjacent", "advisory_only"}
    assert enum != maid_authority, (
        "grounding authority_class must not be the MAID authority_class enum"
    )


# ===========================================================================
# (3) review_state.enum == candidate_state(per-finding).enum
# ===========================================================================
def test_review_state_equals_candidate_state_enum() -> None:
    packet = _load_vendored(PACKET_SCHEMA)
    overlay = _packet_overlay(packet)
    review_state = set(_enum_at(overlay["properties"]["review_state"]))

    item = _finding_item_schema(packet)
    candidate_state = set(_enum_at(item["properties"]["candidate_state"]))

    assert review_state == candidate_state, (
        f"review_state/candidate_state divergence: "
        f"review_state={sorted(review_state)} candidate_state={sorted(candidate_state)}"
    )

    # false-friend guard: candidate_state is NOT the AuthorForge decision-action
    # enum [review, retain, reject, promote].
    decision_action = {"review", "retain", "reject", "promote"}
    assert candidate_state != decision_action, (
        "candidate_state must not be the AuthorForge decision-action enum"
    )


# ===========================================================================
# (4) Fixture validation. Scope: the continuity-findings packet fixtures.
#     valid/edge MUST pass, invalid MUST fail.
# ===========================================================================
def _continuity_fixtures(kind: str) -> list[Path]:
    d = FIXTURE_ROOT / kind
    found = sorted(d.glob("continuity_findings_packet*.json"))
    return found


def test_valid_fixtures_pass() -> None:
    validator = _packet_validator()
    fixtures = _continuity_fixtures("valid")
    # fail-closed: there MUST be at least one valid continuity fixture.
    assert fixtures, "no continuity valid fixtures found (fail-closed)"
    for fx in fixtures:
        errors = list(validator.iter_errors(_load(fx)))
        assert not errors, (
            f"valid fixture {fx.name} failed: {[e.message for e in errors]}"
        )


def test_edge_fixtures_pass() -> None:
    # NOTE: in this repo edge fixtures are *valid boundary cases* (pact's own
    # validate_contract_fixtures.py records them as ``edge_passed``). The minimal
    # warningless / empty-findings continuity edge packet is a legitimately valid
    # instance, so this gate asserts edge fixtures PASS rather than fail.
    validator = _packet_validator()
    fixtures = _continuity_fixtures("edge")
    assert fixtures, "no continuity edge fixtures found (fail-closed)"
    for fx in fixtures:
        errors = list(validator.iter_errors(_load(fx)))
        assert not errors, (
            f"edge fixture {fx.name} unexpectedly failed: {[e.message for e in errors]}"
        )


def test_invalid_fixtures_fail() -> None:
    validator = _packet_validator()
    fixtures = _continuity_fixtures("invalid")
    # fail-closed: there MUST be at least one invalid continuity fixture, else
    # the "must fail" assertion below would be vacuously true.
    assert fixtures, "no continuity invalid fixtures found (fail-closed)"
    for fx in fixtures:
        errors = list(validator.iter_errors(_load(fx)))
        assert errors, (
            f"invalid fixture {fx.name} unexpectedly PASSED (should be rejected)"
        )


# ===========================================================================
# (5) Structural locks: additionalProperties:false on finding / evidence span /
#     grounding_ref; unevaluatedProperties:false on the packet.
# ===========================================================================
def test_structural_additional_properties_locks() -> None:
    packet = _load_vendored(PACKET_SCHEMA)

    # finding object
    item = _finding_item_schema(packet)
    assert item.get("additionalProperties") is False, (
        "finding object lost additionalProperties:false"
    )

    # evidence span object
    span = item["properties"]["evidence_spans"]["items"]
    assert span.get("additionalProperties") is False, (
        "evidence span object lost additionalProperties:false"
    )

    # grounding_ref
    gr = _load_vendored("grounding_ref.schema.json")
    assert gr.get("additionalProperties") is False, (
        "grounding_ref lost additionalProperties:false"
    )


def test_packet_unevaluated_properties_lock() -> None:
    packet = _load_vendored(PACKET_SCHEMA)
    assert packet.get("unevaluatedProperties") is False, (
        "continuity packet lost unevaluatedProperties:false (structural lock)"
    )
