# R3 Start-Closure Hypothesis — prospective freeze

**Session:** R3 — Start-Reachable All-Reply Closure Audit  
**Freeze status:** PROSPECTIVE — frozen before decisive ply-3/4/5 frontier expansion  
**Review mode:** independent viability review; G15 forbidden; R4 not started  
**Result vocabulary:** `SURVIVED`, `FAILED`, `PARTIAL`, `NO_CANDIDATE`

## 1. Primary proposition

R3 tests, without weakening after decisive frontier inspection:

> There exists a prospectively frozen START_REACHABLE expansion mechanism under the G10 semantic rules and the forward G12.STATE.SERIAL.v2 identity profile that grows a nontrivial start-rooted White-strategy DAG, keeps every admitted Black node exact-all-reply represented, and leaves an unresolved exact frontier at no more than 50% of the competent raw legal-tree leaf count while using exact full-state rather than board-only merging.

A bounded test may remain unconnected to an historical solved basin. Such a result is not an initial-position non-loss certificate.

## 2. Exact theorem state and root

Semantic rules are G10.RULES.v1.0 as carried forward by G12. Equality follows the G12 v2 semantic fields:

- 64-square piece placement;
- side to move;
- four monotone castling rights;
- effective en-passant square only when at least one en-passant capture is legally available;
- exact halfmove clock;
- exact bounded repetition-count map inside the current barrier epoch.

REP identity is board + side + castling rights + effective EP. A pawn move, capture, or permanent castling-right reduction is a repetition barrier and resets prior repetition counts. Canonical equality is on the full semantic payload; no board-only quotient is permitted.

Root is the standard initial position with White to move, KQkq rights, no effective EP, halfmove 0, and repetition map containing the root REP key with count 1.

Claimable/automatic draw and terminal semantics remain part of the contract. At the frozen <=5-ply horizon, 50/75-move and threefold/fivefold thresholds are expected to be inactive; any unexpectedly active claim/automatic draw is recorded rather than suppressed.

## 3. Expansion mechanism

R3 tests an exact transposition DAG with asymmetric move treatment:

- **Black nodes:** every legal Black move is generated. No pruning, policy filtering or engine evaluation is permitted. Exact-identical full successor states may merge.
- **White nodes:** retain every move matching one prospectively selected semantic move class. If the selected class has no move at a White node, that node becomes unresolved; there is no opening-sequence fallback.
- Horizon leaves are always unresolved unless they enter an already-certified exact object.

This is a structural closure experiment. A horizon leaf is not certified non-loss merely because expansion stops.

## 4. White semantic grammar and selection

The frozen move-effect atoms are:

- `ANSWER_CHECK`: any legal move when White is currently in check;
- `DEVELOP_MINOR`: move a White knight or bishop from its original home square to a different square;
- `CENTER_PAWN`: advance a White pawn originating on files c,d,e,f;
- `CASTLE`;
- `CAPTURE`;
- `GIVES_CHECK`.

Candidate classes are the following fixed disjunctions:

1. `ANSWER_CHECK OR DEVELOP_MINOR`
2. `ANSWER_CHECK OR CENTER_PAWN`
3. `ANSWER_CHECK OR DEVELOP_MINOR OR CENTER_PAWN`
4. `ANSWER_CHECK OR DEVELOP_MINOR OR CASTLE`
5. `ANSWER_CHECK OR DEVELOP_MINOR OR CENTER_PAWN OR CASTLE`
6. `ANSWER_CHECK OR DEVELOP_MINOR OR CENTER_PAWN OR CASTLE OR CAPTURE OR GIVES_CHECK`

No square-ID exception, named opening sequence, engine score or topological patch is allowed.

**Training allowance:** on the discovery branch only, inspect legal/full-state structure through ply 2. Select the candidate with the smallest White-choice ratio among candidates having at least one admissible White move at every encountered White node; tie-break by fewer atoms, then the list order above. No ply >=3 data may be used to change the selected class.

Maximum program complexity is one semantic phase (strictly below the allowed two-phase ceiling).

## 5. Discovery and held-out start branches

Both branches are exact descendants of the standard root and are defined before decisive expansion.

