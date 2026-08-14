<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G9_Road_to_100_Assessment.docx
original_sha256: 9fbc063a2928ef75854c402b6503fbcff9cbedd18358294b068e528f4c61fa21
derivative_filename: G9_Road_to_100_Assessment.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

G9
# Where We Are on the Road to 100%
*A capability-based progress assessment toward a machine-checkable White-non-loss proof from the standard initial position*
G9 PROGRESS ASSESSMENT | HEADLINE SCORE + UNCERTAINTY + SENSITIVITY
11 August 2026
> Headline assessment: 24% programme readiness, with a plausible 18%-30% range. This is not “24% of chess positions solved.” Direct proof-path completion from the initial position is still near zero because no certified connection to that position exists yet.
# 1. Freeze the endpoints
| Point | Definition |
| --- | --- |
| 0% | The programme immediately before Pilot 1: no demonstrated symbolic backward-attractor result, no typed proof system, no certificate engine, and no programme-specific exact-solving infrastructure. |
| 100% | A machine-checkable proof, under an explicitly declared complete chess ruleset, that from the standard initial position White has a strategy that cannot lose. The proof must be independently replayable/auditable and must cover every legal Black reply. |
The percentage below is therefore a measure of programme capability/readiness to produce that end-to-end proof. It is not a ratio of solved states to all chess states, and it is not a probability that White can draw.
# 2. Why state-count percentage is the wrong measure
- Chess state space is not one homogeneous pile of equally difficult positions. A single reusable theorem or verifier may remove work across many future arenas, while millions of isolated solved states may contribute almost nothing to a path from the initial position.
- The current eight-man results are restricted families. Treating their state counts as a numerator over “all chess states” would falsely imply both broad material coverage and initial-position connectivity.
- The project is building an end-to-end proof pipeline. The right unit of progress is therefore capability: rules fidelity, exact scale, reusable proof structure, composition, verification, topology coverage and - above all - connection to the initial position.
# 3. Weighting - frozen before scoring
| Dimension | Weight | Reason for weight |
| --- | --- | --- |
| Connection to the initial position | 25 | Does current certified machinery actually reach or constrain the standard starting position? This is the most direct dependency of the final theorem. |
| Rules/model completeness | 10 | Can the state model represent the exact final rules and history-dependent state needed by the theorem? |
| Exact solving scale | 15 | How far has exact solution moved in material, branching, dependency size and execution economics? |
| Reusable proof abstraction | 15 | How much solved truth can be carried by general operations rather than hand-authored tables or square lists? |
| Composition depth | 10 | Can certified subgames and strategy phases be assembled into long proofs without description cost exploding? |
| Verification and reproducibility | 10 | Can another implementation independently check, resume, hash, audit and preserve the result? |
| Breadth of chess topology | 10 | How many qualitatively different tactical/strategic structures have been stress-tested? |
| Remaining combinatorial gap | 5 | How much of the leap from restricted endgame islands to the full game graph has actually been retired? |
The weighting deliberately gives 30% of the total to two “are we actually approaching the initial-position theorem?” dimensions: direct connection (25%) and the remaining combinatorial gap (5%). Exact scale, abstraction and composition together receive 40%, because they are the principal engines that may make later connection feasible. Rules and verification each receive 10%, because a result that cannot represent or independently replay the declared game is not the required theorem.
# 4. Baseline score
| Dimension | Weight | Score / 100 | Weighted points | Assessment |
| --- | --- | --- | --- | --- |
| Connection to the initial position | 25 | 1 | 0.25 | No current G8 proof starts at, reaches back to, or otherwise constrains the standard initial position. Existing results are disconnected solved islands. One point is awarded only for having a proof architecture designed to accept future upstream dependencies. |
| Rules/model completeness | 10 | 20 | 2.0 | Terminal semantics, promotion, capture continuations, checkmate/stalemate and material dependencies are increasingly typed. But the final state model still lacks a complete integrated treatment of history-dependent draw state, repetition, move-count rules, en passant/castling history where relevant, and legal reachability from the initial position. |
| Exact solving scale | 15 | 18 | 2.7 | The engine now solves prospectively frozen restricted eight-man dependency graphs above 80M states and previously hostile 40-48M families in seconds. This is a substantial engineering achievement, but it remains far below unrestricted higher-material/middlegame complexity. |
| Reusable proof abstraction | 15 | 50 | 7.5 | Strict attractors, Branch/Hyperkernel and Filter-Pivot have universal game-graph semantics; typed resource-safe targets, restoration domains and diagnostics form a mature reusable layer. The score is capped because target/abstraction discovery is still partly manual and several topologies retain lookup-like local floors. |
| Composition depth | 10 | 35 | 3.5 | Destination alternatives, second-order attractors and ordered strategy phases have been combined in depth>3 DAGs and a canonical product certificate. Full-chess proof chains will require orders of magnitude more depth, fan-out and transposition sharing. |
| Verification and reproducibility | 10 | 55 | 5.5 | G8 adds content-addressed dependencies, compact payloads, standalone verification, zero-mismatch Bellman audits and preserved error alarms. It is not yet a full formally verified rules/solver stack; two historical provenance exceptions remain frozen, and some verifier paths are slower or memory-heavier than solving. |
| Breadth of chess topology | 10 | 20 | 2.0 | The portfolio now includes pawn races, leapers, sliders, rooks, queens, fortresses, opposing mobile pieces, captures, branching material transitions and adversarial controls. It is still dominated by endgame-like restricted geometries and does not yet cover ordinary middlegame king safety, dense tactics, quiet manoeuvring, opening transpositions or broad pawn structures. |
| Remaining combinatorial gap | 5 | 2 | 0.1 | The programme has learned how to move a local exact-solve frontier and how to compress some proof regions, but essentially none of the enormous material/branching gap between restricted eight-man islands and the 32-piece initial game has been closed end-to-end. |
Weighted total = 23.55 points out of 100, rounded to a headline score of 24%.
> HEADLINE: 24% PROGRAMME READINESS. PLAUSIBLE RANGE: 18%-30%.
The range is intentionally wide. The dominant uncertainty is not any historical count; it is how much leverage the current proof architecture will retain when it encounters ordinary middlegame branching and an opening-scale connection problem. If the universal game-graph operators and certificate decomposition continue to scale, today’s infrastructure deserves more credit. If compact target/strategy discovery becomes the bottleneck and most higher-tree truth must be carried raw, the same present state deserves less.
# 5. Sensitivity analysis
| Scenario | Weighting change | Result | Interpretation |
| --- | --- | --- | --- |
| Proof-path-heavy weighting | 35% initial connection, 10% remaining gap; reduced credit to abstraction/verification | 17.9% -> 18% | Treats disconnected solved islands as much less valuable until a certified route from the start position exists. |
| Baseline capability weighting | Weights shown above | 23.55% -> 24% | Balances current infrastructure with the fact that the initial-position gap dominates the final objective. |
| Infrastructure-heavy weighting | More weight on reusable abstraction, composition and verification; only 17% on connection+gap | 30.0% | Credits the possibility that G6-G8 removed whole categories of future work even though the actual bridge has not been built. |
The score does not swing from “almost nothing” to “almost solved” under reasonable weights. It stays in the high teens to about 30%. That supports 24% as a stable navigation figure rather than a morale-adjusted guess.
# 6. Milestone interpretation
| Milestone | Status | Why |
| --- | --- | --- |
| Proof concept: exact solved regions can expose symbolic structure | Achieved | Pilot 1 and Pilot 2. |
| Reusable exact compositional proof system | Achieved | G3-G7, especially G6 typed proof objects and G7 strategy-language axis. |
| Scalable solver/certifier for selected richer arenas | Achieved at restricted scale | G8 material-signature solver, compact certificates and independent verifier; restricted eight-man ascent. |
| Broad endgame coverage across ordinary material signatures | Not achieved | Portfolio is selective, not exhaustive; full rules/history also incomplete. |
| Bridge from endgames into general middlegame structures | Not achieved | No wide certified basin network at 10-16+ men with dense tactics/king safety/quiet play. |
| Bridge from middlegame basins to the opening/initial position | Not achieved | No current certificate has the standard starting position as an ancestor. |
| Final all-replies non-loss proof and independent reproduction | Not achieved | This is the 100% condition. |
This milestone view explains why the numerical score is neither tiny nor large. The programme has crossed three foundational milestones, but the remaining milestones are much larger and closer to the actual theorem.
# 7. The biggest strengths at G9
- Exactness discipline. The project repeatedly rejected or superseded attractive outputs when move generation, terminal semantics or declarations were wrong.
- Reusable game-graph theory. Strict attractor, Branch/Hyperkernel and Filter-Pivot give a small universal core that does not depend on one chess geometry.
- Typed chess semantics. Resource-safe targets, restoration domains and explicit lower-material continuations reduce the risk of silently importing false monotonicity assumptions.
- Independent certificates. Producer truth and verifier replay are now separate artifacts with hashes and explicit dependency identity.
- Prospective testing. Later stages freeze arenas and vocabularies before outcome truth, making negative transfer scientifically meaningful.
- Engineering evidence. G8 showed that at least one apparent mathematical frontier was actually an implementation frontier and could be removed without changing the arena.
# 8. The biggest gaps
- Initial-position disconnection. This is the single largest gap: the project has no certified path from the normal starting position into any existing solved basin.
- Full rules/state semantics. A final proof cannot ignore claim state, repetition/move counters, historical move rights or other history-dependent legality where they affect outcome.
- Automatic discovery. Today’s proof language is stronger than today’s autonomous proof discovery. Future scale cannot depend on a human inventing every useful target and strategy phase by hand.
- Middlegame topology. Current evidence is still heavily endgame-like. Dense checking, exposed kings, exchange sacrifices, quiet strategic moves and broad pawn structures need their own prospective campaigns.
- Long proof composition. A 23,327-state product DAG is a useful prototype, not evidence that millions of subgames can be composed and verified economically.
- Raw-truth fallback. Some residuals are genuinely lookup-like. The final architecture must be able to carry exact table dependencies without pretending every region will compress symbolically.
- Distributed scale. The G8 engine is efficient on current arenas, but a final programme needs durable multi-machine checkpointing, reproducible orchestration and independent re-execution at much larger scale.
# 9. What would move the percentage materially
| Change | Likely effect on score |
| --- | --- |
| Complete and independently conformance-test the final chess state/rule semantics | Raises rules/model score and reduces risk across every later programme. |
| Demonstrate broad exact 9-12+ man solving with capture-closed dependencies and preserved verifier economics | Raises scale, breadth and remaining-gap scores. |
| Automate prospective discovery of exact targets/strategy phases that transfer held-out | Raises abstraction and composition scores. |
| Construct a reusable certified basin network in materially richer middlegame-like positions | Raises breadth and materially reduces the combinatorial gap. |
| Produce the first certified connection from the standard initial position into that basin network | Largest single step: initial-position connection stops being approximately zero. |
| Close every legal Black deviation and independently replay the complete proof | Takes the programme from a connected candidate proof to 100%. |
# 10. Bottom line
G8 was a major success, but it was a success in method, architecture and selected exact scale - not a claim that a quarter of all chess has been enumerated. The best single number is 24% programme readiness, because the project now has several pieces of machinery that a real weak solution would plausibly need, while the actual bridge from the initial position and most of the material/branching climb remain ahead. If one insists on measuring only already-connected proof path from the initial position, the answer is effectively near zero. G9 therefore treats 24% as a capability score whose job is to guide investment, not as a solved-space statistic.
# Source basis and authority
This G9 synthesis uses the frozen technical handoffs as the historical authority, in the order required by the kickoff memo. Later reconstructions are used only to explain corrections or certification exceptions; they do not silently overwrite the frozen record.
- Pilot_1_Symbolic_Backward_Attractor_Technical_Handoff.docx
- Pilot_2_K2P_vs_K_Technical_Handoff.docx
- Pilot_2_G3_Technical_Handoff.docx
- G4_Three_Pawn_Compositional_Proof_Technical_Handoff.docx
- G5_Prospective_Transfer_Benchmark_Technical_Handoff.docx
- G6_Final_Technical_Handoff.docx and G6_Final_Historical_Certification_Exceptions.md
- G7_Higher_Tree_Position_Discovery_Technical_Handoff.docx
- G8_Certificate_Engine_and_Reascent_Final_Technical_Handoff.docx and G8 Proof Language v0.4
- G9_Review_Road_to_100_Planning_Kickoff_Memo.docx
