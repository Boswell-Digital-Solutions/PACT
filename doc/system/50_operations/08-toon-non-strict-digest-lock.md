# TOON Wave 1 Non-Strict Digest Lock
**Date:** 2026-04-17
**Time:** 22:45 UTC

## Purpose
Freeze exact canonical digests for the non-strict replay cases.

## Inputs
- `tests/fixtures/toon_wave1_replay_cases.json`
- `tests/fixtures/toon_wave1_non_strict_canonical_digests.json`

## Command
```bash
python3 scripts/verify_toon_non_strict_digest_lock.py
```

## Output
- `docs/evidence/toon_non_strict_digest_lock_report.json`

## Fail posture
If canonical semantics drift for the non-strict cases, the digest lock fails.
