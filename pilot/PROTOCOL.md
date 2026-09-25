# RP1 protocol v1 — bounded spatial proof reuse

Frozen before any RP2 discovery or reserved evaluation. The freeze commit is
recorded in `STATUS.md` and `RESULTS.md` after publication. The exact source and
input identities are in `evidence/source-manifest.json`. Changing the method,
queries, budgets or margins creates a labelled new experiment; it cannot repair
this experiment retrospectively.

## 1. Proposition and semantic boundary

For each supplied state, decide **whether White can force Black's checkmate in
at most six plies**, against every admitted Black reply. Return a checked `true`
or checked `false`; resource exhaustion is `UNKNOWN/LIMIT`, never `false`.
False means failure of this bounded proposition, **not a draw or an unbounded
non-win**. Checkmate already present has rank zero. The proving player is White.

The laboratory is a rectangle anchored at a1 on the usual 8×8 board. Both kings
and all other pieces stay inside it. Generate orthodox legal moves with pinned
`chess==1.11.2`, then admit exactly moves whose destinations are inside the
rectangle. Rook rays and attacks follow ordinary geometry; a rook may not jump.
Rectangles are convex, so admitted slider paths also stay inside. Mate/stalemate
use the **restricted** reply set. Consequently a restricted mate need not be an
orthodox mate. Locally valid placements need not be reachable from the initial
chess position. No full-chess or opening theorem is a pilot endpoint.

Main material is White king + rook versus Black king, including rook-capture
exits into two kings. All arms share only: legal terminal adjudication, and the
elementary fact that a bare White king cannot deliver checkmate. Other
insufficient-material shortcuts are prohibited: board boundaries change mating
possibilities. No G12 tables, engine labels, tablebases or missing R-review
programs are solving dependencies.

Main arenas deliberately omit move-count and repetition draws. Position identity
includes the complete rectangle, placement, turn, rights/effective EP and remaining
plies; clocks/fullmove numbers are irrelevant **only in this model**. Roots have
no castling rights or EP. KRK never creates either. The counterplay variant adds
one Black pawn: all pawn pushes/captures and all four promotions on rank 1 are
admitted, with promoted material continuing normally. One Black pawn and no
White pawn cannot create an effective EP capture; castling rights remain absent.

The history variant adds the 50-move and threefold claim actions, including
claims by an intended admitted move, and automatic 75-move/fivefold draws.
Checkmate has precedence over the automatic clock draw. Black may claim a draw;
White may decline its own claim when trying to mate. History keys retain the
halfmove clock and the entire supplied repetition-count map, with no board-only
merge. The model starts from the declared FEN with one occurrence and replays
every supplied move. Clock-seeded roots are conditional metadata states, **not
claims to have recovered their earlier history**. Cycle roots have explicit
legal continuations from their declared endgame anchor. These are rule-compatibility
tests in a restricted game, not full FIDE dead-position/reachability certification.

## 2. Fixed domains, queries and access

`src/benchmarks.py` is the executable generator. Seed: `RP1-2026-09-25-v1`.
Enumerate locally legal nonterminal placements without consulting bounded truth;
select smallest SHA-256 priorities, balanced by side to move, and order by the
same priority. Hash partition 0 mod 8 is smoke, 1 is test, 2–7 are training.
Query hashes include the arena name and role. Generation/scanning costs are
measured shared costs; there is no free oracle behind the sampling operation.

| Role | Rectangle | Material | Queries and when accessible |
|---|---|---|---|
| Development D | 3×4 | KRK | RP1: 8 smoke queries; full small-arena DP reference |
| Donor D | 3×4 | KRK | RP2: 24 training queries, 12 per turn |
| R1 | 3×5 | KRK | 16 test queries in RP2; 24 training queries only after R1 evaluation |
| R2 | 4×5 | KRK | 16 test queries in RP3; then 24 training queries |
| R3 | 4×6 | KRK | 16 test queries in RP3; then 24 training queries |
| R4 | 5×6 | KRK | 16 test queries in RP3; no subsequent acquisition |
| Counterplay C | 5×6 | KRK + Black pawn | RP4: 16 test queries; pawn initially on ranks 2–5 |
| History H | 4×5 | KRK with history | RP4: 16 queries from `history_cohort()` |

