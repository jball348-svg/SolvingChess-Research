**Solving Chess: post-mortem of the backward-composition programme**

Assessment date: 24 September 2026. Repository: jball348-svg/SolvingChess-Research. Snapshot: 3eba1a0c60e8ffca63a85763d176e1da9f904141, the final R6 review state of 19 September 2026.

**The central finding**

The original idea has a sound foundation and the project produced useful results. Working backwards from exact endgame truth is an established solving method. Your stronger hypothesis was that large regions of chess could be represented by compact, reusable propositions, and that composing those propositions would let the proven region expand economically towards the starting position.

The project demonstrated several instances of that phenomenon. It did not establish its repeatability as restrictions were removed and positions became more like ordinary chess.

The missing mechanism was a way to discover and verify enough strategically relevant intermediate regions, covering every opposing reply, without doing approximately the same work as solving the surrounding state space outright. The project repeatedly achieved compact descriptions of truth without demonstrating a corresponding reduction in the cost of obtaining strategically useful truth.

This is a computational and representational gap. Finite-game backward propagation already supplies logical completeness in principle. Unlike the Collatz investigation, no unknown all-depth theorem is needed to justify exhaustive propagation. The open question is whether the proposed compression can make a sufficiently large part of that propagation affordable.

I agree with stopping the accumulated programme on the available evidence. I do not read its results as a refutation of the broader backward-composition idea.

**What I examined and what I could verify**

I traced the original Pilot 1 and Pilot 2 proposals and technical handoffs; the G5–G8 ascent and composition record; the G10–G14 rules, reference proofs and infrastructure; and the R0–R6 final audit. I inspected the relevant machine-readable summaries, sources and nested artifact bundles. Repository agent files were not used as instructions.

I compiled and ran the archived G12 standalone verifier against its preserved certificates. It reproduced the original verification ledger byte for byte: 368,452 KQK states, 399,112 KRK states and 41,619 a-file KPK states, totalling 809,183, with zero reported Bellman/rank mismatches. Its separate same-colour two-bishop scan reproduced 5,938,848 valid states and zero checkmates. These results concern the declared arenas and clean-history roots; they do not certify arbitrary history-decorated versions of those boards. This was my replay of the repository's verifier, not a newly authored independent chess implementation. [G12 bundle][g12]

The late review has a preservation limitation. I found no matching source bytes for the recorded R2 harness, R4 harness, R5 producer or R5 verifier hashes among the checked-in source files and recursively inspected bundled archives. The scan covered 127 source-file occurrences, including duplicate archived copies. Provenance documents record hashes, compiler flags and results, but do not themselves supply those programs. I therefore treat the R1–R5 numerical results below as reported experimental evidence rather than experiments independently reproduced in this post-mortem. The missing files could exist elsewhere; this finding is about the inspected repository snapshot. [R2 provenance][r2json]; [R4 provenance][r4prov]; [R5 provenance][r5prov]

The scope is the preserved repository record, rather than a reconstruction of every earlier conversation.

**Why the starting premise deserves to be taken seriously**

There are two distinct claims in the original idea.

First, exact terminal or endgame knowledge can be propagated backwards. That is mathematically sound. Endgame tablebase generators already implement this broad approach. The original checkers solution combined endgame databases with forward proof search; its published account describes about 39 trillion solved endgame positions and a proof connecting the starting position to established truth. It did not require solving every possible checkers position. This is a concrete precedent for the architecture you had in mind. [Syzygy][syzygy]; [Schaeffer et al., 2007][checkers]

Second, chess might admit sufficiently economical symbolic regions and connections for that architecture to reach the start. This is the substantive research hypothesis. The success of backward propagation alone does not establish it.

The checkers comparison also exposes a difference. Its forced-capture rule helps drive play into the endgame databases. Chess has no corresponding general obligation to exchange pieces on demand. A backward chess method needs to handle an opponent who declines the desired simplification, or certify regions where simplification is unnecessary. That is precisely where intermediate strategy and draw invariants matter. This comparison is an inference from the two games' rules and the published checkers method, not a quantitative prediction of chess difficulty.

