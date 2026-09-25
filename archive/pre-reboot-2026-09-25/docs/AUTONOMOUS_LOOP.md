# Autonomous G-loop operator guide

The outer controller advances the repository through sequential research programmes using
one fresh non-interactive Codex process per G. The G agent owns exactly one programme; the
controller owns sequencing, independent validation, retries, durable logging and Git
freezing.

Bootstrap dry runs use synthetic fixtures. They must never invoke real G14.

## Safety preconditions

Before any live start, all of the following must be true:

- state/PROGRAM_STATE.json validates;
- state/AUTONOMY_STATE.json validates;
- repository bootstrap status is COMPLETE;
- autonomous-loop readiness is READY;
- the next programme is exactly one greater than the latest completed programme;
- sequential permission and launch authorization are true;
- next-programme started is false;
- no contradictory Git or programme state exists;
- configured Codex version, sandbox, approval and network policy are recorded;
- the live command is not using a mock executable.

The controller must print those resolved settings before launching Codex. It must not
silently fall back to unrestricted host access.

At the accepted bootstrap seam, readiness is READY and G14 is authorized only for a later
explicit outer-controller start. G14 remains NOT_STARTED and no real research loop is
running. Any state that has not completed bootstrap acceptance must remain NOT_READY and
the controller must refuse a live start.

The preferred Windows security mode combines the strict workspace permission profile,
auto-reviewed public network access and the elevated sandbox backend required for
path-level read restrictions. Before launching Codex, the controller adds one inheritable
ACE for the invoking controller SID to the isolated `.run/wt` worktree. This preserves
controller access to sandbox-created outputs for independent validation and Git freezing;
it does not grant a broad group, relax the permission profile or authorize silent
privilege fallback. The resolved SID and Windows sandbox mode are retained in the durable
controller ledger. The legacy workspace-write mode remains an explicit opt-in only.

## Commands

Start a later authorized live loop:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --start
~~~

Inspect durable state without launching Codex:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --status
~~~

Validate state and the current freeze without running research:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --validate-only
~~~

Exercise prompt generation and sequencing without invoking real research:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --dry-run
~~~

Resume after a host or process interruption:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --resume
~~~

Bound a future run:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --start --until G20 --max-programmes 5 --max-retries 2
~~~

Exact supported arguments are authoritative in the checked-in command help. If this guide
and command help differ, stop and resolve the documentation mismatch before a live run.

## Fresh-context guarantee

For every normal successor:

~~~text
validated frozen G[N]
  -> generate deterministic G[N+1] prompt
  -> launch fresh codex exec process
  -> validate G[N+1]
~~~

The controller categorically forbids codex exec resume. Successors, same-G infrastructure
retries and recovery attempts always launch a fresh codex exec process. The controller's
own --resume option resumes durable orchestration state; it never resumes a Codex
conversation.

## Run records

Each attempt has a durable directory:

~~~text
logs/orchestration/GNN/<run-id>/
  prompt.md
  events.jsonl
  final.json
  stderr.log
  validation.json
  metadata.json
~~~

Store the exact prompt, prompt hash, Codex version/configuration, starting commit, process
attempt, timestamps and exit status. Large raw event/stderr streams may be ignored by Git
under the retention policy, but accepted validation and critical freeze evidence must be
retained.

## Completion handling

The final Codex message is first admitted by the API-compatible shape in
schemas/g_completion.output.schema.json. The controller then validates it against the
strict local schemas/g_completion.schema.json and repository evidence. The admission
schema is intentionally not semantic authority; every response remains untrusted until
strict repository validation succeeds.

The agent's freeze manifest carries a planned status tag but null actual commit/tag
identities. The controller creates those identities only after acceptance. It tags the
validated content commit, then creates a separate metadata commit recording that content
commit/tag in PROGRAM_STATE, AUTONOMY_STATE, its durable ledger and validation evidence.
The canonical branch ends at the metadata commit; the status tag remains on the content
commit. This avoids self-reference and preserves the no-agent-Git-writes boundary.

- Validated PASS: content commit/tag, metadata commit, atomic publish, then evaluate
  successor permission.
- Validated HOLD: content commit/status tag, metadata commit, atomic publish, then stop.
- Validated BLOCKED: content commit/status tag, metadata commit, atomic publish, then stop.
- Validated FAILED: content commit/status tag, metadata commit, atomic publish, then stop.
- Malformed JSON, missing handoff, invalid transition or failed hashes: reject the result;
  this is an orchestration failure, not PASS/HOLD/BLOCKED.

## Crash and retry

On a subprocess crash:

1. close and preserve the attempt log;
2. inspect Git and programme state;
3. reject any unvalidated partial freeze;
4. retry the same G in a fresh process only when safe;
5. increment the durable attempt and retry counters;
6. stop when the configured retry bound is reached.

Never retry a validated scientific PASS, HOLD, BLOCKED or FAILED as infrastructure
recovery. Never launch the successor after an invalid claimed PASS.

If the validated content commit or status tag already exists but the metadata commit or
remote publication fails, `--resume` must continue that same Git transaction. It verifies
the recorded content tree/tag, finishes the metadata commit and push, and never reruns
Codex for an already accepted scientific result.

## Stop conditions

The loop stops on:

- validated HOLD or BLOCKED;
- failed or unverifiable freeze;
- inconsistent repository state;
- unavailable dependency that forbids the successor;
- exact contradiction requiring roadmap/governance action;
- credentials, destructive external action or financial commitment;
- successor authorization false;
- configured programme/runtime/budget bound;
- explicit project end;
- operator stop.

Stopping is safe when no child Codex process is running and state/AUTONOMY_STATE.json has
been atomically updated with the stop reason. Terminate the controller gracefully where
possible; after forced termination, use --status and --resume rather than --start.

## Manual override

A human override must be explicit and auditable:

1. stop the controller;
2. preserve the active attempt directory;
3. record why intervention is necessary;
4. make no claim-changing edit without frozen authority;
5. run validation;
6. commit the intervention separately from a scientific freeze;
7. resume only if programme and Git state are consistent.

Never edit a prior frozen manifest, commit or tag to make a new result appear historically
valid.

## Current recovered G12 bytes

The exact G12 bundle bytes are recovered, but the mandatory G13 replay is
NOT_PERFORMED. The autonomous loop must not infer that a matching file hash closes that
gate. A later authorized procedure must run and validate the inherited campaign before the
blocker can change.
