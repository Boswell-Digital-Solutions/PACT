# PACT — Known Issues

## doc/system defects found in the BDS-UMIEP-v0.1 review (Closed 2026-10-26) — PACT-DOC-DEFECTS-20261026

1. **Pasted chat text in part 11.** `doc/system/11-operations-and-verification.md` began with "Replace this file:", an old path (`doc/system/50_operations/...`) and a fence with a chat id (`md id="ehwxed"`). The inner code fence was not closed. Root cause: an instruction was pasted into the file with its content. Fix: the part holds only the section, and the fence is closed. The verification commands now include `verify_wave1_promotion_envelope.py`.
2. **Unclosed fence in part 07.** `doc/system/07-dependencies.md` ended inside a `bash` fence. Fix: the fence is closed.
3. **"runtime/service" in part 02.** `doc/system/02-scope-and-role.md` called PACT a "runtime/service repo". No service process exists: no HTTP server and no deployment. Fix: the part says that PACT is a library and command-line repo, and names how consumers use it.
4. **The wave-1 promotion envelope was not documented.** `scripts/emit_wave1_promotion_envelope.py`, its schema and its verifier had no `doc/system/` text. A reviewer read NeuroForge's copy of the envelope as model-promotion machinery. Fix: part 13 now describes the envelope and says that it promotes a serialization admission only.

**Status:** Closed. Scope: the four documentation defects.

## No test proves that a mutated packet fails equivalence (Open 2026-10-26) — PACT-NO-MUTATION-NEGATIVE-TEST-20261026

- **What is wrong**: the slice verifiers prove determinism (for example `scripts/verify_slice_07.py`, "replay package determinism mismatch"), and `packet_hash` is SHA-256 of canonical JSON (`runtime/compiler/packet_base_builder.py`). No test changes a packet and checks that the identity or equivalence check fails.
- **Effect**: a plan that depends on "a mutated packet fails equivalence" has no proof for it.
- **Fix**: none. A negative test needs its own authorization.
- **Status**: Open.
