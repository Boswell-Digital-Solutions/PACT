# TOON Wave 1 Promotion Packet
**Date:** 2026-04-17
**Time:** 21:25 UTC

## Purpose
Freeze the wave-1 proof state into a single operator-reviewable packet.

## Command
```bash
python3 scripts/verify_toon_promotion_packet.py
```

## Output
- `docs/evidence/toon_wave1_promotion_packet.json`

## Contents
The packet records the current hash and byte size for the core wave-1 evidence files, governance documents, registry, and registry schema.

## Fail posture
If any required evidence file is missing, or if an upstream verifier fails, the promotion packet build fails.

## Wave-1 promotion envelope
`scripts/emit_wave1_promotion_envelope.py` derives `docs/evidence/wave1_promotion_envelope.json` from the wave-1 manifest and this promotion packet. The schema is `99-contracts/schemas/wave1_promotion_envelope.schema.json`. `scripts/verify_wave1_promotion_envelope.py` re-derives the envelope and fails on any field, schema, or hash drift.

The envelope carries admitted TOON wave-1 serialization truth to downstream repositories, which consume it and never alter it. NeuroForge keeps a copy at `neuroforge_backend/promotion/mirror/pact_wave1_envelope_mirror.json`. The envelope promotes a serialization admission. It does not promote a model, a route, or a quality result.
