# Historical archive and reading guide

The old programme is preserved in
[`pre-reboot-2026-09-25/`](pre-reboot-2026-09-25/). Every previously tracked entry
is retained at the same relative path with the same Git object and mode: 342
files and two pinned reference-submodule entries. External submodule contents and
untracked/private snapshots were not part of the original tracked tree.

- Original commit: `3eba1a0c60e8ffca63a85763d176e1da9f904141`.
- Original root tree: `7d1ffdf10ce7bab07b381c174712f47f67e7428a`.
- The archived subtree has that same tree identity.
- Readable original layout: [source commit](https://github.com/jball348-svg/SolvingChess-Research/tree/3eba1a0c60e8ffca63a85763d176e1da9f904141).
- Historical outcome: **STOP_CURRENT_METHOD**, preserved unchanged.
- Reboot rationale: [post-mortem of 24 September](POST_MORTEM_2026-09-24.md).

The post-mortem is a later assessment, stored beside the exact snapshot. It is
not an edit of the old evidence. Its late-review numbers are reported results;
its G12 verifier replay was a separate check with explicitly limited independence.

## Read selectively

| Need | Reference | Why it matters / limitation |
|---|---|---|
| Original stepping-stone premise | [Pilot 2 handoff](pre-reboot-2026-09-25/handoffs/normalized/Pilot_2_K2P_vs_K_Technical_Handoff.md) | Strong restricted composition; fragmented residual and omitted history. |
| Mathematical composition operators | [G6 handoff](pre-reboot-2026-09-25/handoffs/normalized/G6_Final_Technical_Handoff.md), [G6 bundle](pre-reboot-2026-09-25/legacy/originals/G6_Final_Closeout_Bundle.zip) | Branch/Hyperkernel, guarded restoration, actual code and named historical exceptions. |
| Efficient exact representations | [G8 handoff](pre-reboot-2026-09-25/handoffs/normalized/G8_Certificate_Engine_and_Reascent_Final_Technical_Handoff.md), [G8 bundle](pre-reboot-2026-09-25/legacy/originals/G8_Final_Closeout_Bundle.tar.gz) | Large restricted solves; inspect internal bundles and preserve original semantics. |
| Full-rule contract and replayable anchor | [G10 handoff](pre-reboot-2026-09-25/handoffs/normalized/G10_Technical_Handoff.md), [G12 handoff](pre-reboot-2026-09-25/handoffs/normalized/G12_Technical_Handoff.md), [G12 bundle](pre-reboot-2026-09-25/legacy/originals/G12_Final_Rules_Reference_Bundle.zip) | Source, verifier and small endgame certificates; clean-history guards limit reuse. |
| Earlier scaling evidence | [R1 reconstruction](pre-reboot-2026-09-25/REVIEW/R1_ASCENT_EVIDENCE_RECONSTRUCTION.md), [R1 results](pre-reboot-2026-09-25/REVIEW/R1_SCALING_RESULTS.md) | Separates engineering gains from proof/discovery gains. |
| Prospective discovery and its real cost | [R2 target](pre-reboot-2026-09-25/REVIEW/R2_TARGET_DISCOVERY_RESULTS.md), [strategy](pre-reboot-2026-09-25/REVIEW/R2_STRATEGY_DISCOVERY_RESULTS.md), [cost audit](pre-reboot-2026-09-25/REVIEW/R2_DISCOVERY_COST_AUDIT.md) | Useful rules; heavy lower-truth dependencies and near-solve acquisition cost. |
| Why branch reduction was insufficient | [R3 closure](pre-reboot-2026-09-25/REVIEW/R3_ALL_REPLY_CLOSURE_RESULTS.md) | All-reply prefix with an unresolved frontier; no certified White non-loss choices. |
| Limits of the final bridge tests | [R4 targets](pre-reboot-2026-09-25/REVIEW/R4_TYPED_TARGET_RESULTS.md), [R5 exactness](pre-reboot-2026-09-25/REVIEW/R5_TARGET_EXACTNESS_RESULTS.md), [R5 economics](pre-reboot-2026-09-25/REVIEW/R5_CERTIFICATION_ECONOMICS.md) | Material-distance obstruction and a sparse four-ply repetition target; neither tests every bridge. |
| What the old stop meant | [R6 verdict check](pre-reboot-2026-09-25/REVIEW/R6_ADVERSARIAL_VERDICT_CHECK.md), [surviving assets](pre-reboot-2026-09-25/REVIEW/R6_SURVIVING_ASSETS.md) | Stops that method; preserves restricted positives and avoids an impossibility claim. |
| External/reference projects | [Reference map](pre-reboot-2026-09-25/references/REFERENCE_MAP.md) | Exact pins and availability limits; these projects are optional references. |

## Known availability and interpretation limits

The post-mortem found no matching checked-in or bundled source for the R2, R4
and R5 audit programs named by their provenance hashes. Those documents support
historical analysis but are not executable dependencies by themselves. Recover
bytes or make a clearly new implementation if needed. G6 also records a G4
reconstruction discrepancy and a G5 rank-label exception; do not silently repair
the record to make old totals match.

Archived READMEs and state files can disagree about what was current at different
historical stages. That is part of the preserved record. They do not route the new
pilot. Archived AGENTS.md files and autonomous-loop commands are inert reference
material for the new project.

Relative links inside the snapshot remain in their old layout. Commands that
assume the old repository root should run in a separate historical worktree or
an explicitly extracted working copy, never by writing into this archive. For an
unmodified old layout:

```sh
git worktree add ../SolvingChess-Research-history 3eba1a0c60e8ffca63a85763d176e1da9f904141
```

The new root `.gitmodules` maps the two unchanged reference commits to their
archived paths. Initialize them only when a named dependency requires them.

To compare the exact snapshot identity with the old root:

```sh
git rev-parse 3eba1a0c60e8ffca63a85763d176e1da9f904141^{tree}
git rev-parse HEAD:archive/pre-reboot-2026-09-25
```

These IDs should match. The reorganization changes location and active guidance;
the complete old tree and Git history remain recoverable.
