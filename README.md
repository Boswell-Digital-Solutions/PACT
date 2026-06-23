<h1 align="center">PACT</h1>

<p align="center">
  <strong>Packet Contracts. Controlled Runtime.</strong>
</p>

<p align="center">
  Governed packet shaping and evidence export for the Forge Ecosystem<br/>
  <em>Every packet validated. Every handoff auditable.</em>
</p>

<p align="center">
  <a href="#key-capabilities"><img src="https://img.shields.io/badge/status-internal_verification-success?style=flat-square" alt="Status" /></a>
  <img src="https://img.shields.io/badge/designation-PAC-blue?style=flat-square" alt="Designation" />
  <img src="https://img.shields.io/badge/runtime-Python_3-blue?style=flat-square" alt="Runtime" />
  <img src="https://img.shields.io/badge/docs-canonical_compliance_2.0-orange?style=flat-square" alt="Docs" />
  <img src="https://img.shields.io/badge/license-internal-lightgrey?style=flat-square" alt="License" />
</p>

<p align="center">
  <a href="#the-solution">Solution</a> -
  <a href="#key-capabilities">Capabilities</a> -
  <a href="#the-forge-ecosystem">Ecosystem</a> -
  <a href="#architecture">Architecture</a> -
  <a href="#verification">Verification</a> -
  <a href="#learn-more">Learn More</a>
</p>

---

## Documentation Contract

- **Repo type:** Governed internal runtime/service repo for packet contracts, runtime receipts, evidence, and operator export surfaces
- **Designation:** `PAC`
- **Authority boundary:** Packet/runtime contract behavior, receipt construction, serialization evidence, replay/live adapter boundaries, TOON proof gates, and bounded operator exports
- **Deep reference:** `doc/system/_index.md`, `doc/PACSYSTEM.md`
- **Assembled system reference:** `doc/PACSYSTEM.md` is the primary built system reference; edit `doc/system/` and rebuild
- **README role:** Product overview and operator entrypoint
- **Truth note:** Status badges, verification status, slice references, and implementation summaries in this README are snapshot facts unless explicitly marked as canonical doctrine or target values

---

## BDS Packet Doctrine

PACT is the packet contract, runtime boundary, and evidence-export subsystem for
the Forge ecosystem.

- **PACT packet schemas** define admissible packet, receipt, degradation, lineage, and export shapes.
- **PACT runtime code** constructs packets, validates schemas, records degradation, and emits deterministic receipts.
- **PACT evidence artifacts** prove what happened during replay/live execution and export packaging.
- **PACT is not canonical business truth.** Product truth, durable memory, customer state, and governance doctrine stay with their owning Forge systems.
- **PACT handoffs must be explicit.** Downstream consumers may inspect packet artifacts, but they do not redefine packet truth after validation.

---

## The Problem

AI systems move context through many boundaries: retrieval, pruning, packet
construction, serialization, model execution, receipts, export bundles, and
operator review. Without a governed packet layer, those boundaries drift.

The common failure modes are familiar:

- packet fields expand silently
- receipts stop matching runtime behavior
- replay and live paths diverge
- downstream systems treat derived artifacts as source truth
- audit bundles cannot prove how a run was shaped
- serialization choices become invisible compatibility risks

**The result?** Faster-looking pipelines that cannot prove what they carried,
why they degraded, or whether downstream consumers received the same contract
they were promised.

---

## The Solution

**PACT** gives the Forge ecosystem a contract-sensitive packet runtime: schemas,
fixtures, runtime validation, degradation reporting, replay/live separation,
TOON proof gates, and deterministic export surfaces in one bounded subsystem.

PACT exists to keep packet movement disciplined. It does not make broad
orchestration decisions. It builds, validates, records, and exports governed
packet evidence so other systems can operate from explicit contracts instead of
implicit payload habits.

> **Why this exists:** Context carriage is a control surface. PACT prioritizes
> packet identity, receipt integrity, fail-closed validation, and deterministic
> evidence over convenience shortcuts.

### Why a Separate Packet Runtime?

PACT is separate because packet truth should not be buried inside app workflow
code, model-provider glue, or product-specific orchestration.

- **Contracts stay inspectable** - JSON schemas and fixtures live under `99-contracts/`.
- **Runtime behavior stays bounded** - packet compilation, validation, degradation, and receipts live under `runtime/`.
- **Replay and live paths stay distinct** - adapters prove the handoff boundary instead of blending execution modes.
- **Evidence stays deterministic** - audit, handoff, run-index, and export packages are written as inspectable artifacts.

### Explicit Non-Goals

