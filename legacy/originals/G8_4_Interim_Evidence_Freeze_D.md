# G8.4 Interim Evidence Freeze D — Seven-Man Recovery + F10 Faithful Completion

**Programme:** G8 Certificate Engine and Re-Ascent  
**Stage:** G8.4 — Recover seven-man wave  
**Date:** 2026-08-11  
**Status:** CLOSED — PASS EXCEPTIONALLY STRONGLY

## 1. Scope and frozen authority

G8.4 was required to attempt the prospectively frozen G7 seven-man holds **F07/F08 unchanged** through the G8 material-signature engine, and to include the full faithful F10 table if economically feasible. No arena shrinking, terminal substitution, or outcome-guided change is accepted.

Frozen F07/F08 model:
- material: `K+B+2P vs K+B+P`;
- White bishop on colour complex C=0;
- White pawns fixed at `a7,c7`, Black pawn fixed at `b2`;
- F07 Black bishop C=1; F08 Black bishop C=0;
- brink-only promotion resources, ordinary mate/stalemate, immediate win for a legal promotion;
- capture-closed optional-material dependency DAG.

Frozen exact G7 held scales used as hard regressions:
- F07: **45,823,238** static-valid states;
- F08: **43,334,293** static-valid states.

F10 frozen control:
- `K + wrong-colour B + correct-colour B + hP vs K`, faithful continuation;
- raw encodings **50,331,648**;
- static-valid **33,305,146**;
- lower dependency checksums: KPK `41,619 = 27,430 W + 14,189 D`; wrong-colour F4 `1,182,440 = 825,269 W + 357,171 D`; correct-colour F4 `1,182,525 = 1,099,020 W + 83,505 D`;
- BK=h8 states **586,893**, immediate checkmates **3,578**;
- G7 status: full truth scale hold.

## 2. F07 exact recovery

Accepted dump-producing run:

- dependency graph: **45,823,238**
- graph White wins: **24,428,400**
- graph Black wins: **12,317,126**
- graph draws: **9,077,712**
- full-material states: **4,759,054**
- full White wins: **2,556,211**
- full Black wins: **2,200,883**
- full draws: **1,960**
- wall: **10.76 s**
- peak RSS: **55,696 KiB**

Full-material direct capture transitions:
- SIG15 (White bishop removed): 217,215
- SIG23 (Black bishop removed): 238,411
- SIG27 (White a7 pawn removed): 148,955
- SIG29 (White c7 pawn removed): 201,330
- SIG30 (Black b2 pawn removed): 924,295
- total: **1,730,206**

Packed persistent validity+outcome storage across all 32 material signatures: **26,763,264 bytes**.

Independent verifier:
- static checked: **45,823,238**, mismatches **0**;
- Bellman checked: **45,823,238**, mismatches **0**;
- wall: **4.08 s**;
- peak RSS: **29,700 KiB**.

Canonical truth SHA-256:
`6cda93279161aba0dfaa07a08e98443fa351b54823ab1b0529faf37354bef992`

## 3. F08 exact recovery

Accepted dump-producing run:

- dependency graph: **43,334,293**
- graph White wins: **21,993,686**
- graph Black wins: **11,672,354**
- graph draws: **9,668,253**
- full-material states: **4,294,949**
- full White wins: **2,305,156**
- full Black wins: **1,987,745**
- full draws: **2,048**
- wall: **10.49 s**
- peak RSS: **54,876 KiB**

Full-material direct capture transitions:
- SIG15: 710,877
- SIG23: 711,753
- SIG27: 535,487
- SIG29: 740,705
- SIG30: 737,839
- total: **3,436,661**

The same-colour arena therefore has ~1.986x as many full-material direct capture exits as F07, consistent with the prospectively frozen topology note that direct bishop exchanges are enabled in F08 and suppressed in the opposite-colour control.

Packed persistent validity+outcome storage: **26,763,264 bytes**.

Independent verifier:
- static checked: **43,334,293**, mismatches **0**;
- Bellman checked: **43,334,293**, mismatches **0**;
- wall: **3.76 s**;
- peak RSS: **29,700 KiB**.

Canonical truth SHA-256:
`fc86918a8b2fbaa71f31464777d0fdc028214fb6092ead616e60f9182d1cf620`

## 4. F10 faithful full-table recovery

The full faithful F10 control is also recovered.

Accepted exact truth:
- static-valid: **33,305,146**
- White wins: **32,828,134**
- draws: **477,012**
- White-win rate: **98.567753%**
- draw rate: **1.432247%**
- Black wins: impossible in the declared lone-BK defender continuation and not present.

BK=h8 slice:
- states: **586,893**
- White wins: **572,681**
- draws: **14,212**
- White-win rate: **97.578434%**
- draws: **2.421566%**
- immediate checkmates: **3,578**

Thus the old G7 terminal falsifier was only a small visible subset of the full destruction effect. The matched F09 result was universal sanctuary preservation (330,264 / 330,264 BK=h8 draws); F10 shows that allowing the added bishop access to the critical corner destroys the sanctuary over almost the entire BK=h8 population.

