from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.verify_toon_non_strict_canonical import _canonical_projection, _digest  # noqa: E402
from runtime.engine import execute_slice_06  # noqa: E402


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    os.environ["PACT_ENABLE_TOON_WAVE1"] = "true"

    cases_path = REPO_ROOT / "tests" / "fixtures" / "toon_wave1_replay_cases.json"
    digests_path = REPO_ROOT / "tests" / "fixtures" / "toon_wave1_non_strict_canonical_digests.json"

    _assert(cases_path.exists(), "replay case fixture is missing")
    _assert(digests_path.exists(), "non-strict canonical digest fixture is missing")

    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    expected_digests = json.loads(digests_path.read_text(encoding="utf-8"))
    by_name = {case["name"]: case for case in cases}

    observed = {}
    for case_name, expected_digest in expected_digests.items():
        _assert(case_name in by_name, f"missing replay case for {case_name}")
        result = execute_slice_06(by_name[case_name]["request"])
        projection = _canonical_projection(result)
        digest = _digest(projection)
        observed[case_name] = {
            "projection": projection,
            "canonical_digest": digest,
        }
        _assert(digest == expected_digest, f"{case_name}: canonical digest drifted")

    out_dir = REPO_ROOT / "docs" / "evidence"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "toon_non_strict_digest_lock_report.json"
    out_path.write_text(
        json.dumps(
            {
                "expected_digests": expected_digests,
                "observed": observed,
                "all_green": True,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"report": str(out_path), "observed": observed}, indent=2))
    print("verify_toon_non_strict_digest_lock: PASS")


if __name__ == "__main__":
    main()
