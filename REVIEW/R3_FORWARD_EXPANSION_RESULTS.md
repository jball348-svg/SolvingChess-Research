# R3 Forward Expansion Results

**Session:** R3 — Start-Reachable All-Reply Closure Audit  
**Frozen decisive horizons:** plies 3, 4 and 5

All counts below use legal histories rooted at the standard initial state and exact full-state identity. Raw path counts preserve duplicate move histories; unique counts merge only exact theorem-state equality.

## Discovery branch D — king-pawn first-move family

### Competent raw baseline

| ply | raw leaf paths | unique exact full states at frontier | exact/full transposition ratio |
|---:|---:|---:|---:|
| 3 | 1,199 | 1,199 | 100.0000% |
| 4 | 26,294 | 19,839 | 75.4507% |
| 5 | 808,373 | 496,086 | 61.3685% |

Cumulative raw nodes through ply 5: **835,909**.  
Cumulative per-level unique full-state nodes: **517,167**.

### Frozen semantic-policy expansion

| ply | policy leaf paths | unique exact unresolved frontier | PROOF_FRONTIER_RATIO vs raw leaf |
|---:|---:|---:|---:|
| 3 | 281 | 281 | 23.4362% |
| 4 | 6,243 | 4,714 | 17.9280% |
| 5 | 38,824 | 13,064 | **1.61609%** |

Cumulative policy path nodes through ply 5: **45,391**.  
Cumulative per-level unique policy states: **18,102**.

The policy frontier falls far below the frozen <=50% threshold at all three decisive points.

## Held-out H — queen-pawn first-move family

The strategy language and all state/closure rules were applied unchanged.

### Competent raw baseline

| ply | raw leaf paths | unique exact full states at frontier | exact/full transposition ratio |
|---:|---:|---:|---:|
| 3 | 1,099 | 1,099 | 100.0000% |
| 4 | 24,394 | 18,377 | 75.3341% |
| 5 | 690,301 | 411,566 | 59.6212% |

Cumulative raw nodes through ply 5: **715,837**.  
Cumulative per-level unique full-state nodes: **431,085**.

### Frozen semantic-policy expansion

| ply | policy leaf paths | unique exact unresolved frontier | PROOF_FRONTIER_RATIO vs raw leaf |
|---:|---:|---:|---:|
| 3 | 281 | 281 | 25.5687% |
| 4 | 6,248 | 4,719 | 19.3449% |
| 5 | 38,916 | 13,181 | **1.90946%** |

Cumulative policy path nodes through ply 5: **45,488**.  
Cumulative per-level unique policy states: **18,224**.

Largest-horizon held-out degradation relative to D is:

`1.90946 / 1.61609 = 1.18153x`

which is inside the frozen <=2x transfer gate and still far below the absolute 50% frontier gate.

## What causes the reduction?

Pure exact full-state transposition alone is modest by ply 5:

- D: 496,086 / 808,373 = 61.3685% of raw leaf paths;
- H: 411,566 / 690,301 = 59.6212%.

The semantic policy adds a much larger reduction:

- D policy frontier = 13,064 states = 2.6334% of the competent raw exact-full-state frontier;
- H = 13,181 = 3.2026%.

Therefore R3's favorable structural frontier number is **not** merely a transposition-table result. It is dominated by prospectively frozen White strategy-choice restriction while retaining every Black reply.

## White choice volume

Across the frozen expanded White decision layers (including the first semantic family at the root):

- D: retained 39,107 / 190,196 legal White edges = **20.5614%**.
- H: retained 39,199 / 182,214 legal White edges = **21.5126%**.

This is an empirical branching reduction only. R3 does not infer from it that the retained edges are game-theoretically sufficient.

## Basin/target entry

No R3 state is claimed to enter a G12 KQK/KRK/KPK certified basin with compatible full-state identity. No historical basin connector is manufactured from a board match.

Thus these results establish bounded structural expansion economics, not `BASIN_CONNECTED` and not an `INITIAL_POSITION_CERTIFICATE`.
