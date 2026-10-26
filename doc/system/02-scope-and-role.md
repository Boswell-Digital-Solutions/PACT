## 01. Scope and Role

PACT is a governed internal runtime library and command-line repo within the Forge workspace. It runs no service process: there is no HTTP server and no deployment. A consumer imports the runtime in-process (forgeHQ `app/drivers/pact_client.py`) or runs its scripts. `scripts/operator_api.py` is a command-line entry point.

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
