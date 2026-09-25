# R3 Negative Evidence

**Session:** R3 — Start-Reachable All-Reply Closure Audit

## 1. Structural compression is not proof closure

The largest R3 positive number is a small unresolved frontier:

- D: 13,064 exact states versus 808,373 raw leaf paths;
- H: 13,181 versus 690,301.

But no ply-5 state enters an existing compatible exact non-loss basin, and no W/D/L theorem was proved for the retained White choices.

Therefore the semantic language has shown **branching compression**, not correctness of a White non-losing strategy.

This is the central reason R3 is not `SURVIVED`.

## 2. Full-rule history materially destroys board-only merging

At ply 5:

- D: 277,360 board placements become 496,086 exact full states, multiplier 1.78860x;
- H: 237,652 become 411,566, multiplier 1.73180x.

Maximum exact theorem states per identical board already reach 59 and 51 respectively.

A start-side approach that budgets using board transpositions alone is therefore materially optimistic even at five plies.

## 3. Exact transposition alone is not strongly sub-tree by ply 5

Raw exact full-state frontiers remain:

- D: 61.3685% of raw leaf histories;
- H: 59.6212%.

So ordinary exact transposition-table savings are not the mechanism producing the R3 policy result. The favorable frontier depends on constraining White choices.

## 4. White-choice soundness remains completely open

The frozen policy `ANSWER_CHECK OR CENTER_PAWN` was selected from legal structure, not outcome truth. R3 has no basis to say that one retained move is non-losing at every White node.

It may eventually fail because:

- some White node requires a move outside the class;
- all class moves at a node may lose;
- a strategically necessary quiet non-pawn move may be absent;
- the class may cease to have any legal move at deeper horizons.

No such failure was patched in R3; equally, no theorem rules it out.

## 5. The horizon is shallow

The decisive ladder is only plies 3/4/5. This is enough to discriminate raw-tree, full-state and semantic-policy growth early, but not enough to exercise:

- repetition claims;
- 50/75-move draws;
- deep castling-history diversity;
- mature exchange networks;
- basin entry;
- middlegame topology.

The maximum raw repetition count is 2 and halfmove clock 4. Thus R3 measures history identity before it measures history-dependent draw outcomes.

## 6. No basin connection

No exact state-identity-compatible transition into G12 KQK/KRK/KPK is found or claimed. The current start-side and lower-tree components remain disconnected.

This is not itself an R3 failure condition, but it means R3 does not retire `START_TO_BASIN_CONNECTOR`.

## 7. Independent R3 verifier not built

R3 reproduced frozen G11 perft anchors and repeated the experiment deterministically, but did not create a second structurally independent implementation of the full R3 policy/state experiment.

This is adequate for a discriminating review experiment classified PARTIAL, not for a SURVIVED certificate claim.

## 8. Fine-grained timing not separately instrumented

Canonicalization, semantic-feature extraction and candidate selection were included in aggregate construction work rather than separately isolated. No favorable economic claim is promoted beyond the measured aggregate policy-vs-raw runs.

## 9. Negative synthesis

R3 does **not** find that all-reply structural expansion immediately degenerates into the raw game tree. That specific strongest failure hypothesis is weakened.

Instead it locates the next bottleneck more precisely:

> a compact prospectively frozen start-rooted semantic policy can suppress frontier growth while keeping every Black reply, but the programme does not yet know how to certify that the retained White choices are non-losing or connect them to exact typed targets without reintroducing near-raw truth acquisition.

That distinction must control R4.
