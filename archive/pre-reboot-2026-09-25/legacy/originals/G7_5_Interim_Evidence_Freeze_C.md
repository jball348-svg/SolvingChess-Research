# G7.5 Interim Evidence Freeze C

**Date:** 11 August 2026  
**Stage:** G7.5 — Fire the frozen G6 architecture upward without retuning  
**Status:** **PASS STRONGLY — architecture reuse confirmed with explicit type boundaries. G7 remains open.**

## 1. Freeze rule

G7.5 does not discover a new grammar. It applies the frozen G6 proof architecture to the exact G7 higher-tree families and records success, failure, or out-of-domain status before G7.6 is allowed to synthesize anything new.

The type discipline used here is the frozen G6 classification:

- **Universal / mathematical:** strict attractor, role-dual sanctuary attractor, Branch-Kernel Factorization, finite-n Hyperkernel Factorization.
- **Reusable schemas:** exact projection information, resource-safe TARGET construction, residualization/grouping/certificate composition, localization-lift diagnostic.
- **Conditional finite chess theorems:** FAR5, FAR3 slider, FAR3 knight-with-exception, and the one-bishop wrong-colour corner sanctuary theorem.
- Conditional theorems are not widened by analogy.

## 2. Exact G7 inputs

### G7F01 — opposite-colour bishop race
`K+B+d7 vs K+B+e2`, opposite bishop complexes.

Full-material truth: **5,105,749 = 2,506,683 W + 2,519,613 B + 79,453 D**.

### G7F02 — same-colour bishop race
`K+B+c7 vs K+B+f2`, same bishop complex.

Full-material truth: **4,761,076 = 2,321,127 W + 2,321,127 B + 118,822 D**.

### G7F09 — fortress ascent
`K + 2 wrong-colour bishops + h-pawn vs K`, faithful continuation.

Exact truth: **16,557,288 = 12,115,187 W + 4,442,101 D**.

The faithful four-man dependency again reproduces **1,182,440 = 825,269 W + 357,171 D** and the exact lower `BK=h8` sanctuary.

## 3. PROJECT fires; restoration remains non-monotone

Projection itself remains mechanically useful because the G7 graphs contain exact lower-material truth.

### F01 full-material projection scans

| Projection | Exact lower-W antecedents | Restored W | Restored D | Restored B |
|---|---:|---:|---:|---:|
| delete White bishop | 2,192,425 | 2,154,192 | 4,269 | 33,964 |
| delete Black bishop | 2,842,052 | 2,498,425 | 46,868 | 296,759 |
| delete White pawn | 324 | 324 | 0 | 0 |
| delete Black pawn | 3,910,436 | 2,503,731 | 27,354 | 1,379,351 |

### F02 full-material projection scans

| Projection | Exact lower-W antecedents | Restored W | Restored D | Restored B |
|---|---:|---:|---:|---:|
| delete White bishop | 2,070,016 | 2,065,988 | 36 | 3,992 |
| delete Black bishop | 2,620,273 | 2,302,095 | 68,216 | 249,962 |
| delete White pawn | 0 | 0 | 0 | 0 |
| delete Black pawn | 3,752,257 | 2,301,237 | 38,220 | 1,412,800 |

F09 has two exact deletion projections, one for each identical bishop. Across **33,114,576 valid projection instances**, **22,957,573** project to a lower four-man White win. Restoring the second bishop preserves **22,894,100** of those but changes **63,473** projection instances to draws. At the full-state level, **11,712,482** states have at least one lower winning bishop-deletion projection; **60,462** of those are draws after restoration.

This is exact higher-tree projection information, but **not** a FAR violation: G6 FAR5/FAR3 quantify over `K+X+P vs K` restored from KPK. F01/F02 contain extra opposing material and F09 restores a second bishop into an already four-man bishop ending. FAR5/FAR3 are therefore **OUT OF FROZEN DOMAIN**, not failed.

## 4. TARGET gives the expected typed split

The old G6 double-brink race/path instance was fired literally into F01/F02:

- **F01:** 635,658 target states; **75,764 non-wins**.
- **F02:** 650,857 target states; **74,376 non-wins**.

This is a clean failure of the old **instance**, whose frozen domain did not include an extra opposing bishop access resource.

By contrast, the unchanged faithful-fortress target remains exact in F09:

`pawn rank >= 6 ∧ d(WK,h8) <= 4 ∧ d(BK,h8) >= 5`

- Direct target: **1,448,464**, **0 non-wins**.
- Strict White attractor: **8,295,062**, **0 non-wins**.
- White-win basin coverage: **68.4683%**.

