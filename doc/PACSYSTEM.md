# PACT - Compiled System Reference

**Designation:** PAC
**Document role:** Canonical compiled technical reference for the PACT contract and runtime harness
**Source:** `doc/system/`
**Build command:** `bash doc/system/BUILD.sh`
**Document version:** 2.1 (2026-09-10) - flattened to one globally-numbered doc/system/NN-kebab-case.md sequence (01-20) per BDS Documentation Protocol v2.0 section 5.3, replacing the 2.0 numbered-subdirectory layout in which local per-section numbers collided across sections
**Protocol:** BDS Documentation Protocol v2.0; BDS Repo Documentation System Canonical Compliance Standard

> **Generated artifact warning:** `doc/PACSYSTEM.md` is assembled output. Edit
> the source modules under `doc/system/` and rebuild. Hand edits to the
> compiled artifact are overwritten by the next build.

Assembly contract:

- Command: `bash doc/system/BUILD.sh`
- Validation: `bash doc/system/validate_snapshots.sh` runs during assembly
- Primary output: `doc/PACSYSTEM.md`

This `doc/system/` tree is the canonical source of truth for PACT. It uses
explicit **truth classes**: canonical facts define repo role, authority
boundaries, contract behavior, runtime behavior, and verification doctrine;
snapshot facts are dated, audit-derived counts and current implementation
inventory that may drift between audits.

| Part | File | Contents |
| --- | --- | --- |
| §1 | `01-repo-identity.md` | Repo Identity |
| §2 | `02-scope-and-role.md` | Scope and Role |
| §3 | `03-service-contract.md` | Service Contract Surface |
| §4 | `04-receipt-serialization-evidence-strategy.md` | Receipt Serialization Evidence Strategy ADR |
| §5 | `05-runtime-topology.md` | Runtime Topology |
| §6 | `06-runtime-serialization-boundary.md` | Runtime Serialization Boundary ADR |
| §7 | `07-dependencies.md` | Dependencies |
| §8 | `08-governance-and-controls.md` | Governance and Controls |
| §9 | `09-toon-wave1-rollout-and-feature-flag.md` | TOON Wave 1 Rollout and Feature Flag ADR |
| §10 | `10-toon-extension-admission-policy.md` | TOON Extension Admission Policy |
| §11 | `11-operations-and-verification.md` | Operations and Verification |
| §12 | `12-toon-wave1-proof-gate.md` | TOON Wave 1 Proof Gate Operations Note |
| §13 | `13-toon-wave1-promotion-packet.md` | TOON Wave 1 Promotion Packet |
| §14 | `14-toon-ci-gate.md` | TOON Wave 1 CI Gate |
| §15 | `15-toon-replay-matrix.md` | TOON Wave 1 Replay Matrix |
| §16 | `16-toon-golden-hash-lock.md` | TOON Wave 1 Golden Hash Lock |
| §17 | `17-toon-non-strict-canonical-lock.md` | TOON Wave 1 Non-Strict Canonical Lock |
| §18 | `18-toon-non-strict-digest-lock.md` | TOON Wave 1 Non-Strict Digest Lock |
| §19 | `19-toon-wave1-manifest.md` | TOON Wave 1 Manifest |
| §20 | `20-appendix-repo-layout.md` | Appendix — Repo Layout Snapshot |

## Quick Assembly

```bash
bash doc/system/BUILD.sh
```

---

## 00. Repo Identity

### Purpose
PACT is the packet-and-control contract runtime that provides governed packet shaping, auditability, replay/live execution boundaries, deterministic evidence, and operator-facing export surfaces.

### Canonical identity
- Repository name: `PACT`
- Designation: `PAC`
- Canonical compiled artifact: `doc/PACSYSTEM.md`
- Source tree root: `doc/system/`
- Build entry: `doc/system/BUILD.sh`

### Documentation posture
This repo uses the canonical modular documentation posture where source truth is maintained under `doc/system/` and assembled into `doc/PACSYSTEM.md` through the governed build path.

---

## 01. Scope and Role

PACT is a governed internal runtime/service repo within the Forge workspace.

It currently proves and documents these responsibility areas:
- contract validation
- corpus validation
- runtime execution and degradation handling
- replay/live adapter behavior
- telemetry and evidence emission
- export manifests and replay packages
- control-plane catalog, detail, and handoff
- operator API boundary
- deterministic audit transfer bundles
- run-level indexing and audit packaging
- run-level export summary packaging

PACT is not canonical business truth and is not a generic free-running orchestrator. It is a bounded packet/runtime system with explicit audit and operator surfaces.

---

## 10. Service Contract Surface

