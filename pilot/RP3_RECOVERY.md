# RP3-MR1: authorized measurement-recovery comparison

Frozen before replacement outcomes, 2026-09-25. This appendix does not amend the
RP1 source manifest or convert the original blocked experiment into a completed
experiment. The user explicitly authorized this bounded comparison and publication
to main. No RP4/RP5 or held-out cohort is authorized here.

## Preserved record and bounded copy search

Local commit `d1f75fff5a28c92921f889fa4ca87d566fba467d` survives. Its exact tree,
`ce7927d46f16bc8aa52b633e2305621cb69f254c`, was published as
`6c37c4765d204362d16a2647625521e0fc6f740d` by a normal fast-forward from
`35d409bf67198340446bd7021c95e8c1dc1f5cfc` before new measurements. The GitHub
commit identity differs because publication used the authenticated app; the local
commit and its parent remain preserved locally. All 565 archive members, all
frozen source/evidence hashes, 64 distinct roots, 16 added proof objects, 50 added
cache witnesses and 12 application witnesses were verified without new search.

The bounded search covered surviving scratch/tmp evidence paths, the raw archive,
all local refs/path history and unreachable commits, and saved-file title/content
searches for RP3 evidence. The remote still held the source freeze; its prepared
blocked tree has the same incomplete bytes. No authentic complete replacement was
located. Search details and hashes are in `evidence/rp3-recovery/copy-search.json`.

The original F repeat 3 R2 report has 14/16 rows; rows `70417dcad8bb70aa` and
`8e37219ffa244d50`, final search counters and the application-event tail remain
unavailable. Its complete timing envelope, process-wide WORK/check totals and all
16 certificates remain original evidence. They do not recover missing search
counters or per-query costs. The separate original R2 G acquisition report was
reconstructed from surviving original records; its missing phase/table details
remain unavailable. Neither record is overwritten or filled from other repeats.

## Persistence changes and unchanged experiment

The cause of the original storage loss is undetermined. The old writer directly
truncated reports, flushed events without fsync, and accepted process exit without
checking row/counter/event completeness. New adapters use atomic temporary-file
write + file fsync + replace + directory fsync for JSON, an append-only fsynced
query-row journal, event fsync every 32 events and at query/final checkpoints, and
a final digest manifest. Both child and parent validate row order/count, counters,
phase presence, certificate identities, event counts and the completion manifest.
The process envelope is durably written too. Any incomplete record stops progress;
there is no selective retry. Fault controls use synthetic data and a known RP1
fixture only. Full original source bytes remain unchanged; only persistence is
wrapped. All new I/O/check overhead stays inside the new envelopes.

Solver/checker semantics, six-ply proposition, generators, queries, candidate
ordering/admission, training procedure, cache policies, budgets, library limits,
three-repetition policy, rotations and decision margins are unchanged. Same pinned
Python/chess code; a changed executable path, session/host-load uncertainty and new
durability overhead limit cross-session timing comparability. No normalization or
timing correction will be applied. Human/LLM/shell/publication costs are unavailable,
not zero. No new package installation is required.

## Fixed schedule

1. Retain RP2's R1 prefix exactly. Retain every original R1/R2 acquisition and
   freeze the checked, repeat-identical R2-trained libraries before R3 exposure.
2. Replace the entire R2 measurement block: B/C/F/G, three serial fresh-process
   repeats, orders BCFG / CFGB / FGBC. F loads its original eight donor objects;
   G loads the sixteen-object R1-trained library; C loads its R1-trained cache.
   The R2 query cohort was previously inspected. This is not unseen transfer.
3. R3 primary evaluation: the same three rotations; G has 24 objects. Then three
   donor-only G ablations, then three rotating B/C/F/G reverse-query-order runs.
4. R3 training for C/G in orders CG / CG / GC; freeze repeat-identical libraries.
5. R4 primary evaluation and the same ablation/reverse controls. Stop. No R4
   acquisition, counterplay/history generation, anchor search or later stage.

