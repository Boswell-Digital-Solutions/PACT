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
