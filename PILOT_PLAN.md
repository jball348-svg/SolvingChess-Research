# Five-part pilot: does proof reuse compound?

## Question and scope

Can an accumulating library of exact proofs make fresh discovery progressively
more economical on harder chess tasks, while preserving useful coverage and all
opponent replies?

The pilot has five parts, identified as RP1–RP5 to distinguish them from historical
Pilots, G-stages and R-reviews. It tests a bounded method, not a solution of chess.
A negative finding concerns the declared models, methods and budgets.

Four observations motivate it: G8 made some large computations much cheaper;
G6 showed useful proof composition; R2 found transferable rules at roughly the
cost of exact solving; R3–R5 never produced a scalable connected strategy. The
open issue is whether these gains can accumulate. See the
[post-mortem](archive/POST_MORTEM_2026-09-24.md) and
[reference guide](archive/README.md).

## Common experimental contract

Part 1 chooses concrete details and freezes them in one `pilot/PROTOCOL.md` before
decisive experiments. It must specify the following.

**Task and semantics.** Define the same externally fixed propositions/queries
for every method, the proving player, the target or safety property, move rules,
terminal rules, history treatment, lower-material dependencies and certificate
format. Restricted games are permissible primary laboratories, with an explicit
boundary to full chess. Exactness permits no accepted false certificate.

**What counts as reuse.** A reusable proof object includes its domain, proposition,
semantic guards, strategy/progress or invariant witness, dependencies and checker.
It may cover a parameterized family rather than individual state IDs. Extensional
answer caching is a useful separate comparator. A short predicate whose membership
requires a large oracle must expose and pay for that oracle.

**Benchmarks.** Use a tractable chess family with at least four ordered evaluation
rungs, plus two structurally different held-out variants. Size must grow through
explicit domain/transition changes, not duplicated states or renamed coordinates.
Include an ordinary counterplay challenge and a rules/history challenge. Specify
how much is historically known and keep decisive held-out outcomes out of method
selection. Fix generators, seeds, query order and training/evaluation boundaries.
Historical anchors are regression controls, not unseen transfer evidence.

**Comparators.** Compare a competent exact solver/search with ordinary warm caching,
the same machinery with a fixed donor proof library, and the same machinery with
a growing library. Give all arms the same admissible shared lower truth, resource
limits and ordinary caching opportunities. Include a generic answer-cache control
with a comparable storage budget where the representation makes that meaningful.
Record when equal memory is impossible. A full-arena exact solve is an additional
reference where feasible, rather than a deliberately expensive sole baseline.

**Equal work.** Score every method on the frozen queries, including unknowns and
failures. Compare cost at matched coverage and report cost/coverage curves where
completion differs. Do not compare a handful of easy successful proofs against
the cost of answering a stronger complete-W/D/L task. A method unable to reach
the declared coverage has not demonstrated an equivalent-task speedup. Retain
all attempt costs; do not select a favourable common-success subset after testing.

**Cost.** Record discovery/training, dependency construction, complete graph scans,
failed candidates, engine/solver calls, verification, loading, application, fallback
search, peak memory and library/dependency bytes. Report both the full first-use
cost and amortized cost over the evaluated sequence. Shared costs get their own
ledger column and must not disappear or be double-counted. For the growing arm:

    total through k = initial acquisition and verification
                    + sum of all discovery, application, verification and
                      unresolved-query work through evaluation rung k

Compare that total with equally accounted baselines. Also record deterministic
work proxies such as fresh state expansions, examined edges and proof obligations
settled. Report noise/repeat policy; wall time alone is insufficient.

Record human/LLM-guided discovery interventions, candidate revisions and available
time/usage information. Freeze the procedure before evaluation rather than hiding
per-arena redesign outside the timer. Distinguish measured construction/replay cost
from unavailable historical discovery effort, and declare any inherited knowledge
treated as sunk. Missing costs limit an end-to-end economic claim; they are not zero.