New data go exclusively under `evidence/rp3-recovery/`. There are 72 new processes:
12 R2 replacements, 27 R3 evaluations/controls, six R3 acquisitions, and 27 R4
evaluations/controls. Reconciliation never calls a reserved generator or solver.
Existing validated directories may be skipped on operational resume; missing or
incomplete records are not rerun. All original and new expenses count against
the four-CPU-hour RP3 budget; the original per-run limits remain unchanged.

## Frozen accounting and gates

Pair repeat i with original RP2 repeat i. Let A(k,i) be the amended modeled
first-use cost: donor acquisition + unchanged R1 evaluation + each update first
usable by k + replacement R2 evaluation + new primary evaluations through k.
R1/R2 training is charged first at R2/R3, and R3 training first at R4. Each modeled
use pays one acquisition, not three; actual spending sums all measured repetitions.
No original candidate failure, duplicate, cap rejection or unused acquisition is
refunded. Shared query generation already appears once within each arm's process
envelope, not once per lookup. Nested application/check/search phases are never
added on top of their enclosing cost.

Report these separate views for every prefix:

- A: amended modeled comparison given the installed environment; raw evaluation,
  acquisition, CPU/wall median and range, total/query, coverage, work and storage.
- A + original shared setup once: the setup-inclusive modeled comparison.
- R: recovery-inclusive attributable model, A plus the original R2 evaluation
  envelope for the same arm/repeat at every prefix from R2 onward. This retains
  all replaced effort without pretending both blocks answered new queries.
- R + shared expense once: add original setup, original measured common
  preflights/reconciliations, and measured MR1 preparation/orchestration/audit
  expense once. The whole recovery overhead is a conservative shared surcharge
  from R2 onward, even when its final audit occurs later. R1 remains unchanged.
- Actual expense: sum every original/new process, all repetitions, all controls,
  original setup and measured audits/preflights/orchestration exactly once. Show
  controls separately; their acquisition is already actually paid. An ablated
  modeled G retains all G acquisition expense even though it loads only donors.

Missing original counters stay null/unavailable in R. New counters describe the
replacement runs only. Report known work and lower bounds separately from complete
totals. In particular, F repeat 3 recovery-inclusive expansions are unavailable.
Actual expense is not a median or a sum of medians. Unmetered activity stays labelled.

Apply the unchanged cumulative gates at both R3 and R4: matched 16/16 per rung;
at least 25% lower median cumulative CPU AND wall cost versus the best B/C/F;
at least 50 ms absolute saving in each; slowest G repeat faster than fastest
comparator repeat in each; and at least 25% fewer acquisition-inclusive fresh
fallback expansions. Also disclose evaluation-only expansions and all generated
edge/checking work. Apply each metric against its best comparator, a conservative
interpretation if their rankings differ. Report each gate, even after failure.

For ablation, substitute donor-only G evaluation at R3/R4 while retaining every
G acquisition and preceding prefix (R4 includes the R3 ablation). At least half
of any positive primary cumulative saving must disappear; absent a positive
saving the causal-benefit gate cannot pass. Report rung-local effects too. For
reverse order substitute reversed R3/R4 evaluations, retain R1/R2 and acquisitions,
and report cumulative and rung-local comparisons. A claimed primary advantage
must not reverse. No primary positive advantage means order support is unestablished,
not a pass by vacuity. Report all ratios even when gates fail.

Apply economic gates to A and R; also show their setup/common-expense-inclusive
versions. A positive conclusion requires surviving recovery-inclusive accounting
and adequate complete work evidence. If gates fail, report no demonstrated
cumulative benefit without changing the method. Distinguish raw one-off savings,
fixed-library benefit and cumulative benefit. No asymptotic or full-chess claim,
and no RP5 final decision, follows from RP3-MR1.
