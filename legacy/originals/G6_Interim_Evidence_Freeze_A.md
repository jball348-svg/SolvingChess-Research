# G6 Interim Evidence Freeze A

**Date:** 11 August 2026  
**Scope:** G6.0 reconstruction plus first restoration, target-transfer, BRIDGE and nested-scaling campaign.

## Gate status

G5 count/membership reconstruction is independently strong: KPK, both G5 universes, both corrected W/D basins, restoration-failure counts and immediate-stalemate subsets, direct targets and strict target attractors all reproduce exactly. Historical max-rank labels do not yet reproduce (new 26/22 versus frozen 24/21), so rank numbering is explicitly non-certified. Full G4 reconstruction remains open because the prose handoff specifies an optional-pawn internal graph but is not being treated as sufficient implementation detail to invent capture-state encoding.

## New certified/negative results

- **KRK lower-material certificate:** 399,112 static-valid states; 376,868 W / 22,244 D. All 175,168 valid White-to-move KRK positions are wins.
- **TARGET_SAFE:** the original G5 geometric target fails on the c-file only through immediate Black-to-move stalemate (16 N, 50 B). Adding the semantic guard `not immediate stalemate`, frozen before b/e evaluation, yields zero false positives on held-out b/e and retains large strict attractors.
- **Rook restoration:** `projected KPK win AND not immediate stalemate => restored K+R+P win` has zero violations in all tested rook families, including d2-d7.
- **Far restoration guard:** the frozen distance>=5 guard transfers with zero violations to bishop and rook on held-out a/b/c/e full-rank files, but fails for edge knights (103 a-file, 46 b-file). This is preserved as a topology-specific falsification.
- **BRIDGE mechanism:** splitting TARGET_SAFE by **Black king side of the pawn file** produces strict pure bridges: N-d 3,486; B-d 9,756; N-b 1,937; B-b 234. The analogous **White king side** control is much weaker: 17, 1,708, 57, 0. Rook is zero in both. Defender-controlled target ambiguity is therefore a strong candidate predictor, not yet claimed as the historical cause of G3/G4.
- **Scaling:** TARGET_SAFE stays unchanged and zero-counterexample as d-file ranks expand 5-7 -> 4-7 -> 2-7, while exact arena size grows to 2.423M N / 2.362M B / 2.266M R. Restoration shows a phase transition at rank 2 for N/B but not R.

## Main unresolved items

1. Historical G5 rank-label convention.
2. Full G4 implementation-level graph reconstruction.
3. Retrospective G3/G4 bridge-mechanism audit.
4. New critical-manifold atlas passes and opposing-minor arena.

The JSON ledger is authoritative for this interim G6 freeze; raw command logs and SHA-256 sums are bundled alongside the solver sources.
