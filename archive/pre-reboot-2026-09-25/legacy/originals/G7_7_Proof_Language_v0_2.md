# G7 Proof Language — v0.2 after G7.7 Backward Fire

**Date:** 11 August 2026  
**Status:** G7.7 backward audit complete; these classifications supersede the candidate statuses in v0.1 where stated.

## 1. `G7.FILTERED_ATTRACTOR.v0.2`

**Classification: PROMOTED — derived universal strategy-language reachability field/operator.**

The mathematical fixed point remains ordinary G6 strict attraction on an attacker-edge-pruned graph. The proof-language extension is that a certificate retains the original game graph and declares a semantic attacker-edge language `F`, proving that the target is forceable while the attacker remains inside `F` before target entry.

The first frozen instantiation is `CHECK`: every pre-target attacker move must give check; final target entry is exempt. Backward fire shows that CHECK is useful but not uniformly dominant: it retains high fractions in some minor-piece arenas, ~30% in rook/fortress examples, and can lose share sharply as earlier pawn ranks are added. Therefore **the operator is general; the coverage of a particular strategy language is topology-dependent.**

## 2. `G7.FILTER_PIVOT.v0.2`

**Classification: PROMOTED — universal finite-game factorization / core composition operation.**

For `A=Attr(T)`, `C=Attr_F(T)`, `Q=A\C`, define `K_F` as attacker-owned states in `Q` having an `F`-excluded edge into `C` (outside any target-entry exemption). Then `Q` is nonempty iff `K_F` is nonempty and is exactly the ordinary residual backward closure generated from `K_F` outside `C`.

Promotion basis:
- mathematical proof frozen in G7.6;
- 100,000 arbitrary finite graph/filter regressions, 0 mismatches;
- G7 higher-tree exact regressions F01/F02/F09;
- G7.7 backward fire: 24/24 all-file advanced same-side N/B/R arenas exact, 3/3 nested full-rank d-file arenas exact, faithful-terminal fortress exact, all with 0 missing/extra.

The operation is distinct from G6 Branch/Hyperkernel composition: Branch/Hyperkernel factors defender choice among **destinations/targets**; Filter-Pivot factors the attacker’s first necessary departure from a declared **strategy language**. Their populations can overlap weakly: only 3,190 / 117,430 = 2.7165% of the frozen bishop c-file ordinary pure-BRIDGE region lies in the CHECK corridor.

## 3. Strategy-language scaling annotation

A proof object may now report `strategy_retention = |Attr_F(T)| / |Attr(T)|` and `pivot_amplification = |Attr(T)\Attr_F(T)| / |K_F|`. These are descriptive certificate metrics, not universal chess constants.

On the corrected d-file rank-band expansion 5-7 -> 2-7, ordinary target attraction grows by 1.339x N / 1.568x B / 1.990x R, while CHECK grows by 1.000x / 1.0016x / 1.0001x. The quiet-required complement grows 4.050x / 4.778x / 2.410x. This is retained as a retrospective scaling observation, not promoted as a theorem.

## 4. `G7.RESTORE.CONVERSION_SAFE_WHITE_MOBILE.v0.1`

**Classification after backward fire: CONDITIONAL SHARPENING, existing RESTORE object type.**

In the original G5 d-file rank5-7 N/B arenas, the backward-specialized guard `restored mobile piece not on own promotion square` removes 551 of 1,086 knight failures and 509 of 1,557 bishop failures, but leaves 535 and 1,048 failures respectively. It therefore does not subsume FAR3/FAR5 or become a universal restoration law.

## 5. `G7.SANCTUARY_ACCESS_GUARD.v0.1`

**Classification: CONDITIONAL GUARD/FALSIFICATION FAMILY; no new object class.**

The G6 faithful wrong-colour fortress is the lower-material base anchor: the existing wrong-colour bishop cannot access the promotion corner and `BK=corner => draw` is exact. G7 F09/F10 supply the nontrivial lift preservation/destruction split. G6 contains no matched extra-resource lift arena, so G7.7 does not invent a backward count.