Your distinction from Collatz is therefore correct. Under the declared automatic draw rules, chess has a finite game tree: there are finitely many pawn advances and captures, and the automatic 75-move rule bounds the intervening stretches. Exhaustive solution exists in principle. Finiteness does not establish that a compact proof or an affordable procedure for finding it exists. It also leaves the starting position's exact outcome to be determined. [FIDE, Article 9.6][fide]

One scope detail matters: G10 freezes the project's target as proving that White can avoid losing from the starting position. That would be a substantial result. By itself it would not distinguish a draw from a forced White win. Establishing a draw requires the corresponding non-loss guarantee for Black as well. [G10 contract][g10]

**The missing piece, stated precisely**

Let T be a set of already certified non-losing states, with the relevant rules and history included. Backward reasoning adds a nonterminal state when:

- White to move: at least one legal successor is already certified.
- Black to move: every legal successor is already certified.

Writing A₀ = T, the finite-step attractor is obtained by repeating

$$
A_{r+1}=A_r\cup\{s\in V_W:\exists t\in\operatorname{Succ}(s),\ t\in A_r\}\cup\{s\in V_B:\operatorname{Succ}(s)\subseteq A_r\},
$$

where V_W and V_B here contain only nonterminal states; terminal results are handled explicitly. The rank r supplies a progress certificate for forced entry into T.

The repo had this logical machinery. What it lacked was a demonstrated way to represent and compute enough of these sets economically when they became large and tactically varied.

For the proposed symbolic route, an intermediate region needed four properties at once:

| Requirement | What it means | Where the project stood |
|---|---|---|
| Exactness | Every admitted state really has the promised strategy under its declared rules. | Achieved in restricted arenas and some later high-material cases. |
| Strategic relevance | The region closes obligations on a strategy from the initial position against every opposing reply. | No complete initial-position strategy was certified. |
| Economical acquisition | Finding and verifying the region costs materially less than solving the surrounding problem by a competent exact baseline. | Not demonstrated repeatably for the required bridge. |
| Sustained extension | The mechanism continues working as restrictions are removed or the proof frontier advances. | Transfers existed, but no sustained ascent or contraction of the unresolved root-relevant problem was shown. |

These are coupled requirements. A compact formula with a costly hidden database satisfies a different requirement from a cheap, self-contained theorem. A large proven set which an opponent can avoid may contribute little to a root proof. A perfect four-ply invariant may occur too rarely to connect useful regions.

There is also an alternative to forcing entry into a small endgame: certify a closed safe region in which White always has a preserving move and every Black move remains safe. With appropriate terminal and draw reasoning, such an invariant can prove non-loss without forcing exchanges. Therefore “everything must eventually reach a low-material tablebase” is stronger than the actual task. R5's repetition contract was one narrow attempt at this alternative.

The missing object was consequently not necessarily one elegant chess lemma. It could have been a family of reusable invariants, a sound abstraction, better strategy discovery, or a sufficiently economical search procedure. The record does not identify a unique final lemma after which all remaining work becomes routine.

**The strongest positive evidence**

The programme's early success was more substantive than merely fitting an attractive classifier to outcomes.

Pilot 2 reported that KPK inheritance plus forcing a rank-gap-one pawn formation certified 223,230 of 228,500 wins, or 97.69%, in its restricted adjacent-pawn arena. The formation was used as an adversarial reachability target: the opponent could choose replies. That is a genuine example of the proposed stepping-stone mechanism. It still left a fragmented boundary, and its fixed files, restricted material and omitted history state limited transfer. These are the original pilot's figures; later reconstruction conventions produced slightly different underlying outcome counts. [Pilot 2 handoff][pilot2]

G6 identified why combining targets can prove more than taking the union of their separately solved basins. A defender may be unable to prevent entry into one of several good regions, while being able to choose which one. The Branch-Kernel argument formalizes that case. Its bishop example reported 4,302 kernel states generating 117,430 additional union-only states, an amplification of 27.2966. This is useful compositional mathematics. The amplification is a state-count ratio after constituent basins exist; it is not evidence of a 27-fold reduction in total solving cost. [G6 handoff][g6]

