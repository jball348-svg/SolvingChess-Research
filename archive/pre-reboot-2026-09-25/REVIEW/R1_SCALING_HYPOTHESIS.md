# R1 Scaling Hypothesis — prospective freeze

**Session:** R1 — Scaling and Lifting Audit  
**Freeze status:** PROSPECTIVE — frozen before any R1 outcome truth is inspected  
**Review mode:** independent viability review; G15 remains forbidden  
**Result vocabulary:** `SURVIVED`, `FAILED`, `PARTIAL`, `NO_CANDIDATE`

## 1. Primary falsifiable proposition

R1 tests the following proposition without weakening it after outcome inspection:

> There exists a repeatable ascent/lifting mechanism, already latent in the G6–G8 stack, such that prospectively increasing material and relaxing geometric restrictions can produce new exact chess truth while the combined discovery, solve and verification burden grows materially slower than naive state-space expansion.

The proposed latent mechanism is not “a faster solver” alone. It is the conjunction of:

1. **material-signature decomposition** so only one live signature is solved at a time while lower signatures are reused as exact dependencies;
2. **strict semantic-target attractors** using the frozen G5 target rather than an outcome-fitted target;
3. **the frozen G8 semantic move-language palette** and ordered one-switch filtered attractors;
4. **exact dependency replay** by a separate Bellman verifier.

R1 will separately score truth-production scaling and proof/discovery leverage.

## 2. Frozen finite-game model for the new R1 ladder

The new R1 experiment uses a deliberately small, review-only board model so several prospectively ordered material/restriction levels can be tested exactly.

### State model

- Standard 8×8 board.
- Pieces are WK, BK, one White mobile piece (bishop unless otherwise declared), plus labeled White pawns.
- Both sides to move are represented.
- Static-valid legal placements only:
  - no overlap;
  - kings are not adjacent;
  - the king of the side that is **not** to move may not already be attacked by the side-to-move material;
  - the side-to-move king may be in check.
- No castling, en-passant, halfmove clock, repetition count or claim history.
- This is therefore **historical board-state semantics**, not G10/G12 full-rule state.
- Reachability type is **ARENA_ADMISSIBLE**, never START_REACHABLE.

### Move/terminal model

- Ordinary legal king, bishop/rook and White-pawn moves.
- White pawns move toward rank 8.
- Promotion is a White-winning terminal.
- Ordinary checkmate is a White-winning terminal.
- Stalemate is draw.
- If BK captures a White non-king piece, play enters the exactly solved lower material signature.
- Cyclic non-winning play is draw under the one-sided reachability solve.
- No outcome is imported from an external tablebase.

### Material signatures

Each subset of the declared White non-king material is a separately indexed signature. Lower signatures are solved first and reused exactly by higher signatures. The producer records:

- number of live signatures;
- states per signature;
- total dependency states;
- maximum live-signature state count;
- ratio `total dependency states / max active signature states`;
- solve time and peak RSS.

This ratio is the principal R1 memory-economics test of material-signature decomposition. It is **not** treated as truth-discovery leverage.

## 3. Frozen semantic proof objects

### 3.1 G5 common target — unchanged

For the labeled d-pawn, the direct semantic target is exactly:

- d-pawn exists and is on d6 or d7;
- Chebyshev king distance `d∞(WK,d8) <= 4`;
- Chebyshev king distance `d∞(BK,d8) >= 5`.

No extra square, rank, material-count or outcome-dependent predicate may be added after the freeze.

### 3.2 Strict target attractor

The strict target attractor is computed **inside the top material signature**.

- Actual entry into the frozen target is required.
- Promotion, checkmate and material-reduction exits do **not** count as shortcuts for this proof object.
- Black retains all legal top-signature replies.
- White may use any legal top-signature move.

Metrics:

- direct target size;
- target false positives against exact W/D truth;
- strict attractor size;
- strict attractor share of the exact top-signature White-win basin;
- residual win count and residual fraction.

### 3.3 Frozen G8 strategy palette

The allowed White move languages are frozen before outcome inspection:

- `CHECK`: the move leaves BK in check;
- `KING_ONLY`: the moving piece is WK;
- `PAWN_ONLY`: the moving piece is any White pawn;
- `MOBILE_PIECE_ONLY`: the moving piece is the declared bishop or rook.

No square-ID language and no new semantic class may be added.

For every ordered pair F→G, R1 computes the exact nested filtered attractor

`ATTR_F( ATTR_G( TARGET ) )`

inside the same top signature. Black replies are never filtered.

Metrics:

- best frozen one-switch coverage of the ordinary strict-target attractor;
- residual count;
- identity of the best frozen pair;
- whether any arena-specific predicate was required (frozen answer must remain zero).

## 4. Prospectively frozen ascent ladder

All pawn files are fixed by label. Allowed rank sets are part of the arena declaration and may not be changed after outcome inspection.

