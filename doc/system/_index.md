# PACT - Compiled System Reference

**Designation:** PAC
**Document role:** Canonical compiled technical reference for the PACT contract and runtime harness
**Source:** `doc/system/`
**Build command:** `bash doc/system/BUILD.sh`
**Document version:** 2.0 (2026-06-22) - canonical compliance migration
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
| §1 | `00_overview/00-repo-identity.md` | 00. Repo Identity |
| §2 | `00_overview/01-scope-and-role.md` | 01. Scope and Role |
| §3 | `10_service-contract/00-service-contract.md` | 10. Service Contract Surface |
| §4 | `10_service-contract/01-receipt-serialization-evidence-strategy.md` | Receipt Serialization Evidence Strategy ADR |
| §5 | `20_runtime/00-runtime-topology.md` | 20. Runtime Topology |
| §6 | `20_runtime/01-runtime-serialization-boundary.md` | Runtime Serialization Boundary ADR |
| §7 | `30_dependencies/00-dependencies.md` | 30. Dependencies |
| §8 | `40_governance/00-governance-and-controls.md` | 40. Governance and Controls |
| §9 | `40_governance/01-toon-wave1-rollout-and-feature-flag.md` | TOON Wave 1 Rollout and Feature Flag ADR |
| §10 | `40_governance/02-toon-extension-admission-policy.md` | TOON Extension Admission Policy |
| §11 | `50_operations/00-operations-and-verification.md` | 50. Operations and Verification |
| §12 | `50_operations/01-toon-wave1-proof-gate.md` | TOON Wave 1 Proof Gate Operations Note |
| §13 | `50_operations/03-toon-wave1-promotion-packet.md` | TOON Wave 1 Promotion Packet |
| §14 | `50_operations/04-toon-ci-gate.md` | TOON Wave 1 CI Gate |
| §15 | `50_operations/05-toon-replay-matrix.md` | TOON Wave 1 Replay Matrix |
| §16 | `50_operations/06-toon-golden-hash-lock.md` | TOON Wave 1 Golden Hash Lock |
| §17 | `50_operations/07-toon-non-strict-canonical-lock.md` | TOON Wave 1 Non-Strict Canonical Lock |
| §18 | `50_operations/08-toon-non-strict-digest-lock.md` | TOON Wave 1 Non-Strict Digest Lock |
| §19 | `50_operations/09-toon-wave1-manifest.md` | TOON Wave 1 Manifest |
| §20 | `99_appendices/00-appendix-repo-layout.md` | 99. Appendix — Repo Layout Snapshot |

## Quick Assembly

```bash
bash doc/system/BUILD.sh
```