G8 showed that some earlier apparent walls were implementation walls. Packed material signatures and better solving/certificate machinery recovered tasks that had timed out. The later review reconstructs a 44.82-million-state case solved in 9.65 seconds after an earlier run exceeded 180 seconds, and restricted eight-man cases with roughly 83–88 million dependency states solved in about 19 seconds. That is substantial engineering progress. The eight-man label must retain its restrictions: several pawns were confined to particular near-promotion squares, so this was far from an unrestricted eight-piece tablebase. [R1 reconstruction][r1hist]

R2 provides the strongest late evidence for prospective semantic discovery. Without seeing top-level outcome labels, its search selected a short target and a two-stage strategy, “give check, then attack the black pawn.” The strategy covered about 99.75% of the chosen composite attractor in the discovery arena and 99.58% in the held-out arena. This shows that useful rules could be selected before consulting the answers for the top arena. It preserves real value in the original hypothesis. [R2 target results][r2target]; [R2 strategy results][r2strategy]

R5 also preserved a positive result: some exact, nonterminal, 30–32-piece draw contracts existed on states reachable from the real starting position. High material did not make structural proof impossible. Their scarcity and acquisition cost prevented them from supplying the required bridge. [R5 exactness][r5exact]

**Where the apparent progress stopped accumulating**

The experiments exposed several different ways for a promising local mechanism to fail to scale.

**1. Compact output did not consistently mean cheap discovery.** R2's short target contained the atom “a certified lower-material capture exit exists.” That atom depended on exact lower truth: about 18.3 million lower states in the discovery family. The top arena itself had about 5.0 million states and 53.8 million edges. Zero top-level labels was an important information restriction, but the experiment still constructed extensive exact graph information.

Its reported discovery cost was 33.91 seconds against 26.53 seconds for complete exact acquisition, a ratio of 1.278. A later replay was nearer parity. The correct conclusion is that an acquisition advantage was not demonstrated. The ratio is neither an asymptotic lower bound nor proof that optimization or amortized reuse could never help. [R2 arena][r2arena]; [R2 cost audit][r2cost]

R5 made the same distinction vivid: very small accepted witnesses emerged from searches examining millions of candidate/reply events. Its reported policy costs were about 0.81 and 0.84 of the unrestricted-White baseline for the identical bounded target proposition. There was a saving, but it accompanied only five and seven certified roots. The accepted witness-edge counts were also a proxy, rather than a complete accounting of all dependency and verification costs. [R5 economics][r5cost]

**2. The unexplained residue did not reliably shrink.** G6's fixed target remained sound when pawn ranks were widened, but its share of wins fell from 33.135% to 22.471% for the knight topology and from 34.117% to 26.884% for the bishop topology. Rook coverage stayed around 90.7%. New winning mechanisms appeared faster than the same target absorbed them in two of the three families. [G6 handoff][g6]

R1 similarly reported stable residuals of roughly two-thirds of wins across its main restricted ladder, rather than a disappearing tail. Its hostile rook case exposed a fixed strategy-language failure: the best supplied program covered only 43.504% of the target attractor. R2's better selected language partly answered that objection. This sequence is evidence against a particular fixed vocabulary and automatic scaling assumption, rather than against all semantic discovery. [R1 results][r1results]

**3. Small-material theorems were not monotone under adding pieces.** Extra friendly material can change stalemate, obstruction and available moves. Opposing material adds checks, captures and counterplay. The programme found genuine restoration counterexamples and replaced broad claims with guarded domains. Those guards are useful mathematics, but maintaining them is part of the problem that grows during ascent.

Terminal conventions also mattered dramatically. G6's faithful wrong-bishop fortress comparison reported 274,296 outcome changes when promotion was instead treated as immediate victory. An exact theorem under the shortcut cannot be transferred unchanged into full chess. G10–G12's rules work was therefore necessary, although it did not supply the missing scaling mechanism. [G6 handoff][g6]; [G10 contract][g10]

