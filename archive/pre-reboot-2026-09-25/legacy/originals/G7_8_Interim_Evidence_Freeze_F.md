# G7.8 Interim Evidence Freeze F — Proof-Graph Ascent and Adversarial Controls

**Date:** 11 August 2026  
**Status:** **G7.8 CLOSED — STRONG PASS WITH PRESERVED HIGH-BRANCH COMPLEXITY FLOOR. G7 remains open for G7.9.**

## 1. Stage rule

G7.8 composes already-frozen proof objects; it does not introduce a new grammar. Destination-choice objects are G6 Branch/finite-n Hyperkernel. Strategy-language objects are G7.7-promoted FILTERED_ATTRACTOR and FILTER_PIVOT. High-branch controls are taken from the G7.0/G7.1 prospective atlas; no outcome-guided shrinking or replacement is permitted.

## 2. Multi-level proof DAG: F02 same-colour bishop race

Frozen exact arena: `BB_same_c7_f2`, K+B+P vs K+B+P, full-material stratum 4,761,076 states.

### Layer A — exact lower-material destination objects

The three exact White-winning material endpoint signatures are SIG7, SIG11, SIG14. The full three-target strict attractor has 612,427 full-material states. Proper one-/two-target combinations explain 605,232; the irreducible three-way residual has **7,195** states.

### Layer B — finite-n Hyperkernel

The irreducible three-way residual factors exactly through **1,641 defender Hyperkernel states**:

`1,641 -> 7,195`, amplification **4.384521633x**, closure missing 0 / extra 0.

### Layer C — reuse the derived proof object as a target

Treat the certified 7,195-state irreducible region itself as a target. Its strict White attractor inside the already-certified three-target attractor is:

**23,327 states**, all in the full-material stratum.

This is **3.242112578x** amplification over the derived target and **14.21511274x** over the original 1,641-state Hyperkernel.

### Layer D — strategy-language proof on the derived target

The unchanged CHECK-filtered attractor to the 7,195-state derived target contains **23,026 / 23,327 = 98.70964976%** of the second-order attractor.

The remaining **301** quiet-required states factor exactly through **239 FILTER_PIVOT states**, amplification **1.259414226x**, with **0 missing / 0 extra**.

### Exhaustive fixed-point audit

All **612,427** full-material states in the parent three-target attractor were scanned forward:

- derived strict-attractor member violations: **0**
- derived strict-attractor outside fixed-point qualifiers: **0**
- derived CHECK-attractor member violations: **0**
- derived CHECK-attractor outside fixed-point qualifiers: **0**

Thus the multi-level chain is independently fixed-point certified rather than merely replaying a queue result.

## 3. Cross-axis interaction: destination irreducibility vs strategy language

Within the 612,427-state F02 full three-target attractor:

| Destination class | CHECK corridor | Quiet-required | Total |
|---|---:|---:|---:|
| Proper one-/two-target explainable | 581,012 | 24,220 | 605,232 |
| Irreducible three-way Hyperkernel residual | 1,235 | **5,960** | 7,195 |
| Total | 582,247 | 30,180 | 612,427 |

Therefore **82.8353%** of the genuinely three-way destination-choice population requires a quiet strategy handoff, versus only **4.0018%** of the proper-subunion population.

This is a strong interaction but not subsumption: destination-choice irreducibility and strategy-language departure are distinct proof dimensions, and the hardest destination-choice population is disproportionately concentrated in the strategy complement.

## 4. Existing F09 deep proof DAG

The faithful `K + 2 wrong-colour bishops + h-pawn vs K` arena supplies a second deep DAG under a different topology and terminal model:

1. semantic TARGET direct set: **1,448,464** exact wins;
2. CHECK-filtered strict attractor: **2,461,867** exact wins;
3. quiet-required complement of the ordinary target attractor: **5,833,195** states;
4. FILTER_PIVOT kernel: **517,120** states;
5. residual closure from pivots: **5,833,195**, 0 missing / 0 extra;
6. union of CHECK corridor and pivot residual reconstructs the ordinary target attractor: **8,295,062 exact wins**.