**Budgets and interpretation.** Part 1 chooses concrete CPU-time, wall-time, RAM,
disk and search budgets after small calibration. Defaults: one machine; no paid
services; at most 10 minutes per run, 8 GiB RAM or half available RAM (whichever
is lower), and four CPU-hours per subsequent experimental part. Tighten these
when needed. Part 1 itself has a one CPU-hour calibration budget. An over-budget
result is retained; resizing happens only prospectively, with a new labelled
protocol. Choose a practical improvement margin above measurement noise before
decisive outcomes, justify it, and report underlying measurements even if the
margin is missed. A first-use cost ratio above one does not end the pilot: later
amortization is the question. A few finite points cannot establish an asymptotic law.

## Part 1 — Make the question testable (RP1)

**Open question:** can we build a small, reproducible and fair experiment from
the actual surviving assets?

1. Replay one available exact anchor, preferably the G12 source/certificate bundle,
   outside the immutable archive. Record the precise semantic scope and hashes.
   The post-mortem replay is a reference, not a new Part 1 run.
2. Select one main benchmark family, four size/restriction rungs and two held-out
   variants. Prefer material-adjacent families where known lower proofs can be
   used, then progressively relax restrictions. Avoid a benchmark consisting only
   of near-promotion races. Do not require a leap from opening positions to tiny
   tablebases inside an impossible capture budget.
3. Implement or adapt a runnable exact baseline and certificate-checking seam.
   Run only known controls and the smallest development smoke case to check move
   semantics, resource feasibility and instrumentation. Missing late-review source
   should lead to a named new implementation, not an attempted repair of old gates.
4. Freeze the protocol, candidate-discovery procedure and allowable search space,
   library update schedule, query/coverage metrics, budgets and decision margins.
   Choose one principal mechanism and at most one predeclared alternative. Commit
   the freeze before Part 2 sees decisive evaluation outcomes.

**Deliverables:** `pilot/PROTOCOL.md`, minimal runnable source/checks, exact replay
commands and the opening section of `pilot/RESULTS.md`, with compact raw outputs.
Update STATUS.md. No new discovery or compounding success is claimed here.

**Endpoint:** READY_FOR_RP2 if the baseline and protocol are usable; otherwise
BLOCKED with a precise reproducibility or feasibility finding. Routine fixes
within the calibration budget are expected. Do not run Parts 2–4.

## Part 2 — Acquire new reusable proofs (RP2)

**Open question:** can the selected procedure find useful proof objects, and what
does acquiring them actually cost?

Use the declared donor/development domain to build a small library. Candidate
search may use semantic predicates, strategy programs, reachability composition,
draw/safety invariants or the predeclared alternative. Human/engine heuristics and
labelled training data are allowed if their use and cost are explicit; none can
replace exact acceptance checks.

Separate proposing candidates from verifying their domain and every opponent
reply. Freeze discovered objects before first transfer evaluation. Evaluate on
the reserved initial test queries without outcome-driven patches. Record a
certificate for every accepted object, all failed attempts and the cost of hidden
dependencies. Compare against solving the same task without this library.

**Deliverables:** the actual objects, checker, provenance and cost/coverage results
in the consolidated record. State whether any new structurally reusable object
was acquired, rather than merely replaying stored answers or relabelling old rules.

**Endpoint:** a bounded positive, negative or inconclusive acquisition result.
Acquisition overhead is carried forward into Part 3. Sound objects can be tested
for amortization even when their initial acquisition loses to a complete solve.
If no new object is obtained, say so; fixed-library reuse may still be measured,
but it cannot support a claim of cumulative new-proof discovery.

## Part 3 — Measure whether reuse compounds (RP3)

**Open question:** does an expanding library reduce fresh work beyond fixed
knowledge, generic caching and better implementation?

Run the four-rung sequence under the frozen update schedule. Evaluate each rung
with only the library available before that evaluation. Learning from a completed
rung for the next is permitted and fully costed; it is not retrospective transfer.
Run the ordinary-cache, fixed-library and growing-library arms on identical
queries. Keep cache budgets and access to lower truth explicit.

For every prefix of the sequence, report total acquisition-plus-solving cost,
coverage, fresh expansions/edges, verification cost and stored dependencies.
Show the break-even point if one occurs, and explicitly report none otherwise.
At later rungs, remove newly learned modules in an ablation to test whether they
cause the saving. Use a predeclared order check if order could explain the result.