**4. Branch reduction did not establish safe choices.** R3 reduced the discovery branch's ply-five exact frontier from 496,086 states to 13,064 by restricting White's moves while retaining all Black replies in the expanded prefix. The frontier construction was much cheaper. However, every horizon state remained unresolved, and the retained White choices had no non-loss certificate. One can make a search tree small by choosing moves; proving that the selected moves suffice is the essential difficulty. [R3 expansion][r3exp]; [R3 closure][r3closure]

**5. Full rules reduced easy state merging.** The same board placement can carry different castling rights, en-passant possibilities, move clocks and repetition histories. R5 reported 3,903,222 full states for 1,556,742 board placements in its discovery frontier, a multiplier of 2.507; some boards represented 264 distinct full states. These shallow measurements do not predict the eventual multiplier. Nor do they prove that a coarser sound abstraction is impossible: proving safe equivalences is itself another potential source of compression. They do show why simply merging matching boards was not an adequate solution. [R5 state audit][r5history]; [FIDE Articles 9.2–9.6][fide]

**Why coverage percentages could not measure distance to solving chess**

For a root proof, placement in the strategy graph matters more than global density. At a Black node with twenty legal replies, certifying nineteen leaves the node unresolved until the twentieth is handled. A region can cover millions of positions and fail to cover the reply Black can choose. Conversely, a small region can be extremely valuable if White can force entry into it.

Thus 99% coverage of a restricted endgame's wins is not 99% of a path to the initial-position theorem. Likewise, R5's 0.49% and 0.68% figures are not estimates of the fraction of chess that admits structural proofs. They are fractions of two fixed 1,024-state cohorts, selected lexicographically within forcing/quiet strata, under one bounded target proposition. They are not random samples of chess positions.

A strategically relevant progress measure would track unresolved obligations in an actual root strategy: which were discharged, which new opposing branches were exposed, what could be soundly merged, and what total acquisition/verification cost was incurred. The programme never demonstrated a repeatable favourable trend on that quantity.

This explains why assembling more exact islands could feel productive while the final connection remained out of reach. The missing information concerned how opposing choices connected the islands, not merely how much exact truth had been accumulated inside them.

**How strongly did the final audit test the original premise?**

The audit was valuable. It separated reported success from relevance to the global proof, froze candidates before testing, preserved failures, and explicitly refused to label unresolved frontier states as draws. Its final STOP_CURRENT_METHOD decision is defensible as a decision about continuing this programme. [R6 verdict][r6]

Its empirical conclusions are narrower than a dismissal of backward chess solving.

| Audit observation | What it supports | Important limit |
|---|---|---|
| R2 discovery cost 1.278× full exact acquisition | No demonstrated cost advantage for that discovery experiment. | A small constant-factor comparison on one family does not determine scaling or amortized economics. |
| R4 certified 0/1,024 in both cohorts | The frozen shallow terminal/current-endgame target grammar did not certify these roots. | Every root had at least 30 pieces. Five plies cannot reach a three- or four-piece target. That component of failure follows from a material bound. |
| R5 certified 5/1,024 and 7/1,024 | Four-ply forced repetition, plus one attraction pair, was sparse on these cohorts. | It tests one particularly restrictive invariant, not general middlegame non-loss invariants. |
| R5 unrestricted White choices produced the same counts | The attraction policy was not hiding a larger nearby basin for the same bounded proposition. | It does not test arbitrary proof horizons, targets or strategy languages. |

R4 still tested whether early terminal wins/draws could provide useful certificates, so it was not devoid of experimental content. But it supplied very little evidence against a multi-stage route through intermediate regions: the available low-material targets were known to be far outside its horizon. [R4 targets][r4targets]

R5 addressed this weakness with FERL-4. Its exact contract was essentially: White chooses, every Black reply is covered, White chooses again, every Black reply returns to the identical repetition position or an exact draw. Repeating the contract permits a draw claim. The theorem is coherent.

Its rarity near the opening is also structurally understandable. Any Black pawn move, capture or permanent castling-right loss on a continuing branch kills the required barrier-free return. A target requiring every Black reply to respect such a short exact repetition is a narrow tactical condition. General drawing strategies can allow irreversible changes, long manoeuvres, several interchangeable safe regions, or eventual simplification. FERL-4 does not represent those possibilities. [R5 hypothesis][r5hyp]

