<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G9_What_We_Have_Done_Plain_English.docx
original_sha256: b12691f502236e01c2cd802cec6f5b159d5ec38c8d07b761205b6a4a83569aca
derivative_filename: G9_What_We_Have_Done_Plain_English.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

G9
# What We Have Done, in Plain English
*Pilot 1 through G8: what the programme tried, what it learned, and what remained unsolved*
RETROSPECTIVE SYNTHESIS | READER-FACING PLAIN-ENGLISH HISTORY
11 August 2026
> The programme did not solve chess. It built and repeatedly tested a way of turning exact local chess truth into reusable, independently checkable proof components - and learned where that approach works, fails, and needs stronger engineering.
# Executive summary
The programme began with a narrow question: if we exactly solve a small chess situation, is the answer just a giant list of positions, or can much of that list be explained by a small number of meaningful chess ideas? Pilot 1 showed that the answer can be “yes, there is structure.” The following stages then tried to find out whether that structure repeats, whether different exact results can be chained together, whether the same proof ideas survive on new kinds of positions, and whether the software can scale without losing exactness.
By G8, the project had progressed from one hand-built endgame experiment to a reusable exact solver, a typed proof language, compact certificates that another program can replay, several forms of proof composition, and exact prospectively chosen restricted eight-man arenas. Just as importantly, it had also accumulated hard negative results: some local boundaries remain almost lookup-like; restoration rules that look obvious can fail; a symbolic surface can look impressive while carrying little information; certificate verification can be more expensive than solving; and a solver frontier can be an implementation problem rather than a mathematical one.
The decisive limitation is unchanged: all of this work is still on selected finite islands. None of the current certificates begins at the normal initial chess position. That gap is not a footnote; it is the central reason G9 exists.
| Era | Question | What changed |
| --- | --- | --- |
| Pilot 1 -> Pilot 2 | Does useful symbolic structure exist, and does it repeat? | From one fortress example to a different pawn-only replication. |
| G3 -> G5 | Can exact pieces of truth compose and transfer without fitting each new arena after the fact? | From retrospective compression to prospective, falsifiable proof-language transfer. |
| G6 | Can the discoveries be organized into a reusable proof system? | Typed proof objects, domains, composition theorems, regression discipline and cross-arena classification. |
| G7 | Can that architecture climb into richer, more highly branching positions? | Higher material, capture DAGs, strategy-language proofs, and an explicit scale boundary. |
| G8 | Can the implementation and certificates clear that boundary and climb again? | Material-signature engine, compact certificates, independent verification, ordered strategy phases and restricted eight-man re-ascent. |
# Pilot 1 - Find out whether exact chess truth has a readable shape
## 1. What problem were we trying to solve?
The first experiment used a deliberately small wrong-colour bishop and rook-pawn fortress. Black had a known corner sanctuary. The question was not “is this ending solved?” but “if we work backward from a safe region, does the resulting exact set have a meaningful shape?”
## 2. What did we actually do?
- Enumerated 1,182,440 static-valid four-piece states inside the declared model.
- Worked backward from the 22,008-state h8 sanctuary using an exact adversarial predecessor calculation.
- Corrected artificial boundary conditions by treating real safe captures, KPK outcomes and stalemate properly instead of pretending every exit from the chosen arena was unsafe.
- Grouped positions by meaningful geometry and searched for timing and access rules rather than memorizing squares.
## 3. What did we learn or build?
- The stubborn bishop-sensitive frontier collapsed onto two exact move-order-adjusted race ties: a White-king race and a pawn-promotion race. All 1,181 residual king/pawn/turn geometries lay on one or both zero-slack surfaces.
- Bishop relevance then localized to a narrow diagonal cone and mostly short intervals on a diagonal, so a large solved region could be described in layers rather than as a flat list.
- The resource-isolation experiment also showed that most bad bishop placements were explained by either White king or pawn counterplay, with only a small synergy remainder.
## 4. Why did that matter?
This was the proof of concept for the whole programme: exact backward solving can reveal reusable chess structure, and “where complexity lives” can itself be described.
## 5. What did it leave unsolved?
The final mobile-king boundary did not collapse into one tiny formula. Pilot 1 also used restricted/static-valid state semantics, terminalized its sanctuary operationally, and omitted history-dependent draw rules. It proved structure inside one finite arena, not a statement about chess from the initial position.
# Pilot 2 - Check that the idea was not a one-off fortress trick
## 1. What problem were we trying to solve?
Pilot 2 removed the bishop and fortress corner entirely. White had two adjacent central pawns against Black’s king. The aim was to see whether exact symbolic composition still appeared in a materially and geometrically different game.
## 2. What did we actually do?
- Solved 236,976 static-valid states exactly: 228,500 White wins and 8,476 draws under the frozen convention.
- Projected positions into exact one-pawn KPK subgames and tested whether those lower-material wins survive when the second pawn is restored.
- Searched for a second cooperative target and then asked whether White can force entry into it against resistance, not merely whether the target itself is winning.
## 3. What did we learn or build?
- Exact KPK inheritance certified 197,108 wins, or 86.26% of the whole winning basin, with only ten immediate-stalemate exceptions.
- A one-rank stagger between the two pawns became a second exact cooperative theorem. Strict reachability into that target certified another 26,122 wins.
- Together the two mechanisms certified 97.69% of all White wins. The remaining difficult positions localized tightly around Black’s blockade.
## 4. Why did that matter?
This was the first strong replication and the first convincing demonstration that exact lower-material truth and a new semantic stepping stone can compose under adversarial play.
## 5. What did it leave unsolved?
The hard residual did not yield a tiny contact grammar. A tempting “escort the pawns until they become autonomous” hypothesis failed on most of the genuinely hard frontier. The arena still used restricted files/ranks and incomplete full-game history semantics.
# G3 - Add one more exact layer, then stop before the proof becomes a disguised lookup table
## 1. What problem were we trying to solve?
G3 returned to the final Pilot 2 residual. It had two jobs: see whether another compositional layer could be added, and decide whether the remaining king/blockade boundary had a genuinely compact grammar.
## 2. What did we actually do?
- Independently reconstructed all load-bearing Pilot 2 checksums before adding new inference.
- Terminalized the union of the two already-proved regions and computed a strict “return to the certified library” attractor.
- Built a bounded semantic language for the final blockade geometry and fixed a stopping rule before fitting.
## 3. What did we learn or build?
- The union-return bridge added 2,852 more exact wins with zero draw false positives, lifting symbolic coverage to 98.94%.
- The remaining 214 mixed geometries became semantically separable after one extra orientation concept, but exact description still needed roughly 200 leaves for 214 geometries.
## 4. Why did that matter?
G3 established a crucial methodological principle: a failed compression attempt can be a successful scientific result if the stopping rule was prospective. It prevented the programme from calling an almost one-case-per-case tree a “theorem.”
## 5. What did it leave unsolved?
The last blockade boundary remained essentially local. G3 also exposed a two-position terminal-semantics discrepancy in the inherited Pilot 2 convention, reinforcing that terminal definitions must be part of the proof contract.
# G4 - See whether the proof architecture transfers to a genuine two-sided race
## 1. What problem were we trying to solve?
G4 moved to White’s d/e pawns versus Black’s c-pawn. Both sides could now win. The preferred minor-piece arena was too large for the interactive certificate budget, so the predeclared pawn-race fallback was used rather than shrinking the primary arena after seeing results.
## 2. What did we actually do?
- Solved a 1,356,280-state fully populated slice to 933,667 White wins, 357,349 Black wins and 65,264 draws.
- Reused projection/restoration, semantic target, strict attractor and union-return operations from earlier work.
- After removing robust exact regions, tested three tempo-adjusted promotion/interception clocks on the White-king-sensitive frontier.
## 3. What did we learn or build?
- A friendly-pawn restoration theorem certified 712,156 White wins under a compact stated guard; naive enemy-pawn restoration failed badly.
- A new d7/e7 target had 31,188 exact wins and a 185,269-state strict attractor.
- Returning to the union of certified regions raised coverage to 792,177 wins, 84.84% of the total White-winning basin.
- The exact Pilot-1 zero-slack law did not transfer literally, but 97.67% of the mixed frontier lay within one full move of one of three race/interception surfaces.
## 4. Why did that matter?
G4 showed that the reusable unit was becoming an operation - project, target, attract, bridge, localize - rather than a formula tied to one square pattern.
## 5. What did it leave unsolved?
The 227-position-family blockade tail again hit near-lookup scale: 208 exact coordinate-tree leaves. More importantly, the original G4 optional-pawn/capture implementation artifact was later unavailable; G6 preserved a historical certification exception instead of reverse-engineering hidden semantics.
# G5 - Test transfer prospectively, including the possibility of failure
## 1. What problem were we trying to solve?
G5 changed the scientific standard. Before looking at the new outcome tables, it froze the operation library, feature vocabulary, arena restrictions and stopping rule. It then tested the same language on a knight+pawn and a bishop+pawn arena.
## 2. What did we actually do?
- Solved 1,211,042 knight-arena states and 1,180,148 bishop-arena states under the common frame.
- Applied the same target language, reachability operation, restoration hypothesis, bridge test and one-move critical-slab vocabulary to both arenas.
- Audited and corrected a provisional bishop baseline rather than carrying the attractive earlier count forward.
## 3. What did we learn or build?
- The same exact target formula transferred to both movement topologies and attracted 366,763 knight wins and 373,545 bishop wins with zero draw false positives.
- The same one-move promotion/interception slab contained 99.03% of the knight and 96.06% of the bishop mixed frontier.
- But friendly-minor restoration failed with 1,086 knight and 1,557 bishop counterexamples, mostly not stalemate.
- The union-bridge operation added zero pure bridge states in both arenas, and both final tails crossed the predeclared lookup-scale threshold.
## 4. Why did that matter?
G5 separated genuinely reusable ideas from arena-specific successes. It proved the programme could preserve a clean negative result without retuning the vocabulary until it passed.
## 5. What did it leave unsolved?
Not every earlier operation transferred. The frozen G5 knight maximum-rank label later could not be reconciled exactly with the newer convention; G6 retained it as a provenance/certificate exception while preserving all membership counts.
# G6 - Turn a collection of experiments into a typed proof system
## 1. What problem were we trying to solve?
G6 was the first deliberately broad programme rather than one arena. It asked whether the accumulated operations could be expressed as reusable proof objects with explicit domains, dependencies, terminal semantics, certificates and failure conditions.
## 2. What did we actually do?
- Built a generic exact-game laboratory with typed material signatures, exact lower-material dependencies, target/attractor operators, grouping/localization tools, regression manifests and supersession ledgers.
- Ran a cross-arena portfolio covering knight/bishop/rook pawn endings, opposing-minor captures, a faithful wrong-colour fortress, two-sided pawn races, double-brink adversarial controls and nested scaling families.
- Promoted Branch-Kernel and finite-n Hyperkernel composition from empirical operations to game-graph theorems, with a separate 100,000-random-graph implementation regression.
- Classified restoration as a domain theorem, not a universal monotonic rule; introduced localization lift so a broad near-equality slab could not masquerade as a selective explanation.
## 3. What did we learn or build?
- FAR5 restoration held over 15,251,718 N/B/R antecedents with zero violations; FAR3 held for sliders and failed for the knight only in one exact 96-state family.
- A bishop c-file branch kernel of 4,302 states generated a 117,430-state strict pure bridge, showing large proof-graph amplification.
- A double-brink negative control destroyed timing-manifold selectivity but yielded a tiny 10-leaf tactical grammar that transferred held-out.
- Faithful terminal modelling changed hundreds of thousands of fortress outcomes compared with an earlier immediate-promotion shortcut, demonstrating that terminal semantics belong inside the proof type.
## 4. Why did that matter?
G6 changed the project’s ontology. The reusable object was no longer “a rule about these squares”; it was a typed proof object with an exact game model, domain, dependencies, truth direction and certificate semantics.
## 5. What did it leave unsolved?
G6 closed with two explicit historical certification exceptions: the original G4 capture/material-reduction implementation graph and the G5 knight rank label. It also showed that critical manifolds are only one compression regime, not a universal law.
# G7 - Climb higher in the material tree and discover a second compositional axis
## 1. What problem were we trying to solve?
G7 prospectively selected richer six- and seven-man families using structural descriptors rather than outcome truth. It then fired the G6 architecture upward and asked whether any genuinely new proof-language concept was needed.
## 2. What did we actually do?
- Solved two six-man bishop+pawn versus bishop+pawn arenas exactly and treated their multiple capture endpoints as typed lower-material targets.
- Used Branch/Hyperkernel composition across alternative material transitions. In one three-target case, a 1,641-state Hyperkernel generated a 7,195-state irreducible region.
- Introduced FILTERED_ATTRACTOR: a proof can now restrict the class of attacker moves used before reaching the target, such as checks only.
- Proved FILTER_PIVOT factorization, then fired it backward across the G6 corpus. The operator transferred exactly even though the usefulness of the specific CHECK language varied sharply by topology.
## 3. What did we learn or build?
- The programme now had two distinct composition axes: destination choice (which certified subgame can be forced) and strategy language (what kind of move can be used during a proof phase).
- A depth-greater-than-three mixed proof DAG was constructed from exact endpoints through Hyperkernel, attractor and strategy-language layers.
- G7 also located an honest implementation frontier: several prospectively frozen 40-48 million-state six-man and 43-46 million-state seven-man arenas did not yield exact full tables inside the declared budget.
## 4. Why did that matter?
G7 showed the architecture could climb materially and could express more than “where we end up”: it could also describe phases of how White forces progress.
## 5. What did it leave unsolved?
The strict breadth gate was not fully met because of the scale holds. One planned family was not executed. G7 therefore closed as a strong scientific pass with an explicit scale/breadth exception rather than pretending the frontier had been cleared.
# G8 - Re-engineer the solver and proof layer, clear the G7 frontier, then climb again
## 1. What problem were we trying to solve?
G8 asked whether G7 had found a fundamental proof-language barrier or merely an implementation barrier. It separated chess truth, proof semantics, certificate representation and solver implementation, then rebuilt the engine around reusable material signatures and independent verification.
## 2. What did we actually do?
- Replaced monolithic optional-material propagation with a material-signature dependency DAG. Each signature is solved once and reused by hash.
- Added compact certificate formats and a standalone verifier that regenerates the local proof obligations instead of trusting the producer’s work queue.
- Recovered every frozen G7 scale hold unchanged, including the high-branch and seven-man arenas.
- Tested six predeclared strategy languages across eight arenas and compiled ordered strategy switching as nested filtered attractors.
- Prospectively froze and solved two restricted eight-man K+B+3P vs K+B+P arenas with 88.36M and 82.55M dependency states, independently Bellman-verified with zero mismatches.
## 3. What did we learn or build?
- The old >180-second G7 high-branch controls collapsed to exact solutions in seconds once repeated legality work and monolithic propagation were removed.
- Compact generating payloads could reconstruct much larger proof regions; the F02 product DAG combined destination Hyperkernel and ordered strategy phases to cover its full 23,327-state derived basin.
- The strongest empirical strategy result was that one ordered semantic handoff covered at least 99.156% of every recovered brink/seven-man target basin, while the fortress F09 remained a sharp negative control at only 55.498%.
- Verification was often cheaper than solving, but not always: F09 and F10 remained explicit cases where verification took longer than the producer solve.
## 4. Why did that matter?
G8 turned the project into a much more credible research platform: exact solving, proof compilation and independent replay became separate, reusable layers, and the implementation frontier moved materially upward.
## 5. What did it leave unsolved?
Restricted eight-man truth is still restricted eight-man truth. The arenas are selected finite families, not “all eight-man chess,” and nothing yet connects them to the standard initial position. Certificate compute/memory economics also remain a real scaling dimension.
# What the whole programme has actually accomplished
- Exact finite-game solving became reusable. The project can define selected chess arenas precisely, solve them exactly, and reuse lower-material results as typed dependencies.
- Symbolic proof operations became real objects. Strict attractors, Branch/Hyperkernel composition and Filter-Pivot are not merely names for patterns; they have explicit game-graph semantics and can be independently checked.
- Proofs became composable. Certified destinations and ordered move-language phases can be chained inside a proof DAG rather than rebuilt as one monolithic search.
- Negative results became part of the method. Lookup-like tails, failed restoration, zero pure bridges, saturated timing slabs, verification costs and scale holds are frozen instead of hidden.
- Certificates became independent artifacts. G8 separates producer work from replayable proof payloads and uses hashes, manifests and standalone verification.
- The software frontier moved upward. The programme progressed from four-man and small pawn arenas to prospectively selected restricted eight-man dependency graphs above 80 million states.
# What the programme has not accomplished
- It has not solved all positions with eight pieces, let alone all positions with more material.
- It has not implemented the complete final rules/state semantics required for a proof from the normal starting position.
- It has not demonstrated automatic discovery of all useful targets, abstractions or strategy languages; substantial research judgement is still involved.
- It has not demonstrated million-node or opening-scale proof-DAG composition under full chess branching.
- It has not built a certified bridge from the standard initial position into the currently solved islands.
- It therefore has not established that White cannot lose from the initial position.
# The simplest way to describe the journey
Pilot 1 showed that exact chess truth can have a shape. Pilot 2 showed the shape was not unique to one fortress. G3 showed that exact layers can be chained and that some boundaries should be left uncompressed. G4 showed the operations survive a harder two-sided race. G5 proved that transfer can be tested honestly and can fail. G6 turned the surviving ideas into a typed proof system. G7 climbed higher and added a language for proof strategy phases. G8 rebuilt the engine and certificate stack, cleared the old scale frontier, and climbed to restricted eight-man arenas. G9’s job is to say what that means for the distance still remaining - without confusing infrastructure success with a solved fraction of chess.
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