| ID | Material | Pawn restrictions | Purpose |
|---|---|---|---|
| P0 | K+B+dP vs K | d-pawn d5–d7 | historical-calibration scale, one non-king pawn |
| P1 | K+B+aP+dP vs K | a7 fixed; d5–d7 | one-step material ascent |
| P2 | K+B+aP+dP+eP vs K | a7 fixed; d5–d7; e7 fixed | second material ascent, three pawns |
| P3 | K+B+aP+dP+eP vs K | a6–a7; d5–d7; e6–e7 | same material, restrictions relaxed |
| H1 | K+B+aP+dP+eP vs K | a5–a7; d4–d7; e5–e7 | hostile geometry/mobility control |
| H2 | K+R+aP+dP+eP vs K | a6–a7; d5–d7; e6–e7 | hostile high-mobility/checking control |

The sequence P0→P1→P2 tests material ascent. P2→P3 tests restriction relaxation without adding material. H1 attacks the mechanism with more pawn mobility and more quiet alternatives. H2 attacks it with a materially more checking-capable mobile piece while preserving the pawn ladder.

No arena may be shrunk after a timeout or bad result. A resource hold remains evidence.

## 5. Frozen metrics

For every new arena R1 records at minimum:

- material signature;
- total pieces;
- allowed pawn files/ranks;
- mobile-piece placement freedom;
- number of live material signatures;
- capture closure;
- static-valid top-signature states;
- dependency states;
- mean / p95 / maximum legal branching;
- White-move checking density;
- presence/count of move-resource classes;
- terminal/rules model;
- reachability type;
- producer wall time;
- producer peak RSS;
- verifier wall time;
- verifier peak RSS;
- serialized truth payload size;
- direct target size;
- target false positives;
- strict target-attractor size and win coverage;
- best one-switch coverage;
- residual full-win fraction;
- newly required arena-specific predicates.

## 6. Truth-production scaling gate

Truth-production scaling **survives** P0–P3 only if all of the following hold:

1. all four arenas solve exactly and Bellman-verify without arena shrinkage;
2. each run stays inside the frozen local budget of **300 s wall time and 3.0 GiB peak RSS**;
3. producer time per million dependency states at P3 is no worse than **3×** the median of P0–P2;
4. at P2 and P3, `total dependency states / max active signature states >= 2.0`;
5. at P2 and P3, verifier wall time is no more than **1.5×** producer wall time;
6. no semantic weakening or outcome-dependent legality shortcut is introduced.

A timeout, RSS breach, verifier mismatch or verifier reversal beyond the threshold is preserved as negative scaling evidence.

## 7. Proof/discovery leverage gate

Proof/discovery leverage **survives** P0–P3 only if all of the following hold with the target and palette unchanged:

1. **zero target false positives** in every arena;
2. strict target-attractor coverage at P2 and P3 is at least **20% of the exact top-signature White-win basin**;
3. coverage at P3 is not more than **15 percentage points below P0**;
4. the best frozen one-switch palette covers at least **90% of the ordinary strict-target attractor** in P1–P3;
5. the full-win residual fraction does not worsen by more than **15 percentage points** from P0 to P3;
6. **zero** new arena-specific predicates are introduced.

This gate is intentionally distinct from solver speed. A fast solve with collapsing proof coverage is not a proof-language success.

## 8. Hostile-control gate

The hostile suite is H1 and H2. It passes only if both arenas:

- complete inside the same 300 s / 3.0 GiB budget;
- retain zero false positives for the unchanged target;
- retain at least **15%** strict-target-attractor coverage of their full White-win basin;
- retain at least **75%** best frozen one-switch coverage of the strict target basin;
- require no new predicates.

A target false positive in either hostile arena is an explicit falsification of direct target transfer at that scope.

## 9. Scaling-law discipline

R1 may describe a trend only from at least three ordered points.

For runtime, memory and proof coverage, R1 will report:

- raw observations;
- simple descriptive ratios/slopes;
- any fitted curve only as descriptive;
- no extrapolation to unrestricted chess unless the tested range warrants it.

“No defensible scaling law can yet be inferred” is an allowed and preferred conclusion over overfitting.

## 10. R1 classification rule

- **SURVIVED** — P0–P3 pass both truth-production and proof/discovery gates, and the hostile gate passes.
- **PARTIAL** — exactly one of truth-production scaling or proof/discovery leverage survives, or the main ladder survives but hostile transfer does not.
- **FAILED** — the tested mechanism loses favourable economics, proof leverage collapses, exact target transfer fails materially, or tractability requires retreat to stronger restrictions.
- **NO_CANDIDATE** — used only if implementation/reconstruction shows the proposition cannot be coherently instantiated without changing its meaning.

No impressive individual run may upgrade PARTIAL to SURVIVED.

## 11. Strike discipline

A strike is not automatic from a timeout or one hostile failure.

A strike is considered only if R1 shows that the central claimed lifting mechanism itself collapses into local enumeration / arena-specific redesign, in the sense fixed by `REVIEW/REBOOT_CRITERIA.md`.

## 12. Freeze declaration

This file freezes the proposition, exact model, ladder, hostile controls, proof objects, metrics, budgets and classification thresholds **before any new R1 arena outcome is inspected**.

Subsequent corrections may repair implementation defects, but they may not change the scientific benchmark to improve the result. Any necessary semantic change must be recorded as a deviation and the affected run cannot count as a clean prospective pass.
