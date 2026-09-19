# R4 Held-Out Results

**Session:** R4  
**Held-out family:** `KNIGHT_FIRST`

## 1. Hostile control

H begins at the real standard initial position with any legal first move by a White knight from its original b1/g1 home square.

This materially differs from R3's central-pawn held-out branch. The D-frozen state identity, two-phase strategy program, target grammar, cohort rule, certification rule, complexity limit and selected depth are applied unchanged.

## 2. Exact ply-6 held-out frontier

H produces:

- **449,623** unique exact full theorem states;
- **303,288** board placements;
- HISTORY_MULTIPLIER = **1.48250x**;
- maximum exact states per board = **15**;
- phase-collision count = **0**;
- **556,105** legal Black edges represented during the expanded prefix;
- **39,526 / 233,083 = 16.9579%** White edges retained during the prefix.

The deterministic cohort contains 1,024 states:

- 512 forcing-contact;
- 512 quiet;
- 30–32 pieces;
- 0 direct exact targets;
- 29 states initially in check.

## 3. Unchanged exact certification

D froze the maximum remaining depth at 5 after none of depths 1/3/5 reached 25%.

Applied unchanged to H:

- certified: **0 / 1,024**;
- `CERTIFIED_POLICY_COVERAGE = 0.0000%`;
- `CERTIFICATION_RESIDUAL = 100.0000%`;
- memo configurations: 9,459;
- explored edges: 9,441;
- examined Black edges before failure: 2,508;
- inner solver wall: 0.2920 s.

The held-out >=15% coverage gate fails completely.

Residual degradation is numerically 1.0x because both D and H residuals are 100%, but that is a transfer of failure, not a positive gate.

## 4. Held-out raw baseline

The exact all-White bounded baseline also fails under the unchanged 2 GiB resource cap:

- **std::bad_alloc**;
- 71.58 s elapsed;
- 2,024,280 KiB peak RSS;
- no complete bounded target truth acquired.

## 5. Interpretation

The R4 failure is not specific to the king-pawn branch. It survives a materially different knight-first start family unchanged.

This is adverse evidence for the current target grammar and semantic certification bridge. It does not prove that no richer exact intermediate target can work; that is the remaining R5 escape hatch.
