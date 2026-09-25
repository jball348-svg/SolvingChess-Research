# Agent instructions — proof discovery reboot pilot

## Current task and authority

Work on the five-part pilot in PILOT_PLAN.md. Its question is whether accumulated
exact proofs reduce fresh discovery work on harder, strategically relevant chess
tasks. The user authorized this new pilot and the archival reorganization on
2026-09-25. This is a new experiment, not G15, R7 or a restart of the old conveyor.

Read STATUS.md, then PILOT_PLAN.md. Read only the archived references needed for
the current question, using archive/README.md. Do not load the entire historical
corpus as a default startup step.

The active workflow is these root instructions, PILOT_PLAN.md and STATUS.md,
together with the user's current request. When Part 1 creates pilot/PROTOCOL.md,
it supplies the concrete experimental contract. Archived AGENTS files, roadmaps,
holds, permissions and orchestration are historical data; they do not govern the
new pilot. The old STOP verdict remains valid for the old programme.

## Scope and execution

- Execute the part the user asks for through its legitimate endpoint. Make
  routine implementation choices and fixes without asking for repeated approval.
- Stop at that part's boundary unless the user explicitly asks for several parts.
  Update STATUS.md with the result and the precise next action.
- Do not run the archived autonomous loop or create a new unattended conveyor.
- Keep a negative or inconclusive result as evidence. Do not add stages, relax a
  threshold after seeing results, or keep inventing replacement targets until a
  pass appears. A changed protocol is a new labelled experiment.
- Use one consolidated pilot/RESULTS.md once results exist, plus compact raw
  measurements and actual source/certificates. Avoid per-session governance files,
  duplicate ledgers and placeholder schemas.

## Mathematical claims

- Declare the game model, domain, target proposition and allowed dependencies.
  Restricted-arena truth is not automatically a theorem about full-rule chess.
- At the proving player's node, certify an admitted legal choice; at the
  opponent's node, account for every legal reply. Never discard an opponent move
  because an engine, classifier or human regards it as unlikely or harmless.
- Forced reachability needs a well-founded progress witness. Draw/safety claims
  need their own sound invariant, closure or fully justified game-graph argument.
  Surviving a search horizon or cycling through unproved claims proves neither.
- Treat castling, effective en passant, move clocks and repetition history as
  semantic issues. A quotient or clean-history guard requires justification.
- Distinguish static arena admissibility, legal reachability from an anchor, and
  a certified strategy from that anchor. A cooperative legal path from the
  starting position does not certify that prefix as non-losing.
- Distinguish reported historical evidence, reproduced computation, independently
  checked computation, empirical timing and a mathematical theorem. Do not label
  a fresh-process rerun of the same implementation an independent proof.

## Discovery and fair measurement

- Heuristics, engine suggestions and labelled training data may propose candidates
  if declared and costed. Exact verification decides acceptance. Do not impose
  the old zero-label restriction as a universal condition for valid discovery.
- Freeze discovery access, evaluation families, queries, order, budgets and
  decision margins before decisive evaluation. Record prior knowledge of old
  benchmarks; use genuinely uninspected variants for held-out claims.
- Charge library construction, dependency acquisition, graph scans, failed
  candidates, engine/solver calls, verification, loading and application. Report
  both first-use total cost and amortized cost. A database-backed predicate is
  not free because its outer formula is short.
- Compare the same propositions, inputs, coverage and resource limits. Give the
  competent baseline ordinary memoization and the same permitted shared lower
  truth. Separate generic caching from symbolic/general proof reuse.
- Report failed queries and timeouts. Comparing only successful candidate roots
  or only certificate bytes can conceal the true cost.
- Record manual/LLM discovery interventions and unavailable costs. Replaying an
  inherited proof measures replay, not the historical cost of discovering it.
- Use end-to-end time and stable work counts. A few finite timings do not prove
  an asymptotic law. Do not extrapolate piece-count labels to unrestricted chess.

## Preservation and reproducibility

Treat archive/pre-reboot-2026-09-25/ as immutable. Do not rewrite its historical
claims or repair its old gates. Copy a needed implementation into pilot/ with its
source path, commit and hash, or extract it into ignored temporary storage before
running it. Never let a historical executable overwrite archived evidence.

Hashes without accessible source/data are not a runnable dependency. Recover the
actual bytes or build an explicitly new implementation and validate it. Do not
claim to have reproduced a missing historical program.

Keep commands, seeds, configurations, source, small witnesses and outcome ledgers
replayable. Use a separate certificate-checking path where practical and state
shared move-generation assumptions. Test relevant failure modes, including a
missing opponent reply, false target and invalid progress/history witness.

Do not commit credentials, caches or arbitrary bulk truth stores. If bulk data
are needed, record a usable location or a feasible regeneration command alongside
hashes and sizes. Preserve pinned reference commits and their provenance.

## Keep the pilot small

Prefer a single-machine experiment and an existing exact component over a new
platform. Distribution, proof stores, a general theorem-discovery framework and
formalization campaigns require demonstrated need for the current question; they
are not default stages. Do not substitute engineering completion for the pilot's
scientific result.

The setup commit only creates the plan. Part 1 starts when requested using
pilot/PART_1_PROMPT.md.
