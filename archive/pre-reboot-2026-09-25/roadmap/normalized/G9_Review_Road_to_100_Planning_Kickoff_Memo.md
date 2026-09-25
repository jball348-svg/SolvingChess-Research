<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G9_Review_Road_to_100_Planning_Kickoff_Memo.docx
original_sha256: 55a5a8b86cea3119268d4cfc8bb9b68825ef2081bec8eb5a7d2d8ea262a910fe
derivative_filename: G9_Review_Road_to_100_Planning_Kickoff_Memo.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

# G9 Review, Road-to-100 and
Long-Range Programme Planning
*KICKOFF MEMO  |  SYNTHESIS + PROGRESS ASSESSMENT + DEPENDENCY-ORDERED PLANNING*
11 August 2026
| G9 mission. Stop doing new chess experiments for one programme. Explain, assess, and plan.<br>G9 must translate the entire Pilot 1 -> G8 programme into plain English, estimate where the programme stands on a user-defined 0-to-100 road toward a weak solution of chess, and then design the dependency-ordered sequence of future programmes needed to reach 100. The output is a planning architecture, not another solved arena. |
| --- |
PROJECT TYPE: RETROSPECTIVE SYNTHESIS + STRATEGIC ASSESSMENT + LONG-HORIZON ROADMAP
PRIMARY AUDIENCE: a smart reader who does not have advanced mathematical training and has not followed every technical session.
PRIMARY OUTPUTS: three standalone documents: plain-English history; road-to-100 assessment; G10-onwards plan.
> G9 should not create a G10 kickoff memo. It should create the map from which later kickoff memos can be written.
# 1. Authority and frozen starting point
Historical authority. Use the frozen technical handoffs in order: Pilot 1, Pilot 2, G3, G4, G5, G6, G7, G8. Later reconstructions do not silently overwrite earlier frozen truth. The two G6 historical certification exceptions remain exactly as frozen unless original artifacts are recovered.
Immediate technical starting point. G8 closed as a full programme pass: the solver moved to reusable material-signature dependencies, compact certificates and independent verification; every frozen G7 scale hold targeted by G8 was recovered unchanged; strategy languages became composable ordered phases; and two prospectively frozen restricted-eight-man arenas were solved exactly and independently verified.
What this does not mean. Exact restricted-eight-man results are not a percentage of chess. The programme has demonstrated methods, proof objects and scaling behaviour on selected finite arenas; it has not connected those arenas to a proof from the standard initial position. G9 must preserve that distinction throughout.
# 2. Starting history - shorthand only, not the G9 deliverable
The following is only an orientation checklist. G9 must independently produce the full plain-English review from the frozen handoffs rather than copying these one-line summaries.
| Stage | One-line orientation |
| --- | --- |
| Pilot 1 | Showed that a large exact backward non-loss region can have a layered geometric description rather than being only a huge list of positions; also exposed a real local-complexity boundary. |
| Pilot 2 | Replicated the idea in a different pawn ending and showed that exact lower-material results and a new stepping-stone can be combined to explain most wins. |
| G3 | Added another exact compositional layer, then deliberately stopped when the final local grammar became almost lookup-like. |
| G4 | Moved to a harder three-pawn race with both sides able to win; the proof architecture transferred, but the last blockade tail again resisted compact exact description. |
| G5 | Turned transfer into a prospective test. Some operations transferred strongly; others failed. This separated genuinely reusable ideas from arena-specific successes. |
| G6 | Built the first cross-arena proof-system prototype: exact attractors, Branch/Hyperkernel composition, restoration theorems, sanctuary logic, proof typing and broader held-out testing. |
| G7 | Climbed materially higher, discovered the strategy-language / Filter-Pivot axis, composed deeper proof DAGs, and honestly froze a high-branch/seven-man engine frontier. |
| G8 | Re-engineered solving/certification, cleared the G7 frontier, compiled compact independently verifiable certificates, generalized ordered strategy switching, and prospectively reached exact restricted-eight-man arenas. |
# 3. G9 output contract
G9 must finish with exactly three substantive reader-facing documents. Supporting notes/ledgers may exist internally, but the programme outputs are:
- Document 1 - What has been done, in plain English: A stage-by-stage account from Pilot 1 through G8. It should explain the problem, what was tried, what was discovered, why it mattered, and what remained unsolved. It should be readable without equations. Technical terms may appear only when immediately translated into ordinary language.
- Document 2 - Where we are on the road to 100%: A defensible progress assessment from 0 = the start of Pilot 1 to 100 = a machine-checkable proof that, from the standard initial chess position, White has a strategy that cannot lose under the declared ruleset. It must produce a single headline percentage, an uncertainty/range, and the reasoning behind it.
- Document 3 - The plan from G10 onward: A dependency-ordered, high-level programme map from the current state to 100. It may contain ten stages or hundreds. Numbering must follow the dependency structure; do not compress the roadmap merely to make it look manageable.
> Do not turn Document 3 into a near-term wishlist. Its purpose is to map the whole remaining problem, including large, uncomfortable and currently uneconomic steps.
# 4. Workstream A - plain-English historical map
The historical review is not a technical abstract. It should explain the programme as a sequence of changing ideas and capabilities. For each stage, answer the same five questions:
1. What problem were we trying to solve?
1. What did we actually do?
1. What did we learn or build?
1. Why did that matter for the overall chess-solving project?
1. What limitation, failure, or open question did the stage leave behind?
## Plain-language discipline
- Prefer phrases such as "work backward from positions we already understand" before terms such as "strict attractor".
- Explain "certificate" as a compact object another program can independently check, before giving its formal type name.
- Explain "Branch/Hyperkernel" as a way of proving a position is safe because the opponent cannot avoid giving access to one of several already-solved destinations.
- Explain "strategy language" as restricting the kind of move White is allowed to use during one phase of a proof, such as checks or king moves.
- Never imply that exact results on a restricted arena solve all positions with the same number of pieces.
- Include negative results. Lookup-like tails, failed inheritance rules, non-transfer, verification costs and engine frontiers are part of the achievement because they prevented false generalization.
## Required historical arc
The review should make the change in programme shape visible:
| Programme era | Question being answered |
| --- | --- |
| Pilot 1 -> Pilot 2 | Does symbolic structure exist, and does it replicate? |
| G3 -> G5 | Can exact stepping stones compose and transfer without fitting each arena after the fact? |
| G6 | Can the discoveries be organized into a reusable proof system with mathematical/core versus conditional/local components? |
| G7 | Can that proof architecture climb to materially richer and more highly branching positions? |
| G8 | Can the implementation and certificates scale enough to clear the engineering frontier and climb again? |
# 5. Workstream B - estimate progress from 0 to 100
Freeze the endpoints before scoring. 0 is the programme immediately before Pilot 1. 100 is the requested end-state: a machine-checkable proof from the standard initial position that White has a non-losing strategy under an explicitly declared complete chess ruleset.
The percentage must not be calculated as solved states divided by an estimate of all chess states. That number would be both misleading and structurally irrelevant. G9 should score progress as programme capability toward the end-to-end proof.
## Mandatory dimensions to assess
| Dimension | Question for G9 |
| --- | --- |
| Connection to the initial position | How much of the current proof machinery actually reaches or constrains the standard starting position rather than isolated endgame slices? |
| Rules/model completeness | How close is the state model to the exact rules that the final proof must use, including history-dependent draw and special-move state where relevant? |
| Exact solving scale | How far has exact solution moved in material count, branching, signature complexity and state population, and what scaling law is actually evidenced? |
| Reusable proof abstraction | How much of solved truth can be represented by general proof operations rather than raw truth tables or arena-specific rules? |
| Composition depth | Can certified subgames and strategy phases be combined into long proof chains without description cost exploding? |
| Verification and reproducibility | Can large results be independently checked, resumed, hashed, audited and preserved without trusting the producer? |
| Breadth of chess topology | How many qualitatively different piece/mobility/fortress/race structures have been tested, and where do current abstractions fail? |
| Remaining combinatorial gap | How large is the leap from restricted eight-man exact truth to the full initial-position game graph, taking into account that raw state count is not the only difficulty? |
## Scoring protocol
- Choose and justify the weighting before assigning the final score. Show the weights.
- Give one headline percentage because the task requires it, but also give a plausible range and explain the dominant uncertainty.
- Run at least one sensitivity check using a different reasonable weighting. If the answer swings radically, say so.
- Separate "we have discovered a useful method" from "we have consumed this fraction of the remaining search space". They are not the same thing.
- Use milestone comparisons where useful: proof concept, reusable proof system, scalable solver/certifier, broad endgame coverage, bridge to middlegame, bridge to opening/initial position, final proof.
- Be willing to give a surprisingly low percentage even after major G8 success if the initial-position gap dominates; be equally willing to credit infrastructure that removes whole classes of future work. The score must follow the rubric, not mood.
> The road-to-100 document should make clear whether the headline percentage is best read as "programme readiness", "proof-path completion", or another construct. Do not smuggle that choice in implicitly.
# 6. Workstream C - map G10 onward all the way to 100
The roadmap is a dependency graph first and a numbered sequence second. If a future capability will be needed at G50, but requires infrastructure that must exist by G12, schedule the dependency at G12. The plan should be long enough to tell the truth about the problem.
## For every planned future stage
- Stage number/name and one-sentence mission.
- Why this stage exists - which specific gap from Document 2 it closes.
- Dependencies that must already be complete.
- Primary research/engineering questions.
- Expected deliverable or proof artifact.
- Advance criteria and a credible failure/stop condition.
- What later stage this unlocks.
- Whether it is primarily science, solver engineering, formal verification, scale computation, or integration.
## Roadmap coverage checklist
G9 must explicitly decide where each of the following belongs. This checklist is not itself the roadmap and should not predetermine the eventual G-numbers:
- Complete final-game state semantics, including any history-dependent rules that a genuine initial-position proof cannot ignore.
- Repository-quality verified move generation and independent rule/model conformance.
- Scaling material-signature solving beyond the restricted eight-man frontier without losing exactness or replayability.
- Systematic coverage of qualitatively different material and movement topologies rather than only incrementing piece count.
- General proof discovery: how new targets, abstractions and strategy phases are proposed prospectively rather than hand-authored forever.
- Long proof-DAG composition and subsumption: controlling proof size when thousands or millions of certified subgames interact.
- Handling positions where compact symbolic compression genuinely fails and raw exact truth must be carried as a dependency.
- Distributed/checkpointed computation, reproducible large-job orchestration and independent verification at scales beyond one session or one machine.
- Bridging from endgame-like exact domains into materially richer middlegame structures with captures, exchanges, king safety and tactical branching.
- Connecting those higher-tree domains to the standard initial position rather than accumulating disconnected solved islands.
- Opening/early-game proof search and transposition management once lower layers are strong enough to serve as certified destinations.
- Final end-to-end proof assembly, audit, replay, independent reproduction and preservation.
## Roadmap shape
G9 may find it useful to group future programmes into broad eras before numbering them, for example: foundation closure; scale and breadth; generalized proof discovery; higher-tree integration; initial-position connection; final certification. Those era names are illustrative only. The actual roadmap must be derived from the gap analysis.
> Do not force the plan into G10-G20. If the dependency analysis says G10-G60, G10-G200 or G10-G1000, write that. Conversely, do not manufacture hundreds of stages merely to sound comprehensive.
# 7. Hard rules for G9
- No new chess result is required. G9 is an analysis/planning programme. Run a new experiment only if a genuinely missing historical fact makes the review impossible, and label it separately rather than letting G9 become G8.10.
- Use the frozen handoffs as history. Preserve superseded figures as superseded and the two G6 historical certification exceptions as exceptions.
- Distinguish exact chess truth inside a declared finite arena from a claim about full chess.
- Never convert "we solved up to restricted eight-man arenas" into "we solved X% of chess" without a justified capability model.
- Do not reward raw state count twice: once as exact-scale progress and again as global game coverage.
- Do not hide the distance to the initial position. The roadmap must make the disconnected-island problem explicit if that is the correct diagnosis.
- Do not assume current abstractions will survive all future topologies. Include planned falsification/held-out stages at suitable intervals.
- Do not optimize the final percentage for morale. It is a navigation instrument.
- Do not make the long-range plan linear if the work is actually branching or parallel. Show prerequisite DAGs and parallel tracks where appropriate.
- Do not produce a G10 kickoff memo as part of G9. Document 3 is a high-level programme map only.
# 8. Suggested internal G9 execution: G9.0-G9.6
| Stage | Freeze point |
| --- | --- |
| G9.0 - Freeze definitions and scoring rubric | Freeze 0, 100, the required scoring dimensions, source precedence and plain-English audience before drafting conclusions. |
| G9.1 - Historical extraction | Build a fact-checked stage ledger from Pilot 1 through G8: goals, actions, exact achievements, failures, corrections, and capability added. |
| G9.2 - Plain-English synthesis | Turn that ledger into Document 1. Remove unnecessary notation without removing the difference between theorem, exact computation, empirical pattern and engineering improvement. |
| G9.3 - Capability and gap map | Describe what the programme can now do end-to-end, what it cannot yet do, and which missing capabilities are prerequisites for others. |
| G9.4 - Road-to-100 scoring | Apply the frozen rubric, generate the headline percentage + interval + sensitivity analysis, and write Document 2. |
| G9.5 - Dependency-first roadmap | Build the long-range dependency DAG, then assign G10+ programme numbers and produce Document 3. |
| G9.6 - Consistency audit and closeout | Check that every roadmap stage addresses a stated gap, every gap has a future owner or explicit unknown, the percentage agrees with the roadmap scale, and no future result has been assumed as already solved. |
# 9. G9 advance criteria
- Document 1 is understandable to a non-advanced-math reader without materially distorting any stage.
- Every stage from Pilot 1 through G8 is represented, including major negative results and superseded/corrected findings that affected methodology.
- Document 2 states a single progress percentage, a defensible uncertainty range, explicit weights/assumptions and at least one sensitivity analysis.
- The percentage is not derived from raw solved-state fraction and clearly distinguishes exact restricted-domain success from full-chess coverage.
- Document 3 reaches all the way to the requested 100 end-state, regardless of how many G-stages that requires.
- The future plan is dependency-ordered: prerequisite engineering, rules, verification and abstractions appear before stages that rely on them.
- Every major present-day gap has at least one future programme owner, or is explicitly marked as an unresolved research unknown that may branch the roadmap.
- At least one planned branch handles the possibility that symbolic compression ceases to scale and raw exact dependencies become dominant.
- The three documents agree with one another: the history explains the score; the score explains the roadmap; the roadmap closes the gaps used to justify the score.
# 10. Failure criteria
- The plain-English history becomes a victory narrative that omits failures, corrections or model caveats.
- The road-to-100 score is a rhetorical guess with no explicit rubric or sensitivity analysis.
- The score treats eight-man exact solving as a direct fraction of the 32-piece game.
- The roadmap begins at the next interesting experiment but does not map the route to the initial position and final proof.
- Later stages depend on rule models, verifiers, distributed infrastructure or proof abstractions that were never scheduled earlier.
- The roadmap assumes unknown scientific breakthroughs as if they were routine engineering tasks.
- The roadmap is made artificially short by merging distinct unsolved capabilities into vague mega-stages.
- G9 quietly performs new G10 research and contaminates the planning baseline with outcome knowledge.
# 11. Research-agent kickoff prompt
| You are beginning G9 of an exact symbolic-chess research programme. G9 is not another solving campaign. Use the frozen Pilot 1, Pilot 2, G3, G4, G5, G6, G7 and G8 technical handoffs as the authoritative history. Your first job is to explain, in plain English for a non-advanced-math reader, what each stage tried, what it achieved, why it mattered and what it failed to solve. Your second job is to assess programme progress on a frozen 0-to-100 scale where 0 is the start before Pilot 1 and 100 is a machine-checkable proof from the standard initial position that White has a strategy that cannot lose under the declared complete chess rules. Do not use solved-state fraction as the percentage. Freeze a multi-dimensional capability rubric before scoring, publish the weights, give one headline percentage plus an uncertainty range and sensitivity analysis, and make the gap to the initial position explicit. Your third job is to build the complete dependency-ordered roadmap from G10 to 100. The roadmap may be short or extremely long; do not force it into a convenient number of stages. Schedule prerequisites before they are needed, distinguish science from engineering and verification, include failure branches, and give each future stage a mission, dependencies, deliverables, advance criteria and what it unlocks. Produce exactly three principal documents: (1) What has been done in plain English; (2) Where we are on the road to 100%; (3) The plan from G10 onward. Do not create a G10 kickoff memo and do not run new chess experiments merely to improve the narrative. G9 succeeds if it leaves an honest, comprehensible map of the entire programme and the entire remaining problem. |
| --- |
# 12. Expected G9 closeout
- G9_What_We_Have_Done_Plain_English.docx
- G9_Road_to_100_Assessment.docx
- G9_G10_Onwards_Long_Range_Plan.docx
A supporting source/assumption ledger may be retained for reproducibility, but it is not a fourth reader-facing deliverable. G9 closes when the three documents pass the consistency audit in G9.6.
| G9 north star: make the journey legible, estimate the distance honestly, and turn the remaining distance into an ordered programme of work. |
| --- |
