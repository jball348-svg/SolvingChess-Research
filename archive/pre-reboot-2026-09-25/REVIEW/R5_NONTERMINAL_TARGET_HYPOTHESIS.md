# R5 Nonterminal Target Hypothesis — prospective freeze

**Session:** R5 — Hostile Synthesis and Nonterminal Bridge Attack  
**Status:** PROSPECTIVE SCIENTIFIC FREEZE  
**Review hold:** OPEN; G15 and R6 forbidden  
**Primary classification vocabulary:** `SURVIVED`, `PARTIAL`, `FAILED`, `NO_CANDIDATE`

## 1. Surviving space after R4

### Genuinely alive
- exact finite-game existential/universal closure;
- exact START_REACHABLE generation under full theorem-state identity;
- semantic White branching compression;
- prospectively frozen semantic target/program discovery;
- Branch / Hyperkernel and Filter-Pivot composition when their leaves are already exact;
- material-signature dependency decomposition;
- typed dependency/certificate/proof-store machinery.

### Strongly disfavoured
- shallow attraction to terminal/draw/current 3–4-piece G12 targets;
- search-until-an-endgame-basin-appears;
- fixed strategy-language universality;
- automatic residual shrinkage with scale;
- board-only theorem-state transpositions;
- proof-payload compression as evidence of cheap truth discovery;
- horizon survival as non-loss evidence.

### Prohibited in R5
Engine/evaluation targets; approximate equality; direct W/D/L target atoms; named opening repertoires; absolute move-line exceptions; square/state-ID patches; post-hoc grammar repair; extensional “non-losing-state” targets; and targets mined from near-complete local W/D/L.

## 2. Primary survival hypothesis

R5 freezes one candidate before any decisive target-membership inspection:

> **FORCED_EXACT_REPETITION_LOCK (FERL-4):** a high-material White-to-move state is an exact nonterminal non-loss target when White has a prospectively bounded semantic strategy that, against every legal Black reply, forces return to the same FIDE repetition identity after exactly four plies without any repetition barrier. Because the returned chess position is repetition-identical and the same four-ply contract remains legal, repeating the contract forces a claimable threefold repetition (or an earlier automatic/claimable draw).

R5 then tests whether direct FERL-4 membership, or one exact White/Black attraction pair into FERL-4, certifies a material fraction of the exact START_REACHABLE D frontier and transfers unchanged to H.

This is deliberately the strongest local draw contract remaining after R4 that:
- lives naturally at high material;
- is exact for a theorem-level reason rather than outcome correlation;
- does not require a lower-material lookup;
- is independently replayable from legal moves and history state;
- has finite bounded proof payload.

## 3. Exact theorem state

Use the R3/R4 full theorem-state contract:

`STATE = (board64, turn, castling_rights, effective_ep, halfmove_clock, repetition_count_map)`.

FIDE repetition identity is:

`REP_ID = (board64, turn, castling_rights, effective_ep)`.

A repetition barrier is any move that:
- moves a pawn;
- captures;
- permanently changes castling rights.

No board-only merge is allowed.

## 4. FERL-4 exact semantics

A nonterminal White-to-move theorem state `s` satisfies FERL-4 iff there exists an admitted White move `w1` such that, for **every** legal Black reply `b1`, there exists an admitted White move `w2` such that, for **every** legal Black reply `b2`:

1. no move on `w1,b1,w2,b2` is a repetition barrier;
2. no line terminates in BLACK_WIN before the return;
3. the resulting state `s4` has exactly `REP_ID(s4) = REP_ID(s)`;
4. any earlier exact draw/claim termination is accepted as non-loss instead of requiring the return.

The two White choices may depend on the exact theorem state reached after Black's preceding reply. Black is never pruned.

### Exactness theorem

If FERL-4 holds at `s`, White cannot lose from `s`.