Every test/training cohort uses respectively 8/12 queries per turn. H instead
has four clock-0 roots, four clock-98 roots, four one-cycle histories, and four
two-cycle histories. Its first eight roots are paired with already evaluated
R2 boards. It is **unseen history/rule transfer**, not an unseen-board claim.
Cycles are the first four SHA-ordered admissible anchors with a lexicographically
first legal, capture-free four-ply return; the history includes one/two complete
cycles. Selecting legal cycles reveals no bounded winning labels. The generator
must fail visibly if four such anchors cannot be generated within budget.

Rungs add actual squares and transitions: 15, 20, 24, 30 squares. They are not
duplicate states or relabelled boards. The largest main arena has at most 48,720
raw KRK states; including two-king exits and seven remaining-depth layers gives
at most 353,220 state-depth pairs. This is a combinatorial bound, not a measured
later-rung runtime. The four-piece/history variants can exhaust the budget.

RP1 has seen G12's historical results, the complete D reference, the recorded
smoke and synthetic controls. Thus D has **no held-out status**. No R1–R4/C/H
cohort has been generated or solved in RP1. RP2 may use only D for acquisition
before freezing its donor library, then evaluate R1 without changes. RP3 reuses
those R1 measurements; it does not call R1 unseen a second time. C/H generation,
outcomes and anchor searches remain inaccessible to discovery until RP4.

## 3. Exact baseline and certificate seam

`solver.py` implements demand-driven AND/OR search with a warm exact
transposition table and conventional capture/check/UCI ordering. White is OR,
Black is AND. Both successful and failed subproblems are cached. Horizon, mate,
stalemate, claims and bare-king exits are distinguished. This is the principal
baseline, not an expensive complete W/D/L solve. `reference.py` provides an
additional complete-arena layer DP; it was used only on D in RP1.

Each certificate binds the semantic model, root, full state key and remaining
depth. OR-true/AND-false nodes contain one admitted witness; OR-false/AND-true
nodes contain every legal move. Depth decreases exactly by one on each edge.
Leaves are checked terminals or bounded-failure horizon leaves. `checker.py`
regenerates replies, replays transitions and rejects wrong targets, missing
moves, circular witnesses, unreachable baggage and invalid history merges.
It does not call the producer or trust its Boolean labels. It **shares**
`model.py` and python-chess with the solver: this is separate proof traversal,
not an independent formalization of chess. RP5 must preserve that limitation.

The fixture template in the seam test is not a seed for any experimental arm.
The executable interface is present now; later parts may add their measurement
driver and the mechanical candidate enumeration below, without redesigning it.

## 4. One discovery mechanism; no alternative

The principal mechanism is **spatial proof skeletons with checked boundary
conditions**. Take a newly checked positive KRK proof, replace its absolute
coordinates with offsets from the root Black king, and canonicalize over eight
square symmetries. Retain its complete White strategy, Black reply branches and
mate leaves. Required depth is the actual longest witness path, not the search
horizon used to find it. No pawn symmetry is assumed.

A proof object contains root material/turn/geometry, required plies, relative
move DAG, terminal/progress witnesses, identity and provenance to its checked
donor certificate. Its permitted family consists of placements/rectangles where
those relative moves are legal, every opponent reply is accounted for and every
leaf really is mate. **Membership is not free:** every new application instantiates
the DAG and runs the exact checker in the new domain/history. A new escape,
illegal White move, draw claim or incompatible history rejects the application;
its full work remains charged and ordinary search continues. Successfully
instantiated DAGs enter the same ordinary cache as baseline results.

The frozen acquisition algorithm for each permitted training cohort is:

1. Run the ordinary baseline on all 24 training queries, in generator order,
   caching normally. Do not use proof-library pruning during this acquisition
   pass, so F/G/C receive an identical, auditable information source.
2. Independently check each available root certificate. For each positive root,
   traverse its positive subproofs breadth-first, UCI-ordered, skipping terminal
   roots. Consider at most the first 32 subproof roots per training query.
