<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G4_Three_Pawn_Compositional_Proof_Technical_Handoff (1).docx
original_sha256: 3b945bdc82ca5672513b1745679d0a2cc1eafe159d0cdeaf25b2babf7a32b4d8
derivative_filename: G4_Three_Pawn_Compositional_Proof_Technical_Handoff (1).md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

G4: Cross-Arena Compositional Proof Replication
Restricted K+d/e pawns versus K+c-pawn: exact finite-state results, inherited lemmas, strict symbolic targets, union bridging, three-clock localization, and the final blockade complexity boundary
| STATUS: G4 FROZEN — PASS. PROOF ARCHITECTURE TRANSFERS; FINAL LOCAL BLOCKADE GRAMMAR REACHES NEAR LOOKUP SCALE. |
| --- |
Frozen research handoff generated from the G4 interactive exact-enumeration session.
11 August 2026
# Executive summary
G4 tested whether the proof architecture developed in Pilots 1–2 and G3 transfers to a materially harder arena with a genuine opposing pawn race. The originally preferred K+B+P versus K+N arena was rejected for this interactive certificate-quality pass because even useful fixed-file/colour restrictions left a raw universe on the order of 10^8 encodings. The predeclared fallback was therefore used: White king plus d- and e-pawns versus Black king plus c-pawn, with ranks 2–7 and both sides to move. The switch is methodological, not outcome-driven: it was declared in the G4 kickoff as the fallback if the primary arena could not be made manageable.
The fully populated arena contains 1,356,280 static-valid states and solves to 933,667 White wins, 357,349 Black wins, and 65,264 draws. A lower-material PROJECT→INHERITS operation yields an exact friendly-pawn restoration lemma certifying 712,156 distinct White wins. An independent semantic target—both White pawns on d7/e7 while Black's c-pawn remains on c3–c7—is universally winning in 31,188 states and, when terminalized strictly, attracts 185,269 White wins. Bridging back to the union of certified predicates raises exact coverage to 792,177 / 933,667 = 84.84% of the White-winning basin, with zero non-win false positives.
After two further exact robust direct regions were removed, the remaining White-king-sensitive frontier was tested against tempo-adjusted promotion and interception clocks. The literal Pilot-1 hypothesis—exact zero-slack localization—fails. However, 9,513 / 9,740 mixed reduced geometries (97.67%) lie within one full move of at least one of three equality surfaces: White-vs-Black promotion race, BK arrival at the current pawn front, or BK rendezvous with a moving pawn path. The 227 off-surface geometries are not diffuse: all have Black's pawn on c2–c4, BK within two files of the d/e corridor, and White pawn rank gap at most three.
The final bounded local-grammar test closes G4. Across those 227 blockade-conversion geometries there are 11,360 legal WK placements: 10,033 Black wins, 734 White wins, and 593 draws. Using state-identifying board coordinates an exact decision tree requires 208 leaves for only 227 reduced geometries; with the bounded semantic distance/orientation feature families tried, substantial outcome collisions remain. This is near lookup scale and triggers the predeclared stopping rule. G4 therefore passes through the principled-complexity-boundary branch: the reusable proof operations transfer strongly, while the final conversion topology remains genuinely local and fragmented.
| Quantity | Frozen G4 value | Status |
| --- | --- | --- |
| Fully populated static-valid states | 1,356,280 | Exact count |
| White / Black / Draw | 933,667 / 357,349 / 65,264 | Exact solve |
| Initial reduced geometries | 25,578 | Exact grouping |
| Initial mixed geometries | 12,086 | Exact grouping |
| Friendly-restoration certified wins | 712,156 distinct | Computer-assisted theorem |
| d7/e7 direct target | 31,188 wins; 0 exceptions | Computer-assisted theorem |
| Strict d7/e7 attractor | 185,269 wins; 0 non-wins | Computer-assisted theorem |
| Predicate-union bridge | 792,177 wins = 84.84% | Computer-assisted theorem |
| Post-bridge unexplained White wins | 141,490 | Exact count |
| Two robust direct regions | +3,385 wins | Computer-assisted implications |
| Post-robust unexplained White wins | 138,105 | Exact count |
| WK-sensitive mixed geometries | 9,740 | Exact grouping |
| Within one move of 3 clock surfaces | 9,513 / 9,740 = 97.67% | Exact structural count |
| Off-surface blockade tail | 227 geometries | Exact count |
| Tail WK placements | 11,360 = 734 W + 593 D + 10,033 B | Exact count |
| Exact coordinate-tree cost on tail | 208 leaves / 227 geometries | Compression observation |
# 1. Research question and gate
G4's north-star question was whether lower-material projection, semantic certified targets, strict adversarial reachability, and predicate-union bridges form a reusable proof language when the movement/race topology changes. The gate did not require the third arena to be simple. It required useful exact inheritance or a small exception family; at least one nontrivial semantic target; strict reachability into a target; additional coverage from a union bridge; localization of the unresolved region; and at least one genuinely reused proof operation without square-level special casing.
Frozen verdict: all of those architectural criteria were met. The final local grammar did not compress, and that negative result is part of the pass rather than a defect to tune away.
# 2. Arena and terminal semantics
- White pieces: king, d-pawn, e-pawn. Black pieces: king, c-pawn.
- Each pawn is fixed to its home file and, in the fully populated slice, occupies ranks 2 through 7. Both sides to move are represented.
- The implementation also admitted absent-pawn states internally so legal captures reduce material into exact lower-material states inside the same solved graph rather than artificial exits.
- Ordinary king legality, king captures, pawn pushes, legal initial double pushes, pawn captures, promotion, check, checkmate, and stalemate were represented. En passant, repetition, and move-count claim state were omitted.
- Static validity was used rather than historical reachability from the initial position.
- Ordinary checkmate was classified as a win for the mating side. This differs from the frozen Pilot-2 no-move convention by exactly the two mirror positions documented in G3.
# 3. Implementation regression and corrections
Two early implementation errors were caught before any G4 outcome counts were frozen: a pawn-code/rank mapping error and omission of king captures. All affected provisional outcome counts were discarded. The corrected implementation was then checked against the embedded c-pawn-absent d+e versus K slice.
The embedded slice contains exactly 236,976 static-valid states, matching Pilot 2. Under ordinary checkmate semantics it solves to 228,502 White wins and 8,474 draws, exactly reproducing G3's documented two-position discrepancy from the frozen Pilot-2 convention of 228,500 / 8,476. This regression is the principal solver checksum for the G4 session.
# 4. Exact baseline and first dimensional collapse
The fully populated K+d+e versus K+c slice contains 1,356,280 static-valid states.
| Outcome | States | Share |
| --- | --- | --- |
| White win | 933,667 | 68.84% |
| Black win | 357,349 | 26.35% |
| Draw | 65,264 | 4.81% |
Grouping out White's king by (Pd, Pe, Pc, BK, side to move) yields 25,578 reduced geometries: 13,035 universal White-win, 457 universal Black-win, 0 universal draw, and 12,086 mixed. Thus the new arena begins with a much larger king-sensitive population than Pilot 2.
# 5. Lower-material projection: what transfers and what fails
## 5.1 Enemy-pawn restoration fails
Deleting Black's c-pawn and asking whether a White win survives restoration of the enemy pawn is not monotone. There are 1,308,601 lower-material White-winning antecedents, but only 933,584 remain White wins after restoration; 375,017 become draws or Black wins. This falsifies naïve material-restoration inheritance.
## 5.2 Friendly-pawn restoration transfers
The faithful Pilot-2 analogue is to delete one White pawn, solve the resulting K+P versus K+P position with the same kings and move order, and then restore the friendly pawn. Across both projections there are 1,083,341 winning lower-material antecedent occurrences; 1,083,160 remain White wins. Only 181 projection occurrences fail, corresponding to 177 unique full states.
Of the 181 projection failures, 177 have the restored pawn adjacent to WK. The four non-adjacent failures form one compact family: White pawns on d4/e4, BK on e1, WK on f3 or f4, with either Pc4 and White to move or Pc5 and Black to move.
THEOREM — Friendly-pawn restoration (finite-arena form). If deleting either White pawn yields an exact White-winning lower-material position, then restoring that pawn is also White-winning whenever the restored pawn is non-adjacent to WK, except for the four-position d4/e4–Ke1 obstruction family. Exhaustive application certifies 712,156 distinct full-material White wins with zero counterexamples.
# 6. Arena-specific semantic target and strict stepping stone
An independent exact target was discovered in the genuine cooperative region: Pd=d7, Pe=e7, and Pc on c3–c7. Across the full arena there are 31,188 such states and all are White wins.
To test compositional value rather than descriptive value, this predicate alone was terminalized as success. Promotion and material-reduction exits were failures for this reachability objective. The exact adversarial attractor contains 185,269 White wins and zero draws/Black wins, with maximum target-entry rank 23 plies. Thus 154,081 states force actual entry into the semantic target beyond direct membership.
# 7. Predicate-union bridge
The certified library was defined as the union of the friendly-restoration predicate and the direct d7/e7 target. Terminalizing that union and computing strict reachability produces 792,177 certified White wins with zero non-win false positives: 84.84% of the complete White-winning basin.
Counting inheritance plus the independent d7/e7 attractor first gives 723,163 wins; the union-return operation therefore contributes a further 69,014 wins that are not certified by either mechanism separately. This is the direct G4 replication of G3's predicate-union bridge operation.
# 8. Two additional robust interior regions
Before attacking the mixed boundary, two further zero-counterexample direct-winning regions were removed from the post-bridge residual. Let mW be White's fastest pawn-push count to promotion, mB Black's c-pawn push count, and let the BK distance to the nearer White pawn use Chebyshev distance.
Region A: mB − mW >= 4 and BK is at least two king-steps from both White pawns. This contributes 1,297 residual White wins.
Region B: Pc is on c6 or c7 and BK is at least five king-steps from both White pawns. This contributes 2,128 residual White wins.
The regions overlap in 40 states, so their union removes 3,385 exact residual White wins. The unexplained White basin falls from 141,490 to 138,105.
# 9. Three-clock critical-manifold experiment
## 9.1 Clock definitions
All clocks were expressed in plies so side-to-move is represented directly. Let mW be the minimum pushes for White's faster pawn to promote and mB the minimum pushes for Black's c-pawn. TW = 2*mW − 1[White to move], TB = 2*mB − 1[Black to move], and R = TB − TW is the raw promotion-race slack.
For direct BK interception, let dC be BK's Chebyshev distance to the current square of the nearer White pawn. TC = 2*dC − 1[Black to move], and I = TW − TC. A third moving-path quantity J compares earliest BK arrival with earliest pawn arrival over squares on the White pawns' fastest promotion paths.
## 9.2 Exact-zero-surface hypothesis is falsified
Because alternating plies make the natural parity tie |S|=1 rather than S=0, the strict near-tie test |R|<=1 OR |I|<=1 was evaluated first. It contains only 6,965 / 9,740 = 71.51% of WK-sensitive mixed geometries. Therefore the Pilot-1 exact zero-slack phenomenon does not transfer literally.
## 9.3 One-move critical slab
Widening by exactly one full chess move gives |S|<=3. The union |R|<=3 OR |I|<=3 contains 8,943 / 9,740 = 91.82% of mixed geometries. Replacing the raw race with moving-path interception gives |I|<=3 OR |J|<=3 in 8,977 / 9,740 = 92.17%.
Using all three clocks, |R|<=3 OR |I|<=3 OR |J|<=3 contains 9,513 / 9,740 = 97.67% of the WK-sensitive mixed geometries. This is a structural localization count, not an outcome classifier: the same slabs also contain universal-win and non-win geometries.
# 10. The 227 off-surface blockade-conversion geometries
Exactly 227 mixed geometries remain outside all three one-move clock slabs. They are sharply localized rather than diffuse. Every one satisfies Pc on c2–c4, BK file-distance at most two from the d/e corridor, and |rank(Pd)−rank(Pe)|<=3.
| Property | Exact tail result |
| --- | --- |
| Side to move | 217 Black / 10 White |
| Pc rank | c2–c4 only |
| BK corridor distance | <= 2 in all 227 |
| White pawn rank gap | 0–3 only |
| Race slack R | −5, −7, or −9 only |
| Direct interception slack I | +5 or +7 only |
| Dominant advanced-blockade family | 209 / 227: Black to move and BK 1–3 ranks ahead of advanced White pawn |
These are not race ties. Black is nominally ahead in the promotion race and geometrically well placed to reach the White pawn front, yet WK placement changes W/D/L truth. The appropriate interpretation is blockade conversion: the coarse clocks have already favoured Black, and the remaining question is whether exact king topology converts that advantage.
# 11. Final bounded local-grammar test
The final test deliberately targeted only these 227 geometries, under the same anti-overfitting rule used in G3. They contain 11,360 legal WK placements: 10,033 Black wins, 734 White wins, and 593 draws.
A bounded semantic feature language was tested around: pawn ranks/gap; BK corridor and advanced-pawn relation; WK distances to BK and each pawn; WK distance to pawn-front/support squares; king alignment/opposition-style relations; and corridor-side/orientation atoms. These coarse semantic vectors remain information-incomplete: hundreds of feature cells contain more than one exact outcome. Adding state-identifying board coordinates makes the population exactly separable, but an exact decision tree then requires 208 leaves for only 227 reduced geometries.
| Exact coordinate tree depth | Training accuracy | Leaves |
| --- | --- | --- |
| 6 | 96.25% | 45 |
| 8 | 98.17% | 99 |
| 10 | 99.57% | 152 |
| 12 | 99.87% | 195 |
| 14 | 99.991% | 207 |
| 16 | 100% | 208 |
This is the stopping signal. Exact description cost is essentially one leaf per residual geometry. Continuing by adding absolute-square or micro-orientation exceptions would amount to reconstructing a lookup table rather than discovering a reusable lemma. The final 227 are therefore frozen as a principled local-topology complexity floor under the tested grammar.
# 12. Evidence ledger
| Claim | Result | Status |
| --- | --- | --- |
| Embedded Pilot-2 checksum | 236,976 states; 228,502 W / 8,474 D under ordinary mate semantics | Exact regression |
| G4 baseline | 933,667 W / 357,349 B / 65,264 D | Exact solve |
| Enemy restoration | 375,017 failures | Falsified hypothesis |
| Friendly restoration | 712,156 distinct wins, zero exceptions under stated predicate | Computer-assisted theorem |
| d7/e7 predicate | 31,188 / 31,188 wins | Computer-assisted theorem |
| Strict target attractor | 185,269 wins; zero non-wins; max rank 23 | Computer-assisted theorem |
| Union bridge | 792,177 wins = 84.84%; zero non-wins | Computer-assisted theorem |
| Robust direct regions | 3,385 additional residual wins | Computer-assisted implications |
| Three-clock slab | 9,513 / 9,740 mixed geometries = 97.67% | Exact structural count |
| Off-surface localization | 227; Pc c2–c4, BK corridor<=2, gap<=3 | Computer-assisted one-way localization |
| Tail population | 11,360 WK placements = 734 W + 593 D + 10,033 B | Exact count |
| Tail exact grammar | 208 coordinate-tree leaves / 227 geometries | Compression observation |
# 13. Falsified, weakened, and superseded hypotheses
- Primary K+B+P vs K+N arena was not executed in this interactive pass because the restricted raw scale remained around 10^8; the predeclared K+2P vs K+P fallback was used.
- Naïve enemy-pawn restoration is not a reusable monotonic inheritance law.
- Pilot 2's rank-gap-1 cooperative theorem does not transfer to the three-pawn arena.
- Exact Pilot-1-style zero-slack localization does not transfer literally; a one-move-thick multi-clock slab is required.
- The clock surfaces localize strategic interaction but are not outcome biconditionals.
- The final blockade-conversion population does not admit a compact exact grammar under the bounded semantic DSL tried.
- Any provisional reachability result from the independently reconstructed post-robust graph that exhibited move-semantic mismatch was discarded and is not part of this handoff.
# 14. Proof discipline and scope
All exact/computer-assisted statements are finite-universe claims conditional on the stated implementation and model. Decision-tree leaf counts are representation observations, not mathematical invariants. The arena uses static validity rather than proof of historical reachability and omits repetition/en-passant/move-count claim state. Publication-level use should independently regenerate the graph, persist deterministic bitsets/CSVs and hashes, and emit zero-counterexample logs for every promoted predicate.
# 15. Frozen G4 conclusion
G4 PASSES. The strongest result is architectural, not percentage-based. A materially harder arena with a genuine opposing pawn race reuses lower-material PROJECT/INHERITS, exact semantic TARGET, strict ATTRACTOR, and predicate-union BRIDGE. The chess-specific Pilot-2 formation theorem fails, but the proof operations survive. After the robust interior is removed, 97.67% of WK-sensitive reduced geometries lie in a one-move neighbourhood of three race/interception surfaces; the remaining 2.33% localize to a small blockade-conversion pocket. That pocket then reaches near lookup-scale under a bounded local grammar, reproducing the mobile-king complexity warning of Pilots 1 and 2/G3.
FROZEN G4 VERDICT: PASS — CROSS-ARENA PROOF-LANGUAGE REUSE IS STRONGLY SUPPORTED; THE CRITICAL BOUNDARY IS A THIN MULTI-CLOCK SLAB PLUS A LOCAL BLOCKADE SINGULARITY, AND THE FINAL SINGULARITY HITS A PRINCIPLED DESCRIPTION-COST FLOOR.
# Appendix A. Reproduction checklist
1. Recreate the optional-pawn internal graph and fully populated 1,356,280-state slice.
1. Reproduce the embedded Pilot-2 236,976-state checksum and ordinary-mate 228,502 / 8,474 split.
1. Reproduce 933,667 / 357,349 / 65,264 full W/B/D truth.
1. Recompute both friendly-pawn projections and the 177 unique restoration exceptions; verify the four non-adjacent obstruction states.
1. Flatten and scan the friendly-restoration predicate; confirm 712,156 distinct certified wins.
1. Verify 31,188 d7/e7 target states and strict 185,269-state attractor with zero non-wins.
1. Recompute predicate-union bridge and confirm 792,177 certified wins.
1. Recreate the two robust direct regions and 3,385-state union.
1. Regenerate 9,740 mixed reduced geometries after robust subtraction.
1. Recompute R, I, and J and verify 9,513 / 9,740 within |.|<=3 of at least one surface.
1. Regenerate the 227 off-surface geometries and all exact localization counts.
1. Regenerate their 11,360 WK placements and 734 W / 593 D / 10,033 B split.
1. Re-run bounded grammar audit; document semantic collisions and the 208-leaf exact coordinate-tree reference.
1. Persist model version, source revision, bitset hashes, residual CSV hashes, rank histograms, and zero-counterexample logs.
