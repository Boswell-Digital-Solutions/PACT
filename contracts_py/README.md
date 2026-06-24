# pact-contracts

The **importable consumable form** of PACT's cross-repo contracts. PACT owns the
continuity contract (`99-contracts/schemas/continuity_findings_packet.schema.json`
is the SSOT); this package exposes that vocabulary as plain Python so downstream
repos **consume it instead of hand-mirroring** the enum values.

This is the first slice of the "deeper drift fix": collapse per-repo mirrors into
one consumable owned by the domain authority.

## What's here

- `pact_contracts/continuity.py` — the consumable continuity vocabulary:
  - the six finding **enum** value sets as frozensets (`FINDING_TYPES`,
    `SCOPE_TYPES`, `SPAN_ROLES`, `CONFIDENCES`, `CANDIDATE_STATES`,
    `SEVERITY_HINTS`) — consumed by *validators*;
  - the structural **key** vocabulary as ordered tuples (`FINDING_KEYS`,
    `SPAN_KEYS`, `LINEAGE_KEYS`) — the allowed property keys under the schema's
    `additionalProperties: false`, consumed by the producer-side *packet builder*
    to project onto; and
  - `CANDIDATE_UNREVIEWED` — the candidate-only invariant value (a member of
    `CANDIDATE_STATES`).
  Pure-Python literals (no runtime JSON read) so the package bundles cleanly
  into frozen (PyInstaller) sidecars.

Zero runtime dependencies, by design.

## Authority + drift protection

The values are **pinned to the locked schema** by a gate in PACT:
`99-contracts/tests/test_continuity_consumable_matches_schema.py` asserts each
frozenset == the corresponding enum in `continuity_findings_packet.schema.json`.
A schema change fails that gate until the consumable is updated — and that single
update then propagates to every importer (no per-repo enum edits).

## Consumers

| Repo | What it consumes | How |
|------|------------------|-----|
| NeuronForge (apps copy) | `scripts/validate-continuity-candidate.py` `VALID_*` enums | `from pact_contracts.continuity import FINDING_TYPES as VALID_FINDING_TYPES, ...` |
| NeuronForge (apps copy) | `service/continuity_pact_packet.py` projection keys + candidate-only value | `from pact_contracts.continuity import FINDING_KEYS, SPAN_KEYS, LINEAGE_KEYS, CANDIDATE_UNREVIEWED` |
| neuronforge-local-operator | `scripts/validate-continuity-candidate.py` `VALID_*` enums | same import as the apps copy (path-dep `../../pact/contracts_py`) |

AuthorForge (TS) consumes the same canonical schema via codegen rather than this
Python package (`bun run generate:continuity-vocab`, drift-gated). The only
remaining mirror is migration 036's SQL `CHECK` constraints, which SQL cannot
import — it stays a **gated** mirror by design.

## Freeze / sidecar bundling

NeuronForge ships as a frozen (PyInstaller) Tauri sidecar. Two things make the
bundle work:

1. **requirements.txt path-dep** (`../../../ecosystem/pact/contracts_py`) — the
   freeze venv installs the package, so PyInstaller can bundle it. Assumes the
   Forge repos are colocated (which `apps/Author-Forge/scripts/build-sidecar.sh`
   already assumes). Git-dep alternative if not colocated at freeze time:
   `pact-contracts @ git+ssh://git@github.com/Boswecw/PACT@<ref>#subdirectory=contracts_py`.
2. **Static anchor import** — the validator is loaded via `importlib` at runtime,
   so a freeze tool's static analysis can't see its `pact_contracts` import.
   `service/continuity_check_lane.py` (imported by `service.main`) carries a
   statically-reachable `import pact_contracts.continuity` so the package is
   bundled regardless. (The packet builder `service/continuity_pact_packet.py`,
   imported by the lane, now also imports `pact_contracts` statically — a second
   reachable path — but the explicit anchor is kept so the guarantee does not
   silently depend on the builder's import staying in place.)

### Verify the frozen sidecar bundles it (run on a real build)

```bash
# 1. Freeze the NeuronForge sidecar (from the Author-Forge checkout):
cd apps/Author-Forge && ./scripts/build-sidecar.sh --with-neuronforge

# 2. Confirm the frozen binary can import the package + load the validator:
BIN=apps/Author-Forge/src-tauri/binaries/neuronforge-local-*   # or packaging/dist
#    Smoke the running sidecar's continuity lane, OR (PyInstaller onedir) grep the
#    bundle for the module:
#      ls <frozen>/_internal/pact_contracts/continuity.py
# 3. Functional check: POST a continuity_check task to the running sidecar and
#    confirm it does NOT fail with ModuleNotFoundError: pact_contracts.
```

If the freeze venv didn't install requirements (so the package is missing), the
lane fails closed at validate time — visible, not silent.

## Dev install

```bash
# into the NeuronForge .venv (runtime), or any consumer env:
pip install -e ecosystem/pact/contracts_py
# gates that also need jsonschema/referencing can run with an interpreter that has
# them, e.g.: PYTHONPATH=ecosystem/pact/contracts_py python3 -m pytest ...
```