3. Extract each concrete sub-DAG and run `compile_template`. Deduplicate by
   canonical root piece geometry and side to move (not coordinate names, arena
   identifier or increasing horizon). Keep the first accepted witness per geometry;
   do not replace it later after seeing transfer results.
4. Admit at most **eight new geometries per update**, at most 64 total, at most
   1 MiB serialized library in total, and at most 2,048 nodes per object. Keep
   checking/logging all scheduled candidates; over-cap/duplicate/malformed
   candidates count as attempts, not free discarded work. Preserve the actual
   accepted objects, provenance and attempt costs. There is no engine or human
   candidate editing between evaluations.

This is a deliberately narrow discovery space: geometry/boundary abstraction of
finite mating strategies. It is not discovery of unrestricted symbolic chess
theorems. Merely storing another answer, finding a rotated duplicate, or replaying
a synthetic control is not a new structural object. Report distinct geometries,
objects instantiated outside their donor rectangle, and actual obligations
discharged separately. A transfer advantage must beat the geometry-cache control.

## 5. Arms, update schedule and connected task

| Arm | Persistent information | Acquisition charged |
|---|---|---|
| B: ordinary cache | Exact transposition table within each arena | Its own query work only |
| C: generic geometry cache | Exact state answers with full arena geometry and witnesses, ≤1 MiB | Same scheduled training solves as G; cache extraction/loading |
| F: fixed proofs | D's at most eight templates; ordinary cache | Donor solves, all candidate attempts, acceptance and loading |
| G: growing proofs | Same donor set, then at most eight additions after R1/R2/R3 | All corresponding acquisition, failed attempts and verification |

C uses `cache_geometry`: unlike the proof skeleton guard, its key retains every
square of the arena. It may canonicalize KRK geometry under the same eight
symmetries/translations; pawn/history states use full exact keys. Fill the cache
from every scheduled training root and subproof in the same BFS order, including
negative certificates, until its 1 MiB cap; keep first entries, with no eviction.
Charge its full stored witness bytes and instantiation/checking. C has no eight-
entry quota. It may serve internal search obligations too. This is an intentionally
competent extensional comparator, not a cache indexed only by arbitrary IDs.

All arms share rules, proposition, query order, lower truth, exact checking,
move ordering, cache opportunities and hard resource limits. Each arena starts
with a fresh 500,000-entry ordinary table; a key contains the complete arena,
so these main rungs share no identical transposition keys. Tables remain warm
within an arena/sequence. Persistent libraries/cache have the same serialized
cap; Python index/object overhead need not be equal and is measured, not declared
equal. B does not pay for unused discovery; C does not receive uncharged labels.

RP2 freezes the donor objects before the R1 test. RP3 evaluates each successive
rung with only the preceding library, then acquires from that completed rung's
separate training cohort for the next. Acquisition after Rk is charged in the
prefix ending at R(k+1), when it is first usable. No acquisition follows R4.
For R3/R4, rerun G with all post-donor modules removed; any saving attributed to
new modules must disappear by at least half under this ablation. F is also a
standing donor-only control. Run one reverse-query-order diagnostic at R3/R4
with the libraries frozen; it cannot replace the primary order or its verdict.

RP4 applies the final frozen libraries to C and H with **no acquisition or
outcome-driven repair**. The first four one-cycle H histories are the prospective
local anchor cohort: legal paths from explicitly supplied late-game anchors,
no opening claim, no missing material-reduction bridge. Attempt the same complete
six-ply strategy into verified library proofs/mate; every Black reply remains.
Publish a checked local certificate on success. On bounded failure, publish the
counterstrategy/horizon frontier, without calling it a draw theorem. Library-free
B answers the identical anchors. C also tests whether captures can connect a
four-piece counterplay task to compatible KRK modules.

## 6. Accounting, limits and decision margins

Use `measure.py` for a fresh-process envelope including interpreter startup,
failures and timeouts. Inside it retain phase CPU/wall times and `model.WORK`
counts. Required columns: query generation; dependency construction/loading;
training/discovery; complete graph scans; all candidate attempts (accepted and
failed); application including failed guards; fallback search; certificate
emission/serialization/loading; verification; storage accounting; process peak
RSS; library/dependency/certificate/cache bytes; and every query's outcome.
Application's embedded checking is a subcost, **not added a second time**.
Search totals may contain application: also report their disjoint residual.
Engine calls are explicitly zero. Distinguish zero from unmeasured/unavailable.

