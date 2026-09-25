<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: Pilot_1_Follow_On_Experimental_Program.docx
original_sha256: 67e2e9e799f0e51ab395b32756b727798c63fec167d5b51ffc1e7bf5b0c7b74a
derivative_filename: Pilot_1_Follow_On_Experimental_Program.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

# Follow-On Experimental Program After Pilot 1
*Replication, falsification, scaling gates, and candidate arenas for symbolic backward-attractor research*
SEPARATE NEXT-STEPS MEMO — NOT PART OF THE FROZEN PILOT 1 RESULT
10 August 2026
Research handoff generated from the interactive Pilot 1 scratch experiments.
# Purpose
This memo contains the forward-looking recommendations intentionally excluded from the frozen Pilot 1 technical report. Pilot 1 has already answered its own question: symbolic structure exists in at least one exact chess attractor, but complexity emerges on mobile king-interference boundaries. The next programme should test whether the observed hierarchy replicates outside the specially favourable wrong-bishop rook-pawn geometry.
| Primary next scientific question<br>Does the same hierarchy — robust safe interior -> zero-slack critical surfaces -> small local obstruction grammar — appear in a materially or geometrically different exact chess arena? |
| --- |
# 1. Gate 0: turn Pilot 1 into a reproducible certificate
Before interpreting cross-arena results, the interactive scratch result should be recreated in the repository as a deterministic baseline. This is not a new scientific experiment; it is the minimum engineering gate needed to ensure later comparisons are meaningful.
1.  Re-implement or port the exact four-man and KPK solvers with explicit model versioning.
2.  Emit all counts and bitsets listed in Appendix D of the technical handoff.
3.  Independently cross-check legality and a sample of successor sets.
4.  Persist the 1,181 residual geometries, final 5,623 bad placements, race-surface labels, mechanism labels, diagonal segments and pawn-surface grammar as machine-readable fixtures.
5.  Treat any mismatch with the frozen counts as a blocking issue until explained.
# 2. Replication experiment: choose a structurally different arena
The strongest next test is not “more pieces” for its own sake. It is a second exact arena in which the drawing/non-loss mechanism is qualitatively different enough that the same representation cannot succeed merely because of the h8 corner geometry.
## 2.1 Preferred candidate A: K + two pawns versus K
A two-pawn versus king arena is attractive because it removes the bishop entirely while retaining interacting promotion races, king interception, mutual blocking, and multiple target files. It tests whether zero-slack manifolds and local grammars emerge from pawn/king topology alone. A tablebase-exact W/D/L truth source is straightforward to generate internally at this material size.
- Prefer two pawns with restricted but nontrivial file families (for example adjacent pawns or rook-pawn plus neighbour) before all file pairs.
- Use an exact non-loss target defined by solved W/D/L, not an engine score.
- Mine boundaries for race slacks, king-access regions, opposition motifs, protected-passer relations and promotion-square control.
- Ask whether mixed frontiers again concentrate on equality/zero-slack surfaces rather than throughout the state volume.
## 2.2 Preferred candidate B: a second fortress with a different slider topology
A five-man bishop/pawn fortress family — for example K+B+P versus K+B with carefully chosen opposite-colour or blocking geometry — is the natural second replication after the pawn-only arena. It preserves slider obstruction but removes the special property that one bishop can never control the promotion corner.
The scientific value is high if the representation again factors into a few active geometric manifolds; it is equally high if the frontier explodes, because that would locate the boundary of Pilot 1’s generality.
## 2.3 Candidate C: K+B+P versus K+N or another five-man mixed-piece arena
This is a harder but valuable third candidate because knight influence is local/non-linear rather than diagonal. If a compact predecessor grammar exists here, it would provide much stronger evidence that the phenomenon is not an artefact of line-piece geometry.
# 3. Experimental protocol for every replication arena
1.  Define the exact state universe and legal model before solving anything; publish raw and static-valid counts.
2.  Establish exact W/D/L or another exact target set. No engine evaluation as ground truth.
3.  Compute the exact controllable-predecessor fixed point and preserve every boundary layer.
4.  Group out one positional dimension at a time (piece square, side to move, material subconfiguration) and measure which variables genuinely matter.
5.  Derive simple race, distance, control, mobility and topology features from chess semantics.
6.  Locate the mixed frontier and ask whether it lies on low-codimension equality surfaces.
7.  Use classifiers only for discovery; convert every claimed lemma into an explicit predicate and exhaustively verify it.
8.  Decompose residual masks into intervals/regions/templates if the relevant piece has a geometric movement manifold.
9.  Run resource-freezing or move-subset variants to identify which adversarial resource creates each boundary.
10.  Quantify compression at each hierarchy level and record where exact complexity begins to rise.
# 4. Replication success criteria
Do not call the programme successful merely because some rules can be learned. Require evidence of the same qualitative mechanism. A strong replication would satisfy most of the following:
| Criterion | Strong signal | Warning / failure signal |
| --- | --- | --- |
| Boundary localization | Most mixed states lie on a small number of exact equality/critical surfaces. | Mixed states fill a substantial interior volume with no low-dimensional localization. |
| Geometric grammar | Piece-dependent residuals reduce to intervals, regions, masks or a few parameterized templates. | Rules require near-square-by-square exception lists. |
| Compositionality | Predecessor of a compact predicate admits another compact predicate family. | One compact layer is followed by abrupt description explosion. |
| Mechanism separation | Resource-freezing isolates a few independent adversarial mechanisms. | Failures require highly entangled multi-piece interaction almost everywhere. |
| Exactness | Useful rules remain zero-false-positive under exhaustive verification. | Only approximate classifiers work; exact rules are huge. |
| Cross-arena recurrence | Same abstract constructs reappear with different pieces. | Pilot 1 constructs are specific to h8/wrong-bishop geometry. |
# 5. Kill criteria
| The programme should be willing to fail<br>The value of the next experiments is precisely that they can falsify the broader hypothesis cheaply. Do not rescue the idea by adding opaque features until a classifier fits. |
| --- |
- Exact predicate description size grows roughly in proportion to enumerated state count across successive predecessor layers.
- The mixed frontier does not concentrate on a small number of low-dimensional surfaces.
- Each new layer requires a largely unrelated rule family rather than parameter changes to recurring motifs.
- Resource-freezing does not decompose the difficulty into a small number of mechanisms.
- High accuracy requires exact square IDs and long exception lists, with little advantage over a lookup table.
- The representation is not stable when the target draw set is modestly broadened.
- A second arena shows no meaningful analogue of the Pilot 1 hierarchy.
# 6. Improve the symbolic representation before scaling material aggressively
Pilot 1 suggests that “predicate” should not mean a flat CNF/DNF over square features. The useful representation was hierarchical: race surface -> active movement manifold -> local interval -> small correction. A follow-on system should represent this hierarchy directly.
## 6.1 Suggested predicate DSL
- Distance/race atoms: Chebyshev distance, pawn moves to promotion, tempo-adjusted slack.
- Region atoms: king in rectangle/diagonal cone/critical-square neighbourhood.
- Movement-manifold atoms: bishop diagonal band, rook file/rank, knight neighbourhood, pawn corridor.
- Projection operations: closest point on a movement manifold to a king or target.
- Interval/ray constructors with endpoint offsets from a projection.
- Attack/control and blocker relations.
- Move-subset reachability: can a resource neutralize/interfere within n plies?
- Parameterized union/intersection of a small number of such objects.
The objective should be minimum exact description length under a grammar whose primitives have chess meaning, rather than minimum generic decision-tree depth.
# 7. Automated lemma discovery and certification loop
| 1. Solve exact finite arena.<br>2. Select boundary / residual set R.<br>3. Generate candidate semantic abstractions A1...Ak.<br>4. Fit/discover a compact candidate rule P.<br>5. Exhaustively verify P => R (or P <=> R where intended).<br>6. Return all counterexamples.<br>7. Refine the grammar using counterexample structure, not arbitrary features.<br>8. Store P as a certified lemma with domain, coverage, complexity and witness strategy.<br>9. Use certified lemmas as targets for the next predecessor layer. |
| --- |
For existential Black nodes, store a witness move for each certified state; for universal White nodes, store or hash the complete successor audit. This converts symbolic discoveries into proof-carrying artifacts rather than prose descriptions.
# 8. Test compositional stepping stones explicitly
Pilot 1 mostly compressed a single fixed-point basin after solving it. The next programme should test the stronger original hypothesis directly: can a sequence of symbolic predicates be composed as certified stepping stones?
P3  =>  Black can force P2  =>  Black can force P1  =>  Black can force D0.
For each candidate Pi, require exact adversarial verification over the entire predicate set, not just membership in an already solved cumulative attractor. Extract witness strategy maps and measure whether the symbolic complexity of Pi remains stable as the chain moves outward.
# 9. Broaden the target set deliberately and measure representation stability
A crucial stress test is to replace a single sanctuary target with a union of independently certified non-loss mechanisms: tablebase draws, dead material reductions, stalemate regions, fortress predicates, and other safe exits. Pilot 1 already showed why this matters: an artificially narrow target created 18,404 spurious bishop-sensitive states.
For each broadened target, measure both basin growth and symbolic-description growth. A useful representation should absorb additional exact draw mechanisms without description complexity increasing as rapidly as the state count.
# 10. Quantitative research dashboard
| Metric | Why it matters |
| --- | --- |
| \|D_n\| and \|B_n\| | Raw attractor and boundary growth. |
| Exact predicate coverage | How much of solved space is certified symbolically. |
| Predicate grammar size | Literals, AST nodes, region/interval objects, template count. |
| States per symbolic atom | Basic compression efficiency. |
| Number/codimension of critical surfaces | Whether complexity is localized. |
| Residual exception rate | How much square-level fragmentation remains. |
| Mechanism entropy | How many independent counterplay mechanisms are needed. |
| Cross-layer template reuse | Whether stepping stones are compositional. |
| Cross-arena template reuse | Whether abstractions generalize beyond one ending. |
| Proof verification cost | Whether exact checking remains cheap relative to raw solving. |
# 11. Suggested sequence of experiments
1.  Certificate Pilot 1 exactly in the repository.
2.  Run a structurally different four-man pawn/king replication (prefer K+2P vs K restricted families).
3.  If the hierarchy replicates, run a five-man slider fortress replication.
4.  Introduce the hierarchical predicate DSL and re-express both pilots in the same language.
5.  Test explicit Pi -> Pi-1 stepping-stone composition rather than only post-hoc basin compression.
6.  Broaden each target set by adding exact alternative draw mechanisms and measure description stability.
7.  Only after successful cross-arena replication should material count or board-space scale become the primary axis of expansion.
# 12. Decision gates
| Gate | Advance if... | Stop / rethink if... |
| --- | --- | --- |
| G1 — Reproduction | Pilot 1 final counts and lemmas reproduce exactly. | Unexplained discrepancy in state model or certificates. |
| G2 — Second arena | Mixed frontier again localizes to a few semantic critical surfaces. | Frontier is volumetric/unstructured. |
| G3 — Exact grammar | Large fractions admit exact compact hierarchical predicates. | Exactness requires lookup-scale exceptions. |
| G4 — Composition | Several certified predicates force one another with reusable grammar. | Each stepping stone needs unrelated rules. |
| G5 — Target robustness | Adding safe mechanisms grows state coverage faster than description complexity. | Grammar explodes when target is broadened. |
| G6 — Scale | Representation cost grows sublinearly enough to justify more material. | Symbolic cost tracks raw state explosion. |
# 13. Recommended research-agent kickoff framing
The next agent should be told that the objective is not to “prove chess is a draw” and not to reproduce Pilot 1 by hard-coding its discovered rules. The objective is to test whether a general discovery/certification method can recover analogous hierarchical structure in a second exact arena. The agent should actively try to falsify the representation hypothesis and should report a negative replication without softening it.
| North-star question for the next agent<br>Do exact adversarial predecessor regions in a second chess arena decompose into a robust interior plus a small number of low-dimensional critical surfaces whose residual piece geometry admits a compact, compositional, exhaustively verifiable grammar? |
| --- |
# 14. What not to do next
- Do not jump directly to the initial chess position or 32-piece state space.
- Do not replace exact W/D/L truth with Stockfish centipawn evaluations.
- Do not count a neural classifier or high-accuracy decision tree as a symbolic proof.
- Do not continue polishing the wrong-bishop h-pawn arena indefinitely; it has already answered the pilot question.
- Do not scale before reproducing the corrected KPK and terminal semantics.
- Do not hide representation failure by adding raw square IDs or memorized exception lists without reporting description growth.
# Closing recommendation
The best use of the Pilot 1 result is a disciplined replication programme. The wrong-bishop fortress has demonstrated that exact backward attractors can expose symbolic manifolds and local grammars; the king surface has demonstrated that complexity can also grow rapidly. The next evidence that matters is whether that same hierarchy appears in a different exact game geometry under a common discovery language.
