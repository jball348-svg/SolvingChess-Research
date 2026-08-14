# G7.6 Interim Evidence Freeze D

**Programme:** G7 Higher-Tree Position Discovery  
**Stage:** G7.6 — Discover New Abstractions  
**Date:** 11 August 2026  
**Status:** **G7.6 CLOSED — STRONG PASS; first genuinely new strategy-language proof objects promoted for G7.7 backward-fire.**

## Executive result

G7.6 was deliberately stricter than a pattern-mining pass. Candidate names were subjected to G6 dependency/subsumption semantics before promotion. The stage therefore contains both a genuine new abstraction and several attractive ideas that were explicitly reduced to existing G6 object types.

The principal positive result is a new strategy-language layer:

1. **Filtered Strict Attractor** — certify forced reachability while restricting the attacker's pre-target moves to a declared semantic edge class, such as CHECK.
2. **Filter-Pivot Kernel Factorization** — exactly factor the difference between ordinary reachability and filtered reachability through attacker-owned first-disallowed-move pivots, followed by ordinary residual backward closure.

The factorization is proved for finite game graphs, reproduced exactly in F01, F02 and held-out F09, and regression-tested on 100,000 random finite game graphs with arbitrary attacker-edge filters with zero mismatches.

## CHECK corridor discovery and held-out evaluation

The first edge filter is CHECK: every White move before target entry must give check; final entry into the exact target may be a non-checking material transition. Black retains every legal reply.

- F01 triple material-endpoint attractor: 146,068 full states; CHECK corridor 146,044 = 99.9836%.
- F02: 612,427; CHECK corridor 582,247 = 95.0721%.
- Held-out F09 fortress target: 8,295,062; CHECK corridor 2,461,867 = 29.6787%, with 0 false draws and an exhaustive fixed-point audit of all 8,295,062 ordinary-attractor states yielding 0 member violations and 0 outside qualifiers.

The large coverage change is scientifically useful: the object transfers exactly while its usefulness is topology-sensitive. In F02 only 1,235 / 7,195 = 17.1647% of the irreducible three-way Hyperkernel region lies in the CHECK corridor, so check forcing and defender-choice endpoint composition are distinct proof mechanisms.

## Filter-Pivot Factorization

Let `A=Attr(T)` and `C=Attr_F(T)`. Define a pivot as an attacker state in `A\C` with a filter-disallowed edge into `C`. Then the entire `A\C` population is exactly the residual backward closure of those pivots outside `C`.

Exact chess results:

- F01: 24 difference states, 24 pivots, closure 24, 0 missing / 0 extra.
- F02: 30,180 difference states, 19,890 pivots, amplification 1.51735x, closure 30,180, 0 missing / 0 extra.
- F09 held-out: 5,833,195 difference states, 517,120 pivots, amplification 11.28016x, closure 5,833,195, 0 missing / 0 extra.

Generic regression: 100,000 arbitrary finite graphs, random owners/targets/attacker-edge filters; 0 factorization mismatches and 0 nonempty-kernel equivalence failures.

Pivot semantics are not piece-specific. F01 pivots are all quiet king moves. F02 separates into 1,721 king-only and 18,169 bishop-only pivots. F09 uses all three available resources: 215,588 king-only, 196,613 pawn-only, 9,965 bishop-only, plus mixed-resource pivot states.

## Multi-projection candidate: rejected as new object

A very promising initial rule said that if deleting White's bishop and deleting Black's bishop both project to exact White wins, then the full state wins after excluding a single conversion-interference mechanism. This was exact on both discovery families and certified 4,019,471 wins with zero errors.

Subsumption then killed the novelty claim. The same guard plus **only the White-bishop deletion projection** is already exact and strictly broader:

- F01: 2,119,202 / 2,119,202 wins;
- F02: 1,921,464 / 1,921,464 wins.

The useful result is therefore a new higher-tree RESTORE theorem under the existing G6 object type, not a multi-projection object.

The guard is semantic and compact: the restored White mobile piece must neither occupy White's immediate promotion square nor lie in the opponent pawn's immediate promotion-capture cone.

F09 also falsifies broad projection voting: 3,011 full draws survive despite both single-bishop deletion projections being White wins; 2,055 are immediate stalemates.

## Sanctuary preservation/destruction candidate

F09 preserves the lower wrong-colour sanctuary with a second added bishop unable to access h8: all 330,264 `BK=h8` states are exact draws.

F10 was prospectively frozen as the matched held-out toggle: same material count and h-pawn geometry, but the added bishop is moved to the colour complex that can access h8. Structural certification gives 33,305,146 static-valid states and a clean predecessor audit. The complete W/D solve remains beyond the current execution budget and is not claimed.

However the prospective sanctuary prediction is already decisively certified: among 586,893 legal F10 states with `BK=h8`, **3,578 are immediate checkmates**. Hence universal sanctuary preservation is falsified when the added resource gains critical-square access.

This is retained as a strong candidate **sanctuary-access restoration guard**, but not yet a new object type because guarded draw restoration already fits the G6 RESTORE envelope.

## Candidate reduction ledger

- Exchange Funnel -> existing G6 Branch-Kernel over typed material endpoints.
- Transition Hyperkernel -> existing G6 finite-n Hyperkernel.
- Multi-Projection Consistency -> subsumed by simpler guarded single-projection RESTORE.
- Sanctuary Lift -> currently best represented as guarded draw restoration plus a held-out falsification.
- CHECK Corridor -> survives as a strategy-filtered reachability object.
- Filter-Pivot Factorization -> survives as a new universal derived composition object over **move-language restrictions**, not target alternatives.

## Scale / no-result preservation

- F10 full W/D retrograde: scale hold, no W/D emitted.
- F11/F12 b7/g2 prospective multi-projection holdouts were retired before truth evaluation after the multi-projection candidate was subsumed; this avoids spending certificate budget on a hypothesis already rejected as a new object.
- An optional multi-filter strategy-palette sweep exceeded its execution budget before emitting a certified row and is excluded from evidence.

## G7.6 gate

**PASS STRONGLY.** The stage found at least one genuinely new proof-language composition object after the unchanged G6 architecture had already been fired upward, evaluated its CHECK instantiation on a held-out higher-tree topology, proved the graph-theoretic factorization, and preserved multiple reductions/falsifications rather than inflating the object count.

G7.7 should now backward-fire `FILTERED_ATTRACTOR` and `FILTER_PIVOT` across the frozen G6 corpus. No claim of broad chess generality is made until that audit is complete.
