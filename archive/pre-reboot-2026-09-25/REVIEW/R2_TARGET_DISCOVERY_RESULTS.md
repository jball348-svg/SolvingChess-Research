# R2 Target Discovery Results

**Session:** R2 — Topology-Adaptive Proof Discovery Audit  
**Prospective authority:** `REVIEW/R2_DISCOVERY_HYPOTHESIS.md`, `REVIEW/R2_DISCOVERY_IMPLEMENTATION_FREEZE.md`  
**Selected-object freeze:** `REVIEW/R2_SELECTED_OBJECTS_FREEZE.md`

## 1. Outcome information consumed before selection

Complete top-signature D1 W/D/L labels consumed during target generation/selection:

**0 / 5,004,008 = 0.000000% TRUTH_LEAKAGE.**

Discovery did consume exact typed lower-material truth:

- 18,293,044 D1 lower-signature states.

That distinction is material. R2 is zero-label with respect to the target top domain, not truth-free across the dependency DAG.

## 2. Bounded certified seed

The outcome-independent certified exit consists of:

- legal White promotion wins;
- legal captures into exact lower-material states that are White-winning.

The <=4-ply bounded attractor `A4` contains:

**2,374,846 D1 top-signature states.**

Membership is derived from terminal/lower truth plus graph semantics, not complete D1 W/D/L.

## 3. Candidate generation and selection

Frozen concrete state atoms: 20.

Frozen grammar:

- 1-, 2-, 3-literal conjunctions;
- two-clause disjunctions with <=4 total literals;
- no square/state identifiers;
- candidate must be a subset of A4.

Search result:

- exact-admissible conjunction clauses: **168**;
- candidate expressions evaluated: **1,518**;
- 100,000-candidate budget hit: **no**;
- target-search wall: **5.67783 s**;
- selected direct target states: **2,010,533**;
- selected target / A4: **84.6595%**;
- description: **3 semantic literals, 2 clauses**.

Frozen formula:

> `WHITE_CERTIFIED_LOWER_CAPTURE_EXIT_EXISTS OR (WHITE_TO_MOVE AND WHITE_PROMOTION_LEGAL)`

Machine masks:

- clause A: 524288;
- clause B: 5.

No manual tie-break, square patch or post-validation exception was added.

## 4. Pre-W/D/L exact proof memberships

Before complete D1 truth inspection:

- semantic-target-only strict attractor: **2,227,610**;
- semantic membership hash: `4384735952237558686`;
- composite attractor after adding typed exact lower capture endpoints: **2,376,263**;
- composite membership hash: `14867222062096466624`;
- graph/rank verification violations: **0**.

## 5. D1 complete validation

Only after the target/program freeze, complete exact D1 truth was produced:

- top states: 5,004,008;
- White wins: **2,377,388**;
- Black wins: **2,531,075**;
- draws: **95,545**;
- Bellman mismatches: **0**.

Target validation:

| Object | States | False positives | Share of exact White wins |
|---|---:|---:|---:|
| Direct discovered target | 2,010,533 | 0 | **84.5690%** |
| Semantic-only strict attractor | 2,227,610 | 0 | **93.6999%** |
| Composite target attractor | 2,376,263 | 0 | **99.9527%** |

D1 composite residual:

**1,125 wins = 0.0473208% of exact White wins.**

Against the frozen R2 minimums:

- direct exactness: PASS;
- >=15% D1 attractor coverage: PASS by a large margin;
- residual raw ratio <0.67: PASS by a large margin.

## 6. H1 held-out target transfer

The D1 formula is applied unchanged. H1 may compute its own exact lower-signature truth because `WHITE_CERTIFIED_LOWER_CAPTURE_EXIT_EXISTS` is a typed dependency predicate, not a retrained grammar.

Complete H1 truth:

- top states: 5,099,304;
- White wins: **2,473,475**;
- Black wins: **2,472,963**;
- draws: **152,866**;
- Bellman mismatches: **0**.

Unchanged target validation:

| Object | States | False positives | Share of exact White wins |
|---|---:|---:|---:|
| Direct frozen target | 2,080,673 | 0 | **84.1194%** |
| Semantic-only strict attractor | 2,369,156 | 0 | **95.7825%** |
| Composite target attractor | 2,470,802 | 0 | **99.8919%** |

Held-out composite residual:

**2,673 wins = 0.108067% of exact White wins.**

The frozen >=10% held-out coverage threshold passes decisively.

## 7. Description-cost interpretation

The selected target remains constant-size:

- three semantic literals;
- two clauses;
- no exception list;
- no absolute square identifier other than relationally typed promotion resources.

Description size is therefore materially below top-state lookup scale.

However, the most powerful literal is `WHITE_CERTIFIED_LOWER_CAPTURE_EXIT_EXISTS`, which depends on exact lower-material truth. R2 should not misdescribe this as a deep standalone positional theorem: it is a compact semantic selector for conversion into already-certified truth.

## 8. Target-discovery result

**Positive scientific signal:** an exact, compact target was generated/selected with zero top-domain labels and survived an unchanged opposing-bishop colour-complex transfer.

**Limitation:** target discovery is conversion-dominated and its total compute cost is not cheaper than complete exact truth acquisition in D1. The economic failure is assessed in `R2_DISCOVERY_COST_AUDIT.md`.
