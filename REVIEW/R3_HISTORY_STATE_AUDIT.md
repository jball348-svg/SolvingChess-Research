# R3 History-State Audit

**Session:** R3 — Start-Reachable All-Reply Closure Audit

The purpose of this audit is to measure how much apparent board transposition survives after exact theorem history state is restored.

Counts of split board placements below overlap: one board placement can be split by more than one metadata field.

## D raw baseline

| ply | full states | board placements | HISTORY_MULTIPLIER | split by castling | split by EP | split by halfmove | split by repetition | max states / board |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1,199 | 1,199 | 1.0000 | 0 | 0 | 0 | 0 | 1 |
| 4 | 19,839 | 16,016 | 1.23870 | 0 | 32 | 3,272 | 3,705 | 4 |
| 5 | 496,086 | 277,360 | **1.78860** | 537 | 626 | 123,631 | 142,373 | 59 |

## H raw baseline

| ply | full states | board placements | HISTORY_MULTIPLIER | split by castling | split by EP | split by halfmove | split by repetition | max states / board |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1,099 | 1,099 | 1.0000 | 0 | 0 | 0 | 0 | 1 |
| 4 | 18,377 | 14,847 | 1.23776 | 0 | 32 | 3,022 | 3,422 | 4 |
| 5 | 411,566 | 237,652 | **1.73180** | 529 | 587 | 104,909 | 115,069 | 51 |

## Policy frontier

The frozen semantic policy largely suppresses long reversible-move histories at ply 5.

D:
- ply 4: 4,714 full / 3,783 boards = 1.24610x;
- ply 5: 13,064 / 13,003 = 1.00469x.

H:
- ply 4: 4,719 / 3,788 = 1.24578x;
- ply 5: 13,181 / 13,120 = 1.00465x.

At ply 5 the remaining splits are 61 EP/repetition-split board placements in each branch; no castling or halfmove split remains in the policy frontier.

## Scientific interpretation

History is not bookkeeping noise.

At raw ply 5:

- D board-only frontier would be 277,360 placements, but exact theorem identity requires 496,086 states.
- H board-only frontier would be 237,652 placements, but exact theorem identity requires 411,566 states.

Thus board-only merging would overstate compression by a large margin. The maximum multiplicity already reaches 59 exact theorem states for one D board placement and 51 for one H board placement within only five plies.

Castling-right divergence, effective EP, halfmove values and repetition maps all contribute. Repetition claims do not yet fire (maximum observed count is 2), but the metadata still changes full-state equality.

R3 therefore finds an early negative scaling signal for relying on ordinary board transpositions: exact full-rule transposition compression deteriorates materially with depth. The favorable policy-frontier result survives because it reduces the number of histories generated, not because history can be safely quotiented away.
