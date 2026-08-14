# G8.2 Interim Evidence Freeze B — Certificate Compiler + Independent Verifier

**Date:** 11 August 2026  
**Status:** **G8.2 CLOSED — PASS STRONGLY. G8.3 authorised.**

## 1. Stage contract

G8.2 was required to compile the frozen G7 core proof objects and sparse kernel/pivot payloads into a deterministic certificate form, then verify fixed-point/kernel obligations through an implementation path that does not replay producer queue state. No new chess predicate or arena truth was to be introduced.

The accepted implementation is `G8.CERT.v0.1` with sparse `G8DV1` payloads and an independently replayable manifest.

## 2. Truth/dependency authority

The verifier consumes the exact G8.1 truth dependencies only through declared files and SHA-256 identities:

- F01: `e328e0f68c32863945cfbdbbab10fb78cf20f08141af2f53070ccd32a6e11d99`
- F02: `e9604c7489592a84869ba41c64af5abf244e546f5bdeb81eb45a3c4cd7d8d68e`
- F09: `0d550158522726e253a8dc9a271cb1a6f4a8e1c50854f24f79e295f0fdfecbf4`

The final certificate manifest hashes to:

`1014a245457ef9ca8428ccd0604db98f3ff3823760d206d9f0e71e2c7967cb4e`

## 3. F01 Branch certificate

The standalone verifier independently reconstructed the frozen SIG7/SIG11 composition:

- Attr(SIG7): **355**
- Attr(SIG11): **12,831**
- union attractor: **13,842**
- constituent proper union: **13,186**
- irreducible BRIDGE: **656**
- immediate Branch kernel: **152**
- residual closure from payload: **656**
- kernel payload exact: **yes**
- non-winning certified members: **0**

The 152 canonical seeds compile to only **248 bytes**. The independently reconstructed bridge and union masks hash byte-for-byte identically to the producer audit streams.

## 4. F02 Hyperkernel + second-order strategy DAG

The independent verifier reproduced the entire frozen mixed chain:

- single endpoint attractors: **41 / 72,757 / 493,591**
- proper pair attractors: **81,249 / 534,327 / 564,193**
- full three-target attractor: **612,427**
- proper-subunion coverage: **605,232**
- irreducible three-way region: **7,195**
- Hyperkernel: **1,641**
- Hyperkernel closure: **7,195**, exact
- second-order strict attractor: **23,327**
- CHECK-filtered attractor: **23,026**
- quiet-required complement: **301**
- Filter-Pivots: **239**
- pivot closure: **301**, exact
- ordinary fixed-point audit violations: **0**
- CHECK fixed-point audit violations: **0**
- parent-attractor non-wins: **0**

The Hyperkernel payload is **2,135 bytes** and the second-order pivot payload **460 bytes**: **2,595 bytes total**, only **0.12374%** of a raw 2-bit parent-width table. This is **82.75% smaller** than G7's descriptive 15,040-byte sparse-64 seed estimate, while retaining exact semantics.

All five F02 derived membership streams matched producer SHA-256 exactly.

## 5. F09 fortress/strategy certificate

The independent F09 implementation consumes the hashed faithful truth dependency but separately implements move generation, lower-material capture lookup, promotion-continuation typing, CHECK semantics, residual closure and role-dual sanctuary propagation. It reproduces:

- semantic TARGET: **1,448,464**
- ordinary target attractor: **8,295,062**
- CHECK-filtered attractor: **2,461,867**
- quiet-required complement: **5,833,195**
- Filter-Pivots: **517,120**
- pivot residual closure: **5,833,195**, exact
- direct BK=h8 sanctuary: **330,264**
- conservative sanctuary attractor: **3,133,058**
- typed-safe sanctuary attractor: **4,437,719**
- ordinary-attractor non-wins: **0**
- CHECK-attractor non-wins: **0**
- safe-sanctuary non-draws: **0**

The F09 pivot payload is **530,753 bytes**, only **8.708%** of the raw 2-bit F09 parent truth width and **87.17% smaller** than G7's 4,136,960-byte sparse-64 estimate.

All seven F09 derived membership streams matched producer SHA-256 exactly.

## 6. Deterministic replay result

The replay harness performs manifest-sidecar verification, dependency-hash verification, sparse-payload verification, source-hash verification, independent object reconstruction and canonical membership hashing. Final result:

- sparse payload sets exact: **4/4**
- independently reconstructed derived membership hashes: **14/14 exact**
- F01/F02/F09 semantic/count assertions: **all pass**
- manifest: **stable and hash-addressed**

Verifier-only replay walls in the latest run were approximately **2.21 s (F01), 1.57 s (F02), 15.84 s (F09)**. A one-command replay including recompilation completed in **26.42 s**.

Measured standalone verifier peaks were **617,524 kB F01**, **551,280 kB F02**, and **84,356 kB F09**. Thus certificate payload compression is already strong, but the cached reverse-graph implementation for the brink verifier remains memory-heavy. This is preserved as engineering evidence rather than disguised as proof-language cost.

## 7. Independent-verifier alarm that was caught

The first standalone brink verifier mistakenly declared the White brink pawn one rank too high in F01/F02. The resulting proof counts failed immediately. Those outputs were rejected. Correcting the declaration to the frozen d7/c7 squares restored every exact count and all canonical membership hashes.

This is a useful positive certification event: the standalone verifier was not merely parroting producer data, and declaration/semantic mismatch was observable before acceptance. No chess truth changed.

## 8. Certificate economics

| Sparse object | Seeds | G8DV bytes |
|---|---:|---:|
| F01 Branch kernel | 152 | 248 |
| F02 Hyperkernel | 1,641 | 2,135 |
| F02 derived Filter-Pivots | 239 | 460 |
| F09 Filter-Pivots | 517,120 | 530,753 |
| **Total** | **519,152** | **533,596** |

These are proof payload bytes given explicitly hashed exact truth dependencies. The truth dependencies are not free or hidden; they are reusable lower-level certified objects. Producer audit masks are excluded because they are deliberately not part of the certificate.

## 9. G8.2 verdict

**PASS STRONGLY.**

G8 now has a canonical proof-object manifest, compact sparse Branch/Hyperkernel and Filter-Pivot payloads, independent verifier implementations, deterministic source/dependency/payload/membership hashes, and a one-command replay. This satisfies the G8.2 freeze point without changing any frozen arena semantics.

The main remaining G8.2 engineering weakness is verifier RAM on cached high-edge brink graphs, not logical certificate size. That distinction is now measurable.

**Next authorised stage: G8.3 — attack F03, F04 and F06 unchanged with the new material-signature engine.**
