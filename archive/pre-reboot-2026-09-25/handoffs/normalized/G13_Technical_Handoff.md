<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G13_Technical_Handoff.docx
original_sha256: 34cc4caea8fdf9902bd04f14701660f5942c6f12ef3901d50164523330302194
derivative_filename: G13_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

G13
# Distributed and Checkpointed Exact-Compute Platform
Technical Handoff — Frozen Closeout
12 August 2026 | G13.R1
| FROZEN VERDICT — CORE PLATFORM PASS; ROADMAP G13 ADVANCE GATE HELD AT THE MANDATORY G12 REPLAY<br>G13 built and stress-tested the content-addressed manifest, checkpoint, restart, retry, deterministic-merge and repartitioning machinery. The engineering reference passes every accepted determinism and hostile-mutation test. However, the exact G12_Final_Rules_Reference_Bundle.zip bytes required by the G12 Successor Contract were not retrievable from File Library into the active runtime. G13 therefore does not claim the mandatory G12 reference replay, does not claim the full G13 roadmap advance condition, and does not unlock G17. G14 may still proceed sequentially because the roadmap permits proof-store work in parallel, but it inherits this explicit acceptance exception. |
| --- |
# 0. Executive freeze
| Gate / object | Frozen result | Claim class |
| --- | --- | --- |
| Programme number | G13 — Distributed and Checkpointed Exact-Compute Platform | Sequential programme identity |
| G13 compute contract | G13.COMPUTE.CONTRACT.v1 frozen | Engineering specification |
| Engineering reference | 65,536 exact synthetic game states; 2,048 independent components × 32 nodes | Exact finite engineering test; not chess truth |
| Partition/retry campaign | 4, 4-kill/restart, 7, 11 and fresh 13 partitions all converge to identical merged bytes | Deterministic reproduction |
| Frozen truth hash | 00dde19eddcdf236cad2ce5fbfe115c1951d84b52e7224d230095c904bd03d85 | Exact engineering artifact hash |
| Frozen certificate hash | 5594391149c4464d63811741d90969d1bbe5bbc43a20c39a2e47eb30eb687da7 | Exact engineering artifact hash |
| Independent reference replay | 65,536 states; 0 truth/certificate mismatches; 0 Bellman/index mismatches | Independent structural verification |
| Hostile failure injection | 5/5 malformed/corrupt cases rejected | Adversarial engineering test |
| Mandatory G12 replay | BLOCKED — required bundle bytes unavailable in active runtime | Input/provenance frontier; no reconstruction |
| Roadmap G13 advance | NOT FULLY MET; G17 remains blocked | Programme gate status |
# 1. Authority, numbering and source precedence
The immediately preceding completed programme is G12, so the sequential programme is G13. The permanent G9 roadmap assigns G13 the mission of making exact solving resumable, deterministic and multi-machine before larger state growth makes single-session runs fragile. G12 strengthens that mission with a mandatory acceptance baseline: the frozen G12 reference suite must survive worker kill/restart, repartitioning and retry with identical truth/certificate hashes and canonical artifacts.
| Priority | Artifact / authority | Use in G13 |
| --- | --- | --- |
| 1 | G9_G10_Onwards_Long_Range_Plan.docx | Permanent dependency architecture, G13 mission, advance/stop rule and G14 successor mission. |
| 2 | G12_Technical_Handoff.docx | Immediate frozen technical state and binding G13 Successor Contract. |
| 3 | G12_Final_Rules_Reference_Bundle.zip, expected SHA-256 7641e0f8…d5695c | Mandatory machine acceptance dependency. Its hash/inventory were recoverable from frozen records; its bytes were not retrievable into this runtime. |
| 4 | No older handoff | No older artifact was required by the G12 Successor Contract for G13 unless a deliberate G7 scale benchmark was chosen; none was needed. |
# 2. Reconstructed inherited frozen state
G12 had already established the final-rule small-arena anchor layer: G10.RULES.v1.0 remains the semantic rules authority; G12.STATE.SERIAL.v2 is the forward canonical state/serialization profile; KQK, KRK and continuation-aware a-file KPK have exact clean-root W/D/rank certificates; same-colour K+2B vs K has an exact DEAD theorem; history-decorated controls prove that board-only identity is unsafe; and a standalone verifier replayed the frozen tables with zero accepted Bellman/rank mismatch. G12 also preserved the historical failure to recover the original G10 machine payload rather than rewriting provenance.
| Inherited object | Frozen status retained in G13 |
| --- | --- |
| G10.RULES.v1.0 | Unchanged semantic rules authority. |
| G12.STATE.SERIAL.v2 | Forward canonical artifact profile; G13 does not supersede it. |
| G12 final-rule reference suite | Authoritative deterministic acceptance target once machine bytes are available. |
| Original G10 byte/vector chain | Still broken/unrecovered historically; G13 does not heal or alias it. |
| G12 exact chess results | Inherited exact finite-arena truth; G13 performs infrastructure work, not new chess outcome solving. |
| Initial-position connection | Still absent. No G13 result changes START_REACHABLE status or proves White non-loss. |
# 3. G13.0 — dependency recovery and acceptance ruling
Before accepting any distributed replay claim, G13 searched File Library for the exact G12 bundle name, its component filenames and its recorded SHA-256. The frozen handoff and closeout checksum file are retrievable and agree that G12_Final_Rules_Reference_Bundle.zip should hash to 7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c. The bundle payload itself was not exposed as retrievable bytes in the active runtime, and a filesystem search found no surviving copy.
| PROVENANCE / INPUT RULING<br>G13 will not reconstruct the mandatory G12 payload from prose, known checksums or reported result counts. Such a reconstruction could test a new implementation, but it could not establish that the exact frozen G12 machine reference survived checkpoint/distributed replay. G13_G12_Baseline_Status.json therefore freezes BLOCKED_INPUT_UNAVAILABLE. |
| --- |
# 4. G13.1 — content-addressed compute contract
G13.COMPUTE.CONTRACT.v1 separates semantic problem identity from execution topology. This is the central design decision: changing the number of workers or partitions must not rename the mathematical problem or the accepted truth object.
| Object | Frozen identity / rule | Why it matters |
| --- | --- | --- |
| Problem manifest | SHA-256 of canonical JSON semantic problem declaration. Partition count is excluded. | The same exact problem has one identity across worker layouts. |
| Execution plan | Problem hash + immutable shard ranges + execution-order metadata. | Execution provenance is recorded without contaminating truth identity. |
| CAS object | SHA-256 of raw object bytes. | Payload corruption is detectable and objects are immutable by address. |
| Checkpoint | Problem hash + plan hash + shard/range + next cursor + partial truth/certificate object hashes. | A checkpoint cannot be silently resumed under a different problem or partition plan. |
| Shard result | Range + content hashes of exact shard truth/certificate bytes. | Retries are accepted by content identity rather than worker identity. |
| Merge | Strict ascending range coverage; gaps and overlap rejected; object hashes rechecked. | Arrival order cannot change accepted result bytes. |
# 5. G13.2 — checkpoint, retry and worker protocol
- Workers are fresh processes. They receive only the immutable problem manifest, execution plan, CAS location, shard id and checkpoint location; no process-local solver state is part of accepted identity.
- Checkpoints are written by first content-addressing the partial payloads and then atomically replacing the checkpoint JSON. A worker may lose work after the last checkpoint; resumed work is recomputed from the last durable cursor.
- A completed shard may be retried from its terminal checkpoint. The accepted result JSON must be byte-identical; worker name, attempt number and completion order are intentionally excluded from the proof identity.
- The current implementation uses a filesystem CAS and independent CLI workers. This is a multi-machine-capable protocol boundary, not a claim that this session physically used separate computers: manifests and CAS objects can be copied/shared to remote nodes without changing accepted identity.
# 6. G13.3 — exact engineering reference workload
Because the mandatory G12 bundle bytes were unavailable, G13 froze a separate engineering reference solely to test the infrastructure. It is deliberately labelled non-chess. The problem contains 2,048 independent deterministic exact-game components with 32 acyclic minimax nodes each, for 65,536 states. Every node has deterministic side-to-move, terminal facts and lower-index children derived from the problem seed. Exact W/D/L-from-White and rank values are therefore finite, reproducible and independently replayable.
| Quantity | Frozen value |
| --- | --- |
| Semantic problem hash | 08f4960faf6b2d5e4d0a93c620373566226dea436318a6da3b5e2022656c9a0d |
| Components | 2,048 |
| Nodes per component | 32 |
| Total states | 65,536 |
| Merged truth bytes | 458,752 |
| Merged certificate bytes | 589,824 |
| Frozen truth SHA-256 | 00dde19eddcdf236cad2ce5fbfe115c1951d84b52e7224d230095c904bd03d85 |
| Frozen certificate SHA-256 | 5594391149c4464d63811741d90969d1bbe5bbc43a20c39a2e47eb30eb687da7 |
Boundary: these are exact results about the G13 engineering test graph. They are not chess tablebase states, do not extend the G12 chess basin, and contribute no direct theorem about the standard initial position.
# 7. G13.4 — kill/restart, repartitioning and deterministic merge campaign
| Scenario | Parts | Completion order | Truth hash | Cert hash | Stress |
| --- | --- | --- | --- | --- | --- |
| A_baseline_4 | 4 | forward | 00dde19eddcdf236… | 5594391149c4464d… | baseline |
| B_kill_restart_4 | 4 | even-odd | 00dde19eddcdf236… | 5594391149c4464d… | controlled kill + checkpoint resume |
| C_repartition_7 | 7 | reverse | 00dde19eddcdf236… | 5594391149c4464d… | baseline |
| D_repartition_retry_11 | 11 | even-odd | 00dde19eddcdf236… | 5594391149c4464d… | completed-shard duplicate retry |
| E_fresh_13 | 13 | reverse | 00dde19eddcdf236… | 5594391149c4464d… | fresh reproduction |
All five executions produced the same full truth and certificate hashes. In the kill/restart campaign, shard 1 was deliberately terminated with return code 99 at component 632 after 120 components of that launch; the durable checkpoint snapshot hashes to e811ad98236d585f0eb94f0960e5c351be9f1d3b3f635777ebea6a382879b2d9. Restart from the last checkpoint converged to the baseline bytes. In the 11-partition campaign, a completed shard result was deleted and regenerated from its terminal checkpoint; its result JSON was byte-identical before and after retry.
# 8. G13.5 — independent replay and hostile failure injection
A separate verifier implementation decodes the merged engineering certificate and independently reconstructs every node obligation. It checked 65,536 states with zero truth/certificate disagreement and zero Bellman/index mismatch.
| Adversarial test | Accepted behavior |
| --- | --- |
| plan_problem_hash_mismatch | REJECTED as required |
| cross_plan_checkpoint_reuse | REJECTED as required |
| missing_shard_blocks_merge | REJECTED as required |
| overlap_blocks_merge | REJECTED as required |
| cas_tamper_detected | REJECTED as required |
The hostile suite covers a problem/plan hash mismatch, reuse of a checkpoint under a different execution plan, a missing shard at merge, an overlapping shard plan, and deliberate mutation of a content-addressed object. All five were rejected. No unexplained nondeterministic merge or hidden result-bearing process state was observed in the accepted campaign.
# 9. New reusable capabilities created by G13
| Object / capability | What is now available | Likely downstream use |
| --- | --- | --- |
| G13.COMPUTE.CONTRACT.v1 | Versioned separation of semantic problem identity, execution plans, checkpoints, shard results and CAS objects. | G14 proof store; G17 scale jobs; G18 raw truth carrier. |
| Deterministic range scheduler | Fresh-process workers, explicit immutable ranges, completion-order-independent merge. | Multi-node exact solves without result identity depending on worker layout. |
| Checkpoint/resume protocol | Atomic checkpoint commit over content-addressed partial payloads with exact plan/range identity checks. | Long-running G17+ jobs; failure recovery. |
| Retry idempotence | Completed shard replay from terminal checkpoint returns byte-identical result metadata and payload hashes. | At-least-once schedulers and worker loss. |
| G12 adapter / gate | Exact expected bundle and component hashes are encoded; payload is accepted only on exact hash match. | Immediate closure when the frozen G12 bundle bytes become retrievable. |
| G14 projection | Lossless field map for semantic version, source, arena/problem, truth, certificate, dependency and supersession identity. | Prevents G14 from baking partition topology into proof identity. |
# 10. Negative results, blockers and non-claims
- The mandatory G12 machine reference replay was not performed. Known G12 result counts and hashes are not a substitute for the exact input bytes.
- G13 therefore does not meet the full G12 Successor Contract acceptance baseline and does not unlock G17.
- The engineering reference is not chess truth and must never be counted as an enlarged solved chess basin.
- The session demonstrated independent subprocess workers on one host, not a physical multi-host cluster deployment. The protocol is multi-machine-capable because accepted identity is file/manifest/CAS based; physical cluster orchestration remains an implementation deployment detail.
- G13 does not supersede G12.STATE.SERIAL.v2, does not repair the historical missing G10 payload, does not create a durable proof repository (G14), and does not shrink the trusted verifier core (G15).
- No new initial-position reachability or White-non-loss result was established.
# 11. Corrections and supersessions within G13
Two engineering defects were found and corrected before freeze. First, the initial reference child-selection loop could cycle forever when a requested fanout exceeded the distinct residues obtainable from the fixed digest-byte cycle; it was replaced by a guaranteed-unique deterministic consecutive-child rule. Second, the first duplicate-retry test changed result JSON solely because a terminal checkpoint was rewritten with an incremented checkpoint sequence. The worker was corrected so an already-complete terminal checkpoint is reused rather than rewritten. After both fixes, the full campaign, independent replay and hostile suite were rerun from scratch and the frozen hashes above were produced. No pre-fix output is accepted.
# 12. Artifact inventory and verification status
| Artifact | SHA-256 (prefix) | Role |
| --- | --- | --- |
| G13_Compute_Contract_v1.json | 030930d52931d8d9346d… | Compute/checkpoint/CAS identity specification. |
| g13_platform.py | 251989338b314ab3804b… | Reference scheduler, worker, checkpoint, CAS and deterministic merge implementation. |
| g13_reference_campaign.py | 6044286ad3111b681863… | Kill/restart/repartition/retry/fresh-process campaign. |
| g13_reference_verifier.py | 091a50337700f40e3c03… | Independent structural verifier for the engineering reference certificate. |
| g13_failure_injection.py | 343c22e18f30d8dbda5d… | Hostile identity/merge/CAS mutation tests. |
| g13_g12_adapter.py | 1cc4bd229964f40d28fe… | Exact G12 bundle hash/inventory gate; refuses reconstruction. |
| G13_Reference_Campaign_Ledger.json | 5e88a8880692cc25fe70… | Authoritative deterministic-campaign results. |
| G13_Reference_Verification_Ledger.json | 2bc6a60db751209db7cc… | Zero-mismatch independent replay ledger. |
| G13_Failure_Injection_Ledger.json | b62c92ab23ca2c06f6d6… | 5/5 hostile cases rejected. |
| G13_G12_Baseline_Status.json | 59df1bbaf7dd0a550e97… | Frozen mandatory-input blocker. |
| G13_Freeze_Manifest.json | 4097ff1a7850dbfd0f38… | Machine-readable G13 freeze authority. |
| G13_Distributed_Compute_Bundle.zip | 584a22452cdbc6b296e2… | Portable frozen machine bundle containing the accepted contract, sources, ledgers, representative plans, checkpoint snapshot and reference truth/certificate. |
# 13. Implications for the G9 roadmap
| Roadmap stage | G13 close implication |
| --- | --- |
| G13 | Core engineering architecture passes its own deterministic and hostile tests, but the stage advance gate is held because the exact G12 reference bundle replay is unperformed. |
| G14 | May proceed sequentially: roadmap dependencies permit G14 in parallel after G11. It should ingest G13 identities losslessly and preserve the G13 acceptance exception as a first-class provenance state. |
| G15 | Still requires G10-G14; because G13 is not fully accepted and G14 is not yet built, G15 remains blocked. |
| G17 | Explicitly NOT unlocked. Before nine-/ten-man scaling is authoritative, the exact G12 bundle must be recovered and pass the G13 kill/restart/repartition baseline. |
| G18+ | The CAS/result separation is useful infrastructure but does not itself constitute a raw exact-truth carrier or proof store. |
# 14. Current position at G13 close
| FROZEN CLOSE POSITION<br>The project now has a concrete content-addressed distributed-compute contract, independent fresh-process workers, durable checkpoints, strict resume identity, idempotent retry, deterministic range merge, corruption detection, a reproducible exact engineering reference and a G14-compatible identity projection. The new machinery survived controlled worker loss, changed completion order and three different repartitionings without changing accepted result bytes. The remaining blocker is external to the new core logic but still binding: the exact frozen G12 machine bundle was not retrievable, so the required chess-reference acceptance replay remains open. |
| --- |
# 15. Successor Contract — G14
| Successor item | Frozen instruction |
| --- | --- |
| Programme number | G14 — Proof Store and Content-Addressed Dependency Graph. |
| Immediate mission | Create a durable repository for exact truth tables, sparse proof objects, arena declarations and dependency identities, using G13 content identities without making worker/partition topology part of proof identity. |
| Roadmap questions | Define immutable solved-object identity; link semantic/rules/source/truth/certificate hashes; retain superseded artifacts safely; resolve every proof dependency by immutable identity. |
| Inherited G13 contract | G13.COMPUTE.CONTRACT.v1 is the execution/provenance interface. G14 must preserve semantic problem identity separately from execution-plan identity. |
| Mandatory inherited exception | G13 mandatory G12 acceptance replay is OPEN because G12_Final_Rules_Reference_Bundle.zip bytes were unavailable. Do not convert G13 into a full PASS or unlock G17 until exact bundle hash 7641e0f8…d5695c is recovered and the G13 adapter/campaign reproduces the frozen G12 truth/certificate/canonical artifact hashes under kill/restart and repartitioning. |
| G14.0 recommended pre-gate | Attempt exact G12 bundle recovery once. If bytes are available, run the pending G13 acceptance replay before relying on G13 for scale. If still unavailable, preserve the exception and continue G14 schema/proof-store work because G14 can proceed in parallel; do not fabricate the bundle. |
| G14 store requirements | Store semantic version, state profile, source hash, arena/problem hash, truth hash, certificate hash, dependency hashes, supersession status and execution provenance without lossy translation. Historical broken G10 identity and G12 v2 identity must remain distinct. |
| Advance condition | Any proof object can resolve every dependency by immutable identity and reproduce the exact declared model. G14 PASS alone does not heal the open G13/G12 replay exception. |
| Older artifacts genuinely needed | None by default beyond G9 roadmap + this G13 handoff. The exact G12 bundle becomes genuinely required only for the pending G13 acceptance replay; no Pilot-G8 history is required for G14 schema work. |
| What G14 unlocks | G15 onward only once its own gate is met and the foundation blockers, including the open G13 acceptance exception, are explicitly resolved or carried according to dependency rules. |
# 16. Final frozen conclusion
G13 closes at a genuine artifact frontier, not a fabricated PASS. The distributed/checkpointed compute machinery itself is now concrete, deterministic under the tested fault/repartition regimes, independently replayed on its engineering reference, and protected by explicit identity/corruption failure rules. But the one acceptance test G12 made mandatory is still impossible without the exact frozen G12 bundle bytes. The correct downstream state is therefore: G14 may proceed with proof-store engineering in parallel; G17 scale remains blocked; and the pending G12-through-G13 replay must be closed immediately if the exact bundle becomes retrievable.