- **D — discovery branch:** White first move is any legal king-pawn advance from e2 (one or two squares).
- **H — held-out branch:** White first move is any legal queen-pawn advance from d2 (one or two squares).

The root-to-branch first move is a semantic family declaration, not a learned sequence. After that move, the identical selected White class, full-state identity, Black-all-reply rule and budgets apply unchanged.

No predicate may be added after H is inspected.

## 6. Frozen horizons and budgets

Training stops at ply 2.

Decisive ordered test points are exact plies **3, 4 and 5** from the standard root. Raw competent baseline and proof-DAG metrics are recorded at all three. Ply 2 is retained as a diagnostic/training point only.

Resource ceiling for the complete R3 experiment:

- wall-clock target: 180 s per baseline/mechanism run;
- peak RSS target: 2.0 GiB;
- no outcome-driven benchmark shrinking.

If ply 5 cannot complete inside the declared budget, that is negative scaling evidence; results at completed frozen horizons remain valid but no three-point trend may be claimed.

## 7. Competent raw baseline

For each horizon/branch, baseline expansion uses the same legal move generator and exact full-state transition semantics as the mechanism, with:

- every legal move for both sides;
- exact full-state transposition canonicalization;
- separate raw move-tree leaf/node counts without disabling transpositions;
- no engine pruning.

## 8. Frozen diagnostics

At each test point:

`TREE_COMPRESSION = unique_exact_full_states / raw_legal_tree_nodes`

`PROOF_FRONTIER_RATIO = unresolved_exact_frontier_states / raw_leaf_nodes`

`BLACK_REPLY_CLOSURE = represented_black_legal_edges / total_black_legal_edges_encountered`

`WHITE_CHOICE_RATIO = retained_white_edges / total_legal_white_edges_encountered`

`HISTORY_MULTIPLIER = exact_full_states / distinct_board_placements`

`CLOSURE_COST_RATIO = proof_DAG_construction_wall / competent_raw_exact_forward_wall`

Also record cumulative/raw nodes, exact unique states, duplicate ratio, White/Black nodes, history-distinct same-board states, castling/EP/halfmove/repetition split counts, memory and any certified-basin entries.

## 9. Positive thresholds

`SURVIVED` requires all of:

- every admitted state exact START_REACHABLE from the declared root/branch;
- Black reply closure 100% at every expanded Black node;
- state-identity violations 0;
- illegal/omitted Black moves 0;
- no engine/evaluation pruning;
- selected White class frozen before ply >=3 inspection;
- at least three completed decisive horizons;
- largest-horizon PROOF_FRONTIER_RATIO <= 0.50;
- compression trend does not collapse toward raw-tree growth across the three points;
- held-out largest-horizon frontier ratio <= 2x discovery ratio and <= 0.50;
- history multiplier is measured and does not invalidate claimed exact merging;
- no absolute opening-sequence exception;
- verifier/replay regenerates the recorded edge/state counts exactly;
- result is stronger than transposition-table savings alone.

Because no shallow opening path is expected to hit G12 KQK/KRK/KPK, lack of basin entry alone does not force failure. But absence of any proof-relevant typed leaf prevents calling a merely structural prefix an INITIAL_POSITION_CERTIFICATE.

## 10. Failure/strike conditions

Serious failure evidence includes near-raw frontier growth, history-state explosion that destroys merging, semantic-class emptiness requiring line memorization, held-out collapse, unsafe board-only merge, heuristic Black pruning, or inability to complete the frozen shallow ladder.

A strike is taken only under REVIEW/REBOOT_CRITERIA.md: e.g. no falsifiable mechanism, only shallow enumeration presented as proof progress, local line fitting, unsafe pruning, or failure to narrow the start/all-reply obligation.

## 11. Freeze declaration

The proposition, exact state identity, root, semantic grammar, selection rule, discovery/held-out branches, horizons, metrics, budgets, thresholds and strike conditions above are frozen **before decisive ply-3/4/5 frontier data are inspected**.

Implementation defects may be repaired only if semantics and frozen scientific choices remain unchanged. Affected provisional outputs are discarded and recorded.
