# Repository-native research protocol

This document converts the prior session/handoff practice into a deterministic repository
state machine. It governs research runs after bootstrap; it does not authorize one.

The permanent roadmap and the immediately preceding frozen handoff remain the scientific
authorities. state/PROGRAM_STATE.json routes work to them but cannot replace or silently
reinterpret them.

## State machine

The normal lifecycle is:

~~~text
FROZEN G[N-1]
  -> authorized START for exactly G[N]
  -> EXECUTE G[N]
  -> CLOSE candidate
  -> deterministic validation
  -> accepted Git commit and status-specific immutable tag
  -> fresh process may start G[N+1]
~~~

Any HOLD, BLOCKED, FAILED, inconsistent state or rejected freeze stops the successor
transition. Programme transitions are strictly sequential. A completion or freeze that
claims G[N] -> G[N+2] is invalid even if its other artifacts look plausible.

## START

Before changing research state, the one-G agent must:

1. Validate all machine-readable state against the checked-in schemas.
2. Confirm the worktree and last frozen Git identity satisfy the orchestrator's starting
   policy.
3. Resolve exactly the next programme from state/PROGRAM_STATE.json.
4. Confirm sequential permission, explicit launch authorization and started state.
5. Read AGENTS.md.
6. Read the permanent roadmap named by programme state.
7. Read the immediately preceding frozen technical handoff.
8. Read every active rules, state, proof/certificate and compute contract named by state.
9. Read state/OPEN_BLOCKERS.md and reconstruct all exact, conditional, empirical, failed,
   negative and open state.
10. Consult references/REFERENCE_MAP.md only to decide which indexed references are
    materially relevant. Do not bulk-load reference projects.
11. Allocate a unique run ID and durable run directory.
12. Record the exact generated prompt and prompt SHA-256.
13. Declare only the resolved current programme.

The agent must stop before research if authorization is false, state is contradictory,
the predecessor is not frozen as required, or the resolved programme is not exactly the
successor encoded by the strict transition contract.

## EXECUTE

Within the one authorized programme, the agent must:

- perform all legitimate substages needed to reach the programme's advance or stop
  condition;
- obey the frozen rules and state identity contracts;
- preserve exact versus empirical and engineering distinctions;
- preserve negative results, failed attacks and contradictions that affect interpretation;
- prospectively freeze cohorts, benchmarks and acceptance criteria where required;
- seek counterexamples and hostile mutations;
- use structurally separate production and verification paths where practical;
- record commands, versions, inputs, outputs, hashes, resource bounds and deviations;
- import reference ideas only with exact provenance and the active programme's required
  independent verification;
- avoid outcome-driven shrinking or weakening of a verifier;
- avoid beginning, scaffolding scientific work for, or claiming progress in the successor.

An exact finite computation may support an EXACT claim only for its declared domain and
only when the computation and verification contract justify that classification. A
synthetic engineering workload remains ENGINEERING_TEST. Neither becomes chess truth by
wording.

## Claim classes

Every material claim in a freeze manifest and handoff must use one of:

- EXACT
- FORMALLY_PROVED
- INDEPENDENTLY_REPLAYED
- EMPIRICAL
- ENGINEERING_TEST
- CONDITIONAL
- SUPERSEDED
- FAILED
- BLOCKED
- NOT_CLAIMED

The handoff must explain domain, assumptions, evidence and remaining gaps. Machine labels
do not replace that explanation.

## CLOSE

A programme close candidate must include, at minimum:

- research/GNN/GNN_Technical_Handoff.md;
- research/GNN/GNN_Freeze_Manifest.json;
- all required exact artifacts and hashes;
- deterministic validation and replay instructions;
- explicit claim classes and domains;
- negative results and retained counterexamples;
- blockers and held gates;
- roadmap implications;
- an explicit successor contract;
- an updated state/PROGRAM_STATE.json;
- a final object admitted by schemas/g_completion.output.schema.json and independently
  conforming to the stricter schemas/g_completion.schema.json.

The API-admission schema uses only the output-schema subset accepted by Codex and checks
the response shape. It is not a transition authority. The outer validator must apply
schemas/g_completion.schema.json to enforce the programme/predecessor relation, scientific
status consistency, exact successor/stop routing and closeout fields.

