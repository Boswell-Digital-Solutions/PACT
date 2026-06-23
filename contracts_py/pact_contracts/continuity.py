"""Canonical continuity-finding vocabulary — the consumable Python form.

These frozensets mirror ``continuity_findings_packet.schema.json`` field-for-field
and are pinned to it by a gate in PACT
(``99-contracts/tests/test_continuity_consumable_matches_schema.py``). They are
kept as pure-Python literals (NOT read from the JSON at runtime) so the package
bundles into frozen (PyInstaller) sidecars with no data-file dependency.

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

__all__ = [
    "FINDING_TYPES",
    "SCOPE_TYPES",
    "SPAN_ROLES",
    "CONFIDENCES",
    "CANDIDATE_STATES",
    "SEVERITY_HINTS",
]
