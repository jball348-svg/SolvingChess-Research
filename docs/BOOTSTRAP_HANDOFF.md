# Bootstrap infrastructure handoff

**Document status:** accepted infrastructure handoff

**Bootstrap result:** PASS

**Frozen content commit/tag:**
`08faa1ffdf5cbb492d3fffab89d7bbf07cd177a7` / `bootstrap-v1.0.0`

**Completed at:** 2026-08-14T09:33:22Z

## Frozen seam

- Latest completed research programme: G13
- G13 core engineering: PASS
- G13 roadmap advance gate: HOLD
- Next sequential programme: G14
- G14 authorized after bootstrap: true
- G14 started: false
- Autonomous-loop readiness: READY
- Real autonomous loop running: false

The exact G10, G11 and G12 bundles are recovered at their frozen identities. Required
replays remain NOT_PERFORMED. Historical G11 HOLD and G13 roadmap HOLD are not rewritten
by byte recovery.

## Migration

- Original files inventoried: 129 occurrences, 124 unique contents, 59,994,517 bytes
- Original bytes preserved: all 129 occurrences match declared size and SHA-256 after
  relocation
- Normalized Markdown derivatives: 29, each bound to its DOCX and audit
- Conversion exceptions: all 29 are LOSS_AUDITED_WITH_LIMITATIONS; only recorded
  header/footer placement and character-run formatting simplification
- Artifact registry: SHA-256
  482199338b76d8c3e0a67f162cfb7324e0b7186508cfdc929651dd1f21cf476c;
  129 occurrences, 334 archive members, 192 outer checksum references and 152 internal
  checksum references; zero observed mismatches
- Recovered/missing artifacts: G10, G11 and G12 required bundles recovered exactly;
  63 G7-era checksum references remain expected-only because no bytes were supplied

See docs/MIGRATION_REPORT.md for exact paths, hashes and claim boundaries.

## Programme state and governance

- state/PROGRAM_STATE.json: routes G13 to authorized but not-started G14; frozen authority
  and registry paths/hashes are populated; bootstrap is COMPLETE and readiness is READY
- state/AUTONOMY_STATE.json: STOPPED, validation PASS, retry bound 2, no real research
  loop started, awaiting an explicit later start, and observed CLI/security identity
  recorded
- state/REFERENCE_REGISTRY.json: all three projects remain
  NON_AUTHORITATIVE_REFERENCE and bind immutable Git or snapshot identities
- Root AGENTS.md discovery: PASS using
  `codex.exe -C C:\Solving_Chess debug prompt-input
  'BOOTSTRAP_AGENTS_DISCOVERY_ONLY'`; the resolved prompt contained the complete root
  instructions and marker
- Strict sequential-transition rejection: covered by the orchestration test suite and
  fail-closed validators

## References

- Decision Coordinates is pinned at
  eadf71ef1d0562b18124959c63b4a8a2613c6c4c.
- Structural Invariants is identified by per-file manifest
  5b62101a73bfa85277f7246ee2b304921921828e2f0b1bb50d618d917512a1ca
  over base ade9f4e51ed3048e915386d82e0b53d28ed7e3ab. The deterministic
  local-private ZIP has SHA-256
  71ed9950df89c9d61e04c08895c28596c7c1964cb3615478008061b15bfc5be3.
  Licensing and durable private hosting constraints remain explicit.
- The public SolvingChess legacy repository is pinned at
  1861f4a8ea4978b1599a042809f9f7cd53345151.

All remain NON_AUTHORITATIVE_REFERENCE. The private tree and ZIP are ignored and must not
enter the main repository history.

## Autonomous infrastructure

- Observed Codex version: codex-cli 0.147.0-alpha.6.6
- Observed executable SHA-256:
  592958896cbffa154709618476fc9c9bf7fe73957e9a4fc12094c5051b6c69b3
