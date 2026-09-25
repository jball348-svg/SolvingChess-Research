# R2 Selected Objects Freeze — before W/D/L validation

**Session:** R2 — Topology-Adaptive Proof Discovery Audit  
**Arena:** `R2D1_BB_SAME_F7_D2`  
**Status:** PROSPECTIVE OBJECT FREEZE  
**Truth leakage at freeze:** **0 full-domain top-signature W/D/L labels**

This freeze was produced after `R2_DISCOVERY_HYPOTHESIS.md` and
`R2_DISCOVERY_IMPLEMENTATION_FREEZE.md`, and before any complete D1 or H1
top-signature W/D/L solve or inspection.

## Discovery execution

The final semantics-preserving harness implementation has:

- source SHA-256: `047b354ce4d7f863a291f34cead28d8c0d4db60b8424ec7d1d8ef93943f649d8`
- executable SHA-256: `6c8dfad8eca6df10f6c35e07b1008b557d1576c84240cb46a309cc38d8420aef`

An earlier implementation attempt spent excessive time in generic
`staticValid` overlap sorting. It was discarded before any discovery output or
top W/D/L inspection. The accepted implementation replaces that sort with
logically equivalent direct pairwise occupancy checks; the arena, rules, atoms,
candidate order, budgets and thresholds are unchanged.

Accepted D1 unlabeled structural quantities:

- raw encodings: 35,684,352
- static-valid all-signature states: 23,297,052
- static-valid top-signature states: 5,004,008
- exact lower-signature states consumed as typed dependencies: 18,293,044
- top-signature normal graph edges: 53,785,408
- mean top-signature successor count: 10.7485
- capture moves: 2,894,027 / 56,679,435 = 5.10596%
- checking-move density: 3.87364%
- quiet moves: 53,785,408
- White capture edges: 1,707,314
- Black capture edges: 1,186,713
- mobile-piece capture edges: 1,757,343
- live direct capture destinations: signatures 7, 11, 13 and 14

The complete top-signature W/D/L truth was not available to discovery.

## Frozen semantic target

Bounded certified basin:

- `A4`: 2,374,846 states

Target search:

- exact-admissible conjunction clauses: 168
- total candidates evaluated: 1,518
- candidate budget hit: no
- selected direct target: 2,010,533 states
- selected target / A4: 84.6595%
- description: 3 literals in 2 clauses
- no square/state exceptions

Frozen formula:

`WHITE_CERTIFIED_LOWER_CAPTURE_EXIT_EXISTS OR (WHITE_TO_MOVE AND WHITE_PROMOTION_LEGAL)`

Machine masks:

- `clauseA = 524288`
- `clauseB = 5`

This target was selected solely by exact containment in the bounded certified
A4 basin plus the frozen deterministic ranking.

## Frozen proof basins before W/D/L

- semantic-target-only strict attractor: 2,227,610
- semantic-target-only membership hash: `4384735952237558686`
- composite attractor with typed exact lower-material capture endpoints: 2,376,263
- composite membership hash: `14867222062096466624`

Independent rank/graph checks in the discovery process:

- semantic attractor violations: 0
- composite attractor violations: 0

## Frozen strategy program

All 55 one/two-atom move classes were evaluated against the unlabeled composite
target attractor.

Highest single-class coverages:

1. `ATTACKS_BLACK_PAWN_AFTER_MOVE`: 98.8226%
2. `GIVES_CHECK`: 98.2658%
3. `ATTACKS_BLACK_BISHOP_AFTER_MOVE`: 98.0784%
4. `ATTACKS_BLACK_PAWN_AFTER_MOVE AND ATTACKS_BLACK_BISHOP_AFTER_MOVE`: 97.7139%
5. `DEFENDS_WHITE_PAWN_AFTER_MOVE`: 97.7024%
6. `MOVES_WHITE_KING_CLOSER_TO_WHITE_PROMOTION`: 97.5894%

Frozen ordered one-switch program:

`GIVES_CHECK -> ATTACKS_BLACK_PAWN_AFTER_MOVE`

Machine masks:

- `F_req = 1`
- `G_req = 64`

Frozen coverage:

- program membership: 2,370,207
- composite target attractor: 2,376,263
- coverage: 99.7451%
- program membership hash: `10500123484221588853`
- strategy description: 2 move literals + 1 switch
- inner/program exact graph violations: 0

## Discovery cost before validation

Accepted discovery wall time: **33.9099 s**, including exact lower-signature
dependencies, graph/feature generation, A4, target search, ordinary attractors,
55 strategy classes and 36 one-switch programs.

The full exact top-signature solve time is deliberately unknown at this freeze
and will be measured only in the validation phase.

## Immutable validation instruction

D1 validation and H1 transfer must use exactly:

- `clauseA=524288`
- `clauseB=5`
- `F_req=1`
- `G_req=64`

No atom, clause, phase, arena, threshold or exception may be added after this
point.

**FULL-DOMAIN D1/H1 W/D/L VALIDATION HAS NOT YET OCCURRED.**