Reason: every Black branch either reaches a draw earlier or returns after four plies to exactly the same repetition identity with no repetition barrier. Legal-move availability from that repetition identity is unchanged except that halfmove/repetition counters advance toward draw conditions. White can replay the same certified response relation. After at most two successful returns, the starting repetition identity has occurred at least three times and a legal threefold claim exists; a 75-move/fivefold automatic draw can only terminate earlier in White's favour. No W/D/L label of the surrounding domain is used.

FERL-4 is therefore a sufficient exact draw contract, not a classifier correlated with draws.

## 5. Frozen White semantic program

Use one phase and at most six semantic move literals:

`ANSWER_CHECK OR REVERSIBLE_QUIET_NONPAWN OR CENTER_PAWN OR CASTLE OR CAPTURE OR GIVES_CHECK`

Definitions:

- `ANSWER_CHECK`: any legal White move while White is in check.
- `REVERSIBLE_QUIET_NONPAWN`: legal non-pawn, non-capture, non-promotion White move that does not reduce White castling rights.
- `CENTER_PAWN`: legal move by a White pawn originating on files c,d,e,f.
- `CASTLE`: legal White castling move.
- `CAPTURE`: legal White capture.
- `GIVES_CHECK`: legal White move whose resulting position checks Black.

FERL-4 itself additionally requires its four certified cycle plies to contain no repetition barrier, so irreversible policy moves cannot make a false target.

No second phase, named line, square patch or state exception is permitted.

## 6. START_REACHABLE domains

Generate exact policy DAGs from the true standard initial state through ply 6.

### Discovery D
First White move is e2-e3 or e2-e4.

### Hostile H
First White move is any legal knight move from the original b1 or g1 home square.

The state model, policy, target theorem, cohort construction, attraction depth and all thresholds apply unchanged to H.

## 7. Frozen cohorts

At the exact White-to-move ply-6 frontier, select at most 1,024 exact theorem states per family:

- up to 512 with `FORCING_MOVE_AVAILABLE = true`;
- up to 512 with it false;
- lexicographically smallest states under the R5 canonical full-state serialization within each stratum;
- no outcome truth in selection.

`FORCING_MOVE_AVAILABLE` means at least one legal White capture or checking move.

The R5 harness must also report the complete ply-6 frontier counts and history multiplier.

## 8. Certification rule

A cohort state certifies iff either:

1. it directly satisfies FERL-4; or
2. within **one White/Black attraction pair** (maximum local attraction depth = 2 plies), White has at least one admitted move such that every legal Black reply reaches a White-to-move FERL-4 state or an exact draw.

At attraction White nodes, existence is over the frozen semantic program. At all Black nodes, every legal reply is required.

Horizon survival is never a certificate.

## 9. Target-exactness hostile attack

Before crediting coverage, actively test:
- checks and check evasions;
- captures and zwischenzugs;
- king-safety changes;
- pawn breaks;
- exchange-order changes;
- castling-right changes;
- effective en-passant changes;
- repetition/history divergence;
- quiet Black moves;
- any branch in which a supposed four-ply return differs in turn, board, castling rights or effective EP.

One counterexample to an accepted certificate kills the unconditional FERL-4 implementation.

A structurally separate replay verifier must re-generate every legal Black reply for every accepted certificate and confirm the exact REP return/draw condition.

## 10. Truth leakage

`LOCAL_TRUTH_LEAKAGE = outcome-labelled states used before target/program freeze / states in complete validation domain`.

Frozen pre-result value: **0**.

Already certified rule semantics and historical exact dependencies are allowed, but FERL-4 does not use lower-material W/D/L.

Strong survival requires <=5%.

## 11. Competent exact baseline

After the target/program freeze, run the same direct/one-pair FERL-4 proposition with:

- **all legal White moves** allowed at the attraction White node;
- all legal Black replies;
- identical FERL-4 target verifier;
- identical cohorts and exact state identity.

This baseline answers the same proposition. It is not complete chess W/D/L.

## 12. Frozen resource budget