PACT is **not**:

- A generic LLM orchestrator
- A product workflow engine
- A canonical business database
- A replacement for DataForge, NeuroForge, Forge Command, SMITH, Rake, or customer systems
- A place to silently add packet fields because a downstream app wants them
- A transport layer that collapses local and cloud semantics into one vague path

These constraints are intentional and enforced through contracts, fixtures, and
verification scripts.

### Operating Assumptions

- Packet and receipt schemas are compatibility-sensitive.
- Identity, lineage, hashes, and carriage fields are high-risk surfaces.
- Degradation must be explicit, not inferred from logs after the fact.
- Replay/live behavior must remain distinguishable in receipts and evidence.
- TOON rendering must stay behind governed proof gates and admission controls.
- Documentation claims must stay aligned with the implementation and executable proof.

---

## Key Capabilities

<table>
<tr>
<td width="50%">

### Contract Validation

Schemas, valid fixtures, invalid fixtures, vendored schema sync checks, and
corpus linting prove packet families before runtime behavior depends on them.

</td>
<td width="50%">

### Packet Compilation

Runtime builders construct packet bases, answer packets, policy response
packets, search assist packets, safe failures, and receipts against locked
schema contracts.

</td>
</tr>
<tr>
<td width="50%">

### Degradation Control

Budget pressure, retrieval fallback, pruning/reranking limits, serialization
fallback, and safe-failure behavior are surfaced as explicit runtime state.

</td>
<td width="50%">

### Replay/Live Boundaries

Provider adapters separate deterministic replay from live execution and record
the resulting compatibility posture in receipts and evidence.

</td>
</tr>
<tr>
<td width="50%">

### Evidence Export

Telemetry, manifests, run indexes, handoff bundles, audit transfers, and run
export summary packages produce operator-readable proof artifacts.

</td>
<td width="50%">

### Operator API Surface

Bounded operator requests expose catalog, detail, audit transfer, handoff, run
index, and export summary package flows without turning PACT into a broad app
control plane.

</td>
</tr>
<tr>
<td width="50%">

### TOON Wave 1 Proof Gates

TOON rendering remains controlled through registry validation, feature-flag
posture, golden hashes, replay matrices, and non-strict canonical digest locks.

</td>
<td width="50%">

### Canonical Documentation

The modular `doc/system/` tree assembles into `doc/PACSYSTEM.md` and keeps repo
identity, runtime topology, governance, and operations in a governed reference.

</td>
</tr>
</table>

---

## The Forge Ecosystem

PACT sits between contract authors, runtime producers, model-facing paths, and
operator review surfaces. It keeps packet semantics explicit while other Forge
systems own their own authority domains.

```text
+-------------------------------------------------------------------+
|                                PACT                               |
|              Packet Contract and Evidence Runtime                 |
+-------------------------------------------------------------------+
|                                                                   |
|   +------------+   +------------+   +------------+   +----------+ |
|   |  Schemas   |   |  Runtime   |   |  Evidence  |   | Operator | |
|   |99-contracts|   | validation |   |  exports   |   | surfaces | |
|   +-----+------+   +-----+------+   +-----+------+   +----+-----+ |
|         |                |                |               |       |
|         +----------------+-------+--------+---------------+       |
|                                  |                                |
|                       Validated packet evidence                   |
|                                  |                                |
|        +--------------+----------+----------+--------------+      |
|        |              |                     |              |      |
|   DataForge      NeuroForge           Forge Command       SMITH   |
| durable truth    inference paths      operator review  governance |
|                                                                   |
+-------------------------------------------------------------------+
```

| System | Relationship to PACT |
|--------|-----------------------|
| **DataForge** | Owns durable ecosystem truth; may persist or retrieve evidence but does not delegate business truth to PACT. |
| **NeuroForge** | Consumes governed packet/runtime behavior at inference boundaries where packet contracts matter. |
| **Forge Command** | Presents operator-facing evidence and review surfaces; PACT provides bounded export artifacts, not broad operator control. |
| **SMITH** | Owns governance authority; PACT preserves contract and evidence boundaries under that governance posture. |
| **Rake and product apps** | May feed or consume context artifacts through explicit handoffs, but app workflow state remains outside PACT. |

---

## The Experience

PACT is intentionally quiet. The operator experience is a contract and evidence
workflow, not a dashboard.

### Operator Surfaces

