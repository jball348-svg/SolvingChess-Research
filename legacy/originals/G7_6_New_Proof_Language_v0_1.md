# G7.6 New Proof-Language Candidates — v0.1

**Programme:** G7 Higher-Tree Position Discovery  
**Stage:** G7.6 — Discover New Abstractions  
**Date:** 11 August 2026  
**Status:** frozen candidate specification for G7.7 backward-fire

## 1. Promotion discipline

G7.6 applies the G6 object discipline: a new name is not a new proof object. Candidate objects are promoted only if they do not collapse under dependency/subsumption to an existing G6 object class, and every finite chess instantiation used as evidence is exhaustively certified on its declared domain.

## 2. FILTERED_STRICT_ATTRACTOR

### Object ID
`G7.FILTERED_ATTRACTOR.v0.1`

### Status
**DERIVED UNIVERSAL OPERATOR / NEW PROOF-LANGUAGE FIELDING.** Mathematically this is ordinary strict reachability on an attacker-edge-pruned strategy graph. It is not claimed as a new fixed-point theorem beyond G6 strict attractor semantics. Its proof-language novelty is that the original game graph is held fixed while the certificate additionally declares an attacker **strategy-edge filter**.

### Contract
Given a finite game graph, target `T`, and an attacker-edge predicate `F(s,z)`, define `Attr_F(T)` as the least set containing `T` such that:

- attacker-owned `s` enters when at least one legal successor `z` is already in the set and the edge is `F`-admissible;
- defender-owned `s` enters only when it has at least one legal continuation and every legal continuation enters the set;
- external promotion/capture/material shortcuts follow the same terminal/shortcut contract as the ordinary attractor;
- target-entry edges may be declared admissible independently of `F` when the certificate intends `F` to constrain only the pre-entry strategy.

The certificate therefore proves not merely `s can force T`, but `s can force T using an F-constrained attacker strategy before target entry`.

### Concrete G7 instantiation: CHECK corridor
`F(s,z) := move s->z gives check`, with final entry into the exact target exempt from the check requirement.

Certified results:

| Arena | Ordinary strict target attractor | CHECK-filtered attractor | Retained share |
|---|---:|---:|---:|
| F01 opposite-colour B+P vs B+P, three material endpoints | 146,068 full-material | 146,044 | 99.9836% |
| F02 same-colour B+P vs B+P, three material endpoints | 612,427 full-material | 582,247 | 95.0721% |
| F09 two-wrong-bishop fortress, safe conversion target | 8,295,062 | 2,461,867 | 29.6787% |

F09 fixed-point audit: 8,295,062 ordinary-attractor states checked; 0 filtered-member violations; 0 outside fixed-point qualifiers; 0 false draws.

The F02 irreducible three-way Hyperkernel region overlaps the CHECK corridor in only 1,235 / 7,195 = 17.1647%, showing that move-filtered forcing and defender-choice material composition are distinct mechanisms.

## 3. FILTER-PIVOT KERNEL FACTORIZATION

### Object ID
`G7.FILTER_PIVOT.v0.1`

### Status
**UNIVERSAL / MATHEMATICAL (derived factorization), candidate new G7 composition object.**

### Inputs
- ordinary strict attractor `A = Attr(T)`;
- strategy-filtered attractor `C = Attr_F(T)` under identical game/terminal/shortcut semantics;
- therefore `T subset C subset A`.

### Pivot kernel
Define `K_F` as attacker-owned states `s in A \ C` for which there exists a successor `z in C` reachable by an attacker edge excluded by `F` (and not covered by a target-entry exemption).

Interpretation: these are the first states where an ordinary winning strategy must leave the declared strategy language in order to enter the already-certified filtered corridor.

### Factorization theorem
Let `Q = A \ C`. Then:

1. `Q` is nonempty iff `K_F` is nonempty.
2. `Q` is exactly the ordinary residual backward closure of `K_F` outside `C`, treating successors already in `C` as safe base states and using attacker-existential / defender-universal predecessor semantics on the residual.

### Proof
Because `T subset C subset Attr(T)=A`, monotonicity and idempotence of strict attraction give `Attr(C)=A`. Consider the ordinary attraction from `C` toward `A`. A first newly admitted state outside `C` cannot be defender-owned: the defender rule is unchanged by the strategy filter, so a defender state all of whose replies were already in `C` would itself already belong to `C`. Therefore every first-layer state is attacker-owned and enters `C` through an attacker edge that the filter excluded; these states are exactly `K_F`. Subsequent ordinary attraction from that first layer, with `C` already safe, is precisely the stated residual closure. This proves both equality and the nonempty-kernel criterion.

