"""Canonical continuity-finding vocabulary — the consumable Python form.

These literals mirror ``continuity_findings_packet.schema.json`` field-for-field
and are pinned to it by a gate in PACT
(``99-contracts/tests/test_continuity_consumable_matches_schema.py``). Two kinds:

* the six finding **enum** value sets (``FINDING_TYPES`` … ``SEVERITY_HINTS``),
  consumed by *validators*; and
* the structural **key** vocabulary (``FINDING_KEYS`` / ``SPAN_KEYS`` /
  ``LINEAGE_KEYS``) plus the candidate-only invariant value
  (``CANDIDATE_UNREVIEWED``), consumed by the producer-side *packet builder*.

All are kept as pure-Python literals (NOT read from the JSON at runtime) so the
package bundles into frozen (PyInstaller) sidecars with no data-file dependency.

Consumers import these instead of redefining their own copies, e.g.::

    from pact_contracts.continuity import FINDING_TYPES, SCOPE_TYPES

If the locked schema changes, PACT's gate fails until these are updated in
lockstep — and that single update propagates to every importer.
"""

from __future__ import annotations

#: candidate_findings[].finding_type
FINDING_TYPES: frozenset[str] = frozenset(
    {
        "continuity_tension",
        "progression_break",
        "transition_gap",
        "descriptive_mismatch",
        "repeated_movement",
        "escalation_mismatch",
        "state_carry_forward_issue",
        "causal_link_unclear",
    }
)

#: candidate_findings[].scope_type
SCOPE_TYPES: frozenset[str] = frozenset(
    {
        "scene_local",
        "adjacent_scene",
        "scene_window",
        "chapter_window",
    }
)

#: candidate_findings[].evidence_spans[].span_role
SPAN_ROLES: frozenset[str] = frozenset(
    {
        "setup",
        "contrast",
        "carry_forward",
        "mismatch_signal",
        "transition_signal",
        "progression_signal",
    }
)

#: candidate_findings[].confidence
CONFIDENCES: frozenset[str] = frozenset({"low", "moderate", "high"})

#: candidate_findings[].candidate_state (also packet-level review_state)
CANDIDATE_STATES: frozenset[str] = frozenset(
    {
        "candidate_unreviewed",
        "candidate_review_in_progress",
        "candidate_retained",
        "candidate_rejected",
        "candidate_promoted",
    }
)

#: candidate_findings[].severity_hint (optional)
SEVERITY_HINTS: frozenset[str] = frozenset({"minor", "moderate", "major"})

# ---------------------------------------------------------------------------
# Structural key vocabulary — the allowed property names a PRODUCER may project
# onto a continuity finding / evidence span / lineage triple. The packet schema
# is ``additionalProperties: false`` on findings and spans, so a producer that
# wraps upstream blobs must project onto exactly these keys. Kept as ordered
# tuples (schema property order) so projection output stays deterministic.
# Pinned to the schema by the same PACT gate as the enums.
# ---------------------------------------------------------------------------

#: allowed keys on a continuity finding (additionalProperties: false)
FINDING_KEYS: tuple[str, ...] = (
    "finding_id",
    "finding_label",
    "finding_type",
    "claim",
    "scope_type",
    "scope_bounds",
    "evidence_spans",
    "confidence",
    "uncertainty_note",
    "review_note",
    "candidate_state",
    "related_finding_ids",
    "severity_hint",
    "taxonomy_tags",
)

#: allowed keys on an evidence span (additionalProperties: false)
SPAN_KEYS: tuple[str, ...] = (
    "scene_id",
    "span_text",
    "span_role",
    "chapter_id",
    "position_hint",
)

#: the all-or-nothing context lineage triple carried on packet_base
LINEAGE_KEYS: tuple[str, ...] = (
    "task_intent_id",
    "context_bundle_id",
    "context_bundle_hash",
)

#: the candidate-only invariant value — a producer never promotes; both a
#: finding's ``candidate_state`` and the packet-level ``review_state`` start
#: here. Member of CANDIDATE_STATES (pinned by the PACT gate).
CANDIDATE_UNREVIEWED: str = "candidate_unreviewed"

__all__ = [
    "FINDING_TYPES",
    "SCOPE_TYPES",
    "SPAN_ROLES",
    "CONFIDENCES",
    "CANDIDATE_STATES",
    "SEVERITY_HINTS",
    "FINDING_KEYS",
    "SPAN_KEYS",
    "LINEAGE_KEYS",
    "CANDIDATE_UNREVIEWED",
]
