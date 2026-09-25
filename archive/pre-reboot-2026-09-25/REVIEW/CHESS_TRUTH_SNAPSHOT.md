# Chess truth snapshot at review opening

This reports the repository's own state, not an independent verdict.

## Objective

A machine-checkable weak solution establishing that White has a non-losing strategy from the standard initial position under the declared complete ruleset, covering every legal Black reply.

## Current routing state

- Latest completed programme: G14.
- G14 passed its own proof-store/preservation gate but claims no new chess truth.
- G15 is not authorized or started.
- G15 and G17 remain blocked by the mandatory G12-through-G13 acceptance replay.
- The autonomous loop is stopped.

## Connected-proof state

G9 explicitly says direct proof-path completion from the initial position is near zero and scores initial-position connection at 1/100. No later frozen handoff through G14 claims a certified connection from the standard initial position.

## Strong assets already claimed

- Exact finite-game/attractor machinery and reusable graph operators from G6-G8.
- Exact restricted six-, seven- and eight-man results.
- Material-signature solver, compact proof objects and verification paths.
- Final-rule state semantics and small-arena G12 anchors with history-aware controls.
- Deterministic distributed/checkpoint engineering from G13 on a synthetic fixture.
- Content-addressed proof storage and hostile-mutation/offline verification from G14.

## Explicit limits already recorded

- Restricted eight-man arenas are not broad eight-piece coverage.
- Some residuals have lookup-like local floors.
- Compact certificates do not guarantee cheaper verification.
- Automatic target/strategy discovery lags the proof language.
- Ordinary middlegame topology and opening connectivity remain largely unaddressed.
- `ARENA_ADMISSIBLE` does not imply start reachability.
- The enormous gap to the 32-piece initial game has not been closed end-to-end.

The review must decide whether these are temporary limitations of a genuinely scalable mechanism, or evidence that the programme solves increasingly sophisticated disconnected islands without a route across the central bridge.
