# Reference projects

This directory indexes adjacent work that may inform later Solving Chess programmes.
Reference presence does not confer scientific authority.

Read references/REFERENCE_MAP.md for selective retrieval and
state/REFERENCE_REGISTRY.json for machine-readable identities, status and restrictions.

## Layout

- projects/decision-coordinates — pinned Git submodule.
- projects/solvingchess-public — pinned Git submodule.
- manifests/ — tracked immutable reference identities and snapshot inventories.
- local/structural-invariants-endgames — ignored private working copy.
- local-snapshots/structural-invariants-endgames.snapshot.zip — ignored local-private
  snapshot archive.

The local and local-snapshots directories must not enter main-repository Git. The complete
structural snapshot manifest remains tracked so future authorized runs can verify locally
available bytes without flattening them into the main history.

## Use

Consult the map, retrieve only materially relevant paths and record exact provenance in the
active G handoff. Independently verify any imported result to the proof standard of that G.

See docs/REFERENCE_POLICY.md for promotion, licensing and storage rules.