Thus a semantic base object plus a typed strategy language plus a kernel/residual composition certifies **5.727x** as many states as the direct TARGET set. The pivot kernel alone amplifies **11.28015741x** into the quiet-required complement.

On the defender side, the independently frozen sanctuary DAG still certifies **4,437,719 / 4,442,101 = 99.9014%** of the exact draw basin.

## 5. High-branch adversarial controls

The controls are predeclared G7.1 candidates, not post-hoc slices.

### G7F06 — QB_d7_e2

`K+Q+P vs K+B+P`, queen unrestricted, bishop colour-invariant, d7/e2 brink pawns.

- exact static-valid states: **40,499,052**
- prospective structural mean branching: **14.897**
- checking density: **15.823%**
- capture density: **3.077%**
- sampled predecessor audit: **175,353 reverse edges, 0 unsound; 175,172 forward edges, 0 missing**
- full exact retrograde: **no W/D/L emitted within 180 s; run terminated at execution/certificate budget**

### G7F04 — RB_c7_f2

`K+R+P vs K+B+P`, rook unrestricted, bishop colour-invariant, c7/f2 brink pawns.

- exact static-valid states: **44,820,777**
- prospective structural mean branching: **13.454**
- checking density: **6.673%**
- capture density: **2.625%**
- sampled predecessor audit: **157,400 reverse edges, 0 unsound; 156,749 forward edges, 0 missing**
- full exact retrograde: **no W/D/L emitted within 180 s; run terminated at execution/certificate budget**

No partial outcome propagation is accepted as chess evidence. Neither control is shrunk or substituted after the run.

## 6. Scaling/economics evidence

Completed exact baselines from earlier G7 stages:

- F01: 23,728,925 static-valid, **28.829 s**
- F02: 22,770,972 static-valid, **27.198 s**
- F09: 16,557,288 static-valid, **20.750 s**

These complete at about 0.80–0.84 million static-valid states per wall-clock second under their respective implementations. By contrast F04/F06, at roughly 1.7–2.0x the exact-state count and higher branch/check mobility, did not complete in 180 s: a >6x wall-clock increase over the solved six-man baselines before any result certificate was available. This is retained as an implementation/certificate scaling boundary, not a universal complexity law.

The new F02 multi-level verifier itself runs in **2.96 s wall-clock** with **526,588 kB peak RSS** in the present intentionally simple byte-mask implementation. Current raw proof masks use one byte per raw encoding (35,684,352 bytes each); this is engineering convenience, not a compressed certificate format.

A sparse 64-bit seed representation would require only:

- F02 deep DAG: 1,641 Hyperkernel + 239 second-order pivots = 1,880 encoded seeds = **15,040 bytes**, or **0.645 seed bytes per 23,327 final certified states**, excluding semantic target definitions and verifier code;
- F09 Filter-Pivot: 517,120 pivots = **4,136,960 bytes**, or **0.499 seed bytes per 8,295,062 target-attractor states**, again excluding semantic target/filter definition and verifier code.

These seed ratios are descriptive certificate-economics metrics, not full standalone proof-file sizes: a verifier still needs the move generator, lower-material truth/proof dependencies, and declared terminal semantics.

## 7. G7.8 verdict

**STRONG PASS.** G7 now has:

- a depth>3 typed proof DAG in which an exact lower-material destination composition creates a derived proof object, that object is reused as a target, and a strategy-language certificate/factorization is layered on top;
- a second large fortress proof DAG where Filter-Pivot reconstructs millions of quiet-required wins;
- exact evidence that destination and strategy composition interact without collapsing into one another;
- two prospectively selected, graph-audited high-branch controls preserved as honest complexity-floor outcomes;
- explicit runtime, storage and seed-amplification accounting.

No new proof-object type is promoted in G7.8. The result is architectural composition and scaling evidence. G7.9 should synthesize the cross-level language, decide which operations are core, identify the current compute frontier, and set the G8 gate.
