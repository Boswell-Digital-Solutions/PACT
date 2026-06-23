"""
Cross-repo SYNC VERIFIER for the continuity contract (drift gate, tier 2).

The per-repo enum gates each assert their LOCAL vendored schema copy matches that
repo's mirror (TS const arrays / Python validator constants / SQL CHECKs). That
catches a repo editing its mirror out of step with its own vendored copy — but it
CANNOT catch the case where pact (the SSOT) changed and a repo simply never
re-vendored: there, the stale vendored copy still agrees with the stale local
mirror, and the per-repo gate passes green while the repo is silently behind
canonical.

THIS gate closes that hole: it proves every vendored copy registered in
VENDOR_MANIFEST.json is byte-identical (sha256) to its upstream schema in
ecosystem/pact/99-contracts/. If pact changes and a consumer didn't re-vendor,
this goes RED.

It also enforces manifest completeness in both directions:
  - every canonical continuity schema has at least one registered consumer, and
  - every vendored *.schema.json found on disk under a registered vendor dir is
    itself registered (so an unregistered vendored copy can't escape the gate).

Run (colocated ecosystem):
    cd ecosystem/pact/99-contracts && python3 -m pytest tests/test_vendored_schema_sync.py -v
Override the ecosystem root with FORGE_ECOSYSTEM_ROOT if repos live elsewhere.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

_THIS = Path(__file__).resolve()
# tests -> 99-contracts -> pact -> ecosystem -> <ECOSYSTEM ROOT>
_DEFAULT_ROOT = _THIS.parents[4]
ROOT = Path(os.environ.get("FORGE_ECOSYSTEM_ROOT", str(_DEFAULT_ROOT)))
MANIFEST_PATH = _THIS.parents[1] / "VENDOR_MANIFEST.json"


def _load_manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


_MANIFEST = _load_manifest()
_VENDORED = _MANIFEST["vendored"]


def test_manifest_is_nonempty():
    # Fail-closed: an empty manifest must NOT trivially pass.
    assert _VENDORED, "VENDOR_MANIFEST.json lists no vendored copies"
    assert _MANIFEST.get("continuity_schemas"), "manifest has no continuity_schemas list"


@pytest.mark.parametrize(
    "entry",
    _VENDORED,
    ids=[f"{e['consumer']}:{Path(e['path']).name}" for e in _VENDORED],
)
def test_vendored_copy_matches_upstream(entry):
    """Each vendored copy must be byte-identical (sha256) to its upstream pact schema."""
    vendored = ROOT / entry["path"]
    upstream = ROOT / entry["upstream"]
    assert upstream.exists(), f"upstream missing: {upstream} (manifest entry for {entry['consumer']})"
    assert vendored.exists(), (
        f"vendored copy MISSING: {vendored} — consumer '{entry['consumer']}' must re-vendor "
        f"{Path(entry['upstream']).name} from pact"
    )
    uh, vh = _sha256(upstream), _sha256(vendored)
    assert vh == uh, (
        f"VENDOR DRIFT: {entry['consumer']} copy of {Path(entry['upstream']).name} is stale.\n"
        f"  vendored {vendored}\n    sha256={vh}\n"
        f"  upstream {upstream}\n    sha256={uh}\n"
        f"  -> re-vendor (copy upstream over the vendored file)."
    )


def test_every_canonical_schema_has_a_consumer():
    """Each canonical continuity schema must be vendored by at least one consumer,
    so a newly-added canonical schema with zero registered consumers is flagged."""
    upstream_names = {Path(e["upstream"]).name for e in _VENDORED}
    missing = [s for s in _MANIFEST["continuity_schemas"] if s not in upstream_names]
    assert not missing, f"canonical schema(s) with NO registered vendor consumer: {missing}"


def test_no_unregistered_vendored_copies():
    """Every *.schema.json (and the continuity valid fixture) found on disk under a
    registered vendor dir must be in the manifest — an unregistered vendored copy
    would silently escape the sync check."""
    registered = {str((ROOT / e["path"]).resolve()) for e in _VENDORED}
    targets = ("*.schema.json", "continuity_findings_packet.valid.json")
    found: list[str] = []
    for vdir in _MANIFEST.get("vendor_dirs", []):
        base = ROOT / vdir
        if not base.exists():
            continue
        for pat in targets:
            for f in base.rglob(pat):
                found.append(str(f.resolve()))
    assert found, "no vendored schema files found on disk under any registered vendor_dir"
    unregistered = sorted(set(found) - registered)
    assert not unregistered, (
        "vendored copies on disk but NOT in VENDOR_MANIFEST.json (would escape the sync gate):\n  "
        + "\n  ".join(unregistered)
    )