The freeze manifest must conform to schemas/freeze_manifest.schema.json. It must bind the
roadmap, predecessor handoff and active contracts by immutable identity; inventory every
frozen output; and encode the exact sequential transition.

The agent-authored manifest records only the planned status tag: gNN-frozen for PASS, or
gNN-hold, gNN-blocked or gNN-failed for the corresponding non-PASS result. Its actual Git
commit and tag fields are null because those identities cannot be embedded in the content
they identify. After accepting the immutable manifest, the outer controller creates a
tagged content commit and then a separate metadata commit. The metadata commit records the
content commit/tag in PROGRAM_STATE and AUTONOMY_STATE; the canonical branch ends at that
metadata commit while the status tag continues to identify the immutable content commit.
The agent does not write Git metadata.

The G agent then exits. It does not commit/tag on its own unless the frozen orchestration
policy explicitly delegates that transaction, and it never begins the next G.

## Independent repository validation

Before accepting a close, the outer controller validates mechanically:

1. expected programme and predecessor;
2. strict one-step transition;
3. required handoff and freeze manifest existence;
4. JSON/schema validity;
5. recorded path containment and artifact existence;
6. sizes and SHA-256 identities;
7. programme-state consistency;
8. successor authorization state;
9. declared test command results;
10. absence of successor research outputs;
11. unresolved contradictions or missing claimed-PASS evidence;
12. acceptable Git diff scope.

The validator enforces repository transaction rules. It does not replace scientific peer
verification.

An agent-reported PASS is rejected if repository validation fails. Rejection is not a
scientific result.

## Git freeze

After mechanical repository validation PASS, the orchestrator owns the deterministic
transaction for any legitimate scientific terminal result: PASS, HOLD, BLOCKED or FAILED.
The scientific gate result remains distinct from validator success.

1. stage only validated programme outputs, accepted evidence and state changes;
2. create and verify one intentional content commit;
3. create the immutable status tag on that content commit: gNN-frozen for PASS, or
   gNN-hold, gNN-blocked or gNN-failed for the corresponding non-PASS result;
4. update PROGRAM_STATE.last_frozen_git and
   AUTONOMY_STATE.last_accepted_freeze with the content commit/tag;
5. create a separate controller metadata commit without rewriting the tagged content;
6. atomically push the canonical branch through the metadata commit and the status tag,
   then verify both remote identities;
7. retain the accepted validation report and controller transaction evidence;
8. stop after validated HOLD, BLOCKED or FAILED;
9. only after scientific PASS consider a fresh process for an authorized successor.

Never tag an invalid repository result. Non-PASS closeouts use their status-specific tag
and must not be described as PASS. Never rewrite an accepted tag or frozen history.

## HOLD, BLOCKED and FAILED

- HOLD records a legitimate gate stop that may require external action or a later decision.
- BLOCKED records a validated dependency or input barrier.
- FAILED records that the programme's declared execution or gate failed.
- A process crash, malformed final response or invalid freeze is an orchestration failure,
  not one of those scientific statuses.

Validated HOLD, BLOCKED or FAILED always stops the outer loop. A scientific FAILED result
is frozen evidence, not a retryable transport error. The orchestrator never skips the
programme to retain motion.

## Recovery

A crash, malformed response or fixable controller/transport failure before a valid freeze
leaves the same programme active. Preserve its logs, inspect repository integrity and retry
the same G in a fresh process only when mechanically safe and within the retry bound.
Scientific PASS/HOLD/BLOCKED/FAILED records are never retry inputs.

A failure after a validated content commit or status tag is publication recovery, not a
same-G scientific retry. Verify and reuse the accepted content identity, complete the
controller metadata commit and remote transaction, and do not launch Codex again.

If repository state is contradictory, stop. Do not guess which partial output should win.

Normal successor execution always uses a fresh Codex process. Conversation resume is not a
substitute for a new G context.

## Bootstrap boundary

The bootstrap repository may contain schema, orchestration and empty directory scaffolding
for G14. None of it is G14 research. Bootstrap must not invoke the real runner. After
bootstrap acceptance, programme state may authorize G14 for a later explicit
outer-controller --start while started remains false. During bootstrap:

- do not run the real autonomous loop;
- do not implement the G14 proof store;
- do not create a G14 handoff or freeze manifest;
- do not claim G14 progress;
- do not advance G15 or G17.