Accepted producer/dump run:
- F10 solve: ~**9.1–9.8 s** depending on dump/audit mode;
- dump run peak RSS: **81,208 KiB**;
- packed membership bytes across KPK + both F4 dependencies + F10: **13,381,632**.

Canonical truth SHA-256:
`aa145109278da9570f4f30860f7e8346f8285323301e50ae2941075a5ea521b2`

## 5. F10 dependency alarm and rejected result

The first reconstructed F10 pass was **rejected** despite matching the F10 static population and terminal witness counts, because its lower wrong-colour F4 dependency returned 825,671 wins instead of the frozen 825,269.

The defect was isolated to a reverse-edge implementation error in the reconstructed F4 helper: a reverse h2->h4 double-pawn predecessor was admitted when h3 was occupied by the bishop. The forward graph correctly rejected the move. This created exactly **402 spurious wrong-colour F4 wins**.

After the predecessor fix:
- KPK: `27,430 W / 14,189 D` exact;
- wrong-colour F4: `825,269 W / 357,171 D` exact;
- correct-colour F4: `1,099,020 W / 83,505 D` exact.

No F10 truth from the rejected dependency pass is retained.

## 6. Independent F10 verification

A separately implemented forward/Bellman verifier loads only the packed truth dependencies and reconstructs static validity, legal continuations, faithful promotion outcomes, lower-material exits, terminal mate/stalemate logic and Bellman obligations.

Combined dependency verification:
- checked states: **35,711,730** (KPK + wrong F4 + correct F4 + F10)
- static mismatches: **0**
- Bellman mismatches: **0**
- F10 White wins: **32,828,134**
- F10 draws: **477,012**
- BK=h8: **586,893**
- BK=h8 White wins: **572,681**
- immediate mates: **3,578**
- verifier wall: **14.08 s**
- peak RSS: **16,648 KiB**.

## 7. Engineering conclusion

G8.4 removes the seven-man frontier rather than merely nudging it:

- F07 exact seven-man hold -> recovered in ~10 s.
- F08 matched seven-man hold -> recovered in ~10 s.
- F10 faithful 33.3M full-table hold -> recovered in ~9 s producer time and independently verified.

The key G8 engineering pattern survives the higher material count: solved-once typed dependencies, packed validity/truth, and reuse of certified membership eliminate repeated legality/dependency work that dominated the earlier monolithic retrogrades.

F07/F08 also show that seven-man material count itself was not the limiting variable: full-material strata are only ~4.3–4.8M states, while the optional-material closure spans ~43–46M. Signature decomposition turns that closure from one monolithic propagation problem into 32 ordered dependency nodes.

## 8. Scientific consequence

The matched F07/F08 pair now supplies exact seven-man truth for later G8.5 strategy-language analysis. The large difference in capture-edge density is structural and prospectively predicted, while the full W/B/D populations remain close in the full-material stratum: both are ~53.7% White wins, ~46.2–46.3% Black wins, and under 0.05% draws.

F10 upgrades the G7 sanctuary-access result from terminal falsification to full exact population truth. Critical-square access is not merely sufficient to create exceptional mating witnesses: in the frozen matched control it converts **97.58% of all BK=h8 states into White wins**.

This remains evidence for the existing `SANCTUARY_ACCESS_GUARD` / RESTORE family, not a new proof-object class.

## 9. Source/binary hashes

Seven-man producer source:  
`8675dce2ee71fe25c0c321324334fa2e42b53b4b72e2853c3c79cfe4aaa298d4`

Seven-man dump producer source:  
`f8613f43633f4148bff964b25200f4707e18e70bbbcc012d9ea594ece0e06423`

Seven-man independent verifier source:  
`cb5091cb13cc99dcdcb44b219267326f2308816893875f78561a2df83dade75b`

F10 producer source:  
`c351eb3ee960d7667c2d66bfa25806aebb693c7bca216769b378aca0397af018`

F10 dump producer source:  
`74e5cbfe0281ddef168379cf1ad45cef469a61386a7198199ed59b99b6c675fc`

F10 independent verifier source:  
`e8d63790df818a33b0fc37402cac8a0535b7f32bacfd3837bf776d86c8217f62`

## 10. G8.4 gate

**PASS EXCEPTIONALLY STRONGLY.** The stage required first recovered seven-man exact tables or preservation of a sharper frontier. Instead:

1. both frozen seven-man holds are recovered unchanged;
2. both have exhaustive independent static and Bellman verification;
3. the optional F10 faithful full table is also recovered;
4. F10 reproduces every frozen dependency and terminal checksum before its new W/D truth is accepted;
5. the original seven-man/high-branch G7 execution frontier is therefore no longer present at these scales.

**Next authorised stage: G8.5 — strategy-language algebra across old and newly recovered arenas under the predeclared semantic filter palette.**
