# Solving Chess — proof discovery reboot pilot

**Status: five-part pilot planned; Part 1 has not run.**

The research question is deliberately narrower than solving chess:

> Does a growing library of exact, reusable chess proofs reduce the fresh work
> needed to establish further strategically useful truth as the problem grows?

The previous programme produced real restricted proofs and useful machinery, but
did not establish that its gains compounded. This pilot tests that missing claim.
It does not resume the old G-programme or reverse its final STOP_CURRENT_METHOD
decision.

## Start here

- [Pilot plan](PILOT_PLAN.md): five questions, experiments and decision criteria.
- [Current status](STATUS.md): the only active progress and next-action record.
- [Agent instructions](AGENTS.md): how to work on this pilot.
- [Part 1 kickoff prompt](pilot/PART_1_PROMPT.md): ready to paste into a new session.
- [Archive guide](archive/README.md): selected references and the complete old tree.

| Part | Question |
|---|---|
| 1 — Benchmark and baseline | Can we measure proof reuse fairly and reproducibly? |
| 2 — Discover new reusable proofs | Can useful proof objects be acquired at a measured cost? |
| 3 — Test cumulative reuse | Does the growing library outperform fixed knowledge and ordinary caching? |
| 4 — Transfer and strategy connections | Do the savings survive changed chess and close actual opposing replies? |
| 5 — Replay and decide | What has been established, and is a bounded follow-on justified? |

Success requires exactness, useful coverage and honest total-cost accounting.
Compact descriptions, bigger state counts and completed infrastructure are not
substitutes for those measurements. An expensive first discovery can still pay
for itself through later reuse; that is something to measure rather than assume.

## Repository layout

The active project consists of this README, AGENTS.md, PILOT_PLAN.md, STATUS.md and
the small `pilot/` working area. Code, a frozen protocol and experimental results
will be added there only when the relevant part runs.

Everything previously tracked is preserved under
[`archive/pre-reboot-2026-09-25/`](archive/pre-reboot-2026-09-25/), including the
old instructions, orchestration, state, review, source and bundles. Historical
paths and conclusions are unchanged inside that snapshot. Archived instructions
are reference material, not the active workflow.

The [post-mortem](archive/POST_MORTEM_2026-09-24.md) explains the reboot's rationale.
There is currently no new chess theorem, measured pilot speedup or claim of
progress toward a complete initial-position proof.
