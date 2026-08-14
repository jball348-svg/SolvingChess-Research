# Solving Chess

Solving Chess is a repository-native continuation of a long-running exact symbolic-chess
research programme. Historical originals, normalized human documents, machine artifacts,
programme state, validation evidence and future G-programme work are kept separate so that
claims remain reproducible and provenance remains inspectable.

The repository has completed infrastructure bootstrap and is parked at the accepted
migration seam:

- latest completed research programme: G13;
- next sequential programme: G14 — Proof Store and Content-Addressed Dependency Graph;
- G14 post-bootstrap outer-controller authorization: true;
- G14 started: false;
- autonomous-loop readiness: READY;
- real autonomous loop: not running.

G13's distributed/checkpointed engineering architecture passed its own workload, but its
roadmap advance gate remains on HOLD. Exact G10, G11 and G12 bundles have now been
recovered at their expected SHA-256 identities; required inherited replays remain
NOT_PERFORMED. Byte recovery and integrity verification do not retrospectively rewrite
the historical HOLDs or establish new chess results.

## Authorities

Start with state/PROGRAM_STATE.json. It routes readers to:

1. the normalized permanent G9 roadmap;
2. the normalized frozen G13 technical handoff;
3. the active G10.RULES.v1.0 rules contract;
4. the active G12.STATE.SERIAL.v2 serialization contract; and
5. the repository research protocol.

Normalized Markdown is agent-facing. An inherited original remains the controlling byte
authority wherever conversion loses structure or the two differ.

## Operator interface

The intended autonomous start command, after bootstrap validation reports READY, is:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --start
~~~

Do not run that command unless state/PROGRAM_STATE.json reports autonomous-loop readiness
as READY. G14 authorization applies only to a later explicit outer-controller start after
bootstrap acceptance; bootstrap itself must not launch it. The loop must use one fresh
Codex process per G and validate each freeze before advancing.

Inspect state without starting research:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --status
~~~

Validate repository contracts:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --validate-only
~~~

Resume a previously accepted or safely recoverable orchestration attempt:

~~~powershell
python scripts/orchestration/autonomous_g_loop.py --resume
~~~

See docs/AUTONOMOUS_LOOP.md for stop, recovery and manual-override rules.

## Repository map

- state/ — routing state, artifact/reference registries, blockers and orchestration ledger.
- roadmap/ and handoffs/ — immutable originals plus normalized derivatives.
- legacy/ — other inherited originals and derivatives.
- research/ — new work, one directory per G.
- references/ — non-authoritative adjacent projects and retrieval metadata.
- artifacts/ — manifests, fixtures and explicitly governed immutable objects.
- scripts/ — migration, validation and orchestration entry points.
- schemas/ — machine contracts for state, registries, completions and freezes.
- docs/ — protocol, operator and migration documentation.
- logs/orchestration/ — durable run records under the documented retention policy.

No infrastructure document, placeholder directory or synthetic test is a chess theorem.
