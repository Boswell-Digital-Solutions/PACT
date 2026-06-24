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
2. **packet_class admission — RE-FRAMED 2026-06-23 (not a ceiling).** The earlier
   note read this as a continuity "ceiling to lift." On inspection it is *correct
   scoping*, not a gap: NeuroForge's `promotion/mirror/pact_wave1_envelope_mirror.json`
   is a **PACT-owned, TOON wave-1** envelope (feature flag `PACT_ENABLE_TOON_WAVE1`,
   profiles `plain_text_with_toon_segment`) whose `allowed_packet_classes` is
   deliberately `[search_assist_packet]`. `continuity_findings_packet` is rightly
   excluded — wave-1 is not a continuity wave. Continuity cloud promotion, if ever
   wired, would be its **own** future promotion wave with its own envelope, NOT an
   edit to wave-1's allow-list. No change needed.
3. **Committed-fixture conformance — RESOLVED 2026-06-23.** Added a NeuronForge
   gate `tests/test_continuity_fixture_conformance.py` scoped to fixture *purpose*:
   curated `inputs/case-packets/*.json` must pass intake (the intentional
   `*-partial-lineage*` negative fixture is pinned to fail-closed), and every
   committed `outputs/*.envelope.json` finding is asserted to use only canonical
   enum values (ENUM MEMBERSHIP — not full-schema conformance, since the envelopes
   are immutable historical run artifacts). Adversarially proven (bogus enum →
   RED; corrupted input → RED). Vendored canonical, fail-closed.

## Deeper fix — first consumption slice (2026-06-23)

The drift gates make mirrors *loud*; the deeper fix *collapses* them by having
consumers IMPORT one source instead of hand-copying. First slice landed:

- **`pact-contracts`** (`ecosystem/pact/contracts_py/`) — a tiny zero-dependency,
  frozen-safe Python package owned by PACT (the continuity domain owner) exposing
  the six finding enums as frozensets. Pinned to `continuity_findings_packet.schema.json`
  by `99-contracts/tests/test_continuity_consumable_matches_schema.py` (the
  consumable can't drift from the schema).
- **NeuronForge consumes it**: `scripts/validate-continuity-candidate.py` now does
  `from pact_contracts.continuity import FINDING_TYPES as VALID_FINDING_TYPES, ...`
  instead of hand-defining the enum sets — verified the imported object IS the
  package's (`validator.VALID_FINDING_TYPES is pact_contracts.continuity.FINDING_TYPES`).
  Freeze-robust via a requirements path-dep + a static anchor import in
  `service/continuity_check_lane.py` (the validator is `importlib`-loaded). See
  `contracts_py/README.md` for the build-sidecar verify recipe.

Why PACT and not `forge_contract_core`: the latter is a **governed, RFC-gated
code/ops proving-slice** repo (`source_drift_finding`/`promotion`/`execution`
families, `code_fix_*` enums) — continuity is manuscript-domain, so it belongs
with its owner (PACT), not parked in a different-domain hub.

Consumers migrated so far:
- **NeuronForge validator** (Python) → imports `pact_contracts.continuity`.
- **AuthorForge api** (TS) → `continuity-findings.ts` enums are GENERATED from the
  vendored canonical schema (`generate:continuity-vocab` + `check:continuity-vocab-drift`),
  not hand-typed.

Remaining mirrors (next migrations): AuthorForge **frontend** union types
(`apps/frontend/src/lib/continuity/types.ts` — generate next), AuthorForge
**migration 036 SQL CHECKs** (SQL can't import → stays a gated mirror, by design),
the operator-copy validator/prompts, and NeuronForge's `continuity_pact_packet.py`
builder. All remaining mirrors stay protected by the drift gates meanwhile.

## Scope notes

- Whole-tree sweep was partly throttled; repos not exhaustively swept for *new*
  mirrors: forge-smithy, DataForge-Local, Forge_Command, Cortex, context-runtime,
  forgeHQ. `forge_contract_core` encodes **zero** continuity dimensions — and it
  should: it's a governed, RFC-gated **code/ops** proving-slice repo, the wrong
  domain for a manuscript contract. The continuity consumable lives with its owner
  (PACT) — see "Deeper fix — first consumption slice" above.
- These gate files are additive (tests + vendored schema copies + manifest). No
  production code changed.
