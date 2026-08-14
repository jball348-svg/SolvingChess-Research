# Solving Chess — Agent Instructions

## Mission

This repository is a long-running exact research programme whose end condition is a
machine-checkable weak solution of chess under the declared frozen rules contract.

Scientific correctness, provenance and reproducibility outrank apparent progress.

## Start-of-run authority

Before research:

1. Read state/PROGRAM_STATE.json.
2. Read the permanent roadmap identified there.
3. Read the immediately preceding frozen technical handoff.
4. Read docs/RESEARCH_PROTOCOL.md.
5. Consult references/REFERENCE_MAP.md only to determine whether external reference
   work is relevant.
6. Read older historical or reference material only when a named dependency or current
   research question actually requires it.

Later frozen handoffs override roadmap assumptions only where they explicitly do so.

Never silently repair frozen history.

## Bootstrap seam

Infrastructure bootstrap is not a research programme. At the migration seam:

- G13 is the latest completed research programme.
- G13 core engineering passed, but its roadmap advance gate remains on HOLD.
- The exact G10, G11 and G12 bundle bytes have been recovered; the inherited mandatory
  replays remain NOT_PERFORMED where recorded in programme state.
- After bootstrap acceptance, G14 is the next sequentially authorized programme. It remains
  not started and may begin only through a later explicit outer-controller --start.
- Bootstrap work must not create G14 research, a G14 handoff, or a G14 scientific claim.

## One-G execution boundary

A normal autonomous research process executes exactly one new G programme.

Within that G, continue through all necessary substages until its legitimate
advance/stop condition is reached.

Do not start the following G.

The external orchestration layer launches a fresh Codex process for the next G.

## Claim discipline

Maintain explicit distinctions between:

- formally proved;
- exact finite computation;
- independently replayed;
- empirical;
- engineering validation;
- conditional;
- negative;
- superseded;
- failed;
- blocked;
- not claimed.

Never promote evidence through wording.

Synthetic engineering workloads are not chess truth.

Arena admissibility is not start reachability without required evidence.

## Frozen artifacts

Inherited originals are immutable.

Never rewrite, repack or reserialize a frozen artifact while retaining its old identity.

Use frozen identity and provenance contracts exactly.

Broken historical chains remain broken unless an explicitly versioned later authority
legitimately supersedes them.

## Research behaviour

Prefer falsifiable prospectively declared tests.

Freeze cohorts/benchmarks before outcome inspection when the claim depends upon them.

Actively seek counterexamples.

Preserve failures that affect interpretation.

Never outcome-shrink a benchmark merely to manufacture PASS.

If exact evidence contradicts the desired roadmap, preserve the contradiction.

## Verification

Producer success is insufficient where independent replay is practical.

Use structurally separate verifiers, hostile mutation, fresh-process replay and
deterministic reproduction where appropriate.

Investigate mismatches rather than averaging or suppressing them.

Never weaken a verifier merely to accept unexplained producer output.

## References

Projects under or indexed by references/ are normally NON_AUTHORITATIVE_REFERENCE.

Use them selectively.

Do not load an entire reference project merely because it exists.

When a referenced idea/result enters a Solving Chess proof or decision, record exact
provenance and verify it to the standard required by the active G.

## Code and tests

Keep deterministic operations scriptable.

Record build/test/replay commands.

Prefer machine-readable manifests over prose-only state.

Relevant unexplained failing tests prevent PASS.

## Repository state

state/PROGRAM_STATE.json routes work but does not replace frozen handoffs.

A research G closes only with its required handoff, manifest, hashes, validation and
state update.

Do not rewrite frozen Git history.

Do not commit credentials, secrets or incidental runtime caches.

## Large artifacts

Do not place arbitrarily large generated truth stores into ordinary Git history merely
because they exist.

Follow the currently frozen proof-store/CAS policy.

Preserve identities and provenance even where bulk bytes reside externally.

During bootstrap, artifacts/cas/ is only a migration-era placeholder. Its existence is
not a G14 proof-store design or result.

## Subagents

Use subagents when genuine independence or parallelism materially improves quality.

Good uses include:

- independent verifier;
- hostile review;
- repository archaeology;
- literature/reference triage;
- separate falsification campaigns;
- read-heavy exploration.

The primary agent owns integration and final claims.

Shared assumptions can defeat supposed independence.

## G closeout

Before declaring a G complete, produce all artifacts required by
docs/RESEARCH_PROTOCOL.md.

The final machine completion record must state PASS, HOLD, BLOCKED or FAILED.

Do not begin the next G yourself.

Return control to the external orchestrator.

## User interaction

Do not ask the user to perform reasoning available from the repository.

Human input should be required only where genuinely unavoidable, such as:

- credentials;
- destructive external actions;
- financial commitments;
- unavailable external artifacts;
- or unresolved governance/scientific choices with no frozen authority.

Otherwise proceed autonomously.
