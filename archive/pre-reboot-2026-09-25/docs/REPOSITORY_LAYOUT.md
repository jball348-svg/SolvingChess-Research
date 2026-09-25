# Repository layout

The layout separates immutable inherited bytes, agent-facing derivatives, new research,
runtime state and non-authoritative references.

~~~text
/
  AGENTS.md
  README.md

  state/
    PROGRAM_STATE.json
    ARTIFACT_REGISTRY.json
    REFERENCE_REGISTRY.json
    AUTONOMY_STATE.json
    OPEN_BLOCKERS.md

  roadmap/
    originals/
    normalized/

  handoffs/
    originals/
    normalized/

  legacy/
    originals/
    normalized/

  research/
    G14/
    G15/
    ...

  references/
    README.md
    REFERENCE_MAP.md
    manifests/
    local/                  # ignored working copies
    local-snapshots/        # ignored private snapshots

  schemas/
  scripts/
    migration/
    bootstrap/
    orchestration/
    validation/

  artifacts/
    manifests/
    fixtures/
    bundles/
    cas/

  logs/
    orchestration/

  docs/
  staging/
~~~

schemas/g_completion.output.schema.json is the API-compatible response-admission shape.
schemas/g_completion.schema.json is the stricter local semantic/transition contract. The
outer validator must apply both; API admission alone cannot authorize a programme result.

## Immutable originals

roadmap/originals, handoffs/originals and legacy/originals contain inherited bytes. Files
are classified by role, not converted in place:

- the long-range strategic roadmap goes under roadmap/originals;
- technical handoffs go under handoffs/originals;
- other primary inputs, bundles, checksums, sources and evidence go under
  legacy/originals.

Original bytes never change for presentation. Duplicate source occurrences may remain
separately registered even when their content hashes agree.

The recovered exact G12 reference bundle has the canonical migration path:

legacy/originals/G12_Final_Rules_Reference_Bundle.zip

It must not be duplicated under artifacts/bundles merely for symmetry.

## Normalized derivatives

Agent-facing Markdown derivatives live in the corresponding normalized directory and bind
their source filename and SHA-256. They are derivatives, not replacements for original
authority. JSON, source code, archives and binary certificates stay in their native format.

If conversion loses a table, identifier, status word or other meaningful structure, record
the loss and treat the original as controlling.

## State

state/PROGRAM_STATE.json is the routing object. It must remain compact and point to frozen
authorities rather than restating their full content.

state/ARTIFACT_REGISTRY.json inventories inherited and repository artifacts by content and
occurrence. state/REFERENCE_REGISTRY.json indexes adjacent work without importing its
authority. state/AUTONOMY_STATE.json is the tracked orchestration-state projection; the
controller's transaction ledger under the common Git directory remains the runtime
recovery authority.

Every state file validates against its named schema. State changes associated with a G are
part of that G's validated freeze transaction.

The status tag identifies the validated content commit. A following controller metadata
commit records that content commit/tag in PROGRAM_STATE and AUTONOMY_STATE, so neither
commit is required to contain its own hash.

## New research

All post-bootstrap scientific work is isolated under research/GNN. A placeholder README
may describe authorization and NOT_STARTED state. The first substantive file for a G may
be created only by its authorized one-G run.

No programme may write into its successor directory.

## Artifacts

artifacts/manifests and artifacts/fixtures contain checked-in validation material.
artifacts/bundles contains only deliberately governed new bundles, not duplicate migrated
originals.

artifacts/cas is a migration-era placeholder until G14 defines and freezes the proof-store
policy. Directory names must not be interpreted as completed research.

Large generated truth stores are not committed to ordinary Git by default. They require
registration, immutable identity, explicit retention and an approved storage mechanism.

## References

Reference metadata and small reproducibility manifests are tracked. Working copies and
private snapshots under references/local and references/local-snapshots are ignored. The
former flat Other projects staging directory was removed after its contents were either
pinned as submodules or preserved by the governed private-snapshot policy.

An indexed reference remains NON_AUTHORITATIVE_REFERENCE until a governed import records
exact provenance and verification.

## Runtime logs

Each Codex attempt has a unique logs/orchestration/GNN/run-id directory. Raw event and
stderr streams may be ignored under the retention policy; accepted validation, completion
and critical freeze evidence are retained.

The .run directory is reserved for short-lived controller coordination and is never
authority.
