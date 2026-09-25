# Global proof architecture

## Required theorem

At 100%, the repository needs an independently replayable proof that, from the standard initial chess position under the frozen full rules, White has a strategy that avoids loss against every legal Black reply.

## Required logical route

```text
standard initial position
  -> start-reachable full-rule states
  -> White strategy covering every Black reply
  -> certified higher-tree/middlegame progress
  -> certified lower-tree non-loss basins
  -> exact terminal/draw truth
  -> White cannot lose
```

Every arrow needs a theorem, exact certificate, or composition rule whose hypotheses are themselves certified.

## Current roadmap route

G10-G15 foundations -> G16-G22 scale/endgame basins -> G23-G28 automated discovery/composition -> G29-G34 middlegame basin network -> G35-G39 initial-position connector/all-reply closure -> G40-G42 final proof.

That is an execution architecture, not itself a bridge theorem.

## The Chess Bridge Problem

The central audit target is the missing mechanism that turns exact lower-tree truth into repeatable progress at materially richer positions without first solving essentially the entire higher-material game graph.

A useful bridge must be stronger than "solve more pieces", "carry raw truth", "build a basin", "search forward until it meets the basin", "cover all replies", or "make the solver faster".

Three candidate forms count:

1. A lifting/composition theorem deriving large higher-material certified regions without enumerating essentially all parent states.
2. A demonstrated scaling law across increasingly unrestricted material/topology classes with viable compute and verification economics.
3. A genuinely `START_REACHABLE` all-replies certificate whose covered frontier expands by an iterable certified mechanism.

The review may discover another form, but it must state it precisely and attack it.