### Exact chess regressions

| Arena | `|A\C|` | Pivot kernel | Amplification | Residual closure | Missing | Extra |
|---|---:|---:|---:|---:|---:|---:|
| F01 | 24 | 24 | 1.0000x | 24 | 0 | 0 |
| F02 | 30,180 | 19,890 | 1.51735x | 30,180 | 0 | 0 |
| F09 held-out topology | 5,833,195 | 517,120 | 11.28016x | 5,833,195 | 0 | 0 |

Generic implementation regression: **100,000 arbitrary finite game graphs with random attacker-edge filters; 0 factorization mismatches; 0 failures of the `Q nonempty iff K_F nonempty` criterion.** This is implementation evidence, not a substitute for the proof above.

### Chess-semantic pivot mining

- F01: all 24 pivots have a quiet king edge into the CHECK corridor.
- F02: 1,721 king-only and 18,169 bishop-only pivot states; no mixed king+bishop pivots.
- F09: 517,120 pivots spread across king, pawn and bishop resources: 215,588 king-only; 196,613 pawn-only; 9,965 bishop-only; 6,084 king+bishop; 83,120 king+pawn; 818 bishop+pawn; 4,932 with all three available.

Thus the kernel is not a disguised piece-specific exception list. It identifies where a forcing strategy must hand off from one semantic move language to another.

## 4. Candidate that reduced to G6: MULTIPROJECTION_CONSISTENCY

The initial candidate required both `PROJECT(delete White bishop)=W` and `PROJECT(delete Black bishop)=W`, guarded against immediate conversion interference by the restored White bishop. It was exact on F01 and F02:

- F01: 2,114,676 / 2,114,676 wins;
- F02: 1,904,795 / 1,904,795 wins.

But subsumption rejects it as a new object. With the same guard, `PROJECT(delete White bishop)=W` alone is already exact and strictly broader:

- F01: 2,119,202 / 2,119,202 wins;
- F02: 1,921,464 / 1,921,464 wins.

Therefore the second projection contributes no proof power. The useful discovery is a new **conversion-interference restoration guard**, which belongs to the existing G6 RESTORE/INHERITS object class.

The guard found by exhaustive failure mining is:

`restored White mobile piece is not on White's promotion square AND is not in the opponent pawn's immediate promotion-capture cone`.

The unqualified projection-voting idea also fails in F09: 3,011 states have both single-bishop deletion projections White-winning while the full two-bishop state is drawn; 2,055 of those failures are immediate stalemates.

## 5. Sanctuary access: strong finite split, not yet a new object class

F09 establishes exact preservation with an added bishop that cannot access h8:

`BK=h8 => draw` for 330,264 / 330,264 states.

F10 was prospectively frozen as the matched control in which the added bishop changes colour complex and can access h8. Its full 33,305,146-state W/D solve remains a scale hold, but no full tablebase is required to falsify universal sanctuary preservation: among 586,893 static-valid `BK=h8` states, 3,578 are immediate checkmates.

This is strong evidence for a **critical-resource-access guard** on sanctuary restoration. At G7.6 it is not promoted as a new proof-object type because draw-restoration under a semantic guard already fits the G6 restoration envelope. It remains a candidate theorem/schema for later generalization.

## 6. Other G7 candidate types already reduced earlier

- `EXCHANGE_FUNNEL` over material endpoints reduces to G6 Branch-Kernel composition once lower-material endpoints are typed as targets.
- `TRANSITION_HYPERKERNEL` reduces exactly to the G6 finite-n Hyperkernel theorem; F02's 1,641-state defender kernel generates the 7,195-state irreducible three-way material-transition region.

These reductions are successful architectural results, not failed science.

## 7. G7.7 compatibility requirement

The objects allowed into G7.7 backward-fire are:

1. `G7.FILTERED_ATTRACTOR.v0.1` — new proof-language strategy-filter field/operator, with CHECK as the first certified instantiation;
2. `G7.FILTER_PIVOT.v0.1` — new universal derived composition/factorization object;
3. `G7.RESTORE.CONVERSION_SAFE_WHITE_MOBILE.v0.1` — new conditional finite restoration theorem, **existing G6 object type**;
4. `G7.SANCTUARY_ACCESS_GUARD.v0.1` — candidate guard/falsification family, not yet promoted as a new object type.

G7.7 must fire the two genuinely new strategy-language objects backward against every type-compatible G6 arena before either is labelled generally useful in chess.
