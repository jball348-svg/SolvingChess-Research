# G8.1 Interim Evidence Freeze A — Material-Signature DAG Solver Core

**Programme:** G8 Certificate Engine and Re-Ascent  
**Stage:** G8.1 — Material-signature solver core  
**Date:** 11 August 2026  
**Status:** **CLOSED — STRONG ENGINEERING PASS. G8.2 AUTHORISED.**

## 1. Stage contract

G8.1 changes representation and execution only. Frozen G7 arena semantics remain authoritative. The stage must reproduce F01/F02/F09 before any frozen scale hold is touched, solve material signatures as typed dependency nodes, pack truth membership, and preserve capture/promotion semantics.

No G7 hold arena was shrunk, redefined or inspected for outcome truth during G8.1.

## 2. New solver architecture

### Brink-race engine — F01/F02

The old optional-material monolith represented all 16 presence/absence combinations inside one raw arena. G8.1 instead solves each of the 16 material signatures exactly once, ordered by increasing material population. Capture moves are explicit edges into an already-solved child signature. Promotion remains the frozen immediate-win brink terminal for these arenas.

Persistent truth is packed:

- validity: 1 bit / raw encoding;
- side-to-move W/L/D outcome: 2 bits / raw encoding;
- only the currently solved signature owns a transient one-byte universal-predecessor counter.

The 16 signature tables together require **13,381,632 bytes** of persistent validity+truth storage. The old monolithic brink source allocated three byte-wide raw arrays (`valid`, `out`, `rem`) over the 35,684,352 raw encodings, i.e. 107,053,056 bytes before queue/vector overhead.

### Faithful-fortress engine — F09

The dependency chain is explicit:

1. `K+P vs K` faithful h-file child;
2. `K+B+P vs K` faithful wrong-colour-bishop child;
3. `K+2B+P vs K` F09 parent with canonical unordered identical bishops.

Black bishop capture exits to the exact F4 child. Black pawn capture exits to the declared same-colour two-bishop draw. Promotion is not converted to an unconditional win: it is routed through a named exact continuation oracle for the declared promoted-material-vs-lone-king model, including king capture of the promoted unit, stalemate and checkmate.

Packed persistent validity+truth storage across KPK/F4/F5 is **6,500,352 bytes**. The active F5 universal counter remains transient.

## 3. Exact F01 regression

Frozen G7 baseline:

- capture-closed graph: 23,728,925 states;
- graph W/B/D: 7,282,421 / 8,205,091 / 8,241,413;
- full SIG15: 5,105,749;
- full W/B/D: 2,506,683 / 2,519,613 / 79,453;
- direct full-signature capture edges: SIG7 255,368; SIG11 231,650; SIG13 981,578; SIG14 214,347; total 1,682,943;
- historical solve wall time: 28.829 s.

G8.1 result:

- graph: **23,728,925**;
- graph W/B/D: **7,282,421 / 8,205,091 / 8,241,413**;
- full: **5,105,749**;
- full W/B/D: **2,506,683 / 2,519,613 / 79,453**;
- capture-edge vector: **255,368 / 231,650 / 981,578 / 214,347**, total **1,682,943**;
- exhaustive Bellman scan: **23,728,925 checked, 0 mismatches**;
- solver-only wall time: **18.620 s**;
- solver speedup over frozen baseline: **1.548x** (**35.41% less wall time**);
- audited run wall time: **29.277 s** including full-graph Bellman regeneration;
- peak RSS: **42,264 kB**.

Canonical G8 truth hash:

`e328e0f68c32863945cfbdbbab10fb78cf20f08141af2f53070ccd32a6e11d99`

## 4. Exact F02 regression

Frozen G7 baseline:

- capture-closed graph: 22,770,972 states;
- graph W/B/D: 7,043,319 / 7,043,319 / 8,684,334;
- full SIG15: 4,761,076;
- full W/B/D: 2,321,127 / 2,321,127 / 118,822;
- direct capture edges: SIG7 784,233; SIG11 784,233; SIG13 811,070; SIG14 811,070; total 3,190,606;
- historical solve wall time: 27.198 s.

G8.1 result:

- graph: **22,770,972**;
- graph W/B/D: **7,043,319 / 7,043,319 / 8,684,334**;
- full: **4,761,076**;
- full W/B/D: **2,321,127 / 2,321,127 / 118,822**;
- capture-edge vector: **784,233 / 784,233 / 811,070 / 811,070**, total **3,190,606**;
- exhaustive Bellman scan: **22,770,972 checked, 0 mismatches**;
- solver-only wall time: **16.730 s**;
- solver speedup over frozen baseline: **1.626x** (**38.49% less wall time**);
- audited run wall time: **27.245 s** including full-graph Bellman regeneration;
- peak RSS: **41,632 kB**.

