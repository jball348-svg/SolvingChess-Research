<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: Pilot_2_K2P_vs_K_Technical_Handoff.docx
original_sha256: 61d0b039202eb6562360b2b1dc14951b93999bbc4f983ec8c3773c45d68c64ea
derivative_filename: Pilot_2_K2P_vs_K_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

# Pilot 2: Symbolic Composition in K + Two Pawns versus K
Frozen technical handoff, exact finite-state results, compositional lemmas, residual frontier, and complexity warning
> STATUS: PILOT 2 FROZEN — G2 PASSED; 97.69% OF WINS COVERED BY TWO EXACT COMPOSITIONAL MECHANISMS
10 August 2026
Research handoff generated from the exact interactive Pilot 2 experiments.
# Executive summary
Pilot 2 was the deliberately different replication arena proposed after Pilot 1. It removes the bishop and fortress corner entirely and asks whether exact chess truth again admits a hierarchy of robust interior, low-dimensional critical frontier, and reusable symbolic stepping stones. The arena is White king plus adjacent central d- and e-pawns versus Black king, with each pawn on ranks 2–7.
The answer is a strong positive replication with a genuine complexity warning. The exact arena contains 236,976 static-valid states, of which 228,500 are White wins and 8,476 draws. An exact lower-material KPK inheritance lemma certifies 197,108 of those wins. After removing inherited one-pawn wins, a second exact cooperative predicate — the pawns being exactly one rank apart — is universally winning in its residual domain and, when used as an adversarial reachability target, certifies another 26,122 wins. Together the two mechanisms cover 223,230 / 228,500 = 97.69% of the complete winning basin.
The final unexplained region is small and sharply localized around Black's blockade. After both mechanisms are removed, 13,736 states remain: 5,270 wins and 8,466 draws, grouped into 520 pawn/BK/turn geometries. Of these, 214 are White-king-sensitive. Every one of those 214 places Black's king within two files of the d/e pawn corridor and from one rank behind to two ranks ahead of the advanced pawn. The last frontier remains local and structured, but it did not collapse to a tiny exact contact-mask grammar under the representations tried.
| Quantity | Frozen value | Status |
| --- | --- | --- |
| Raw encodings | 294,912 | Exact count |
| Static-valid states | 236,976 | Exact count |
| White wins / draws | 228,500 / 8,476 | Exact W/D solve |
| Maximum White-win rank | 23 | Exact attractor |
| KPK(d) valid / wins / draws | 41,358 / 28,853 / 12,505 | Exact subsolver |
| KPK(e) valid / wins / draws | 41,358 / 28,853 / 12,505 | Exact subsolver |
| KPK inheritance certified wins | 197,108 (86.26% of all wins) | Computer-assisted theorem |
| Cooperative residual after inheritance | 39,858 = 31,392 wins + 8,466 draws | Exact count |
| Rank-gap-1 universal target | 14,382 states / 504 geometries | Computer-assisted theorem |
| Wins forcing rank-gap-1 target | 26,122 / 31,392 cooperative wins | Exact reachability |
| Combined certified wins | 223,230 / 228,500 = 97.69% | Exact composition |
| Final residual | 13,736 = 5,270 wins + 8,466 draws | Exact count |
| Final reduced geometries | 520 = 264 universal win + 214 mixed + 42 universal draw | Exact grouping |
# 1. Research question and experimental logic
Pilot 1 established that one wrong-colour-bishop rook-pawn attractor compressed hierarchically, but its special corner and diagonal geometry could have been doing most of the work. Pilot 2 therefore asks a stronger replication question: does a materially and geometrically different exact arena yield reusable exact predicates that compose under adversarial play?
The chosen d+e adjacent-pawn arena retains promotion races, king interception, mutual pawn support, move order, captures, and stalemate, while removing sliders and any preselected fortress square. The experiment was not designed to find a generic tablebase heuristic. Exact W/D truth and exact reachability were the ground truth throughout.
# 2. Exact arena and conventions
- White pieces: king, d-pawn, e-pawn. Black piece: king.
- Each pawn occupies its home file and a rank from 2 through 7.
- Both sides to move are represented.
- Ordinary king legality, pawn pushes, legal initial two-square pawn moves, captures, promotion, check legality, and stalemate are represented under the solver model.
- Static validity is used rather than proof of historical reachability from the initial chess position.
- Vertical reflection d↔e is an exact symmetry of the selected arena.
Raw encoding count: 64 WK squares × 6 d-pawn ranks × 6 e-pawn ranks × 64 BK squares × 2 sides to move = 294,912.
# 3. Exact W/D baseline
The finite game was solved as a White-win attractor. Promotion is a White-winning terminal. Legal pawn captures reduce material and are classified by exact lower-material KPK truth where applicable; draw terminals remain outside the White-win set. The fixed point contains 228,500 wins and 8,476 draws, with maximum win rank 23.
The central-file choice supplies a strong implementation checksum: reflecting every valid state across the vertical axis and swapping d/e pawn identities produced zero W/D mismatches over all 236,976 states.
# 4. First dimensional collapse: group out White's king
States were grouped by (d-pawn rank, e-pawn rank, BK square, side to move), varying the White king over every legal square. There are 4,330 such reduced geometries. Exactly 4,072 are wins for every legal WK square, 258 are mixed, and none are draws for every legal WK square. All 8,476 draws lie inside those 258 mixed geometries.
| Reduced class | Geometries | Interpretation |
| --- | --- | --- |
| Universal win | 4,072 | WK square does not affect W/D |
| Mixed | 258 | Some legal WK squares win and some draw |
| Universal draw | 0 | None in the initial grouping |
# 5. Autonomous-pawn experiment
To separate pawn strength from king assistance, White's king was removed as an active resource and the pawn pair was solved against BK. Of the 4,330 pawn/BK/turn geometries, 2,958 allow the pawns to force promotion autonomously and 1,372 do not.
Of the 258 mixed full-game geometries, 254 lie in the autonomous-pawn failure region. The remaining four are not strategic exceptions: each contains one immediate stalemate WK placement. Thus autonomous pawn strength almost perfectly explains where WK sensitivity can begin.
# 6. Falsified stepping-stone hypothesis: autonomous entry
A stronger hypothesis was tested: perhaps hard wins work by escorting the pawns until they enter an autonomous-pawn winning geometry. The autonomous-winning region was terminalized as a target and promotion/material-reduction shortcuts were treated as failures for this reachability objective.
Globally, 214,590 / 228,500 wins (93.9%) can force this target. But on the 254 genuinely strategic geometries only 1,472 / 5,366 winning WK placements (27.4%) can do so, and every one of the 254 contains wins that bypass autonomous entry. Therefore autonomous entry is not the general mechanism of the hard frontier.
# 7. White-king region topology and contact locality
The 254 strategic geometries contain 13,838 legal WK placements: 5,366 wins and 8,472 draws. Their raw square masks are numerous, but their topology is simple. In 182/254 geometries both winning and drawing WK sets are single king-move-connected regions; another 54 have one connected winning region and two drawing components. Overall 236/254 = 92.9% have a single connected winning region.
| Draw components | Win components | Geometries |
| --- | --- | --- |
| 1 | 1 | 182 |
| 2 | 1 | 54 |
| 1 | 2 | 16 |
| 3 | 1 | 2 |
Across the strategic frontier there are 2,738 winning WK squares adjacent in king-move geometry to a drawing WK square. Relative to the nearest pawn, the winning-side boundary uses only 36 offsets. 81.1% lie within Chebyshev radius 2 of a pawn, 99.4% within radius 3, and all within radius 4. In 252/254 geometries the frontier touches a WK square adjacent to a pawn; the remaining two first touch at distance 2.
However, exact pawn-adjacent contact masks did not reduce to a tiny vocabulary: after symmetry/translation normalization roughly 65 distinct masks remained among the 127 mirror-canonical strategic cases, and a flat semantic exact tree required roughly 92 leaves. This is a real complexity warning, not a result to conceal.
# 8. Exact KPK inheritance lemma
The decisive mechanism-separation experiment removed either pawn and classified the corresponding KPK state with the same kings and side to move. Across the complete arena, 197,118 positions have at least one corresponding one-pawn ending that is winning for White. In the full two-pawn game, 197,108 of those are wins and exactly 10 are draws. All ten draws are immediate stalemates.
> Theorem — KPK inheritance. Within this arena, if either corresponding K+d-pawn vs K or K+e-pawn vs K state is a White win, then the full two-pawn state is also a White win unless the added pawn makes the position immediately stalemate.
This exact inherited predicate certifies 197,108 / 228,500 = 86.26% of all White wins. It is a reusable lower-material theorem, not a classifier fitted to the two-pawn table.
The ten stalemate exceptions form two mirror families: Ke6 with Pe7 and Pd on d2–d6 against Ke8, Black to move; and the reflected Kd6 with Pd7 and Pe on e2–e6 against Kd8, Black to move.
# 9. Genuine cooperative residual
Removing every state certified by KPK inheritance leaves 39,858 states in which neither pawn individually wins with the same kings and move order: 31,392 full-game wins and 8,466 draws. Grouping by pawn ranks, BK and turn produces 1,400 geometries: 1,144 universal wins, 220 mixed, and 36 universal draws.
| Class after KPK inheritance | Geometries |
| --- | --- |
| Universal cooperative win | 1144 |
| Mixed | 220 |
| Universal draw | 36 |
# 10. Exact one-rank-staggered cooperative theorem
Within the genuine cooperative residual, every geometry in which the d- and e-pawns are exactly one rank apart is universally winning for White. There are 504 such geometries containing 14,382 residual states, with zero exceptions over legal remaining WK placements.
> Theorem — staggered adjacent pawns. In the residual domain where neither pawn wins individually, |rank(Pd) − rank(Pe)| = 1 implies a White win for every legal White-king placement.
The mixed frontier completely avoids rank gap 1. Its original gap distribution was: gap 0 → 24 mixed; gap 1 → 0; gap 2 → 52; gap 3 → 74; gap 4 → 54; gap 5 → 16.
# 11. Explicit compositional stepping-stone test
The rank-gap-1 predicate was then tested in the stronger direction required by the programme. Its 14,382 states were terminalized as a target, and White was required to force that target before promotion or material-reduction shortcuts. The resulting attractor contains 26,122 of the 31,392 cooperative wins (83.2%) and zero false positives.
Combined with KPK inheritance, the two exact mechanisms certify 223,230 of 228,500 wins, or 97.69% of the complete winning basin. This is the central Pilot 2 result: exact symbolic predicates discovered at different abstraction levels compose adversarially and remove almost the entire basin.
236,976 exact states
        |
        +-- KPK inheritance: 197,108 certified wins
        |
        +-- genuine cooperative residual
              |
              +-- force rank-gap-1 target: 26,122 certified wins
              |
              +-- final residual
