# R1 Negative Evidence

**Session:** R1 — Scaling and Lifting Audit

This file preserves adverse results and prevents the positive exact-solve curve from being mistaken for a general chess-scaling theorem.

## 1. H2 falsifies robust fixed-palette strategy transfer

The strongest new R1 negative is prospectively held-out H2:

- same pawn bands as P3;
- same target;
- same four allowed move languages;
- same exact rules model;
- only the bishop→rook topology change is made.

The exact producer and verifier both succeed. The unchanged G5 target is still exact and covers 74.010% of White wins.

Nevertheless the best frozen one-switch strategy combination, PAWN_ONLY→KING_ONLY, covers only **43.504%** of the ordinary strict target attractor.

The hostile pass threshold was 75%.

No post-outcome move language was added.

**Frozen interpretation:** exact solving scales here, and semantic target transfer scales here, but the supplied strategy-language layer does not robustly transfer through this mobility/checking change.

This echoes, prospectively, the historical F09 negative where G8's broader frozen one-switch palette reached only 55.498%.

## 2. The raw/unexplained win residual does not shrink on the main ladder

Strict unchanged-target residual:

- P0: 65.883%;
- P1: 67.690%;
- P2: 67.000%;
- P3: 67.066%;
- H1: 70.403%.

The central bishop ladder therefore does **not** show increasingly large fractions of truth becoming explained by the fixed semantic target. Proof leverage remains substantial but roughly stationary.

This is evidence against narrating state-growth success as progressively cheaper truth discovery.

## 3. Automatic discovery remains absent

R1 deliberately froze the G5 target and G8-style semantic move palette.

That provides a clean transfer test, but it means:

- target invention cost was not solved;
- strategy-language invention cost was not solved;
- no automated abstraction miner was demonstrated;
- no theorem explains how to replace the failing H2 palette without looking at outcome truth.

The H2 failure therefore lands exactly on an R0 concern: the graph operators are reusable, but useful chess predicates/languages remain topology-dependent inputs.

## 4. Material-signature advantage is not monotone

Dependency states / largest active signature:

- P1 2.677×;
- P2 5.191×;
- P3 3.228×;
- H1 2.359×;
- H2 3.222×.

The decomposition consistently provides a useful working-set separation after P0, but there is no monotone multiplicative improvement as restrictions relax.

## 5. Verifier economics remain topology-dependent historically

The new R1 verifier remains cheaper than the producer on every accepted arena, with V/P falling from 0.871× to roughly 0.64–0.68× at larger points.

That does **not** erase G8's existing negative controls:

- F09 verifier 1.651× producer;
- F10 verifier 1.441× producer.

R1 therefore adds a favorable regime; it does not support universal verifier superiority.

## 6. H1/H2 do not create ordinary middlegame relevance

Even the hostile controls retain major artificial simplifications:

- bare-king opponent;
- no opposing non-king material;
- no exchange network except Black king captures;
- no full draw-history state;
- ARENA_ADMISSIBLE only;
- no START_REACHABLE claim.

H2 adds real checking/mobility diversity, but it is still an endgame-like laboratory. More pieces or more checks are not equivalent to ordinary middlegame topology.

## 7. No defensible extrapolation to full chess

The P0–P3 runtime curve is close to linear in dependency-state count over a small bounded family. It is not evidence that full chess has the same scaling variable or exponent.

The tested range lacks:

- opponent piece mobility;
- dense mutual captures;
- king-safety networks;
- quiet multi-piece manoeuvring;
- pawn breaks on both sides;
- history-dependent draw-state multiplication;
- START_REACHABLE connectivity.

Therefore no full-chess cost extrapolation is recorded.

## 8. Harness engineering alarm — preserved but not counted as scientific failure

The initial reverse-predecessor implementation redundantly regenerated all forward moves for each inverse candidate. This produced artificial timeouts on H1/H2 analysis.

The benchmark was not shrunk. A semantics-preserving direct inverse generator was substituted, then accepted only after exact historical P0 reproduction and exact equality with already-completed pre-repair outputs.

This alarm is preserved because it demonstrates how easily implementation overhead can masquerade as a scale law. It is **not** counted as negative chess evidence after the repaired harness reproduces the same truth.

## 9. R1 negative synthesis

R1 does not find a raw exact-solving wall in the tested range.

The adverse signal is more strategic:

> reusable exact game-graph operators and a semantic target survive controlled ascent, but useful strategy-language coverage can collapse under a modest topology change, while the unexplained full-truth residual does not systematically shrink.

That is why R1 cannot classify the overall lifting proposition as SURVIVED.