The final thresholds—20% coverage, a cost ratio at most 0.75, bounded grammar and horizons—were reasonable prospective screening choices. They are not mathematical boundaries separating viable and impossible chess-solving methods. Small regions might compose well; broad regions might be strategically irrelevant. No such alternative successful composition was demonstrated, but the thresholds alone cannot exclude it.

The discovery restrictions also narrow the inference. An exact proof may use heuristics to propose moves or candidate regions, provided its final verification establishes the required legal-reply conditions. Avoiding outcome labels was useful for testing whether the symbolic language could discover structure independently. It is not a logical requirement for every valid solving architecture. The review's tightly constrained, evaluation-free policy experiments consequently leave broader heuristic-guided, exactly verified approaches largely unassessed. This observation identifies the scope of the tests; it does not demonstrate that those alternatives would solve the missing computational problem.

There is therefore room for your view that the general idea was not exhaustively explored. It was not. That leaves a research possibility, without supplying positive evidence that a breakthrough was close or that extending the same conveyor would have found one.

**Why the process became convoluted**

My interpretation is that the process increasingly developed components whose interfaces could be specified precisely while the content needed to fill those interfaces remained unresolved.

Once small exact regions existed, it was possible to build typed proof objects, certificate formats, distributed execution, checkpointing, content-addressed storage and increasingly elaborate stage gates. These were tangible, testable tasks. A reusable way to produce ordinary middlegame truth was much harder to specify, so it persisted as a future dependency.

The roadmap's later stages required broad endgame basins, new discovery/lifting methods, a middlegame network and a start-to-basin connector. Those were substantial unresolved research problems. Naming stages and their desired outputs did not derive them from the earlier operators. The final roadmap audit correctly identified this discontinuity. [R0 roadmap audit][r0road]

Some complexity was necessary: precise terminal rules, ranks preventing circular proofs, and opponent quantifiers are essential. Other complexity was premature relative to the central uncertainty. G13's distributed infrastructure and G14's proof store supplied engineering progress while the supply of strategically useful proof objects remained the bottleneck. G14's own truth snapshot explicitly records no new chess truth. [Truth snapshot][snapshot]

The positive lesson is that the process did contain mechanisms for correcting attractive stories. A missing reverse predecessor for the double pawn push overturned an early restoration narrative; G8 overturned some performance failures through representation improvements; later reviews distinguished policy compression from proof. The project did learn.

The negative lesson is that stage completion was not consistently tied to a demonstrated reduction of the eventual root-proof problem. A long sequence of legitimate local passes could coexist with an unclosed central dependency. That is the most important process similarity to the Collatz project.

Preservation also weakened cumulative knowledge. G6 carried an unreproduced historical G4 graph and a G5 rank-label discrepancy; the later audit retains source hashes without the corresponding programs in this snapshot. These issues do not explain the entire failure, but they make it harder for the next investigation to distinguish dependable assets from recorded claims. [G6 handoff][g6]; [R5 provenance][r5prov]

**What retains value**

| Asset | Value supported by the record | Limit on the claim |
|---|---|---|
| Exact semantic stepping stones | Some endgame truth decomposes into reusable, adversarially composable propositions. | No demonstrated universal or sustained ascent law. |
| Branch/Hyperkernel and filtered-attractor machinery | Clear mathematical organization of proof composition and strategy restrictions. | Does not automatically make basin discovery or edge checking cheap. |
| Efficient restricted solvers and certificate replay | Useful executable research infrastructure; some genuine speed improvements and preserved reference proofs. | Speed on restricted arenas is not a forecast for unrestricted chess. |
| R2 prospective rule selection | Evidence that useful targets and programs can be found without top-level answer labels. | Cost advantage and broader transfer remain unestablished. |
| Full-rule state model and adversarial controls | Prevents several tempting but unsound shortcuts. | Exact history handling also introduces computational burdens. |
| Negative results and corrected errors | Identifies specific failed representations, invalid monotonicity assumptions and misleading metrics. | Does not establish lower bounds against other representations. |

