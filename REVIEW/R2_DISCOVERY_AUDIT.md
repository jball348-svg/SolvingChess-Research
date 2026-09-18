# R2 Topology-Adaptive Proof Discovery Audit

**Session:** R2  
**Result:** **PARTIAL**  
**Review status:** OPEN  
**G15:** NOT STARTED  
**R3:** NOT STARTED

## 1. Proposition tested

R2 tested whether an outcome-independent discovery procedure can generate/select compact exact chess-semantic targets and strategy languages on a transition-rich arena with opposing mobile material, using the existing finite-graph proof algebra, without square fitting or first acquiring complete top-domain W/D/L truth.

The proposition, arenas, semantic grammars, label budget, candidate limits, strategy depth and thresholds were frozen before complete D1/H1 top-domain outcome inspection.

## 2. Mechanism tested

The tested mechanism is:

1. exact lower-material dependencies;
2. a bounded <=4-ply certified basin generated from promotion and exact winning capture exits;
3. zero-label semantic target enumeration/ranking inside that certified basin;
4. strict/composite target attraction;
5. semantic move-effect class enumeration;
6. exact filtered-attractor ranking;
7. one ordered strategy switch;
8. held-out unchanged application;
9. only then complete W/D/L validation.

No top-domain W/D/L label participates in target/program selection.

## 3. Primary positive findings

### Zero-label target discovery works at R2 scope

The selected target is:

`WHITE_CERTIFIED_LOWER_CAPTURE_EXIT_EXISTS OR (WHITE_TO_MOVE AND WHITE_PROMOTION_LEGAL)`.

It uses 3 literals / 2 clauses, has zero D1 false positives and zero H1 false positives.

D1:

- direct target: 84.5690% of exact White wins;
- semantic-only strict attractor: 93.6999%;
- composite attractor: **99.9527%**;
- residual raw truth: **0.0473208%**.

H1 unchanged:

- direct target: 84.1194%;
- semantic-only strict attractor: 95.7825%;
- composite attractor: **99.8919%**;
- residual raw truth: **0.108067%**.

### Strategy-language discovery works at R2 scope

The miner generated 55 semantic move classes and selected:

`GIVES_CHECK -> ATTACKS_BLACK_PAWN_AFTER_MOVE`.

D1 exact coverage of the composite basin:

**99.7451%.**

H1 unchanged:

**99.5773%.**

No square patch, retraining, extra phase or post-outcome grammar change was needed.

### Existing graph machinery composes cleanly

Semantic target, typed lower endpoints, strict attractor and nested filtered attractors all pass rank/graph verification with zero reported violations. Complete W/D/L solves pass Bellman verification with zero mismatches.

## 4. Primary negative finding

Discovery is not economically favorable against the exact solver.

Accepted D1:

- discovery: 33.9099 s;
- complete exact-truth acquisition: 26.5349 s;
- `DISCOVERY_COST_RATIO = 1.2780`.

The prospectively frozen <=1.0 economic threshold fails. A timing replay was closer to parity but still did not establish a stable sub-solve advantage.

This prevents `SURVIVED`.

## 5. Truth leakage and dependency truth

Top-signature labelled states consumed during discovery:

**0 / 5,004,008 = 0.000000%**.

But discovery consumes **18,293,044 exact lower-signature states**. The target is conversion-driven and relies on that exact dependency layer.

R2 therefore demonstrates **prospective proof-object discovery over exact lower truth**, not truth-free semantic induction.

## 6. Description complexity

Target:

- 3 literals;
- 2 clauses.

Strategy:

- 2 move literals;
- 1 switch.

No exception list.

Description cost is far below raw top-state lookup scale, and residual raw truth is also far smaller than R1 at this scope.

## 7. Held-out transfer

H1 changes the bishop colour-complex topology while preserving the material signature and brink resources. Direct mobile-piece captures fall from 1,757,343 to 496,508 while checking density rises.

The objects survive unchanged with zero false positives and >99.5% strategy/composite coverage.

This is genuine held-out structural transfer, but it remains within a narrow promotion-rich six-piece family.

## 8. What R2 establishes

At review level, R2 establishes that:

- a coherent zero-top-label discovery mechanism **can** be formulated from existing programme assets;
- compact exact semantic targets can be automatically selected before top W/D/L;
- semantic strategy programs can be automatically selected before top W/D/L;
- the selected objects can survive an unchanged opposing-material held-out topology;
- the raw residual can fall dramatically at this scope;
- the objects compose with existing exact graph machinery.

This retires the strongest “NO_CANDIDATE / discovery is only post-hoc interpretation” concern at the tested scope.

## 9. What R2 does not establish

R2 does not establish:

- discovery cheaper than exact solving;
- a multi-ascent discovery scaling law;
- discovery on non-brink, non-conversion-dominated domains;
- automatic theorem/guard synthesis beyond target/program selection;
- full-rule history-state discovery economics;
- ordinary middlegame proof semantics;
- START_REACHABLE connectivity;
- initial-position all-reply closure.

## 10. Status of the R1 open dependency

`SCALABLE_TOPOLOGY_ADAPTIVE_PROOF_DISCOVERY_ACROSS_OPPOSING_MATERIAL`

is **NARROWED, NOT RETIRED**.

R2 falsifies the claim that discovery must necessarily inspect complete top truth first. It also falsifies the claim that fixed-palette failure implies no semantic replacement can be selected prospectively.

But “SCALABLE” remains unsupported because:

- discovery compute loses to exact acquisition;
- only one discovery arena plus one closely related hostile topology is tested;
- the target relies heavily on exact lower truth;
- the arena remains promotion-rich and six-piece.

## 11. Classification

Under the frozen R2 vocabulary:

**PARTIAL**

Reason: exact useful zero-label discovery and held-out transfer succeed strongly, but the preregistered discovery-economic gate fails and general scaling/relevance remains unresolved.

## 12. Strike

**NO STRIKE.**

R2 states and genuinely tests the central falsifiable mechanism, produces a discriminating positive/negative split, and materially narrows the open obligation. It is not another post-hoc solved island presented as a bridge.

Strike count remains **0**.

## 13. R3 handoff boundary

R2 does not begin R3.

The independent start-side dependency remains untouched. The smallest high-information R3 question consistent with the review scaffold is:

> **Can a nontrivial START_REACHABLE domain rooted at the standard initial full-rule state be expanded by a prospectively frozen certified mechanism that closes every opponent reply and reaches an already compatible certified basin before the frontier degenerates into raw game-tree enumeration?**

That question tests the independent start/reply-closure risk rather than repeating R2.

## 14. End state

**R2 COMPLETE — REVIEW REMAINS OPEN — R3 NOT STARTED.**
