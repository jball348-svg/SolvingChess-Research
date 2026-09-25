# R2 Discovery Implementation Freeze

**Status:** prospective implementation clarification, committed before any D1/H1 complete top-signature W/D/L solve or inspection.

This file instantiates the atom categories and deterministic enumeration left abstract in `R2_DISCOVERY_HYPOTHESIS.md`. It does not alter any pass/fail threshold.

## 1. Exact concrete D1 state atoms

The target miner uses exactly these 20 positive Boolean atoms, in this lexical ID order:

| ID | Atom |
|---|---|
| S00 | WHITE_TO_MOVE |
| S01 | SIDE_TO_MOVE_IN_CHECK |
| S02 | WHITE_PROMOTION_LEGAL |
| S03 | BLACK_PROMOTION_LEGAL |
| S04 | WK_DISTANCE_TO_WHITE_PROMOTION_LE_1 |
| S05 | WK_DISTANCE_TO_WHITE_PROMOTION_LE_2 |
| S06 | BK_DISTANCE_TO_WHITE_PROMOTION_GE_4 |
| S07 | BK_DISTANCE_TO_WHITE_PROMOTION_GE_5 |
| S08 | WHITE_BISHOP_ATTACKS_BLACK_PAWN |
| S09 | BLACK_BISHOP_ATTACKS_WHITE_PAWN |
| S10 | WHITE_BISHOP_CONTROLS_WHITE_PROMOTION_SQUARE |
| S11 | BLACK_BISHOP_CONTROLS_WHITE_PROMOTION_SQUARE |
| S12 | WHITE_PAWN_DEFENDED_BY_WHITE_KING |
| S13 | WHITE_PAWN_DEFENDED_BY_WHITE_BISHOP |
| S14 | BLACK_PAWN_DEFENDED_BY_BLACK_KING |
| S15 | BLACK_PAWN_DEFENDED_BY_BLACK_BISHOP |
| S16 | BISHOPS_SHARE_DIAGONAL_GEOMETRY |
| S17 | WHITE_BISHOP_ATTACKS_BLACK_BISHOP |
| S18 | SIDE_TO_MOVE_HAS_CHECKING_MOVE |
| S19 | WHITE_CERTIFIED_LOWER_CAPTURE_EXIT_EXISTS |

All are computed from the current board, legal move semantics, relative promotion squares and exact lower-material truth only. No top-signature W/D/L label is read.

## 2. Exact concrete move atoms

The strategy miner uses exactly these 10 positive move-effect atoms:

| ID | Atom |
|---|---|
| M00 | GIVES_CHECK |
| M01 | CAPTURES |
| M02 | CAPTURES_MOBILE_PIECE |
| M03 | CAPTURES_PAWN |
| M04 | MOVES_WHITE_KING_CLOSER_TO_WHITE_PROMOTION |
| M05 | MOVES_WHITE_KING_FARTHER_FROM_BLACK_PROMOTION |
| M06 | ATTACKS_BLACK_PAWN_AFTER_MOVE |
| M07 | DEFENDS_WHITE_PAWN_AFTER_MOVE |
| M08 | ATTACKS_BLACK_BISHOP_AFTER_MOVE |
| M09 | ENTERS_EXACT_LOWER_WHITE_WIN |

Only White attacker edges are filtered. Black replies remain unfiltered.

## 3. Candidate enumeration

Target clauses:

- all nonempty 1-, 2- and 3-atom conjunctions over S00–S19;
- a conjunction is exact-admissible only when every matching top-signature D1 state is in the prospectively defined A4 certified basin;
- all two-clause disjunctions of exact-admissible conjunctions whose total literal count is <=4;
- redundant disjunctions where one clause subsumes the other are skipped because they denote the same set;
- candidates are enumerated by increasing total literal count, then first clause bitmask, then second clause bitmask;
- the hard 100,000-candidate budget from the hypothesis remains controlling.

Selection is exactly the hypothesis ranking: cardinality/A4 coverage, fewer literals, side-to-move diversity, then lexical mask order. Material-signature diversity is constant because target selection is top-signature only.

Implementation uses a 20-bit semantic feature vector and superset-count transform; this changes evaluation cost, not the candidate language.

## 4. Typed lower endpoints and the attractor used for strategy discovery

The selected semantic target remains a top-signature set.

To make R2 actually exercise opposing-material transitions, the proof target used for ordinary/filtered attractor discovery is the typed union:

`R2_COMPOSITE_TARGET = SELECTED_SEMANTIC_TARGET ∪ EXACT_LOWER_CAPTURE_ENDPOINTS`

where `EXACT_LOWER_CAPTURE_ENDPOINTS` means a legal capture from the top signature into a lower signature whose exact lower state is White-winning.

Operationally, lower endpoints are treated as already-certified target exits rather than expanded inside the top-signature attractor.

Promotion/checkmate shortcuts that do not first enter the selected semantic target are **not** counted as target entry. This preserves strict target semantics while allowing exact material-reduction endpoints to compose.

R2 reports both:

- semantic-target-only strict attraction; and
- composite target attraction with typed lower capture endpoints.

The frozen coverage/residual thresholds in `R2_DISCOVERY_HYPOTHESIS.md` are applied to the **composite** proof object because R2 explicitly tests composition across opposing material. Direct target exactness is always reported separately.

## 5. Strategy class/program enumeration

- every one-atom move class M00–M09;
- every two-atom conjunction;
- exact filtered-attractor coverage computed for all 55 classes;
- rank by larger D1 composite-attractor coverage, fewer literals, lexical mask;
- the best **6** classes enter ordered phase search (within the hypothesis limit of at most 12);
- evaluate all 36 ordered `F -> G` programs over those six classes;
- one switch maximum;
- select by larger exact coverage, then fewer total literals, then lexical pair order.

No program is selected from W/D/L coverage.

## 6. Cost accounting

Discovery timing starts before exact lower-signature solving and includes:

- lower-signature exact solve;
- D1 structural/semantic feature generation;
- A4 construction;
- target enumeration/ranking;
- semantic-only and composite ordinary attractors;
- all 55 filtered classes;
- all 36 ordered programs.

The later complete top-signature W/D/L solve is timed separately for `DISCOVERY_COST_RATIO`.

## 7. Validation freeze

After the D1 target and strategy program are printed/frozen by the discovery harness:

- no atom, clause, threshold or program may change;
- D1 full W/D/L may then be solved;
- H1 receives the D1 target formula and strategy program unchanged;
- H1 may compute its own exact lower-material dependencies because those are typed endpoints, not retraining;
- H1 full W/D/L is used only after unchanged object application.

No square-level exceptions are permitted.