Thus the G6 resource-safe TARGET *architecture* survives: a type-compatible instance fires exactly, while an under-typed instance fails instead of being patched post hoc.

## 5. Material endpoints as strict G6 targets

Three exact lower-material White-winning targets were used:

- **SIG7:** White bishop absent.
- **SIG11:** Black bishop absent.
- **SIG14:** Black pawn absent.

### F01 attractors

| Target union | Full-material strict attractor |
|---|---:|
| A7 | 355 |
| A11 | 12,831 |
| A14 | 130,295 |
| A7∪11 | 13,842 |
| A7∪14 | 132,994 |
| A11∪14 | 142,713 |
| A7∪11∪14 | **146,068** |

The triple material-endpoint attractor certifies **5.8271%** of the exact F01 White-win basin.

### F02 attractors

| Target union | Full-material strict attractor |
|---|---:|
| A7 | 41 |
| A11 | 72,757 |
| A14 | 493,591 |
| A7∪11 | 81,249 |
| A7∪14 | 534,327 |
| A11∪14 | 564,193 |
| A7∪11∪14 | **612,427** |

The triple material-endpoint attractor certifies **26.3849%** of the exact F02 White-win basin.

No new reachability theorem was needed: this is unchanged G6 strict-attractor semantics with material-labelled exact targets.

## 6. Branch-Kernel Factorization scales across material endpoints

Every tested two-endpoint pair has positive strict pure BRIDGE.

| Family | Material pair | Pure bridge | Immediate kernel | Amplification |
|---|---|---:|---:|---:|
| F01 | SIG7 + SIG11 | 656 | 152 | 4.3158× |
| F01 | SIG7 + SIG14 | 2,344 | 2,344 | 1.0000× |
| F01 | SIG11 + SIG14 | 16 | 15 | 1.0667× |
| F02 | SIG7 + SIG11 | 8,485 | 1,507 | 5.6304× |
| F02 | SIG7 + SIG14 | 40,731 | 16,963 | 2.4012× |
| F02 | SIG11 + SIG14 | 14,072 | 3,900 | 3.6082× |

So G7.3's first material-endpoint bridge was not an isolated coincidence. The same frozen branch mechanism appears for **all six** tested endpoint pairs.

## 7. First exact material-transition Hyperkernel

This is the strongest G7.5 result.

For the three targets `{SIG7, SIG11, SIG14}`, the proper-subunion base is

`B = Attr(7∪11) ∪ Attr(7∪14) ∪ Attr(11∪14)`.

### F01
- Irreducible three-way region: **0**.
- Hyperkernel: **0**.

This is a clean zero-occurrence case.

### F02
- Full three-target strict attractor: **612,427** full-material states.
- Irreducible three-way region outside every proper-subunion attractor: **7,195**.
- Defender hyperkernel: **1,641**.
- Hyperkernel amplification: **4.3845×**.
- Independent residual backward closure from the hyperkernel: **7,195**.
- Closure missing: **0**.
- Closure extra: **0**.

Therefore the frozen G6 finite-n theorem now factors an exact region whose alternatives are **three materially distinct lower subgames**. This is not merely a renamed square-target experiment.

## 8. Hyperkernel audit alarm and supersession

An initial F02 diagnostic incorrectly printed **7,195 irreducible / 0 kernel**. It is explicitly discarded.

Cause: the analysis pass populated the proper-subunion base `B` lazily while simultaneously scanning states. When a state's successor had a numerically higher encoding, its `B` bit had not yet been filled and was falsely read as absent.

The graph itself was not implicated:

- 250,000-state predecessor duplicate audit: **2,870,352 emissions, 0 duplicate extras**.
- 500,000-state predecessor soundness audit: **5,744,732 reverse edges, 0 unsound**.
- 300,000-state predecessor completeness audit: **3,447,536 forward edges, 0 missing reverse predecessor**.
- Rank trace found the minimum three-way pure state at attractor rank 2: Black to move, eight successors, **all eight already in the proper-subunion base**, exactly as the G6 theorem predicts.

After precomputing `B`, the exact **1,641 → 7,195** factorization above is obtained. No accepted W/D/L truth changed.

This is a positive certification event: the universal theorem caught an analysis implementation error.

## 9. Role-dual sanctuary continues to scale

F09 re-fires the G6 defender-side operation:

- Direct `BK=h8` sanctuary: **330,264 / 330,264 draws**.
- Conservative target-only defender attractor: **3,133,058 draws**, zero White wins.
- Typed safe-exit defender attractor: **4,437,719 draws**, zero White wins.
- Exact draw-basin coverage: **99.9014%**.
- Residual draws: **4,382**.

