# R1 Restriction and Topology Complexity Profile

**Session:** R1 — Scaling and Lifting Audit

This profile prevents piece count or raw state count from standing in for actual restriction relaxation.

## 1. Historical reference points

| Arena/family | Material | Key restrictions | live signatures | state scale | rules/reachability | discovery/proof note |
|---|---|---|---:|---:|---|---|
| G5 bishop | K+B+dP vs K | d-pawn only d5–d7; minor/kings unrestricted | lower capture dependency only | 1,180,148 static-valid | historical board-only; ARENA_ADMISSIBLE | frozen target covers 34.12% of wins; 46/87 lookup-like tail |
| G6 rank-band scaling | K+N/B/R+P vs K | same file; 5–7 widened to 2–7 | typed lower truth | ≈2× matched state growth | historical board-only; ARENA_ADMISSIBLE | target description constant; N/B coverage falls, R stable |
| G7 F01/F02 | K+B+P vs K+B+P | prospectively selected bishop-race families; capture-closed | multiple material endpoints | 23.73M / 22.77M graph states | historical typed finite arena; ARENA_ADMISSIBLE | Hyperkernel / Filter-Pivot transfer |
| G7/G8 F09 | K+2B+hP vs K | wrong-colour fortress structure | typed faithful lower fortress | 16.56M | faithful promotion continuation; ARENA_ADMISSIBLE | strong target; forcing language poor |
| G8 R01/R02 | K+B+3P vs K+B+P | White pawns fixed a7/c7/e7; Black pawn fixed b2; bishop-colour relation is principal matched variation | 64 | 88.36M / 82.55M dependency; 4.42M / 3.88M full | historical board-state arena; ARENA_ADMISSIBLE | exact prospective eight-man solve; strong geometric restriction remains |

Historical branching/check-density/RSS values are not uniformly available and are not imputed.

## 2. New R1 arenas

All new R1 arenas use the frozen board-only finite-game model from `R1_SCALING_HYPOTHESIS.md`: no castling, en-passant, repetition or halfmove history; static-valid states; promotion/checkmate are White-winning terminals for exact truth; lower material is capture-closed; reachability type is ARENA_ADMISSIBLE.

The d-pawn target and four-language palette are unchanged across every row.

| ID | Material / total pieces | pawn bands | live signatures | top valid states | dependency states | mean / p95 / max branching | checking density | producer / verifier | peak RSS P/V | target coverage | best frozen one-switch | new predicates |
|---|---:|---|---:|---:|---:|---|---:|---|---|---:|---:|---:|
| P0 | K+B+dP vs K / 4 | d5–d7 | 4 | 1,180,148 | 1,625,276 | 9.454 / 18 / 22 | 4.006% | 0.259 / 0.225 s | 13.5 / 9.9 MiB | 34.117% | 93.291% | 0 |
| P1 | K+B+aP+dP vs K / 5 | a7 fixed; d5–d7 | 8 | 1,112,870 | 3,158,830 | 9.597 / 19 / 23 | 3.902% | 0.742 / 0.566 s | 17.1 / 12.9 MiB | 32.310% | 93.271% | 0 |
| P2 | K+B+aP+dP+eP vs K / 6 | a7; d5–d7; e7 | 16 | 1,044,751 | 6,126,627 | 9.264 / 18 / 23 | 3.801% | 1.201 / 0.833 s | 21.2 / 16.4 MiB | 33.000% | 93.390% | 0 |
| P3 | same 6 pieces | a6–a7; d5–d7; e6–e7 | 16 | 4,191,884 | 13,532,888 | 9.571 / 19 / 24 | 3.765% | 2.814 / 1.914 s | 63.6 / 46.8 MiB | 32.934% | 93.354% | 0 |
| H1 | same 6 pieces | a5–a7; d4–d7; e5–e7 | 16 | 12,602,226 | 29,734,058 | 9.604 / 19 / 24 | 3.665% | 6.656 / 4.410 s | 168.1 / 120.4 MiB | 29.597% | 89.813% | 0 |
| H2 | K+R+aP+dP+eP vs K / 6 | a6–a7; d5–d7; e6–e7 | 16 | 4,048,418 | 13,043,648 | 10.881 / 23 / 25 | 7.577% | 3.215 / 2.044 s | 63.4 / 46.9 MiB | 74.010% | **43.504%** | 0 |

“Target coverage” is the strict unchanged G5 target-attractor as a fraction of the exact top-signature White-win basin. “Best one-switch” is the best ordered pair from the prospectively frozen CHECK / KING_ONLY / PAWN_ONLY / MOBILE_PIECE_ONLY palette as a fraction of the ordinary strict target basin.

## 3. Exact restriction-relaxation descriptions

### P0 → P1
**Material ascent, not restriction relaxation.** Adds an a7 brink pawn and doubles the number of capture-closed signature combinations. It increases transition possibilities while keeping the new pawn fixed.

### P1 → P2
**Second material ascent, still geometrically friendly.** Adds a fixed e7 brink pawn. Signature count grows from 8 to 16. Top-state count does not grow because fixed occupied squares reduce free-piece placements, but dependency-state count almost doubles.

This is an important example of why raw full-state count alone is a misleading ascent metric.

### P2 → P3
**Genuine same-material restriction relaxation.** The a/e brink pawns each receive a two-rank mobility band. Top valid states grow about 4.01× and dependency states about 2.21×, while the target and strategy palette remain unchanged.

### P3 → H1
**Hostile geometry/mobility relaxation.** All three pawn bands widen. Top valid states grow to 12.60M and dependency truth to 29.73M. This introduces more quiet pawn alternatives and less brink-like geometry without changing the proof vocabulary.

### P3 → H2
**Hostile topology change.** Same pawn bands, but bishop is replaced by an unrestricted rook. Mean branching rises from 9.57 to 10.88, p95 from 19 to 23, and White-move checking density approximately doubles from 3.77% to 7.58%. This is the decisive proof-language hostile control.

## 4. Material-signature working-set advantage

A useful engineering ratio is total dependency states divided by the largest live signature:

| ID | dependency / largest-signature ratio |
|---|---:|
| P0 | 1.377× |
| P1 | 2.677× |
| P2 | 5.191× |
| P3 | 3.228× |
| H1 | 2.359× |
| H2 | 3.222× |

For P1 onward, solving signatures separately retains a >2× working-set separation between total dependency truth and the largest active signature. The advantage is real but not monotone.

## 5. Payload / verifier representation

The R1 harness stores a 16-bit rank witness for every encoding so the verifier can reject self-supporting winning cycles. A compact exact top-truth membership bitset would require:

| ID | top membership bitset | rank-witness file |
|---|---:|---:|
| P0/P1/P2 | 192 KiB | 3.0 MiB |
| P3/H2 | 768 KiB | 12.0 MiB |
| H1 | 2.25 MiB | 36.0 MiB |

These are raw R1 harness payloads, not G8.CERT sparse proof certificates. The target and move-language definitions themselves remain constant-size semantic descriptions; R1 did not build a new sparse certificate compiler.

## 6. Distance to ordinary unrestricted chess

The new ladder genuinely weakens pawn-rank restrictions and H2 increases mobility/checking, but all new arenas remain far from ordinary chess:

- the opponent has only a king;
- White has only one mobile non-pawn piece;
- no White captures of opposing non-king material exist;
- there is no opposing pawn structure or exchange network;
- no castling/en-passant/repetition/halfmove state;
- all states are ARENA_ADMISSIBLE, not START_REACHABLE;
- there is no opening/middlegame king-safety network.

Therefore P3/H1/H2 are useful hostile scaling controls, not claims of middlegame proximity.