- Preferred security profile: strict permission profile with workspace-only writes,
  protected governance/reference inputs read-only, public network controlled by
  auto-review and no local binding; Windows elevated sandbox
- Elevated output handoff: before launch the controller gives only its invoking SID an
  inheritable ACE on the isolated `.run/wt` worktree, so sandbox-created files remain
  controller-readable for independent validation and Git freezing. The SID is recorded in
  the durable ledger; no broad group access or silent privilege broadening is used
- Explicit legacy fallback: workspace-write, network enabled and approval policy never;
  fallback is opt-in and never silent
- Prompt generator: implemented with deterministic state routing and one-G scope
- Fresh-process controller: implemented; `codex exec resume` is forbidden
- Independent freeze validator: implemented with a separate API-admission output shape
  plus strict local schema, path, hash, transition, protected-scope, secret and
  ordinary-Git size checks
- Durable autonomy ledger/recovery: implemented under the common Git directory, with
  same-G bounded retry and resumable publication evidence
- Git freeze/tag transaction: controller-owned two-commit transaction; status-specific
  annotated tag on the content commit, tracked identity metadata in the following commit,
  and atomic push with remote verification

Intended later start command:

```powershell
python scripts/orchestration/autonomous_g_loop.py --start
```

Bootstrap must not execute that command. A later explicit outer-controller start may
launch authorized G14 only after readiness is READY and every preflight check passes.

## Tests

The final integrated suite passes all 60 tests, including the 28-test focused
governance/schema suite and the 20-test focused orchestration suite. The suite covers:

- PASS and exactly-one sequential advance;
- HOLD and BLOCKED scientific stops without retry;
- subprocess crash, malformed final JSON and malformed JSONL;
- claimed PASS missing its handoff;
- invalid/skipped transition and manifest identity mismatch;
- bounded same-G retry in fresh processes;
- inclusive maximum-G stop;
- accepted controller-evidence retention;
- annotated status tag, atomic push and remote verification;
- failed-push resume without rerunning Codex;
- bootstrap gate refusal and proof that dry-run/status do not invoke real G14;
- non-destructive retry recovery;
- migration invariants, deterministic conversion and deterministic private snapshot.

The benign real-CLI synthetic smoke passed at 2026-08-14T09:27:36Z using the preferred
permission profile and Windows elevated sandbox. It admitted the exact API output schema,
wrote and independently re-read the exact workspace marker, completed a public GET, and
returned exit status 0. The executable was `codex-cli 0.147.0-alpha.6.6` at SHA-256
`592958896cbffa154709618476fc9c9bf7fe73957e9a4fc12094c5051b6c69b3`.
The controller-SID handoff was limited to
`S-1-5-21-1472234835-2494744068-1158215870-1001`; the compact evidence record is
`logs/bootstrap/codex_cli_smoke.json`. The smoke was synthetic, did not use programme
routing and did not invoke the autonomous loop.

## Limitations and blockers

- Required original G10/G11 conformance replay is NOT_PERFORMED.
- Mandatory G12-through-G13 acceptance replay is NOT_PERFORMED.
- G15 is blocked by incomplete G14 and the open foundation replay exception.
- G17 is not unlocked.
- The structural reference snapshot has unresolved project-wide licensing and no durable
  private host.
- Private-remote publication and the metadata commit remain controller-owned publication
  operations. The content identity above is frozen and does not change the scientific or
  bootstrap result.

## Final acceptance declaration

```text
BOOTSTRAP = PASS
LATEST_COMPLETED_G = G13
NEXT_G = G14
NEXT_G_AUTHORIZED = true
NEXT_G_STARTED = false
AUTONOMOUS_ORCHESTRATOR = READY_AND_STOPPED
FREEZE_VALIDATOR = PASS
REFERENCE_CORPUS = MIGRATED_AND_AUDITED
REAL_G_LOOP = NOT_RUNNING
```

No infrastructure success is a new chess theorem.
