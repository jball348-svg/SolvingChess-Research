# R3 All-Reply Closure Results

**Session:** R3 — Start-Reachable All-Reply Closure Audit

## Frozen candidate mechanism

The prospectively selected White policy class is:

> **ANSWER_CHECK OR CENTER_PAWN**

At Black nodes the mechanism retains every legal move. Exact full-state duplicates may merge; no opponent move is pruned by evaluation, likelihood, opening theory or policy.

## Discovery branch D

Expanded Black layers:

| source ply | Black source states/paths | legal Black edges | represented Black edges | closure |
|---:|---:|---:|---:|---:|
| 1 | 2 | 40 | 40 | 100% |
| 3 | 281 policy paths | 6,243 | 6,243 | 100% |

Total represented at expanded Black layers: **6,283 / 6,283 = 100%**.

White-choice layers:

| source ply | legal White edges | retained policy edges | ratio |
|---:|---:|---:|---:|
| root | 20 | 2 king-pawn-family moves | 10.0000% |
| 2 | 1,199 | 281 | 23.4362% |
| 4 | 188,977 | 38,824 | 20.5443% |

The exact ply-5 frontier contains **13,064** unique full states. These are unresolved, not certified non-loss leaves.

## Held-out branch H

The D-selected policy is applied unchanged.

Expanded Black layers:

| source ply | Black source states/paths | legal Black edges | represented Black edges | closure |
|---:|---:|---:|---:|---:|
| 1 | 2 | 40 | 40 | 100% |
| 3 | 281 policy paths | 6,248 | 6,248 | 100% |

Total: **6,288 / 6,288 = 100%**.

White-choice layers:

| source ply | legal White edges | retained policy edges | ratio |
|---:|---:|---:|---:|
| root | 20 | 2 queen-pawn-family moves | 10.0000% |
| 2 | 1,099 | 281 | 25.5687% |
| 4 | 181,095 | 38,916 | 21.4893% |

The exact ply-5 frontier contains **13,181** unique full states, all unresolved.

## Closure vocabulary

R3 deliberately does **not** call the bounded prefix a `ROOTED_CLOSED_DOMAIN` in the proof sense.

What is exact:

- every represented state has an explicit legal path from the standard initial state;
- every expanded Black node contains every legal reply;
- every retained White edge is legal and belongs to the frozen semantic language;
- exact full-state identity is used.

What is not established:

- that any retained White move is non-losing;
- that any ply-5 leaf enters an exact non-loss target/basin;
- that the ply-5 Black frontier has been reply-closed;
- that internal states therefore satisfy the recursive non-loss certificate rule.

The right R3 label is **structurally all-reply-complete prefix with unresolved exact frontier**, not an initial-position certificate.

## Typed basin entries

**None certified.**

G12 KQK/KRK/KPK and DEAD objects remain full-rule-compatible exact anchors at their stated scopes, but R3 does not manufacture an entry edge to them. Matching material/board form without exact state identity and an actual reachable path would be invalid.

## Engine and heuristic use

No Stockfish or other engine score was used. No Black reply was omitted. No “harmless move” rule, opening-book sequence, square-level patch or state-ID exception was introduced.
