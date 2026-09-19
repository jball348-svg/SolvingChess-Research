# R4 Reboot Architecture — Bidirectional Certified Frontier

**Session:** R4 — Reboot Candidate Construction and Survival Attack  
**Status:** PROSPECTIVE ARCHITECTURE FREEZE  
**Review hold:** OPEN; G15 forbidden  
**Primary architecture:** **Bidirectional Certified Frontier Reboot**

## 1. Global theorem target

Produce a machine-checkable proof that from the standard initial position, under the frozen full legal-play rules, White has a strategy whose outcome is never BLACK_WIN against every legal Black reply.

R4 does not claim that theorem. It defines the only reboot architecture under test.

## 2. Exact state model

Start-side objects use the G10 semantic rules carried through the G12.STATE.SERIAL.v2 forward identity:

`STATE = (board64, turn, castling_rights, effective_ep, halfmove_clock, repetition_count_map)`.

Equality is exact theorem-state equality. Board-only merging is forbidden.

Lower-frontier objects retain the exact state/rules model declared by their frozen dependency. An edge between frontiers is valid only when rules/state semantics are explicitly compatible or an exact typed conversion proof exists.

## 3. Proof object type

The reboot proof object is a typed directed proof DAG.

At White nodes, certification is existential: at least one legal move admitted by the frozen semantic White program must enter an exact certified target, an exact closed local proof object, an already certified dependency, or a recursively certified state.

At Black nodes, certification is universal: every legal Black reply must enter one of those objects.

Leaves are typed exact targets. Unresolved leaves remain explicit and confer no non-loss status.

## 4. Construction directions

Two certified surfaces are maintained.

### Lower certified frontier

Grow upward from trusted exact dependencies using exact raw truth only where economical, automatic semantic target discovery, Branch/Hyperkernel composition, Filter-Pivot / filtered-attractor factorization, and prospectively frozen hostile controls.

### Start certified frontier

Grow downward from the real initial full-rule state using exact START_REACHABLE forward generation, prospectively frozen semantic White strategy programs, exhaustive Black replies, exact theorem-state identity, and an explicit unresolved frontier.

Neither direction may claim progress merely for enumerating more states.

## 5. Exact operations

Exact operations include:

- legal successor generation;
- full theorem-state canonical identity;
- existential White / universal Black predecessor closure;
- terminal mate/stalemate/automatic-draw semantics;
- exact legal draw-claim semantics where active;
- exact compatibility tests into frozen dependencies;
- strict attractors;
- Branch / Hyperkernel;
- Filter-Pivot / filtered attractors;
- exact proof-DAG replay.

## 6. Prospectively discovered objects

The reboot may prospectively discover:

- semantic typed targets;
- finite semantic White strategy programs;
- target compositions;
- bounded exact local proof objects;
- reusable bridge targets that reduce both frontiers.

Discovery must occur under frozen grammars/budgets and may not inspect complete local W/D/L truth unless the session explicitly budgets that truth as validation rather than selection data.

## 7. Where full raw truth is permitted

Complete raw truth is permitted only:

1. in already trusted frozen dependencies;
2. in a bounded validation domain after the candidate object is frozen;
3. as a competent economic baseline;
4. as an explicitly declared fallback whose cost is counted against the reboot.

A reboot step that first solves essentially the whole validation domain and then describes it semantically has not demonstrated discovery leverage.

## 8. Certified frontier

A **certified frontier state** is a START_REACHABLE or lower-frontier state carrying a replayable exact non-loss/win/draw proof object under its declared rules model.

A state is not certified merely because it survives a horizon, has favorable evaluation, is materially ahead, or belongs to a semantic class.

## 9. New bridge target

A **bridge target** is a typed exact proposition that can be consumed by both a start-side closure step and a lower-side composition/lifting step, or whose certification strictly reduces the named gap between them.

A target that is simply “non-losing state” is invalid because it restates the theorem.

## 10. White strategy certification

White strategy choices are certified only through exact target entry, exact closed local proof, an exact compatible dependency, or recursive certification. Semantic policy membership alone is candidate compression, not proof.

## 11. Black reply closure

Every certified Black node carries 100% of legal Black replies. No engine, likelihood, opening-book, or evaluation pruning is permitted.

## 12. Exact history

Castling rights, effective en-passant, halfmove clock and repetition-count state remain in exact identity. Any safe quotient must itself be separately proved. R3's board/full-state multiplication is treated as adverse prior evidence.

## 13. How the two frontiers meet

A bridge step is credited only when one of these happens:

1. a start-certified state enters an already certified lower target;
2. a lower target is prospectively enlarged specifically toward a frozen start-frontier class;
3. a start-side semantic White-choice class is independently certified against an exact bounded local target;
4. a reusable typed intermediate target is discovered that reduces both sides.

“Enumerate until they touch” is not a bridge mechanism.

## 14. Permitted unresolved work between sessions

Only named bridge obligations may remain unresolved. Each session must leave:

- an exact frozen proposition;
- an explicit unresolved set;
- a proof/dependency ledger change;
- negative evidence;
- a smallest next hostile test if warranted.

Disconnected scale work and infrastructure work are prohibited unless they directly retire a named bridge obligation.

## 15. Unit and metric of progress

The unit of progress is **one retired or sharply narrowed exact bridge obligation through a bounded falsifiable experiment**.

Primary metrics are certified-policy coverage, exact Black closure, truth leakage, certification residual, certification cost ratio, proof payload ratio, held-out transfer and history-state burden.

G-number completion is no longer a progress metric under the reboot.

## 16. Termination as nonviable

The reboot terminates as nonviable if bounded hostile tests show any recurring combination of:

- exact start-side certification requires near-complete local minimax/raw truth;
- certification cost repeatedly approaches/exceeds competent raw truth acquisition;
- typed targets collapse into line/square/state-ID patches;
- held-out transfer collapses;
- exact history destroys the payload advantage;
- Black universal closure forces essentially complete local game solving;
- bridge steps only move the unresolved frontier;
- no session retires or sharply narrows a bridge obligation within the finite reboot budget.

Three review strikes force STOP_CURRENT_METHOD at the next decision session under REVIEW/REBOOT_CRITERIA.md.

## 17. Why this is materially different from G15–G42 / G35–G39

The old roadmap progressed by programme stage and contained desired future capabilities such as forward canonicalization, search for intersections, semantic opening classes and all-reply closure. It did not require each stage to retire one frozen bridge obligation or to beat a competent raw-truth baseline.

This reboot instead:

- makes the bridge obligation the session boundary;
- freezes a falsifiable theorem/experiment before supportive truth;
- requires exact certification, not connector discovery;
- requires hostile unchanged transfer;
- charges discovery/certification against raw truth acquisition;
- permits immediate failure/termination;
- forbids disconnected scale/infrastructure work;
- has no long sequential G ladder.

The architecture therefore stands or falls on repeated certified-surface growth, not on completion of a renamed G35–G39 sequence.

## 18. R4 critical bridge

R4 attacks the first start-side instance:

> Can an R3-derived semantic White-policy frontier be converted into exact non-loss certification against self-certifying typed targets at materially lower cost and payload than complete bounded local target truth, with all Black replies explicit and unchanged held-out transfer?

The architecture is not presumed viable. R4 may fail it.