| Surface | Purpose |
|---------|---------|
| `99-contracts/` | Inspect schemas, fixtures, registry files, and contract tests. |
| `harness/regression/` | Review slice cases and verification reports. |
| `harness/replay/` | Maintain deterministic replay contracts. |
| `harness/adversarial/` | Keep adversarial verification scope explicit. |
| `docs/evidence/` | Store TOON wave proof reports, promotion packets, and manifest artifacts. |
| `control-plane/` | Hold operator catalog, analysis, proposals, and rollout notes. |
| `doc/PACSYSTEM.md` | Read the assembled canonical system reference. |

### Design Principles

- **Contract-first behavior** - schema truth before runtime convenience.
- **Fail-closed validation** - invalid packets and receipts do not proceed silently.
- **Evidence over assumption** - proof artifacts matter more than narrative claims.
- **Compatibility-sensitive evolution** - additive change requires fixtures, reports, and governed admission.
- **Bounded operator actions** - exports and summaries are explicit, not hidden orchestration.

---

## Verification Record

The current assembled system reference records PACT as green through Slice 12.
Treat that as a snapshot fact and re-run verification before claiming release or
promotion evidence.

### Current Top-Level Gates

```bash
cd /home/charlie/Forge/ecosystem/pact
.venv/bin/python scripts/verify_slice_12.py
bash scripts/run_toon_repo_gate.sh
.venv/bin/python -m mypy runtime scripts
bash doc/system/BUILD.sh
git diff --check
```

### Slice Proof Chain

| Surface | Current proof entry |
|---------|---------------------|
| Contract, corpus, runtime, retrieval, adapter, evidence, and export layers | `scripts/verify_slice_12.py` |
| TOON repository gate | `bash scripts/run_toon_repo_gate.sh` |
| Static type pass | `.venv/bin/python -m mypy runtime scripts` |
| Canonical docs assembly | `bash doc/system/BUILD.sh` |
| Whitespace/diff hygiene | `git diff --check` |

---

## Architecture

PACT is a lightweight Python runtime with explicit filesystem-backed contract
and evidence surfaces.

```text
pact/
|-- 99-contracts/        # JSON schemas, fixtures, registry files, and contract tests
|-- adapters/            # App and provider adapter boundary notes
|-- control-plane/       # Operator analysis, proposal, rollout, and catalog surfaces
|-- corpus/              # Evaluation corpus manifests and case files
|-- doc/system/          # Canonical modular system documentation source
|-- doc/PACSYSTEM.md     # Generated assembled system reference
|-- docs/                # Plans, architecture notes, runbooks, and evidence
|-- harness/             # Regression, replay, adversarial, audit, and handoff assets
|-- runtime/             # Packet, retrieval, budget, receipt, export, and telemetry code
|-- scripts/             # Verification, lint, proof-gate, and export scripts
|-- src/                 # Shared package utilities
`-- tests/               # Test fixtures and replay cases
```

### Runtime Modules

| Area | Path | Responsibility |
|------|------|----------------|
| Intake | `runtime/intake/` | Request normalization and boundary shaping. |
| Compiler | `runtime/compiler/` | Packet base, packet compilation, and safe-failure builders. |
| Validation | `runtime/validation/` | Schema validation and packet validation errors. |
| Retrieval | `runtime/retrieval/` | Retrieval selection, pruning, and degradation behavior. |
| Budget | `runtime/budget/` | Class-budget enforcement and retry posture. |
| Rendering | `runtime/rendering/` | TOON rendering and registry-backed serialization behavior. |
| Receipts | `runtime/receipts/` | Runtime receipt construction and serialization evidence. |
| Export | `runtime/export/` | Control-plane, handoff, run-index, audit transfer, and summary exports. |
| Telemetry | `runtime/telemetry/` | Runtime telemetry emission. |

---

## Local Setup

```bash
cd /home/charlie/Forge/ecosystem/pact
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
```

---

## Documentation Assembly

The governed documentation source lives in:

```text
doc/system/
```

Build it with:

```bash
bash doc/system/BUILD.sh
```

The build emits:

```text
doc/PACSYSTEM.md
```

Do not hand-edit `doc/PACSYSTEM.md` for durable changes. Edit the corresponding
source module under `doc/system/` and rebuild.

---

## Learn More

- Canonical assembled reference: [`doc/PACSYSTEM.md`](doc/PACSYSTEM.md)
- Canonical source index: [`doc/system/_index.md`](doc/system/_index.md)
- Contract bundle: [`99-contracts/README.md`](99-contracts/README.md)
- Harness overview: [`harness/README.md`](harness/README.md)
- PACT working rules: [`GEMINI.md`](GEMINI.md)

---

## License

No repo-local license file is present in this checkout. Treat PACT as internal
Forge/BDS material unless a governed license file is added.
