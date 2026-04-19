#!/usr/bin/env python3
"""Emit the wave-1 promotion envelope.

This is the cross-repo carrier of admitted PACT wave-1 truth.  It is
deterministically derived from the already-proved manifest and promotion
packet.  Downstream repos (neuronforge, NeuroForge, ForgeCommand) consume
this envelope; they never generate or alter it.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = REPO_ROOT / "docs" / "evidence"
MANIFEST_PATH = EVIDENCE_DIR / "toon_wave1_manifest.json"
PACKET_PATH = EVIDENCE_DIR / "toon_wave1_promotion_packet.json"
OBSERVABILITY_PATH = EVIDENCE_DIR / "toon_observability_report.json"
REPLAY_PATH = EVIDENCE_DIR / "toon_replay_matrix_report.json"
GATE_REPORT_PATH = EVIDENCE_DIR / "toon_wave1_gate_report.json"
OPERATOR_EXAMPLES_PATH = EVIDENCE_DIR / "toon_wave1_operator_examples.md"

ENVELOPE_PATH = EVIDENCE_DIR / "wave1_promotion_envelope.json"
ENVELOPE_SCHEMA_REL = "99-contracts/schemas/wave1_promotion_envelope.schema.json"


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            text=True,
            capture_output=True,
            check=True,
        )
        return out.stdout.strip()
    except Exception:
        return "unknown"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def build_envelope() -> dict:
    manifest = _load(MANIFEST_PATH)
    packet = _load(PACKET_PATH)
    observability = _load(OBSERVABILITY_PATH)
    replay = _load(REPLAY_PATH)

    requested_profiles = sorted(observability.get("requested_profile_counts", {}).keys())
    used_profiles = sorted({c["used_profile"] for c in replay["cases"]})
    fallback_reasons = sorted(observability.get("fallback_reason_counts", {}).keys())
    registry = manifest["registry"]

    envelope = {
        "promotion_packet_version": packet["packet_version"],
        "source_repo": "pact",
        "source_commit": _git_commit(),
        "wave_manifest_path": _rel(MANIFEST_PATH),
        "wave_manifest_hash": _sha256(MANIFEST_PATH),
        "promotion_packet_path": _rel(PACKET_PATH),
        "promotion_packet_hash": _sha256(PACKET_PATH),
        "strict_success_hash": manifest["strict_success_hash"],
        "non_strict_canonical_digests": dict(manifest["non_strict_canonical_digests"]),
        "allowed_packet_classes": list(registry["supported_packet_classes"]),
        "supported_requested_profiles": requested_profiles,
        "supported_used_profiles": used_profiles,
        "fallback_reason_codes": fallback_reasons,
        "feature_flag_name": manifest["feature_flag"],
        "admission_stage": registry["admission_stage"],
        "generated_at": _dt.datetime.now(tz=_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "operator_evidence_paths": [
            _rel(OPERATOR_EXAMPLES_PATH),
        ],
        "repo_gate_report_path": _rel(GATE_REPORT_PATH),
        "promotion_notes": (
            "Cross-repo wave-1 promotion envelope derived from PACT-owned manifest "
            "and promotion packet. PACT is the upstream serialization authority; "
            "downstream repos may carry this envelope but may not redefine TOON "
            "wave-1 rendering, fallback, or admission rules."
        ),
        "source_schema_versions": {
            "toon_registry": str(registry["schema_version"]),
            "toon_segment": str(registry["segment_version"]),
        },
    }
    return envelope


def main() -> int:
    envelope = build_envelope()
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    ENVELOPE_PATH.write_text(
        json.dumps(envelope, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "wave1_promotion_envelope": str(ENVELOPE_PATH),
        "schema": ENVELOPE_SCHEMA_REL,
        "wave_manifest_hash": envelope["wave_manifest_hash"],
        "strict_success_hash": envelope["strict_success_hash"],
        "non_strict_canonical_digests": envelope["non_strict_canonical_digests"],
        "admission_stage": envelope["admission_stage"],
    }, indent=2))
    print("emit_wave1_promotion_envelope: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