223,230 / 228,500 wins certified = 97.69%
# 12. Final post-two-lemma residual
After removing both certified mechanisms, 13,736 states remain: 5,270 wins and 8,466 draws. They occupy 520 pawn/BK/turn geometries: 264 universal wins, 214 mixed, and 42 universal draws.
| Pawn-rank gap | Universal win | Mixed | Universal draw |
| --- | --- | --- | --- |
| 0 | 98 | 24 | 18 |
| 2 | 110 | 46 | 18 |
| 3 | 54 | 74 | 0 |
| 4 | 2 | 54 | 4 |
| 5 | 0 | 16 | 2 |
The progression is meaningful: as pawn separation grows, robust universal wins collapse and WK dependence dominates. At gap 5 no universally winning geometry remains; at gap 4 only two remain, forming a mirror pair.
# 13. Exact blockade localization of the 214 mixed geometries
The final 214 mixed geometries satisfy a compact exact necessary localization. Let the d/e corridor be files d and e; define BK corridor distance as the minimum file distance from BK to either file, and let r_adv be the rank of the more advanced pawn. Every final mixed geometry satisfies:
BK file-distance from {d,e} <= 2
-1 <= rank(BK) - r_adv <= 2
There are zero exceptions. Thus the final WK-sensitive frontier is confined to a small local interception neighbourhood: BK is at most two files outside the pawn corridor and from one rank behind to two ranks ahead of the advanced pawn. Move order is also sharply skewed: 196/214 = 91.6% are Black to move; only 18 are White to move.
Using only four semantic coordinates — pawn-rank gap, side to move, BK corridor distance, and BK rank relative to the advanced pawn — the 520 residual geometries occupy 81 local-topology cells. Sixty-three cells are class-pure. Twenty-six cells are purely mixed and account for 142/214 = 66.4% of the mixed geometries. The remaining overlap shows that these four variables are not an exact biconditional; finer local king/pawn topology remains necessary.
# 14. Evidence ledger
| Claim | Result | Status |
| --- | --- | --- |
| Static-valid arena | 236,976 | Exact count |
| W/D solve | 228,500 wins / 8,476 draws; max rank 23 | Computer-assisted theorem |
| Reflection symmetry | 0 mismatches / 236,976 | Computer-assisted theorem |
| Initial WK grouping | 4,072 universal win / 258 mixed / 0 universal draw | Exact grouping |
| Autonomous pawn split | 2,958 wins / 1,372 failures | Exact reduced solve |
| Strategic mixed after stalemate | 254 geometries | Exact count |
| Connected winning regions | 236/254 have one win component | Exact topology count |
| KPK inheritance | 197,108 wins; 10 stalemate exceptions | Computer-assisted theorem |
| Cooperative residual | 39,858 = 31,392 wins + 8,466 draws | Exact count |
| Rank-gap-1 theorem | 504 geometries / 14,382 states; zero exceptions | Computer-assisted theorem |
| Rank-gap-1 reachability | 26,122 cooperative wins; zero false positives | Computer-assisted theorem |
| Combined coverage | 223,230 / 228,500 = 97.69% | Exact composition |
| Final residual | 13,736 states / 520 geometries | Exact count |
| Final mixed localization | 214 mixed; corridor<=2; rel-rank -1..2 | Computer-assisted one-way lemma |
# 15. Falsified or weakened hypotheses
- Literal Pilot-1-style promotion zero-slack surfaces did not characterize the 254 strategic frontier; simple Pd=0 / Pe=0 analogues were insufficient.
- Autonomous-pawn entry was not the general hard-case stepping stone: it explained only 27.4% of winning WK placements on the strategic 254.
- Raw translated WK masks remained highly fragmented and were the wrong representation.
- Pawn-adjacent contact masks were local but not tiny: roughly 65 normalized masks and about 92 exact semantic-tree leaves remained.
- The final 214 mixed geometries are sharply localized but not completely characterized by the four coarse blockade coordinates tested.
# 16. Proof discipline and scope
All statements labelled exact or computer-assisted are finite universal claims within the explicitly defined model. Classifier/tree complexity is treated only as a representation observation. Exact lemmas were evaluated against the solved finite sets or exact reachability targets. As in Pilot 1, the remaining publication-level obligation is reproducibility and software correctness: independent move-generation checks, deterministic artifacts, hashes, and zero-counterexample logs should accompany any formal publication claim.
The arena is not a theorem about all FIDE positions with two pawns. It fixes the pawns to d/e files and ranks 2–7, uses static validity rather than historical reachability, and omits repetition and move-count claim state.
# 17. Frozen conclusions of Pilot 2
Pilot 2 passes G2. A materially different exact arena independently reproduces the core representation phenomenon: large solved regions can be decomposed into exact semantic mechanisms that compose under adversarial play, while the unresolved difficulty localizes to a small geometric boundary.
The strongest positive result is compositional rather than merely descriptive. An exact KPK theorem inherited from lower material certifies 86.26% of all wins; an independently discovered cooperative pawn-formation predicate then acts as a true stepping stone and raises exact coverage to 97.69%. This is stronger evidence for the programme than a post-hoc compact classifier.
The strongest negative result is that the final king/blockade boundary remains substantially fragmented. Even after strong localization and symmetry reduction, exact contact topology did not collapse to a handful of templates under the attempted language. Pilot 2 therefore reinforces Pilot 1's warning: symbolic compression can be dramatic and compositional without making every critical boundary simple.
> FROZEN PILOT 2 VERDICT: G2 PASSED — STRONG CROSS-ARENA REPLICATION OF EXACT SYMBOLIC COMPOSITION, WITH A REAL LOCAL-TOPOLOGY COMPLEXITY WARNING.
# Appendix A. Reproduction checklist
1. Enumerate 294,912 raw encodings and confirm 236,976 static-valid states.
1. Solve d- and e-file KPK independently; confirm each has 41,358 valid states, 28,853 White wins and 12,505 draws.
1. Solve the full d+e arena; confirm 228,500 wins, 8,476 draws and maximum win rank 23.
1. Reflect every state d↔e and confirm zero W/D mismatches.
1. Group out WK and confirm 4,330 reduced geometries: 4,072 universal wins and 258 mixed.
1. Recompute autonomous-pawn solve: 2,958 autonomous wins and 1,372 failures; isolate four immediate-stalemate anomalies.
1. Reproduce KPK inheritance: 197,118 one-pawn-winning antecedents, 197,108 full wins and exactly ten stalemate exceptions.
1. Remove inherited states and confirm 39,858 cooperative residual states and 1,400 reduced geometries.
1. Verify rank-gap-1 theorem over 504 geometries / 14,382 states with zero counterexamples.
1. Run strict reachability into rank-gap-1 target and confirm 26,122 cooperative wins.
1. Remove both mechanisms and confirm 13,736 states / 520 geometries / 214 mixed.
1. Check exact blockade localization and 196 Black-to-move / 18 White-to-move split.
1. Persist bitsets, residual CSVs, hashes, model flags, and counterexample logs.
