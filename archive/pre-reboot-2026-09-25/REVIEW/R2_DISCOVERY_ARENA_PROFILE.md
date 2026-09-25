# R2 Discovery Arena Profile

**Session:** R2 — Topology-Adaptive Proof Discovery Audit  
**Rules/reachability:** historical board-state semantics; `ARENA_ADMISSIBLE` only.

## Prospectively frozen pair

| Quantity | D1 discovery | H1 held-out |
|---|---:|---:|
| ID | `R2D1_BB_SAME_F7_D2` | `R2H1_BB_OPP_F7_D2` |
| Material | K+B+f7P vs K+B+d2P | same |
| White bishop colour complex | 0 | 0 |
| Black bishop colour complex | 0 | 1 |
| Pawn placement | White f7, Black d2 | unchanged |
| Free placement | both kings; bishops on declared complex | same |
| Raw encodings | 35,684,352 | 35,684,352 |
| Static-valid all signatures | 23,297,052 | 23,712,702 |
| Static-valid top signature | 5,004,008 | 5,099,304 |
| Exact lower-signature dependency states | 18,293,044 | 18,613,398 |
| Top normal edges | 53,785,408 | 56,378,992 |
| Mean top successor count | 10.7485 | 11.0562 |
| Normal moves including capture exits | 56,679,435 | 58,780,479 |
| Capture moves | 2,894,027 | 2,401,487 |
| Capture density | 5.10596% | 4.08552% |
| Checking-move density | 3.87364% | 4.27541% |
| Quiet top moves | 53,785,408 | 56,378,992 |
| White capture exits | 1,707,314 | 1,203,940 |
| Black capture exits | 1,186,713 | 1,197,547 |
| Mobile-piece capture edges | 1,757,343 | 496,508 |
| White promotion-legal states | 1,915,980 | 1,994,064 |
| Black promotion-legal states | 2,034,377 | 1,994,160 |
| Direct lower capture destinations | sig 7, 11, 13, 14 | sig 7, 11, 13, 14 |

The exact static-valid counts were enumerated **before complete top-signature W/D/L production** and are unlabeled structural measurements. No outcome-driven arena resizing occurred.

## Capture closure

Both arenas use the same four-bit material signature convention:

- bit 3: White bishop present;
- bit 2: Black bishop present;
- bit 1: White pawn present;
- bit 0: Black pawn present.

The full signature is 15. Direct top-signature captures lead to four distinct live lower signatures:

- 7 — White bishop removed;
- 11 — Black bishop removed;
- 13 — White pawn removed;
- 14 — Black pawn removed.

Those signatures close recursively over further captures and terminal promotion/mate/stalemate semantics. Lower exact truth is allowed as a typed dependency by the prospective R2 protocol.

## Structural reason D1 is transition-rich relative to R1

D1 has features absent from R1 H2:

- both White and Black have a mobile non-king piece;
- both sides have an irreversible promotion resource;
- captures are available to both sides;
- four distinct immediate material-reduction destinations are live;
- same-colour bishops permit direct exchange geometry;
- both sides possess checking resources;
- the graph contains tens of millions of quiet top-signature moves;
- promotion, exchange, pawn capture, king capture and line-interference decisions coexist.

This is still a six-piece brink arena, not a middlegame proxy.

## Why H1 is genuinely hostile

H1 changes only the Black bishop colour complex.

That change:

- reduces mobile-piece capture traffic from 1,757,343 to 496,508 edges;
- redistributes capture destinations heavily between bishop-loss and pawn-loss signatures;
- raises mean top branching from 10.7485 to 11.0562;
- raises checking density from 3.87364% to 4.27541%;
- changes which bishop can directly attack each brink pawn and which diagonals interfere.

The discovered D1 target formula, move atoms and one-switch program are applied unchanged. H1 does not participate in candidate selection.

## Terminal/rules model

- ordinary legal king/bishop/pawn movement;
- promotion is immediate win for promoting side;
- mate is win; stalemate is draw;
- unresolved cycles are draw under exact retrograde semantics;
- lower-material captures remain inside the exact dependency graph;
- no castling, en-passant, repetition or halfmove-clock state.

These are intentionally historical finite-arena semantics. No inference to G10/G12 full-rule state is made.

## Distance from ordinary chess

Despite the opposing-material improvement over R1, both arenas remain strongly restricted:

- only six pieces;
- one bishop and one fixed brink pawn per side;
- no rook/queen/knight interactions;
- no broad pawn structure;
- promotion resources are immediately close;
- no history-dependent draw state;
- no START_REACHABLE connection.

R2 therefore tests **topology-adaptive discovery under opposing mobile material**, not middlegame sufficiency.