### External contract families
PACT owns and enforces machine-readable contract surfaces under `99-contracts/`, including schema validation fixtures and operator-facing request/response shapes.

### Contract responsibilities
- packet schemas and packet-base rules
- runtime receipts
- degradation-state and serialization rules
- grounding and lineage artifacts
- operator API request/response contracts
- export/audit package manifest contracts

### Current proving posture
PACT is green through Slice 12 and has a verification chain that proves compatibility through layered slice verification scripts.

---

# Receipt Serialization Evidence Strategy ADR
**Date:** 2026-04-17
**Time:** 20:30 UTC

## Decision
Serialization evidence is carried as a governed nested object inside the runtime receipt.

## Why
Loose top-level fields create drift and weaken compatibility posture.
The nested object preserves requested profile, used profile, render attempt status, fallback status, artifact kind, segment metadata, and token estimates in one controlled contract.

## Consequences
- receipt evolution stays additive and understandable
- operators can inspect rendering behavior without reconstructing it from logs
- future wave extensions must preserve receipt simplicity

---

## 20. Runtime Topology

### Runtime lanes
Primary runtime ownership is expressed across these repo surfaces:
- `runtime/`
- `control-plane/`
- `adapters/`
- `telemetry/`
- `harness/`
- `scripts/`

### Behavioral posture
PACT executes with fail-closed validation, explicit degradation states, replay/live separation, deterministic artifact writing, and operator-readable evidence.

### Current verified runtime scope
The verified runtime path now includes:
- compile and validation flow
- retrieval and budget handling
- replay/live provider resolution
- telemetry and evidence bundles
- run indexing
- audit transfer packaging
- run export summary packaging

---

# Runtime Serialization Boundary ADR
**Date:** 2026-04-17
**Time:** 20:30 UTC

## Decision
PACT keeps model-bound rendering inside the runtime serialization boundary and does not let downstream consumers redefine packet truth.

## Why
The packet remains canonical truth.
The serializer produces a governed artifact form only after packet construction and validation complete.

## Consequences
- packet schemas remain the source of truth
- serializer logic is explicit and bounded
- fallback and fail-closed behavior stay inside runtime control
- downstream consumers may inspect artifacts without owning packet semantics

---

## 30. Dependencies

### Runtime and verification dependencies
PACT is intentionally lightweight, but verification and schema enforcement do require a small Python dependency set.

Repo-local dependency file:
- `requirements-dev.txt`

Current dependency set:
- `jsonschema`
- `referencing`
- `mypy`

### Local execution posture
Repo-local virtual environment usage is the preferred execution path for deterministic verification on Ubuntu systems that enforce externally managed system Python environments.

Expected local startup:
```bash
cd ~/Forge/ecosystem/pact
source .venv/bin/activate
---

## 40. Governance and Controls

### Governance posture
PACT is an internal business system component operating under governance-first design.

### Control expectations
- contract-first development
- deterministic verification
- explicit degradation handling
- evidence over assumption
- bounded operator API actions
- compatibility-sensitive slice layering

### Documentation compliance target
This repo is structured to satisfy the canonical repo documentation posture:
- `doc/system/`
- `doc/system/BUILD.sh`
- repo-class-aware subfolders
- compiled canonical root artifact at `doc/PACSYSTEM.md`

---

# TOON Wave 1 Rollout and Feature Flag ADR
**Date:** 2026-04-17
**Time:** 20:30 UTC

## Decision
TOON wave 1 ships behind `PACT_ENABLE_TOON_WAVE1`, default false.

## Why
Rollout must not outrun control.
Immediate disablement is required if determinism, receipt integrity, or renderer safety regresses.

## Consequences
- stage 1 supports internal implementation and proof only
- stage 2 allows shadow-mode inspection without production dependence
- stage 3 requires green proof gates before downstream reliance
- observability is required so the operator can measure requests, actual use, and fallback reasons

---

# TOON Extension Admission Policy
**Date:** 2026-04-17
**Time:** 21:10 UTC

## Decision
New TOON capability classes are not admitted by silent registry edits.

## Wave 1 allowed state
- capability class: `wave1_ranked_result_segment`
- admission stage: `wave1_internal`
- packet allow-list: `search_assist_packet` only
- field order: `rank`, `title`, `source_ref`, `summary`

## Required for any future extension
1. new schema or schema version if the row contract changes
2. updated loader validation
3. new verification script or expanded proof gate
4. new operator evidence example
5. explicit approval before repo gate accepts the change

## Fail posture
If the registry drifts from the admitted wave-1 state without the matching governance work, the extension governance proof must fail.

---


Replace this file:

`~/Forge/ecosystem/pact/doc/system/50_operations/00_operations_and_verification.md`

```md id="ehwxed"
## 50. Operations and Verification

