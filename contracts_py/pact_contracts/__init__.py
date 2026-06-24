"""pact-contracts — importable consumable form of PACT cross-repo contracts.

PACT owns the continuity contract (99-contracts/schemas/continuity_findings_packet.schema.json
is the SSOT). This package is the *consumable Python form* of that vocabulary, so
downstream repos (NeuronForge, ...) IMPORT it instead of hand-mirroring the enum
values. The authority is still the locked JSON schema; the package's values are
pinned to it by a gate (pact/99-contracts/tests/test_continuity_consumable_matches_schema.py).

Pure-Python, zero-dependency by design — it bundles cleanly into frozen sidecars.
"""

from pact_contracts import continuity

__all__ = ["continuity"]
