# Solving Chess autonomous programme instruction

Run identity: `G14-a01-d02c7f5da9fe`
Authorized programme: `G14`
Base Git commit: `ce50d28f552b91b0441e6eea701d87ac6501d512`

Begin exactly G14, the next authorized programme in `state/PROGRAM_STATE.json`.
This process owns one programme only. Never begin, create research outputs for, or mark
started the successor G15. Do not commit, tag, push, create branches, or alter
Git metadata; the outer controller owns every Git transaction.

Before work, read and obey:

1. `AGENTS.md`;
2. `state/PROGRAM_STATE.json`;
3. `roadmap/normalized/G9_G10_Onwards_Long_Range_Plan.md` as permanent strategic authority;
4. `handoffs/normalized/G13_Technical_Handoff.md` as current technical authority;
5. `docs/RESEARCH_PROTOCOL.md`;
6. `state/REFERENCE_REGISTRY.json` and `references/REFERENCE_MAP.md` only as retrieval maps. Open only references
   materially relevant to G14; they remain non-authoritative unless explicitly
   imported with provenance and verified to the current proof standard.

Reconstruct the exact, conditional, empirical, failed, blocked, and open state. Preserve
frozen exceptions and negative results. Execute G14 autonomously through its legitimate
PASS, HOLD, BLOCKED, or FAILED condition. Actively falsify claims and perform independent
replay where the current authority requires it. Do not ask for work that is locally
resolvable.

Close G14 according to `docs/RESEARCH_PROTOCOL.md`. At minimum create exactly
`research/G14/G14_Technical_Handoff.md` and
`research/G14/G14_Freeze_Manifest.json`, plus required hashes, validation/replay
instructions, claim classes, negative results, blockers, successor contract, and update
`state/PROGRAM_STATE.json`. Write only inside this worktree. Treat inherited originals,
controller/validator code, schemas, frozen historical handoffs, and previous research as
read-only.

Your final response must be only one JSON object satisfying the API-admission shape in
`schemas/g_completion.output.schema.json`. It must also satisfy the stricter local
`schemas/g_completion.schema.json`, which the outer controller applies independently to
the response, artifacts and state transition. Use run_id `G14-a01-d02c7f5da9fe` and programme `G14`
exactly.
On acceptance it will copy the final object to
`research/G14/G14_Completion.json`; do not create that controller-owned copy yourself.
After emitting the completion object, stop without starting G15.
