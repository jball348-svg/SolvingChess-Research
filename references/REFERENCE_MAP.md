# Reference retrieval map

All entries default to NON_AUTHORITATIVE_REFERENCE. This map supports selective retrieval;
state/REFERENCE_REGISTRY.json carries the complete machine metadata.

## Decision Coordinates

- Locator: references/projects/decision-coordinates
- Remote: https://github.com/jball348-svg/chess.git
- Commit: eadf71ef1d0562b18124959c63b4a8a2613c6c4c
- Storage: pinned Git submodule
- Themes: PGN ingestion, deterministic legal-move ordering, decision coordinates, matched
  corpus analysis, semantic move classes
- Potential G relevance: G19, G23–G25, G35–G37
- Best entry points: README.md, AGENTS.md, pyproject.toml and
  data/derived/findings_baseline_vs_random.md
- Boundary: empirical corpus results and FEN-oriented representations are not frozen
  full-rule state truth or exact proof.

## Structural Invariants in Chess Endgames

- Private working locator: references/local/structural-invariants-endgames
- Private snapshot locator:
  references/local-snapshots/structural-invariants-endgames.snapshot.zip
- Remote base: https://github.com/jball348-svg/chess_research.git
- Base commit: ade9f4e51ed3048e915386d82e0b53d28ed7e3ab
- Snapshot identity:
  5b62101a73bfa85277f7246ee2b304921921828e2f0b1bb50d618d917512a1ca
- Tracked per-file manifest:
  references/manifests/structural-invariants-endgames.files.sha256
- Per-file manifest SHA-256:
  5b62101a73bfa85277f7246ee2b304921921828e2f0b1bb50d618d917512a1ca
- Local private ZIP SHA-256:
  71ed9950df89c9d61e04c08895c28596c7c1964cb3615478008061b15bfc5be3
- Storage: materialized local-private snapshot plus tracked per-file manifest; not a
  submodule; durable private hosting remains pending
- Themes: structural endgame theorems/counterexamples, Model C/F terminal semantics,
  controlled attractors, exact rank arrays, independent-verifier patterns
- Potential G relevance: G14, G15, G18–G21, G23–G26 and G30–G34
- Best entry points: README.md, final-assessment.md, task-02/README.md,
  task-02/final-assessment.md, task-03/README.md and task-03/final-assessment.md
- Boundary: Task 03 remains pending; Implementation A output lacks completed
  state-for-state Implementation B agreement. The project-root license is unresolved.

Future agents should open the private tree only if it is locally present and materially
relevant. Missing local bytes are a retrieval limitation, not permission to substitute
the almost-empty base commit.

## Public SolvingChess legacy repository

- Locator: references/projects/solvingchess-public
- Remote: https://github.com/jball348-svg/SolvingChess.git
- Commit: 1861f4a8ea4978b1599a042809f9f7cd53345151
- Storage: pinned Git submodule
- Themes: early Decision Coordinates, representation-space, symmetry-compression and
  mathematical-hypothesis experiments
- Potential G relevance: G19, G23–G25, G35 and G37
- Best entry points: README.md and the README/result files under experiments/
- Boundary: small exploratory legacy repository, not part of the Pilot/G1–G13 frozen
  authority chain.

## Import checklist

When a reference materially enters a G:

1. record project ID, commit/snapshot and exact paths;
2. state whether the import is an idea, implementation, empirical observation, exact
   computation or scientific claim;
3. compare its model with active G10/G12 contracts;
4. independently verify it as required;
5. record failures and non-overlap;
6. cite the governed import in the G handoff and freeze manifest.
