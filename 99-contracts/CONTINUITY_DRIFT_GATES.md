# Continuity Contract — Drift Gates

Step 1 of the "deeper drift fix": the continuity contract is mirrored across many
repos/languages (no shared package yet), so these gates make any silent divergence
a **loud CI failure**. They do NOT move code or add codegen — that's later.

## Canonical SSOT

`ecosystem/pact/99-contracts/schemas/continuity_findings_packet.schema.json`
(+ `$ref` siblings `packet_base`, `grounding_ref`, `source_lineage_digest`,
`serialization_profile_enum`). It is the only machine-readable artifact encoding
every dimension at once, lives in the neutral contract repo, and every consumer's
code already names it as "the locked schema."

## The gate set (7 gates, all adversarially proven to catch injected drift)

| Repo | Gate | Guards |
|------|------|--------|
| pact | `tests/test_continuity_contract_selfconsistency.py` | freezes the 6 enums + packet_class + lineage names + grounding `authority_class`; `review_state==candidate_state`; structural locks (`additionalProperties:false`, `unevaluatedProperties:false`); valid fixtures pass / invalid fail |
| pact | `tests/test_vendored_schema_sync.py` | **cross-repo sync**: every vendored copy is sha256-identical to upstream; every canonical schema has a consumer; no unregistered vendored copy |
| AuthorForge | `apps/api/src/contracts/__tests__/continuity-contract-drift.test.ts` | api const arrays + frontend union types + `036_continuity_findings.sql` CHECKs + **the inline duplicate SQL in `migrationManifest.ts`** (two-copies hazard) + decision-action enum + lineage all-or-nothing |
| NeuronForge | `tests/test_continuity_contract_drift.py` | `validate-continuity-candidate.py` `VALID_*` + v1/v2/v3 prompt enum blocks + schema-doc enums + builder output round-trips the schema + `_FINDING_KEYS/_SPAN_KEYS/_LINEAGE_KEYS` == schema-allowed keys |
| neuronforge-local-operator | `tests/test_continuity_contract_drift.py` | mirror of NeuronForge gate (separate git remote — independent copies of validator/prompts/doc); also cross-checks they still match the apps/ copy |
| NeuroForge | `tests/test_lineage_contract_drift.py` | lineage triple in `context_lineage.py` + `model_router.py` (dedup) + `LineageIdentifiers`; **pins** the `sha256:[0-9a-f]{64}` strictness rule |
| PCC | `tests/lineage_boundary_test.rs` | `ContextBundleManifest`/`ContextAssemblyRequest` fields; encodes the `bundle_hash`↔`context_bundle_hash` rename |

Vendored copies are registered in `VENDOR_MANIFEST.json` (relative to ecosystem
root; override with `FORGE_ECOSYSTEM_ROOT`). The two-tier design: per-repo gates
assert the local mirror == its vendored copy; the sync verifier asserts every
vendored copy == upstream pact (catches "pact changed, repo didn't re-vendor").

Run all: see each row's path. Python gates use system `python3` (has
jsonschema+referencing+pydantic; some repo `.venv`s do not). NeuroForge uses its
own venv. AuthorForge uses `bun test`. PCC uses `cargo test`.

## False-friends the gates deliberately do NOT conflate

- AuthorForge `continuity_finding_decisions.decision` = `[review,retain,reject,promote]` — a decision-action vocab, **not** `candidate_state`.
- NeuroForge MAID `authority_class` = `[official_source,weighted_adjacent,advisory_only]` — **not** the grounding `authority_class` `[primary,secondary,derived]`.
- PCC `bundle_hash` **is** pact's `context_bundle_hash` (intentional rename across the PCC→pact boundary) — not drift.
- continuity `confidence` is the 3-value enum `[low,moderate,high]` — not BugCheck's float confidence.
- prompt `schema_version` `1.0` (candidate-output doc) ≠ pact packet `schema_version` `1.0.0` — different namespaces.

## Existing drift found: NONE

All 6 enums are byte-identical and identically ordered across every mirror today.
The surface is currently converged; these gates keep it that way.

## Latent hazards surfaced (NOT drift in the mirrors — flagged for when continuity goes cross-service)

1. **Lineage hash strictness mismatch — RESOLVED 2026-06-23 (consumer-relax).**
   `context_bundle_hash` is an opaque upstream identity (PCC FNV-1a-64, 16 hex),
   not a NeuroForge-minted digest. NeuroForge's `LineageIdentifiers` previously
   demanded `^sha256:[0-9a-f]{64}$` and would have **rejected** the real producer
   output; it is now aligned to pact's canonical floor (`minLength 8`) and imposes
   no stricter format on this upstream-owned field. NeuroForge's **own** integrity
   hashes (`wave_manifest_hash`/`strict_success_hash`) keep `sha256:64hex`, pinned
   separately. pact/PCC/AuthorForge unchanged (canonical stays `minLength 8`). The
   NeuroForge gate now pins the alignment + the retained integrity strictness.
2. **packet_class admission ceiling (real, latent).** pact enumerates
   `continuity_findings_packet`, but NeuroForge's wave-1 promotion mirror
   (`promotion/mirror/pact_wave1_envelope_mirror.json`) admits only
   `search_assist_packet`. A continuity packet promoted to the cloud seam is not
   admitted today — by design (continuity is local-only), but a ceiling to lift
   when continuity promotion is wired.
3. **Unvalidated committed fixtures (gate-coverage gap).** NeuronForge
   `outputs/*.envelope.json` and `inputs/case-packets/*.json` embed literal enum
   values from real model runs; no gate validates them against the schema. A
   stale/invalid committed fixture would not be caught by the mirror gates.
   **Recommended follow-on:** a fixture-conformance gate validating committed
   envelopes against the candidate schema (kept separate, since these are runtime
   data, not contract mirrors, and may carry legitimate edge cases).

## Scope notes

- Whole-tree sweep was partly throttled; repos not exhaustively swept for *new*
  mirrors: forge-smithy, DataForge-Local, Forge_Command, Cortex, context-runtime,
  forgeHQ. `forge_contract_core` currently encodes **zero** continuity dimensions —
  if it is meant to be the contract registry, that absence is itself the next
  structural step (the "deeper fix" proper: consume the hub instead of mirroring).
- These gate files are additive (tests + vendored schema copies + manifest). No
  production code changed.
