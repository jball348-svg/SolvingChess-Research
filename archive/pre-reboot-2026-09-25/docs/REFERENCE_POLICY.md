# Reference-project policy

Adjacent projects can supply algorithms, experiments, literature trails, negative results
and engineering patterns. Their presence does not place them in the Solving Chess authority
chain.

The default classification is:

NON_AUTHORITATIVE_REFERENCE

## Registration

Every reference entry records:

- stable project ID and name;
- local locator and/or remote URL;
- exact Git commit or snapshot-manifest identity;
- reproducible storage mechanism and current availability;
- broad purpose and approximate payload size;
- principal languages/file types and evidence classes;
- likely programme relevance;
- known overlap and non-overlap;
- provenance and licensing quality;
- bounded-triage date;
- explicit use restrictions.

The machine source is state/REFERENCE_REGISTRY.json. references/REFERENCE_MAP.md is its
human retrieval map.

## Bounded bootstrap triage

Bootstrap review is intentionally shallow. Prefer:

- README and AGENTS files;
- manifests and result summaries;
- project indices and directory structure;
- Git remote, commit and status;
- obvious language/package metadata.

Inspect deeper files only to classify provenance, claim status or storage needs. Bootstrap
must not perform a fresh scientific synthesis.

## Retrieval during a G

An active G agent:

1. reads references/REFERENCE_MAP.md;
2. identifies whether an indexed project is materially relevant;
3. retrieves only the necessary files;
4. records project ID, immutable pin and paths used;
5. distinguishes imported idea, empirical evidence, exact result and implementation;
6. verifies the imported material to the current G's proof standard;
7. records material use and verification in the handoff and freeze.

Do not dump entire adjacent projects into an agent prompt.

## Authority promotion

A reference claim becomes usable in a Solving Chess argument only through a governed
import. The import must bind exact bytes, state the claim and model, document compatibility
with active rules/contracts and supply the verification required by the current gate.

Promotion is claim-specific. It does not make every statement in the source project
authoritative.

## Storage mechanisms

Use the least duplicative reproducible mechanism:

- clean hosted Git repository: pinned external repository or submodule;
- dirty/unhosted repository: per-file immutable snapshot manifest plus private durable
  snapshot;
- non-repository material: content manifest and governed snapshot;
- large regenerable outputs: recipe and identity where sufficient, or explicit external
  object storage if bytes are required.

Never flatten a project with valuable distinct history into the main research corpus.

Tracked manifests stay under references/manifests. Working copies and private snapshots
stay in ignored references/local or references/local-snapshots.

## Registered storage decisions

### Decision Coordinates

Pin:

eadf71ef1d0562b18124959c63b4a8a2613c6c4c

The commit is clean, remotely reproducible and pinned as the submodule
references/projects/decision-coordinates. Do not copy its ignored 311 MB SQLite database
or caches.

### Structural Invariants in Chess Endgames

Remote base:

ade9f4e51ed3048e915386d82e0b53d28ed7e3ab

Supplied snapshot identity:

5b62101a73bfa85277f7246ee2b304921921828e2f0b1bb50d618d917512a1ca

The base remote tracks only .gitattributes and is not the project identity. The supplied
tree is located privately at references/local/structural-invariants-endgames. Its
deterministic local archive is
references/local-snapshots/structural-invariants-endgames.snapshot.zip and is bound by the
tracked per-file manifest. The snapshot must remain private until durable private hosting
and project-wide redistribution rights are resolved. Do not make it a submodule yet.
Preserve its pending Task 03 status.

### Public SolvingChess legacy repository

Pin:

1861f4a8ea4978b1599a042809f9f7cd53345151

This small remote is reproducible and pinned as the submodule
references/projects/solvingchess-public, but remains an adjacent legacy experiment
repository, not a frozen Pilot/G authority.

## Licensing and secrets

Unresolved licensing prevents copying code or publicly hosting a snapshot; it does not
prevent recording a private locator and content identity.

Never place credentials, tokens or private repository access material in reference
metadata.