Stable counters include fresh states/expansions, legal edges generated, examined
search edges, transitions, cache hits, template probes/rejections, checked nodes
and checked edges. Count rejected application work through phase-wide `WORK`,
even when the checker exits before returning its successful audit. Report
terminal versus library-settled obligations and the complete unresolved frontier.
A certificate-byte reduction alone is not a computational saving.

Shared cohort generation is charged once to each arm's equivalent-task total,
with its own ledger column; it is not multiplied by the number of certificate
lookups. The optional complete-arena reference is a separately labelled
comparator/calibration expense, not mandatory hidden overhead on B alone. For G,

`prefix cost = shared inputs + donor acquisition/verification/load + all prior
updates first usable in that prefix + all evaluated application/fallback/check costs`.

Report raw query cost, full first-use cost, cumulative cost and total/query
amortization at every prefix. Report costs of generating negative/unknown answers.
No common-success subset selection. The primary matched-coverage requirement is
**all 16 queries per evaluated rung**, both truth values included. Otherwise give
the full cost/coverage curve and no equivalent-task speedup verdict.

| Budget | Frozen limit |
|---|---|
| Machine/services | One process/core at a time; no paid services |
| One run/cohort | 300 CPU seconds; 600 wall seconds; search deadline 120 wall seconds |
| Ordinary table | 500,000 exact state-depth entries; limit is an unknown, not eviction disguised as truth |
| RAM | min(4 GiB, half available host/cgroup memory); record actual peak RSS |
| Disk | 1 GiB generated data per part; 64 MiB per file; libraries ≤1 MiB each |
| Candidate/total budgets | 32 subproof roots/query; eight accepted/update; RP1 ≤1 CPU-hour; later parts ≤4 CPU-hours each |

Keep every limit result and partially paid cost. A run killed before emitting
per-query results contributes its full envelope cost and marks unfinished
queries UNKNOWN. Do not resize after observing an evaluation. Source tests and
development smoke are allowed fixes before this freeze, not a licence to inspect
reserved outcomes. Resource ceilings apply to sampling and history generation too.

Three serial fresh-process repetitions per arm, carrying each arm's state only
within its prescribed sequence. Reproduce acquisition mechanically each time;
report its repeated costs, but count one acquisition per modeled first use.
Rotate arm execution order cyclically across repeats; no parallel timing runs.
Use medians and min/max, retain all raw repetitions. A second identical query
pass is a warm-cache diagnostic only, not fresh-discovery evidence.

A practical advantage requires **at least 25% lower median cumulative CPU and
wall cost**, at least 50 ms absolute median saving, and the slowest candidate
repeat faster than the fastest comparator repeat. Require at least 25% fewer
fresh fallback expansions and disclose total generated-edge/checking work.
The D smoke's total time varied about 2%; individual short phases were noisier,
so the 25% + absolute + non-overlap rule is deliberately conservative.

Cumulative benefit requires these margins versus the **best of B/C/F** at both
prefixes ending R3 and R4, full matched coverage, the module ablation, and no
reversal in the reverse-order diagnostic. First-use acquisition losing at R1
does not end the pilot. RP4 must report each stress separately and actual anchor
closure; failure can leave a limited restricted result. No finite set of timings
establishes an asymptotic law. RP5 alone makes the final five-part decision.

## 7. Knowledge and missing costs

RP1's LLM implementation/design and historical discovery effort have no reliable
token/CPU/monetary measurement available. They are **unavailable, not zero**.
Record every later human/LLM intervention; post-freeze heuristic redesign is
exploratory and cannot change primary results. This experiment measures automated
acquisition and reuse given the frozen code, not total human research economics.
The installed Python/chess/compiler environment is shared setup; record versions
and installation/acquisition time when newly needed. No historical proof-library
construction cost is silently inherited: G12 is only the separately charged
RP1 reproducibility control. Its original discovery cost remains unavailable.

This protocol commits only an experiment. RP1 claims neither discovery success
nor cumulative savings. Stop after publishing the freeze and readiness evidence.
