# R4 Typed-Target Results

**Session:** R4  
**Prospective target grammar:** frozen before decisive certification

## 1. Exact target types tested

R4 permits only:

1. `WHITE_WIN_TERMINAL` — Black to move, no legal move, Black in check;
2. `DRAW_TERMINAL_OR_CLAIM` — stalemate, automatic draw, or a legally exercisable White draw claim under exact full-rule history;
3. `G12_COMPATIBLE_EXACT_TARGET` — exact full-state-compatible entry into frozen G12 KQK/KRK/KPK/DEAD truth;
4. `RECURSIVE_R4_CERTIFIED` — exact existential-White / universal-Black recursion into targets 1–3.

Horizon survival, material advantage, engine score and “approximately equal” are not targets.

## 2. Direct target availability

At the prospectively selected ply-6 cohorts:

| branch | cohort | piece range | direct terminal/draw targets |
|---|---:|---:|---:|
| D king-pawn | 1,024 | 30–32 | **0** |
| H knight-first | 1,024 | 30–32 | **0** |

The minimum material count is 30 pieces. With at most five remaining plies, even a capture on every ply leaves at least 25 pieces. Therefore G12 3–4-piece exact targets are unreachable inside the frozen local proof budget.

This is an exact material-count obstruction, not a missing lookup implementation.

## 3. Recursive target attraction

D:

- depth 1: 0 certified;
- depth 3: 0 certified;
- depth 5: **0 certified**.

H unchanged at frozen depth 5:

- **0 certified**.

Thus the recursive closure of the frozen target grammar over the tested semantic policy has empty intersection with both R4 cohorts.

## 4. What failed

The failure is **target scarcity**, not target unsoundness.

R4 finds no false-positive target and consumes no complete local W/D/L labels. Instead, the exact objects that can self-certify cheaply near the initial position are absent from the tested 30–32-piece frontier.

The existing G12 lower frontier is far too materially distant to be reached in this bounded local test.

## 5. Consequence for the reboot architecture

The Bidirectional Certified Frontier idea requires intermediate exact surfaces. R4 shows that the simplest admissible surfaces—

- terminal wins;
- exact draw/claim states;
- current trusted lower endgame dependencies—

do not provide a usable start-side bridge at this scope.

Any surviving R5 case must therefore identify a **nonterminal typed intermediate target** that is exact for reasons stronger than “this state is non-losing,” does not require complete local W/D/L to define, and can close all Black replies.

Adding a richer target after seeing R4 would be post-hoc repair and is not permitted inside R4.