Canonical G8 truth hash:

`e9604c7489592a84869ba41c64af5abf244e546f5bdeb81eb45a3c4cd7d8d68e`

## 5. Exact F09 regression

G8.1 first reproduces the faithful lower dependencies:

- KPK: **41,619 = 27,430 W + 14,189 D**;
- F4 wrong-colour bishop fortress: **1,182,440 = 825,269 W + 357,171 D**;
- F4 `BK=h8`: **22,008**, White wins **0**.

F09 result:

- raw full-material encodings: **24,379,392**;
- static-valid: **16,557,288**;
- White wins: **12,115,187**;
- draws: **4,442,101**;
- `BK=h8`: **330,264**, White wins **0**;
- faithful resource-safe TARGET antecedents: **1,448,464**, non-wins **0**;
- exhaustive Bellman scan: **16,557,288 checked, 0 mismatches**.

Performance:

- historical solve wall time: **20.750 s**;
- G8.1 solver-only wall time: **9.738 s**;
- speedup: **2.131x** (**53.07% less wall time**);
- solver + exhaustive 16.56M-state Bellman audit: **15.243 s**, still **26.54% below** the historical solve-only wall time;
- peak RSS: **39,348 kB**.

Canonical G8 truth hash:

`0d550158522726e253a8dc9a271cb1a6f4a8e1c50854f24f79e295f0fdfecbf4`

## 6. Regression verdict

All three required G7 successes reproduce exactly at the membership/count level, and the stronger G8 exhaustive Bellman scans have zero mismatches.

The F01/F02 cross-signature capture vectors match exactly, which is an especially important dependency-DAG audit: the new engine has not merely arrived at the same aggregate W/D/L totals through a changed arena.

F09 simultaneously reproduces the continuation-aware KPK child, faithful F4 child, full F09 truth, direct sanctuary and safe TARGET antecedent count. This strongly constrains accidental terminal-model drift.

Original G7 bitset files are not present in the active runtime, so G8.1 does **not** claim a cryptographic old-mask equality that cannot be checked. Instead this stage freezes new canonical G8 hashes after exact numerical and Bellman reproduction. If an original G7 truth-mask artifact is later recovered, direct hash/membership comparison can be added without changing this freeze.

## 7. Engineering result

The central G8 architectural hypothesis receives an immediate positive result.

For F01/F02, solving signatures independently eliminates the need for one giant mutable optional-material state vector while preserving exact cross-signature semantics. The result is both faster and substantially smaller in core state storage.

For F09, dependency reuse plus packed membership more than halves solve wall time, and even an exhaustive post-solve Bellman reconstruction completes faster than the frozen G7 solve alone.

This is not parallel brute force: all reported runs are single-process, approximately one-CPU executions. The gain comes from representation, smaller active signatures and direct child-table reuse.

## 8. Source / replay hashes

G8.1 source SHA-256:

- `g8_sig_brink.cpp`: `964d9a01ea352c837898b5a0905d1181977c29f43c8f57777ca13d138cba16e1`
- `g8_sig_fortress.cpp`: `5fd32314a0c806701b45fdd023074e5ce6a8b76bddf95b1fb33a7ef759270544`

Build contract:

`g++ -O3 -march=native -std=c++20`

Measured environment:

- Linux x86_64;
- g++ 14.2.0;
- AMD EPYC 9V74-class host;
- runs measured with `/usr/bin/time -v`.

Wall times are therefore frozen as matched-session engineering evidence, not universal hardware-independent constants.

## 9. G8.1 gate

**PASS STRONGLY.** The G8.1 advance condition is met:

- F01 exact membership/count regression: PASS;
- F02 exact membership/count regression: PASS;
- F09 exact membership/count regression: PASS;
- typed dependency decomposition: PASS;
- packed membership: PASS;
- direct material-transition counts: PASS;
- exhaustive Bellman audits: PASS, zero mismatches;
- material wall-time improvement: PASS on all three matched baselines.

**Next authorised stage: G8.2 — certificate compiler + independent verifier.**

The frozen G7 scale holds F03/F04/F06/F07/F08 remain untouched until the G8.2 proof/certificate path exists, as required by the programme order.