### Standard operator workflow
1. enter repo root
2. activate `.venv`
3. install or refresh dependencies from `requirements-dev.txt`
4. run slice verification
5. run mypy
6. rebuild `doc/PACSYSTEM.md` after documentation edits

### Standard verification commands
```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/verify_slice_12.py
python3 -m mypy runtime scripts
bash doc/system/BUILD.sh
---

# TOON Wave 1 Proof Gate Operations Note
**Date:** 2026-04-17
**Time:** 20:55 UTC

## Purpose
Provide one operator-facing gate for the TOON wave-1 proving stack inside PACT.

## Gate command
```bash
python3 scripts/verify_toon_repo_gate.py
```

## What it proves
1. slice 01 boundary behavior is still green
2. slice 02 wave-1 governance behavior is still green
3. slice 03 observability behavior is still green
4. expected repo touchpoints still exist
5. expected evidence artifacts are present after the run

## Operator outputs
- `docs/evidence/toon_wave1_gate_report.json`
- `docs/evidence/toon_wave1_repo_map.md`

## Fail posture
Any failed sub-gate fails the repo gate.
Any missing expected file or artifact fails the repo gate.

---

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

---

# TOON Wave 1 CI Gate
**Date:** 2026-04-17
**Time:** 21:40 UTC

## Purpose
Add a repository-native GitHub Actions gate for the TOON wave-1 proof stack.

## Workflow file
- `.github/workflows/toon-wave1-gate.yml`

## Local verification
```bash
python3 scripts/verify_toon_ci_gate_files.py
```

## CI behavior
The workflow runs the repo gate and uploads evidence artifacts for operator inspection.

## Fail posture
If the workflow stops running the repo gate, or stops uploading evidence artifacts, the local CI gate file verifier must fail.

---

# TOON Wave 1 Replay Matrix
**Date:** 2026-04-17
**Time:** 22:00 UTC

## Purpose
Keep a fixture-driven replay matrix for the admitted wave-1 TOON cases.

## Inputs
- `tests/fixtures/toon_wave1_replay_cases.json`

## Command
```bash
python3 scripts/verify_toon_replay_matrix.py
```

## Output
- `docs/evidence/toon_replay_matrix_report.json`

## Fail posture
If any fixture case changes behavior outside the admitted expectations, the replay matrix proof fails.

---

# TOON Wave 1 Golden Hash Lock
**Date:** 2026-04-17
**Time:** 22:15 UTC

## Purpose
Freeze the admitted wave-1 replay outputs to exact artifact hashes.

## Inputs
- `tests/fixtures/toon_wave1_replay_cases.json`
- `tests/fixtures/toon_wave1_golden_hashes.json`

## Command
```bash
python3 scripts/verify_toon_golden_hashes.py
```

## Output
- `docs/evidence/toon_golden_hashes_report.json`

## Fail posture
If any admitted replay case changes artifact hash, the golden-hash proof fails.

---

# TOON Wave 1 Non-Strict Canonical Lock
**Date:** 2026-04-17
**Time:** 22:35 UTC

## Purpose
Add canonical semantic locking for the non-strict replay cases whose raw artifact hashes are not yet stable.

## Inputs
- `tests/fixtures/toon_wave1_replay_cases.json`
- `tests/fixtures/toon_wave1_non_strict_canonical_targets.json`

## Command
```bash
python3 scripts/verify_toon_non_strict_canonical.py
```

## Output
- `docs/evidence/toon_non_strict_canonical_report.json`

## Fail posture
If fallback or fail-closed semantics drift on admitted fields, the canonical lock fails even when raw artifact hashes are allowed to vary.

---

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

---

# TOON Wave 1 Manifest
**Date:** 2026-04-17
**Time:** 22:55 UTC

## Purpose
Assemble the final wave-level manifest after all proof, replay, governance, and digest locks are green.

## Command
```bash
python3 scripts/verify_toon_wave1_manifest.py
```

## Output
- `docs/evidence/toon_wave1_manifest.json`

## Contents
- strict success hash
- non-strict canonical digests
- registry admission snapshot
- replay cases
- artifact paths
- gate run list

---

## 99. Appendix — Repo Layout Snapshot

### Major repo areas
- `99-contracts/`
- `corpus/`
- `runtime/`
- `control-plane/`
- `adapters/`
- `telemetry/`
- `harness/`
- `scripts/`
- `docs/`

### Notes
This appendix is intentionally lightweight and should be expanded as the repo documentation system matures.