The type-compatible safe exits are exact lower-material draws and stalemate terminals already in the dependency graph.

## 10. RESIDUAL and GROUP_OUT

After exact G6-style certificate subtraction:

| Family | Residual states | Residual grouped geometries after removing WK | Mixed geometries |
|---|---:|---:|---:|
| F01 after triple material attractor | 4,959,681 | 107,725 | 99,409 |
| F02 after triple material attractor | 4,148,649 | 98,392 | 83,029 |
| F09 after White target attr + defender sanctuary attr | 3,824,507 | 192,675 | 2,698 |

F09's two disjoint certificates together cover **12,732,781 / 16,557,288 = 76.9014%** of the entire exact state space. The residual consists of **3,820,125 White wins + 4,382 draws**.

## 11. LOCALIZATION_LIFT reproduces the saturated-clock negative regime

The frozen double-brink promotion race clock was applied to the F01/F02 residuals without retuning. Both fixed pawns remain one move from promotion, so the tempo-adjusted race difference is always within the one-full-move slab.

### F01
- Mixed geometries in frozen race slab: **100%**.
- All residual geometries in slab: **100%**.
- Localization lift: **0 pp**.

### F02
- Mixed: **100%**.
- All residual: **100%**.
- Lift: **0 pp**.

Thus G6's `SATURATED_CLOCKS` diagnosis survives ascent exactly: raw 100% coverage contains zero localization information.

For F09, the frozen G6 record supplies the earlier fortress localization *counts* but the flattened fortress slab predicate was not recovered from the authoritative handoff/library artifacts. G7.5 therefore does **not** reverse-engineer or retune that formula. No unchanged F09 localization count is claimed here.

## 12. Local grammar and STOP

The authoritative G6 record establishes a frozen **10-leaf** double-brink grammar with zero errors on 133,699 non-vacuous held-out states, but the flattened executable predicate is not present in the recovered authoritative artifacts.

Accordingly:

- no “unchanged 10-leaf grammar” transfer is claimed in G7.5;
- no new grammar is fitted to F01/F02/F09;
- the G7 staging rule is obeyed: **new symbolic synthesis belongs to G7.6**.

This is a methodological STOP, not evidence that the higher-tree residual is irreducible.

## 13. Architecture reuse matrix

| G6 operation | G7.5 result |
|---|---|
| PROJECT | **PASS** mechanically; lower-material truth remains useful |
| FAR5 / FAR3 | **OUT OF FROZEN DOMAIN**, neither credited nor falsified |
| RESOURCE-SAFE TARGET | **MIXED/TYPED PASS**: exact F09 instance; old under-typed F01/F02 instance fails |
| STRICT ATTRACTOR | **STRONG PASS** |
| BRANCH-KERNEL | **STRONG PASS**, all 6 material pairs positive |
| FINITE-n HYPERKERNEL | **STRONG PASS**, exact F02 1,641 → 7,195; F01 zero occurrence |
| ROLE-DUAL SANCTUARY | **STRONG PASS**, 99.9014% of F09 draw basin |
| RESIDUAL / GROUP_OUT | **PASS** |
| LOCALIZATION_LIFT | **PASS AS NEGATIVE DIAGNOSTIC**, 0-lift saturated race clocks |
| LOCAL GRAMMAR | **NOT CLAIMED unchanged** because flattened rule was not recovered |
| STOP | **PASS**: no G7.5 post-hoc fitting |
| TERMINAL SEMANTICS TYPING | **STRONG PASS** through faithful F09 dependency regression |

## 14. G7.5 verdict

**G7.5 PASSES STRONGLY.**

The important result is not that every old chess predicate continues to work. It does not. The old double-brink target instance fails immediately when an extra opponent bishop supplies an untyped access resource, and the FAR finite theorems correctly refuse to widen outside their stated domains.

What survives is more valuable:

1. exact projection information continues to feed higher-tree dependency graphs;
2. strict target attractors remain generic;
3. two-way Branch-Kernel composition is widespread over alternative material reductions;
4. the finite-n Hyperkernel theorem produces its first exact **three-material-endpoint** certificate;
5. role-dual sanctuary composition becomes almost complete in the higher fortress arena;
6. localization-lift continues to distinguish a genuinely saturated, non-informative clock regime;
7. proof typing prevents false transfer claims.

The stage therefore ends with a substantially stronger case that the G6 architecture is a typed proof language rather than a collection of small-endgame tricks.

**Next authorised stage:** G7.6 may now discover genuinely new higher-tree abstractions on frozen training families and evaluate them prospectively on held-out material/topology families. No G7.6 discovery is included in this freeze.