Per D/H family:
- frontier generation: <=180 s wall target;
- target/certification producer: <=180 s;
- independent certificate replay: <=180 s;
- competent baseline: <=180 s;
- peak RSS target: <=2.0 GiB;
- cohort cap: 1,024;
- target cycle: exactly 4 plies;
- attraction depth: exactly 2 plies;
- no depth enlargement or cohort shrinking after results.

## 13. Metrics

Report at minimum:
- `TARGET_EXACTNESS_VIOLATIONS`;
- `CERTIFIED_POLICY_COVERAGE`;
- `CERTIFIED_BLACK_CLOSURE`;
- `CERTIFICATION_RESIDUAL`;
- `LOCAL_TRUTH_LEAKAGE`;
- `TARGET_DESCRIPTION_COMPLEXITY`;
- `POLICY_DESCRIPTION_COMPLEXITY`;
- `CERTIFICATION_COST_RATIO`;
- `PROOF_PAYLOAD_RATIO`;
- `HISTORY_MULTIPLIER`;
- `HELDOUT_DEGRADATION`;
- `DEPENDENCY_REDUCTION`;
- direct FERL-4 target count;
- one-pair attraction count;
- total legal Black replies examined;
- target-killing irreversible Black replies.

## 14. Frozen pass/fail thresholds

Strong `SURVIVED` requires all:
- target exactness violations = 0;
- certified Black closure = 100%;
- illegal/omitted replies = 0;
- state-identity violations = 0;
- local truth leakage <=5%;
- D certified-policy coverage >=20%;
- H certified-policy coverage >=10%;
- H residual degradation <=2x D residual;
- target description = one formally stated invariant of comparable complexity to <=6 literals / <=3 clauses;
- White strategy <=2 phases / <=6 semantic move literals;
- certification cost ratio <=0.75 of the competent exact baseline;
- proof payload ratio <=25%;
- no square/state-ID exceptions;
- no absolute opening lines;
- no post-inspection repair;
- completion inside the frozen resource budget;
- a named review dependency is strictly reduced by a nonempty certified set.

`PARTIAL` requires a genuinely exact and materially useful target with one meaningful economic/generalization gate unresolved.

`FAILED` applies if FERL-4 is coherent and prospectively frozen but exactness, coverage, transfer, economics or payload fails, including negligible/zero coverage.

`NO_CANDIDATE` is reserved for failure to formulate any exact nonterminal theorem at all; because FERL-4 is coherent, R5 will use FAILED rather than NO_CANDIDATE if the test returns negligible coverage.

## 15. Economic accounting

A cheap empty target earns no economic credit.

`CERTIFICATION_COST_RATIO` is reported only for a nonempty certified set, or otherwise marked non-creditable with raw producer/baseline costs shown.

`PROOF_PAYLOAD_RATIO` compares accepted certificate theorem states/edges against the competent exact baseline work for the same proposition. An empty proof payload does not pass the <=25% gate.

## 16. Strike conditions

A strike is warranted if R5:
- changes FERL-4 after inspecting membership;
- mines W/D/L and retrofits a target;
- replaces exact repetition identity with board similarity;
- omits legal Black replies;
- increases depth after zero/low coverage;
- reports a cheap zero-coverage run as economic success;
- merely moves a frontier without reducing a named bridge obligation.

A clean, prospectively frozen falsification does not itself create a strike.

## 17. Dependency claim if successful

A successful FERL-4 test would strictly reduce:

`NONTERMINAL_EXACT_INTERMEDIATE_TARGET_CERTIFICATION`

by exhibiting a repeatable, high-material, outcome-independent exact target with start-side all-reply closure.

It would not by itself solve:
- scalable lower-frontier lifting;
- global START_TO_BASIN_CONNECTOR;
- initial-position non-loss.

## 18. Freeze declaration

The target theorem, exact state model, semantic policy, D/H families, cohort construction, four-ply target cycle, two-ply attraction depth, leakage budget, baseline, budgets, thresholds and strike conditions above are frozen **before decisive R5 target-membership or validation results are inspected**.

Implementation defects may be repaired only without changing these scientific choices. Affected provisional outputs must be discarded and preserved.