These could support a bounded research contribution on explainable endgame proofs, proof composition or verification, subject to reproducibility and a proper novelty assessment. This post-mortem has not performed a literature review sufficient to claim those operators or results are new to game-solving research.

The positive evidence warrants preserving the mathematical core and its exact scope. The record does not warrant assigning a probability of solving chess, estimating how many more sessions were needed, or describing the project as one ordinary engineering step away.

**Comparison with Collatz and final judgement**

| Question | Collatz investigation | Chess investigation |
|---|---|---|
| Is there a guaranteed exhaustive finite solution procedure for the stated task? | No finite cutoff for excluding every nontrivial cycle was supplied. | Yes, for the declared finite chess game, at potentially prohibitive cost. |
| What did local success leave open? | The integrality-sensitive, all-scale connection excluding every candidate cycle. | An affordable, root-relevant closure under every opposing reply. |
| Why did machinery fail to accumulate into completion? | Local obstructions did not force a universal contradiction. | Local exact truth did not create a scalable connected strategy proof. |
| What does stopping establish? | Failure of the investigated route to supply its universal bridge. | Lack of evidence that the investigated route supplies its computational bridge. |

My judgement is strongest on three points. The original backward premise is legitimate. The project established real restricted composition and verification results. It did not demonstrate the economical, repeatable intermediate-region construction needed to turn those results into a starting-position proof.

The conclusion that the particular programme had exhausted its evidential case is a reasonable research-management judgement. The conclusion that compact backward chess solving has been ruled out would exceed the evidence.

What was missing was a method for making proof acquisition and adversarial connectivity scale together. That is a substantial part of the solving problem, even though the game is finite. The project clarified this gap and supplied several useful components around it; it did not show that the gap was either close to closing or impossible to close.

[pilot2]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/handoffs/normalized/Pilot_2_K2P_vs_K_Technical_Handoff.md
[g6]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/handoffs/normalized/G6_Final_Technical_Handoff.md
[g10]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/handoffs/normalized/G10_Technical_Handoff.md
[g12]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/legacy/originals/G12_Final_Rules_Reference_Bundle.zip
[r1hist]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R1_ASCENT_EVIDENCE_RECONSTRUCTION.md
[r1results]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R1_SCALING_RESULTS.md
[r2arena]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R2_DISCOVERY_ARENA_PROFILE.md
[r2target]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R2_TARGET_DISCOVERY_RESULTS.md
[r2strategy]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R2_STRATEGY_DISCOVERY_RESULTS.md
[r2cost]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R2_DISCOVERY_COST_AUDIT.md
[r2json]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/provenance/R2_RUN_SUMMARY.json
[r3exp]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R3_FORWARD_EXPANSION_RESULTS.md
[r3closure]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R3_ALL_REPLY_CLOSURE_RESULTS.md
[r4targets]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R4_TYPED_TARGET_RESULTS.md
[r4prov]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R4_IMPLEMENTATION_PROVENANCE.md
[r5exact]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R5_TARGET_EXACTNESS_RESULTS.md
[r5hyp]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R5_NONTERMINAL_TARGET_HYPOTHESIS.md
[r5cost]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R5_CERTIFICATION_ECONOMICS.md
[r5history]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R5_HISTORY_AND_STATE_AUDIT.md
[r5prov]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R5_IMPLEMENTATION_PROVENANCE.md
[r6]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R6_ADVERSARIAL_VERDICT_CHECK.md
[r0road]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/R0_ROADMAP_SUPPORT_AUDIT.md
[snapshot]: https://github.com/jball348-svg/SolvingChess-Research/blob/3eba1a0c60e8ffca63a85763d176e1da9f904141/REVIEW/CHESS_TRUTH_SNAPSHOT.md
[syzygy]: https://github.com/syzygy1/tb
[checkers]: https://cse.sc.edu/~mgv/csce580sp17/gradPres/schaeffer_CheckersIsSolved_Science2007.pdf
[fide]: https://handbook.fide.com/chapter/e012023
