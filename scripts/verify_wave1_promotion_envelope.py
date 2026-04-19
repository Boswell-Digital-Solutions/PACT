#!/usr/bin/env python3
"""Verify the wave-1 promotion envelope against PACT-owned source truth.

Re-derives the envelope from the manifest + promotion packet and asserts
field-by-field equality, schema conformance, and hash freshness.  Catches
any drift between the cached envelope and PACT's authoritative artifacts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import emit_wave1_promotion_envelope as emitter  # noqa: E402

ENVELOPE_PATH = emitter.ENVELOPE_PATH
SCHEMA_PATH = REPO_ROOT / emitter.ENVELOPE_SCHEMA_REL


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _validate_schema(envelope: dict, schema: dict) -> None:
    required = schema.get("required", [])
    for field in required:
        _assert(field in envelope, f"envelope missing required field: {field}")
    properties = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        for key in envelope:
            _assert(key in properties, f"envelope has unknown field: {key}")
    for field, value in envelope.items():
        spec = properties.get(field, {})
        expected_type = spec.get("type")
        if expected_type == "string":
            _assert(isinstance(value, str), f"{field}: expected string, got {type(value).__name__}")
        elif expected_type == "array":
            _assert(isinstance(value, list), f"{field}: expected array")
            if "minItems" in spec:
                _assert(len(value) >= spec["minItems"], f"{field}: minItems {spec['minItems']}")
            if spec.get("uniqueItems"):
                _assert(len(set(value)) == len(value), f"{field}: items must be unique")
        elif expected_type == "object":
            _assert(isinstance(value, dict), f"{field}: expected object")


def main() -> int:
    _assert(ENVELOPE_PATH.exists(), f"envelope not emitted yet: {ENVELOPE_PATH}")
    cached = json.loads(ENVELOPE_PATH.read_text(encoding="utf-8"))
    fresh = emitter.build_envelope()

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    _validate_schema(cached, schema)

    drift_keys = sorted(
        k for k in fresh if k not in {"generated_at", "source_commit"}
        and cached.get(k) != fresh[k]
    )
    _assert(
        not drift_keys,
        f"envelope drift detected on fields: {drift_keys}\n"
        f"cached={json.dumps({k: cached.get(k) for k in drift_keys}, sort_keys=True)}\n"
        f"fresh={json.dumps({k: fresh[k] for k in drift_keys}, sort_keys=True)}",
    )

    manifest = emitter._load(emitter.MANIFEST_PATH)
    _assert(
        cached["wave_manifest_hash"] == emitter._sha256(emitter.MANIFEST_PATH),
        "wave_manifest_hash does not match current manifest file",
    )
    _assert(
        cached["strict_success_hash"] == manifest["strict_success_hash"],
        "strict_success_hash drifted from manifest",
    )
    _assert(
        cached["non_strict_canonical_digests"] == manifest["non_strict_canonical_digests"],
        "non_strict_canonical_digests drifted from manifest",
    )
    _assert(
        cached["feature_flag_name"] == manifest["feature_flag"],
        "feature_flag_name drifted from manifest",
    )

    print(json.dumps({
        "envelope": str(ENVELOPE_PATH),
        "schema": str(SCHEMA_PATH.relative_to(REPO_ROOT)),
        "wave_manifest_hash": cached["wave_manifest_hash"],
        "strict_success_hash": cached["strict_success_hash"],
        "non_strict_canonical_digests": cached["non_strict_canonical_digests"],
        "admission_stage": cached["admission_stage"],
    }, indent=2))
    print("verify_wave1_promotion_envelope: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
