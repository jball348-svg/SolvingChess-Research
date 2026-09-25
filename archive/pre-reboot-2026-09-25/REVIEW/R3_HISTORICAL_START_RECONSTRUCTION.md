# R3 Historical Start Reconstruction

**Session:** R3 — Start-Reachable All-Reply Closure Audit

## Controlling reconstruction

R3 read the REVIEW authority first and then inspected only the start-side historical sources required by the audit: G10, G11, G12 and the G9 long-range plan. Frozen historical artifacts are not amended by this document.

## G10 — exact theorem state

G10.RULES.v1.0 separates repetition-position identity from full theorem-state identity.

- Repetition key `REP1`: piece placement + side to move + persistent castling rights + effective en-passant.
- Full theorem state: board + side + castling rights + effective en-passant + exact halfmove clock + bounded repetition-count map.
- Effective en-passant exists only when at least one en-passant capture is actually legal, including king-safety legality.
- Pawn moves, captures and permanent castling-right reductions are repetition barriers. Counts before the barrier are discarded.
- Within an epoch, occurrence counts are sufficient; an unbounded ordered game-history tape is not required.
- 50-move claims begin at 100 halfmoves; automatic 75-move draw occurs at 150 subject to checkmate precedence.
- Claim actions for threefold and 50-move rules are explicit, including intended-move claims.
- DEAD is the extensional no-checkmate-reachable condition, not an insufficient-material shortcut.
- `ARENA_ADMISSIBLE` and `START_REACHABLE` are distinct types.

The historical G10 handoff made canonical raw bytes the equality authority. The original G10 byte/vector payload was later unavailable.

## G11 — what start-generated testing did and did not establish

G11 built two structurally different move/state implementations and reported zero mismatches across its accepted conformance corpus. Relevant start evidence:

- standard start perft anchors: 20, 400, 8,902, 197,281 at depths 1–4;
- 1,536 deterministic reachable full-state transitions generated from the normal start with zero A/B mismatch;
- dual propagation of castling rights, effective EP, halfmove and repetition metadata.

This is strong move/state engineering evidence.

It did **not** establish:

- an exhaustive START_REACHABLE domain beyond the tested bounded corpus;
- a White strategy;
- all-Black-reply proof closure;
- a non-loss certificate;
- a start-to-endgame/basin connector.

G11 explicitly says its reachable fuzz is not a substitute for G35 reachability proof. Its original roadmap gate also remained on HOLD because exact G10 vector/canonical-byte replay was unavailable.

## G12 — forward identity and full-rule anchors

G12 preserved G10 semantic rules but, under the authorized provenance-failure branch, froze the new forward identity profile `G12.STATE.SERIAL.v2`. Equality remains semantic full-state equality; board-only equality is unsafe.

Exact G12 anchors include:

| Object | Exact result | Start-connection status |
|---|---:|---|
| clean-root KQK | 368,452 states; 345,404 White wins; max rank 20 | ARENA_ADMISSIBLE clean roots |
| clean-root KRK | 399,112; 376,868 White wins; max rank 32 | ARENA_ADMISSIBLE clean roots |
| clean-root a-file KPK | 41,619; 27,430 White wins; max rank 36 | ARENA_ADMISSIBLE clean roots |
| same-colour K+2B vs K | 5,938,848 states; exact DEAD family | ARENA_ADMISSIBLE |

G12 also supplies exact identical-board counterexamples where repetition/halfmove metadata changes truth. Therefore a board transposition is not automatically a theorem-state transposition.

No G12 table has a certified state-identity-compatible entry edge from ordinary start play. R3 therefore has no historical solved basin it may legitimately claim to have reached merely by matching a board placement.

## G35–G39 — mechanism audit

The roadmap stages are useful research specifications but not inherited proofs:

- **G35:** proposes a full-state start forward canonicalizer/transposition DAG. This is an engineering deliverable, not a compression theorem.
- **G36:** proposes search for machine-checkable forward-to-basin intersections. “Search until an intersection appears” is not itself a bridge mechanism.
- **G37:** proposes exact opening semantic move classes/phases. It explicitly warns against one-line/opening-name fitting, but supplies no already-certified opening policy.
- **G38:** proposes all-reply closure and clustering unresolved Black replies into new targets. Finite existential/universal predecessor semantics are inherited, but favorable closure economics are not.
- **G39:** proposes the first root-to-basin proof DAG and requires partial labeling if opponent replies remain uncovered. It is a target milestone, not an established construction.

Thus the actual reusable start-side ingredients before R3 are:

1. exact full-rule state semantics and legal transition machinery;
2. exact full-state equality/canonicalization discipline;
3. finite-game existential White / universal Black closure semantics;
4. semantic move-language ideas from earlier restricted work.

There is no inherited theorem showing that those ingredients yield a materially sub-tree start-rooted proof DAG.

## R3 reconstruction conclusion

The start-side obligation is genuinely open, not merely unimplemented roadmap plumbing. R3 must test whether semantic White-choice restriction plus exact full-state transposition and exhaustive Black replies yields favorable frontier growth, while refusing to call a bounded structural prefix a non-loss proof.