**Deliverables:** the measured curves/tables and small witnesses showing which
earlier proofs discharged which later obligations. Preserve all runs and queries,
including cases where residual work or description size grew faster than coverage.

**Endpoint:** distinguish one-off speedup, fixed-library benefit, cumulative
benefit and no demonstrated benefit. Evidence for compounding needs a practically
meaningful total-cost advantage at matched coverage across later rungs, supported
by work counts and the library ablation. Exact magnitude and uncertainty remain
visible. A faster solver alone does not answer the cumulative-library question.

## Part 4 — Test transfer and useful connections (RP4)

**Open question:** does the benefit survive a changed topology/rule burden and
help close an actual adversarial strategy, rather than accumulate unrelated truth?

Apply the frozen method to the two held-out stress variants. One should weaken
the structural assumptions that made the donor easy, including quiet opponent
counterplay; the other should address history/rules compatibility. Any allowed
adaptation must follow the frozen procedure and have its cost included. An
unplanned successful repair is exploratory evidence, not a held-out pass.

For a prospectively chosen reachable anchor or anchor cohort, attempt a complete
local strategy certificate into compatible library regions, or a closed safety/draw
certificate. Record each opposing reply and every unresolved frontier obligation.
Check reachability and elementary material/distance feasibility before the run.
Use a supplied legal history for full-rule claims. A late-game anchor reached by
cooperative play demonstrates reachability only: its prefix is not an opening proof.

Measure which library objects close required replies, the cost of completing the
local certificate, and the residual obligations when it fails. Compare with the
same anchor task without the learned objects. Raw basin density is secondary.
Full-rule compatibility can use proved guards or a justified quotient; it cannot
silently identify histories because their boards match. Broader draw invariants
are allowed; four-ply exact repetition is not the only permitted target.

**Deliverables:** transfer costs/coverage and the actual strategy or safety witness,
or the unresolved frontier and counterexamples. Keep restricted and full-rule
results separate. There is no requirement to approach 32 pieces in this pilot.

**Endpoint:** establish where the benefit transfers, where it fails, and whether
any root-relevant connection was certified. Failure here can coexist with a useful
restricted result from Parts 2–3.

## Part 5 — Reproduce and make the bounded decision (RP5)

**Open question:** after independent checking and full accounting, what remains?

Replay the decisive certificates through a separately implemented checking path
where practical. Identify shared move-generation assumptions. Use targeted negative
controls for omitted opponent moves, false target membership, circular reachability
and invalid history merges. Reconcile reported totals with raw cost ledgers and
check that code, inputs and witnesses are available, not merely named by hashes.

Choose one conclusion in the final section of pilot/RESULTS.md:

- **FOLLOW_ON_JUSTIFIED:** exact, reproducible cumulative savings at matched coverage
  survive the declared transfer tests and contribute to a connected local strategy.
  Name one bounded next research question and the evidence supporting it.
- **LIMITED_RESULT:** preserve a useful exact/reuse result while stating precisely
  which scaling, transfer or connectivity claim remains unestablished.
- **NO_ADVANTAGE_DEMONSTRATED:** the tested method does not justify continuation
  on the frozen tasks/budget. Preserve its negative evidence and narrow scope.
- **INCONCLUSIVE_OR_BLOCKED:** a specific measurement or reproducibility defect
  prevents the intended comparison. Name it without converting it into a pass or
  a theorem of impossibility.

Do not infer a solution probability for chess or an asymptotic scaling law. Do
not automatically create Part 6, restart G15 or implement a new roadmap. Update
STATUS.md with the final conclusion and leave any follow-on as a concrete proposal.

## Minimal record

Keep the project understandable through this plan, STATUS.md, one experimental
protocol and one consolidated results file. Put code under `pilot/src/`, necessary
tests under `pilot/tests/`, and compact measurements/certificates under `pilot/`.
Use exact commit identities for protocol freezes. Additional documentation must
answer a question these files cannot answer; stage completion is not a reason to
manufacture another handoff hierarchy.
