from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _read_json(path: Path) -> dict:
    _assert(path.exists(), f"missing json artifact: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    os.environ["PACT_ENABLE_TOON_WAVE1"] = "true"

    evidence_dir = REPO_ROOT / "docs" / "evidence"

    required = {
        "gate_report": evidence_dir / "toon_wave1_gate_report.json",
        "observability_report": evidence_dir / "toon_observability_report.json",
        "extension_governance_report": evidence_dir / "toon_extension_governance_report.json",
        "promotion_packet": evidence_dir / "toon_wave1_promotion_packet.json",
        "replay_matrix_report": evidence_dir / "toon_replay_matrix_report.json",
        "golden_hashes_report": evidence_dir / "toon_golden_hashes_report.json",
        "non_strict_canonical_report": evidence_dir / "toon_non_strict_canonical_report.json",
        "non_strict_digest_lock_report": evidence_dir / "toon_non_strict_digest_lock_report.json",
        "repo_map": evidence_dir / "toon_wave1_repo_map.md",
        "operator_examples": evidence_dir / "toon_wave1_operator_examples.md",
    }

    for label, path in required.items():
        _assert(path.exists(), f"missing required artifact: {label} -> {path}")

    gate = _read_json(required["gate_report"])
    replay = _read_json(required["replay_matrix_report"])
    hashes = _read_json(required["golden_hashes_report"])
    canonical = _read_json(required["non_strict_canonical_report"])
    digest_lock = _read_json(required["non_strict_digest_lock_report"])
    extension = _read_json(required["extension_governance_report"])

    manifest = {
        "wave": "toon_wave1",
        "status": "green",
        "feature_flag": "PACT_ENABLE_TOON_WAVE1",
        "strict_success_hash": hashes["strict_cases"]["toon_success"],
        "non_strict_canonical_digests": {
            case_name: payload["canonical_digest"]
            for case_name, payload in digest_lock["observed"].items()
        },
        "registry": extension["registry"],
        "replay_cases": replay["cases"],
        "artifact_paths": {label: str(path) for label, path in required.items()},
        "gate_runs": gate["runs"],
    }

    out_path = evidence_dir / "toon_wave1_manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "report": str(out_path),
                "strict_success_hash": manifest["strict_success_hash"],
                "non_strict_canonical_digests": manifest["non_strict_canonical_digests"],
                "gate_run_count": len(manifest["gate_runs"]),
            },
            indent=2,
        )
    )
    print("verify_toon_wave1_manifest: PASS")


if __name__ == "__main__":
    main()
