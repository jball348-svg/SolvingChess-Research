# R5 Target Exactness Results

**Session:** R5 — Hostile Synthesis and Nonterminal Bridge Attack  
**Frozen target:** FORCED_EXACT_REPETITION_LOCK (FERL-4)  
**Hypothesis freeze commit:** `305b154642f99e5a8c52e8248743615acfb6a956`  
**Target-exactness result:** **PASSED at the tested scope**  
**Overall R5 classification:** determined separately; target exactness alone is not survival.

## 1. Exact proposition tested

A nonterminal White-to-move full-rule state satisfies FERL-4 when White has an admitted first move such that, for every legal Black reply, White has an admitted second move such that every legal Black reply either reaches an exact draw or returns after exactly four plies to the identical FIDE repetition identity:

`REP_ID = (board64, side_to_move, castling_rights, effective_ep)`.

No move in the certified four-ply return may cross a repetition barrier: pawn move, capture, or permanent castling-right reduction.

The target is independent of complete surrounding W/D/L truth.

## 2. Why FERL-4 membership is proof-relevant

If a certified line returns to exactly the same repetition identity, with White to move, and every Black branch is covered, White can replay the same finite response relation.

The first certified return gives a second occurrence of the repetition identity. A second replay gives a third occurrence, at which point the rules contract permits a threefold repetition claim. Any earlier exact draw/claim/automatic-draw termination is already non-loss.

Halfmove/repetition counters may advance between returns, but that cannot invalidate legal move availability encoded by the repetition identity; it can only create an earlier draw condition. The proof therefore does not require a W/D/L label for the surrounding domain.

## 3. Producer result

On the prospectively frozen 1,024-state cohorts:

| Family | Direct FERL-4 targets | Total certified after one attraction pair |
|---|---:|---:|
| D — king-pawn | 1 | 5 |
| H — knight-first | 6 | 7 |

All accepted certificates use exact legal moves and exact repetition identity. No board-only equivalence is used.

## 4. Hostile exactness attack

The producer enumerated every legal Black reply inside every proposed contract. Candidate branches were killed rather than patched when any reply:

- was a capture or pawn move;
- reduced castling rights;
- prevented exact REP identity return;
- altered effective en-passant identity;
- escaped the claimed four-ply return;
- generated an earlier terminal result inconsistent with non-loss.

This automatically subjects the target to checks, captures, intermediate moves, zwischenzugs, king-safety changes, pawn breaks, exchange-order changes, castling-right changes, effective-EP changes, history divergence and quiet opponent moves.

Observed target-killing repetition barriers during policy certification:

- D: **718,197**;
- H: **1,039,312**.

Thus the target is highly fragile under hostile play; those failures are preserved as negative evidence rather than converted into exceptions.

## 5. Separate replay verifier

A separately written bottom-up FERL quantifier implementation was run on the exact frozen cohort dumps. It shares the audit-local legal move/state parser but does not reuse the producer's FERL search routine.

Replay output:

- standard perft: **20 / 400 / 8,902 / 197,281 / 4,865,609**;
- D: cohort 1,024; direct 1; policy-certified 5; unrestricted-baseline 5;
- H: cohort 1,024; direct 6; policy-certified 7; unrestricted-baseline 7.

The replay reproduced all decisive target/certification counts exactly.

Verifier SHA-256:

- source: `38500f5568a2cb8d6176fd1cc9b0a3f1bd05c798a286863dc10e815a8da2da88`;
- executable: `b113e06cc424751b612104d9b95f5629974f9514c6f10e3e4a3e38ba2f13e607`.

The verifier is structurally separate at the target-quantifier level, not an independently authored second chess move generator. Perft regression is therefore load-bearing provenance.

## 6. Exactness metrics

- `TARGET_EXACTNESS_VIOLATIONS = 0`;
- `CERTIFIED_BLACK_CLOSURE = 100%` for every accepted certificate;
- omitted legal Black replies in accepted certificates: **0 observed**;
- illegal Black replies in accepted certificates: **0 observed**;
- state-identity violations: **0 observed**;
- complete/local W/D/L labels used before target freeze: **0**;
- `LOCAL_TRUTH_LEAKAGE = 0%`.

No exactness counterexample was found to an accepted FERL-4 certificate.

## 7. Complexity

Target description complexity is one formally stated invariant:

> a four-ply `exists White / forall Black / exists White / forall Black` exact repetition-identity return contract, with exact-draw exits and no repetition barriers.

This is within the frozen “one formally stated invariant of comparable complexity” ceiling.

The target has no square list, state-ID list, opening line or outcome atom.

## 8. What this establishes

R5 establishes something R4 did not:

> a genuinely nonterminal, high-material, outcome-independent exact target can exist on START_REACHABLE chess states and can carry exact non-loss proof value for structural reasons alone.

That is a real positive result.

It does **not** establish that the target occurs with enough density, cost advantage or compositional leverage to rescue the reboot. Those are separate R5 gates.
