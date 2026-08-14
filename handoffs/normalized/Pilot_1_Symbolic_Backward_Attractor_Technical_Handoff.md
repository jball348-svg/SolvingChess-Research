<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: Pilot_1_Symbolic_Backward_Attractor_Technical_Handoff.docx
original_sha256: e9ab60a0a0c013ca7ab7ca88cfa8520b08fd1f55ae557d3b4dc64652a387aa33
derivative_filename: Pilot_1_Symbolic_Backward_Attractor_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

# Pilot 1: Symbolic Backward Attractor Compression
in a Wrong-Colour Bishop Rook-Pawn Fortress
*Frozen technical handoff, exact finite-state results, computer-assisted proof record, and model corrections*
STATUS: PILOT 1 FROZEN — STRONG POSITIVE SIGNAL WITH A REAL COMPLEXITY WARNING
10 August 2026
Research handoff generated from the interactive Pilot 1 scratch experiments.
# Executive summary
This document freezes the first self-contained experiment designed to test whether an exact backward non-loss region in chess can be compressed into a hierarchy of human-readable symbolic predicates rather than retained as a large unstructured list of positions. The experiment uses a deliberately small wrong-colour-bishop rook-pawn ending: White has king, light-squared bishop and h-pawn; Black has king; h8 is the defending corner that the bishop cannot control.
The experiment was intentionally not an attempt to solve the endgame in the broadest possible sense. Its purpose was narrower: start from a certified/terminalized sanctuary set, propagate exact adversarial predecessors, then ask whether the resulting state sets expose compact geometric structure. The answer in this arena is unambiguously yes, but with an important qualification: the structure is hierarchical rather than reducible to one tiny formula.
| Headline compression chain<br>The original h8-only attractor contained 206,729 predecessor states beyond a 22,008-state seed. Within that predecessor set, 37,456 certified states initially depended on the bishop square. After correcting artificial boundary conditions, 18,404 of those vanished as artefacts, leaving 19,052 old-safe states across only 1,181 king/pawn/turn geometries. Those 1,181 geometries lie exactly on two zero-slack race surfaces, K = 0 or P = 0. Bishop relevance is then confined to a small expanding diagonal cone and normally to one or two local intervals on an active diagonal. |
| --- |
| Quantity | Final / frozen value | Status |
| --- | --- | --- |
| Raw four-man encodings | 1,572,864 | Exact count |
| Static-valid four-man states | 1,182,440 | Exact count |
| h8 sanctuary seed D0 | 22,008 | Exact count |
| Original conservative attractor total | 228,737 | Exact finite-model solve |
| Original predecessor states beyond D0 | 206,729 | Exact finite-model solve |
| Original bishop-sensitive certified states | 37,456 | Exact grouping count |
| Residual old-safe states after safe-exit correction | 19,052 | Exact count |
| Residual king/pawn/turn geometries | 1,181 | Exact count |
| Corrected full safe basin, real h2-h4 in KPK | 308,810 | Exact finite-model solve |
| Corrected KPK universe | 41,619 states = 29,520 White wins + 12,099 draws | Exact finite-model solve |
| Bad bishop placements in residual geometries | 5,623 | Exact corrected count |
| Race-surface split | 703 pawn-only / 261 king-only / 217 intersection | Exact geometry count |
The strongest compact result is the race-boundary lemma. Define dB as Black king Chebyshev distance to h8; dW as White king Chebyshev distance to h8; tau = 1 if White is to move and 0 if Black is to move; and mP as the minimum number of h-pawn moves to promote, counting h2-h4 as one move. Then
K = dW - dB - tau
P = mP - dB - tau
Every one of the 1,181 stubborn geometries satisfies K = 0 or P = 0. There were zero residual geometries in the strict interior K > 0 and P > 0. In other words, exact bishop-square sensitivity appears only when at least one of White’s two principal resources — king approach or pawn promotion — is tied in effective tempo with Black’s king race to h8.
## How to read the proof claims in this report
| Label | Meaning |
| --- | --- |
| Analytic theorem | Proved from the stated finite-game definitions; does not depend on a classifier. |
| Computer-assisted theorem | A finite universal statement checked exhaustively over every state or geometry in the stated domain; zero counterexamples. |
| Exact count | Direct exhaustive count from the stated enumeration / solved set. |
| Compression observation | An exact or near-exact description of a solved set, but the particular representation (for example decision-tree leaf count) is not mathematically unique. |
| Superseded | An intermediate figure invalidated or refined by a later reconstruction or rule correction. |
| Scope warning<br>These are exact statements about the deliberately defined finite pilot model. The scratch experiment used static-valid board states rather than a proof of historical reachability from the initial chess position; it ignores repetition and 50/75-move counters; and the sanctuary target was operationally terminalized. A repository-quality rerun should emit machine-readable certificates before any result is presented as a publication-level chess theorem. |
| --- |
# Contents
- 1. Research question and experimental logic
- 2. Exact finite arena and coordinate conventions
- 3. Static validity and legal move semantics
- 4. Formal controllable-predecessor solver and proof of correctness
- 5. Original h8-only backward attractor
- 6. First symbolic compression: distance shells, race slack, and bishop independence
- 7. Correcting artificial exits: dead draws, KPK, and stalemate
- 8. The 1,181-geometry residual frontier
- 9. Neutralisation-time experiments and falsified hypotheses
- 10. Exact zero-slack race-surface decomposition
- 11. Bishop diagonal cone, interval grammar, and projection locality
- 12. Pawn-only race surface: near-complete compact grammar
- 13. King-only race surface: exact structure and fragmentation
- 14. Race-surface intersection
- 15. Evidence ledger and proof obligations
- 16. Superseded numbers and chronology of corrections
- 17. Frozen conclusions of Pilot 1
- Appendix A. State encoding and solver pseudocode
- Appendix B. Exact original layer counts
- Appendix C. Pawn-surface base-mask vocabulary
- Appendix D. Reproduction checklist and certificate schema
# 1. Research question and experimental logic
The motivating hypothesis was that a proof-oriented chess solver need not work forward from the initial position while enumerating individual variations. Instead, it could begin with a rigorously known non-losing region and work backward, repeatedly finding states from which the defending side can force entry into that region. The key speculative step was that the large predecessor sets might admit compact symbolic descriptions — “stepping-stone lemmas” — which could be iterated and composed.
Pilot 1 therefore asked a falsifiable question: when an exact non-loss target is propagated backwards in a small but nontrivial chess universe, does the boundary rapidly become an arbitrary cloud of FEN-like exceptions, or does it reveal low-dimensional geometric structure? A negative result would have been useful: if even this idealized fortress immediately fragmented into essentially uncompressible square-level cases, that would be a strong warning against the broader programme.
The wrong-colour bishop plus rook-pawn fortress was selected because it has a clear sanctuary geometry and a meaningful interaction between king race, pawn race, bishop control, move order, captures, and stalemate. It is also small enough to enumerate exactly without external tablebases.
| What was deliberately not tested<br>Pilot 1 did not ask whether White can force a draw from the initial chess position; did not search 32-piece chess; did not use Stockfish evaluation as truth; did not infer legality from engine scores; and did not treat classifier accuracy as proof. It was a representation experiment inside an exact finite arena. |
| --- |
# 2. Exact finite arena and coordinate conventions
## 2.1 Material and board restrictions
- White pieces: king (WK), bishop (WB), rook pawn (WP) fixed to the h-file.
- Black pieces: king (BK).
- WP may occupy h2, h3, h4, h5, h6 or h7.
- WB is restricted to the 32 squares of the colour opposite h8; with a1 treated as dark, these are the light squares. Thus WB cannot control h8.
- Both sides to move are represented.
- No castling or en-passant state is relevant in this material class.
## 2.2 Square encoding
Squares use the conventional zero-based integer map sq = 8 × rank_index + file_index, with a1 = 0 and h8 = 63. Files and ranks are each indexed 0…7 internally. Algebraic notation is used throughout the prose.
file(s) = s mod 8;   rank(s) = floor(s / 8)
The bishop diagonal coordinate used later is
delta(s) = rank(s) - file(s).
Because h8 has delta = 0 and the bishop is on the opposite colour complex, its possible delta values are odd: -7, -5, -3, -1, +1, +3, +5, +7.
| delta | Wrong-colour bishop diagonal |
| --- | --- |
| -7 | h1 |
| -5 | f1-g2-h3 |
| -3 | d1-e2-f3-g4-h5 |
| -1 | b1-c2-d3-e4-f5-g6-h7 |
| +1 | a2-b3-c4-d5-e6-f7-g8 |
| +3 | a4-b5-c6-d7-e8 |
| +5 | a6-b7-c8 |
| +7 | a8 |
## 2.3 Raw state encoding and count
The raw Cartesian encoding contains 64 WK squares × 32 WB squares × 6 pawn ranks × 64 BK squares × 2 sides to move:
64 × 32 × 6 × 64 × 2 = 1,572,864 raw encodings.
A convenient integer state identifier used in the scratch solver was equivalent to:
| id = ((((wk * 32 + bishop_index) * 6 + pawn_index) * 64 + bk) * 2 + side_to_move) |
| --- |
# 3. Static validity and legal move semantics
## 3.1 Static validity
A raw encoding is static-valid in the pilot if and only if all of the following hold:
1.  All four pieces occupy distinct squares.
2.  WK and BK are not adjacent.
3.  If it is White to move, BK is not already attacked by WP or WB. This rejects positions in which Black’s preceding move would have left its own king in check.
4.  No historical reachability condition is imposed beyond these static constraints.
Exhaustive enumeration under exactly these rules gives:
1,182,440 static-valid four-man states.
| Why the “Black not in check when White to move” condition matters<br>The scratch enumeration originally looked like a simple non-overlap problem, but the exact 1,182,440 count is recovered only when static turn-legality is included. This is a load-bearing convention and should be preserved in any reproduction. |
| --- |
## 3.2 Four-man legal moves
White legal moves are ordinary WK moves, ordinary WB sliding moves, and h-pawn pushes. The main four-man arena uses the legal h2-h4 double move when unobstructed. Promotion from h7 leaves the fixed four-man material class and is treated as an unsafe exit for Black’s drawing objective.
Black legal moves are ordinary king moves subject to White attacks and king adjacency. In the original conservative solve, captures of WP or WB were treated simply as exits from the arena and therefore as failures to certify. This was deliberately conservative but later shown to create artificial bishop sensitivity.
## 3.3 The sanctuary target D0
The base target D0 consists of every static-valid state with BK on h8. There are exactly 22,008 such states. Operationally, reaching D0 terminates the reachability objective successfully.
| Semantic interpretation of D0<br>D0 represents entry into the classic wrong-colour-bishop rook-pawn sanctuary. The backward solver proves forced entry into D0 under the pilot rules. A separate chess-theoretic certification that every represented h8 position is non-losing is conceptually distinct from the attractor calculation; the pilot terminalized the target rather than continuing play after entry. |
| --- |
## 3.4 Corrected safe exits
The corrected model recognizes additional exact drawing exits for Black:
- BK captures WP legally: the resulting K+B versus K position is a dead draw.
- BK captures WB legally: the resulting K+P versus K state is classified by an exact KPK subsolver; the capture is safe only when the KPK position is drawn for Black.
- Stalemate is a draw and is seeded as safe.
- White promotion remains an unsafe exit for the drawing objective.
# 4. Formal controllable-predecessor solver and proof of correctness
## 4.1 Attractor recurrence
Black is the protagonist: Black wants to force entry into the safe set; White is adversarial and tries to prevent it. Let Succ(s) be the legal successor set under the stated terminal semantics. Starting from safe target A0, define:
A(n+1) = A(n)  union  {s_B : exists s’ in Succ(s_B), s’ in A(n)}  union  {s_W : for all s’ in Succ(s_W), s’ in A(n)}.
The implementation computes this monotonically until a fixed point. A state’s attractor rank is the first n for which it enters A(n); rank therefore upper-bounds the number of plies needed under Black’s forcing strategy against maximally delaying White play, subject to the exact rank-update convention.
## 4.2 Analytic correctness theorem
| Theorem 1 — finite reachability attractor<br>In a finite turn-based game graph with safe terminal target T, the least fixed point of the recurrence above is exactly the set of states from which Black has a strategy forcing T in finitely many plies against every legal White strategy, provided terminal states are classified consistently with the objective. |
| --- |
Proof. For soundness, use induction on attractor rank. Every rank-0 state is safe by definition. If a Black-to-move state enters at rank n+1, it has at least one successor of rank at most n; Black selects it and the induction hypothesis supplies a forcing strategy. If a White-to-move state enters at rank n+1, every legal successor is already in A(n); whichever White chooses, the induction hypothesis applies. Thus every state admitted by the recurrence is genuinely forceable.
For completeness, consider any state outside the fixed point A*. At a Black-to-move state outside A*, no legal successor lies in A*, otherwise the predecessor rule would add it. At a White-to-move state outside A*, at least one legal successor lies outside A*, otherwise the universal predecessor rule would add it. Therefore White can maintain play outside A* whenever White controls the move, while Black has no edge into A* when Black controls the move. Hence Black cannot force the target from outside A*. This proves equality.
## 4.3 Computer-assisted proof discipline
All symbolic lemmas described as exact were checked by direct enumeration against the solved state set. The generic pattern was:
| for each state or geometry g in DOMAIN:<br>predicted = P(g)<br>actual = membership_in_exact_solved_set(g)<br>if predicted != actual (for biconditionals), or predicted and not actual (for one-way lemmas):<br>record counterexample<br>assert number_of_counterexamples == 0 |
| --- |
Decision trees were used only as discovery/compression instruments. A tree leaf count is not itself a theorem. When a tree suggested a rule, the rule was flattened into an explicit predicate and rechecked exhaustively where reported as exact.
# 5. Original h8-only backward attractor
The first rigorous baseline deliberately treated every move leaving the four-man arena as uncertified. This isolates the geometry of forcing h8 but under-certifies genuine draws reached by captures. The fixed point contained 228,737 states, of which 22,008 were seed states and 206,729 were added predecessors. Maximum predecessor rank was 11.
| Layer | New states | Cumulative incl. D0 |
| --- | --- | --- |
| 1 | 29001 | 51009 |
| 2 | 20034 | 71043 |
| 3 | 35802 | 106845 |
| 4 | 24224 | 131069 |
| 5 | 34406 | 165475 |
| 6 | 18593 | 184068 |
| 7 | 25765 | 209833 |
| 8 | 7895 | 217728 |
| 9 | 10045 | 227773 |
| 10 | 523 | 228296 |
| 11 | 441 | 228737 |
| 12 | 0 | 228737 |
## 5.1 Exact distance-wave structure
The layer geometry immediately displayed a clean distance wave in dB = d∞(BK,h8): B1-B2 were exactly dB=1; B3-B4 exactly dB=2; B5-B6 exactly dB=3; B7-B8 exactly dB=4; B9-B10 exactly dB=5; and B11 exactly dB=6. No exceptions were observed.
The pawn rank moved backward in lockstep with the king shell. In every added state:
Black to move: pawn_rank <= 8 - dB
White to move: pawn_rank <= 7 - dB
Equivalently define the early race slack S by S = 8 - dB - pawn_rank when Black moves and S = 7 - dB - pawn_rank when White moves. Every one of the 206,729 added states satisfied S >= 0. Among all static-valid non-seed states, 328,596 satisfied this necessary race condition, of which 206,729 were in the attractor, so the predicate had 100% recall for the attractor but only about 62.9% precision.
## 5.2 Exact first-boundary biconditional
| Theorem 2 — B1<br>Within the static-valid arena, a state is in B1 if and only if Black is to move, BK is on g7, g8 or h7, and WK does not control h8. The exhaustive predicted count is 29,001, exactly equal to the computed B1 count; there were zero false positives and zero false negatives. |
| --- |
The bishop and pawn disappear from this predicate for a structural reason: the wrong-coloured bishop cannot attack h8 and an h-pawn cannot attack h8. Therefore only WK control and the BK adjacency geometry determine whether ...Kh8 is immediately legal.
## 5.3 Early B2 compression
B2 contains 20,034 states. A very simple king-distance predicate, d∞(WK,h8) >= 3, accounts for 19,360 of them (96.6%). The remaining 674 states are distance-2 cases explained by a small set of king-pair geometries in which BK itself prevents White from acquiring h8 control. The precise six-pair exception list was not retained in the final scratch notes and should be regenerated in a repository rerun rather than reconstructed from memory.
# 6. First symbolic compression: race slack and bishop independence
## 6.1 A large exact three-condition safe lemma
Using only semantic features, a simple candidate rule was discovered and then re-enumerated exhaustively in the original h8-only model:
S >= 1  and  dB <= 3  and  dW >= 5  =>  state is in the h8 attractor.
This one three-condition predicate certified 106,913 exact positions with zero false positives in the scratch verification. It is not a complete characterization, but it demonstrates the intended compression phenomenon: a very small formula can stand in for over one hundred thousand enumerated states.
## 6.2 Grouping out the bishop square
To measure whether bishop location was genuinely a high-dimensional variable, states were grouped by the non-bishop geometry g = (WK, BK, pawn rank, side to move). For each g, all legal wrong-coloured bishop placements were examined. A geometry was called bishop-independent if every legal bishop placement was certified, and mixed if some were certified and some were not.
Among the 206,729 added states of the original attractor, 169,273 certified states belonged to bishop-independent geometries, while 37,456 certified states belonged to mixed geometries. Thus 81.9% of the original predecessor basin was already independent of the precise bishop square.
Those 37,456 mixed certified states occurred across 2,354 underlying non-bishop geometries. This was the first important dimensional collapse: tens of thousands of FEN-level cases reduced to a few thousand king/pawn/turn situations.
# 7. Correcting artificial exits: dead draws, KPK, and stalemate
The original mixed region could not be interpreted immediately as genuine chess complexity because the old solver treated Black captures of the pawn or bishop as failures merely because they left the fixed four-man arena. The next phase therefore repaired the terminal semantics before attempting to explain the residual bishop patterns.
## 7.1 Exact K+P versus K subsolver
When Black captures WB, the remaining K+P versus K state may be won for White or drawn. An exact finite KPK solver was therefore constructed, using the same static-validity convention. The KPK universe contains exactly 41,619 static-valid states.
The first KPK implementation accidentally omitted the legal initial h2-h4 double move. It classified 28,616 states as White wins and 13,003 as draws. This was later corrected. With h2-h4 restored, the authoritative split is:
29,520 White-winning KPK states; 12,099 drawn KPK states; total 41,619.
KPK was solved by an exact win attractor for White: promotion is a White-winning terminal; legal capture of the pawn by BK is a draw; at White nodes one winning successor is sufficient; at Black nodes every legal continuation must remain White-winning for the state to be a White win. The same finite-game induction as Theorem 1 proves correctness of this classification within the KPK model.
## 7.2 Corrected four-man safe basin
With pawn captures, KPK-classified bishop captures, and stalemates recognized as safe, the final corrected four-man solve with real h2-h4 contains:
308,810 safe states total; 286,802 beyond the 22,008 h8 seed; maximum attractor rank 15.
A second “neutralisation” attractor was then computed inside the corrected safe set. Its target consisted of states whose non-bishop geometry is safe for every legal bishop placement, plus safe terminal states. This target contained 256,639 states, representing 8,798 universal geometries plus 263 additional terminal states. Every one of the 308,810 corrected-safe states could force this bishop-irrelevant target; the maximum neutralisation rank was 13.
## 7.3 What disappeared from the original 37,456
Of the original 37,456 bishop-sensitive certified states, 18,404 become bishop-independent once the safe exits are modeled correctly. Thus nearly half of the apparent bishop complexity was not chess structure at all; it was an artefact of the experimental boundary.
37,456 - 18,404 = 19,052 residual old-safe states.
Those 19,052 states lie in exactly 1,181 non-bishop geometries. This residual is the main object of the later symbolic analysis.
# 8. The 1,181-geometry residual frontier
Across the 1,181 residual geometries there are 33,461 legal bishop placements in the final corrected reconstruction. Of these, 27,838 are corrected-safe and 5,623 are corrected-unsafe. The original 19,052 states are the subset that were already certified by the conservative h8-only solver and remained in mixed geometries after correction.
The residual therefore admits several different but complementary views:
- 19,052: the old-safe states whose bishop dependence survived correction;
- 1,181: the underlying king/pawn/turn geometries;
- 33,461: all legal bishop placements within those geometries;
- 5,623: the final bad bishop placements that prevent corrected safety in those geometries.
For 1,153 of the 1,181 geometries, the natural representation is “almost every bishop square is safe except a small forbidden set.” The remaining 28 are better represented positively (“only a small allowed set works”). This representation flip is important: forcing every geometry into a forbidden-mask convention artificially inflates complexity.
In the final reconstructed model, the forbidden/allowed behavior across the residual corresponds to 91 distinct masks. Earlier interim figures of 89 masks and 5,260 bad placements were superseded by the reconstructed 91 / 5,623 figures and should not be reused.
# 9. Neutralisation-time experiments and falsified hypotheses
The segment endpoint patterns suggested that “neutralisation tempo” might explain why a bishop is dangerous only within a small window around Black’s route. Several candidate notions were tested. Two plausible simplified models failed, which materially narrowed the explanation.
## 9.1 Falsified hypothesis A: frozen-board capture/fortress time
A first model froze White’s pieces and estimated how quickly BK could capture the bishop, capture the pawn, reach h8, or enter a bishop-independent safe geometry. This did not separate safe from bad bishop placements: more than 90% of genuinely bad placements still appeared neutralisable quickly enough. Static distance-to-capture is therefore not the missing law.
## 9.2 Falsified hypothesis B: bishop flight is the missing dynamic
A second reduced game froze White’s king and pawn but allowed the bishop to move adversarially while BK pursued. This also failed: approximately 97% of truly bad placements remained neutralisable. Bishop evasion by itself is not the main cause of the endpoint correction.
## 9.3 Isolating White’s king and pawn counterplay
The decisive experiment switched White resources on and off independently. Using the final KPK-corrected residual, the 5,623 bad placements split as follows:
| Mechanism classification | Bad placements | Interpretation |
| --- | --- | --- |
| Pawn decisive | 2,646 | Safe if pawn is frozen; bad in full game. |
| King decisive | 2,262 | Safe if White king is frozen; bad in full game. |
| Either alone sufficient | 496 | Freezing either one resource is enough to remove the failure. |
| King+pawn synergy | 219 | Neither resource alone explains failure; interaction is required. |
The two clean independent classes account for 4,908 / 5,623 = 87.3% of the bad frontier. Only 219 placements (3.9%) require genuine king+pawn synergy in this isolation experiment.
The neutralisation rank also showed a striking one-tempo character. In every pawn-driven state, the forced neutralisation time with the pawn frozen was at least the ply on which White first gets a move; 2,363 / 2,646 (89.3%) were exact ties. In the king-driven class, the analogous condition held for every state and 2,041 / 2,262 (90.2%) were exact ties.
# 10. Exact zero-slack race-surface decomposition
## 10.1 Definitions
Let dB = d∞(BK,h8) and dW = d∞(WK,h8), using Chebyshev king distance. Define tau = 1 when White is to move and tau = 0 when Black is to move. Define the minimum number of legal pawn pushes required for the h-pawn to promote by:
mP = 8 - pawn_rank - 1[pawn_rank = 2].
The indicator term accounts for the initial h2-h4 double step. Define two effective race slacks:
K = dW - dB - tau
P = mP - dB - tau
K is the effective White-king lag relative to BK’s race to h8. P is the effective pawn-promotion lag relative to the same Black race. Zero means a move-order-adjusted tie.
## 10.2 Exact race-boundary lemma
| Theorem 3 — residual frontier lies on two zero-slack surfaces<br>For every one of the 1,181 residual non-bishop geometries, K = 0 or P = 0. There are zero residual geometries with K > 0 and P > 0. |
| --- |
| Race surface | Geometries |
| --- | --- |
| P = 0 and K > 0 (pawn-only boundary) | 703 |
| K = 0 and P > 0 (king-only boundary) | 261 |
| K = 0 and P = 0 (intersection) | 217 |
| K > 0 and P > 0 | 0 |
Proof status: computer-assisted theorem. For each of the 1,181 geometries, K and P were calculated directly from coordinates and side to move. The assertion (K=0) OR (P=0) was checked; the counterexample count was zero. The 703/261/217 partition sums exactly to 1,181.
## 10.3 Mechanism-specific strengthening
| Theorem 4 — king-driven failures<br>Every one of the 2,262 king-driven bad bishop placements satisfies K = 0. Zero exceptions. |
| --- |
Unpacked by move order: when Black moves first, dW = dB; when White moves first, dW = dB + 1. The side-to-move term exactly compensates the initial tempo.
| Theorem 5 — pawn-driven failures<br>2,634 of 2,646 pawn-driven failures (99.55%) satisfy P = 0. For pawns on h3-h6 there are zero exceptions. The only 12 exceptions are local h2 cases. |
| --- |
Thus the residual complexity is not spread through the interior of state space. It is concentrated at exact race equalities, where the bishop decides whether White can exploit the tied tempo.
# 11. Bishop diagonal cone, interval grammar, and projection locality
## 11.1 Exact expanding diagonal cone
For the 1,153 “forbid-mode” geometries, every forbidden bishop placement satisfies the exact cone law:
|delta(WB)| <= 2*dB - 3.
This means that as BK moves one king-step farther from h8, precisely one additional pair of wrong-colour bishop diagonal bands can become relevant. The corresponding maximum active bands are:
| dB | Potentially harmful bishop bands |
| --- | --- |
| 2 | delta = ±1 |
| 3 | delta = ±1, ±3 |
| 4 | delta = ±1, ±3, ±5 |
| 5 | delta = ±1, ±3, ±5, ±7 |
Across those 1,153 geometries only 17 distinct sets of active diagonals occurred. The six most common active-band sets — {-1,+1}, {-1}, {-1,+1,+3}, {+1,+3}, {+3}, and {+1} — cover 1,108 / 1,153 = 96.1% of the forbid-mode geometries.
## 11.2 Interval theorem on each active diagonal
| Theorem 6 — at most two forbidden components per active diagonal<br>Across 2,176 active diagonal occurrences in the forbid-mode population, the forbidden bishop squares form at most two contiguous intervals on each diagonal. Exactly 2,124 diagonal occurrences have one interval and 52 have two; none require three or more components. |
| --- |
Those 2,176 active diagonals contain 2,228 forbidden segments in total. Of these, 1,383 are suffixes anchored to the h8-near edge of the diagonal and 716 are prefixes anchored to the opposite edge. Thus 2,099 / 2,228 = 94.2% are edge-anchored rays; only 129 are genuinely interior/single-square segments.
## 11.3 Projection locality
For an active diagonal delta, define Pi_delta(BK) as a legal bishop square on that diagonal minimizing Chebyshev distance to BK (with a deterministic tie rule when needed). Express a segment endpoint as a signed number of bishop steps from this projection.
For edge-anchored prefixes, all endpoint offsets lie in {-3,-2,-1,0,+1}; 93.7% are 0 or -1. For edge-anchored suffixes, all starting offsets lie in {0,+1,+2,+3,+4}; 88.9% are 0,+1 or +2. Therefore every edge-segment boundary lies within four bishop steps of the BK projection.
Normalizing intervals by this projection produced only 35 distinct local interval patterns when projection ties were chosen naturally for the interval, or 42 under one rigid global tie convention. The 15 most common normalized patterns cover 93.6% of active diagonals. This is a strong indication that the bishop dimension is governed by a small local grammar rather than arbitrary square masks.
# 12. Pawn-only race surface: near-complete compact grammar
The 703 geometries with P=0 and K>0 were analyzed separately. This is the cleanest surface because the pawn is fundamentally a one-dimensional clock.
## 12.1 Only three bishop diagonals matter
| Theorem 7 — pawn-boundary active diagonals<br>On every pawn-only residual geometry, a bad bishop can lie only on delta = -1, +1 or +3. No bishop on \|delta\| = 5 or 7 is bad anywhere on this surface. |
| --- |
All edge-anchored segment endpoints on this surface lie between -1 and +3 diagonal steps of Pi_delta(BK).
## 12.2 Exact delta=+3 sublemma
The delta=+3 diagonal is a4-b5-c6-d7-e8. Across all 703 pawn-only geometries, the only bad bishop square on this diagonal is e8. Moreover, Be8 is bad exactly for BK in the six-square set {c3,c4,d4,d5,e5,e6}. In zero-based coordinates (f,r), this set is described by:
2 <= f <= 4  and  r - f in {0,1}.
This is an exact computer-assisted biconditional over the pawn-only surface.
## 12.3 Thirteen base masks
For the delta=±1 geometry, a compact “base mask” was selected from only 13 distinct square sets using BK position, pawn rank, side to move and K. The exact base-mask vocabulary recovered from the scratch record is:
| Mask | Forbidden bishop squares in base template |
| --- | --- |
| M1 | {h7} |
| M2 | {a2,b3,c4,d5,e6,f7,h7} |
| M3 | {b1,c2,d3,f7,e8,g8} |
| M4 | {a2,b3,c4,d5,e6,h7} |
| M5 | {f7,e8,g8} |
| M6 | {e8} |
| M7 | {b1,c2,d3,e4,f7,e8,g8} |
| M8 | {e8,g8} |
| M9 | {b1,c2,f7,e8,g8} |
| M10 | {b1,c2} |
| M11 | {b1,c2,d3} |
| M12 | {b1,c2,d3,e4} |
| M13 | {h7,e8,g8} |
A semantic decision tree choosing among these 13 base masks required 18 leaves for exact selection on the relevant base-key population. The selector itself is a compression artifact rather than a unique theorem, but the 13-mask vocabulary is an exact enumerative fact of the derived representation.
## 12.4 Base-mask selector contexts recovered from scratch
The scratch record also retained the base-key mapping used by the 13-mask learner. Each tuple below is (BK square, pawn rank, side-to-move code, K), where side code 0 = White to move and 1 = Black to move. These are included to allow a research agent to reconstruct the exact base system without guessing:
| Mask | Base-key contexts (compressed notation) |
| --- | --- |
| M1 | (e7,5,1,1); (f7,5,0,1..4); (f7,6,1,2..5) |
| M2 | (f8,5,0,1..4); (f8,6,1,1..5) |
| M3 | (c3,2,1,1); (c3,3,1,1); (d4,2,0,1..2); (d4,3,0,1..2); (d4,4,1,2..3) |
| M4 | (f7,6,1,1); (e8,4,0,1..3); (e8,5,1,1..4) |
| M5 | (c4,2,1,1..2); (c4,3,1,1..2); (d5,4,1,1..3) |
| M6 | (d5,2,0,1..2); (d5,3,0,1..2); (e6,4,0,1..3) |
| M7 | (d4,4,1,1); (e5,4,0,1..3) |
| M8 | (e6,5,1,2..4) |
| M9 | (c3,2,1,2); (c3,3,1,2) |
| M10 | (d3,2,1,1); (d3,3,1,1) |
| M11 | (e4,4,1,1..2) |
| M12 | (f4,4,1,1) |
| M13 | (e6,5,1,1) |
The base-key contexts are transcribed from the final scratch output. “1..4” denotes each integer K value in that inclusive range.
## 12.5 White-king blocker rule and final 20 corrections
After choosing the base mask, applying a simple line-of-sight blocker rule — truncate the forbidden bishop ray when WK physically lies between the bishop and the relevant critical endpoint — gives the exact final bishop mask in 683 / 703 pawn-only geometries (97.15%).
The remaining 20 geometries fall into five local correction types: remove d3 in 8 cases; remove the a2-e6 prefix in 5; remove h7 in 3; remove e4 in 3; remove f7 in 1. Two of these correction families were fully retained in the scratch notes:
- Remove d3 (8 cases): BK=c3; K=1; Black to move; WP on h2 or h3; WK on b5,b6,b7 or b8.
- Remove e4 (3 cases): BK=d4; WP=h4; K=1; Black to move; WK on c6,c7 or c8.
The exact coordinate predicates for the remaining three correction families (a2-e6 prefix, h7, and f7) were not preserved in the condensed scratch transcript. Their counts and removed squares are preserved, but a publication-quality reproduction should regenerate the exact predicates from the solved residual CSV rather than infer them from memory.
| Pawn-surface compression result<br>All 703 pawn-only geometries are exactly represented by: P=0,K>0; three possible active diagonal bands; one of 13 base masks; a direct White-king blocking operation; and five small local correction families. The representation is hierarchical and chess-semantic rather than a 703-entry FEN table. |
| --- |
# 13. King-only race surface: exact structure and fragmentation
The 261 king-only geometries satisfy K=0 and P>0. This surface is smaller than the pawn surface but materially more complex because WK is a two-dimensional moving obstruction rather than a one-dimensional promotion clock.
Across these 261 geometries there are 1,572 bad bishop placements. Their absolute diagonal-band distribution is:
| \|delta\| | Bad placements | Share |
| --- | --- | --- |
| 1 | 1,298 | 82.6% |
| 3 | 175 | 11.1% |
| 5 | 75 | 4.8% |
| 7 | 24 | 1.5% |
Thus 93.7% of king-surface bad placements lie within |delta|<=3, and all edge boundaries remain within -2 to +2 bishop steps of Pi_delta(BK). The cone and locality principles remain strong.
However, the exact mask selector is much less compact. There are 50 distinct final masks among the 261 geometries. Using a semantic feature set including king coordinates/distances, pawn rank and projection features, an exact decision tree required approximately 78 leaves. Depth-limited accuracy was roughly 52% at depth 4, 77% at depth 6, and 90% at depth 8.
| Interpretation<br>The king surface is the first robust complexity warning. Geometry remains highly local, but the topology of a mobile White king creates many more distinct local cases than the pawn clock. The pilot therefore falsifies the strongest naive hypothesis that every backward boundary should collapse to one or two simple rules. |
| --- |
# 14. Race-surface intersection
There are 217 geometries with K=0 and P=0. These combine both zero-slack resources. Bad bishop placements remain strongly concentrated near the fortress diagonals: approximately 75.5% occur on |delta|=1 and about 91% within |delta|<=3. Edge-boundary offsets remain in the small window -2 through +3 relative to BK projection.
The intersection contains 40 distinct final masks. An exact semantic selector required roughly 63 leaves in the scratch representation. This is again structured but not reducible to a tiny universal formula with the features tried.
# 15. Evidence ledger and proof obligations
| Claim | Result | Status | Reproduction obligation |
| --- | --- | --- | --- |
| Raw/state counts | 1,572,864 raw; 1,182,440 static-valid | Exact count | Re-enumerate state IDs and validity predicate. |
| Original attractor | 228,737 total; 206,729 predecessors; max rank 11 | Computer-assisted theorem | Recompute fixed point; compare layer histogram. |
| B1 predicate | 29,001 exact biconditional | Computer-assisted theorem | Evaluate predicate on every static-valid state. |
| Original race slack | All 206,729 predecessors satisfy S>=0 | Computer-assisted one-way lemma | Enumerate all predecessor states. |
| Bishop-independent original basin | 169,273 states; 37,456 mixed certified | Exact grouping count | Group by (WK,BK,pawn,stm). |
| KPK corrected | 41,619 = 29,520 wins + 12,099 draws | Computer-assisted theorem | Solve KPK attractor with h2-h4. |
| Corrected basin | 308,810 total; 286,802 predecessors; max rank 15 | Computer-assisted theorem | Recompute safe-exit attractor. |
| Neutralisation attractor | All 308,810 ranked; max rank 13 | Computer-assisted theorem | Target universal geometries + safe terminals. |
| Residual | 19,052 old-safe states; 1,181 geometries; 5,623 bad placements | Exact count | Recreate residual CSV. |
| Race surface | Every residual geometry has K=0 or P=0 | Computer-assisted theorem | Zero counterexamples over 1,181 geometries. |
| King mechanism | 2,262/2,262 king-driven bad placements have K=0 | Computer-assisted theorem | Variant solver + race predicate. |
| Pawn mechanism | 2,634/2,646 pawn-driven have P=0; 12 h2 exceptions | Computer-assisted theorem/count | Variant solver + race predicate. |
| Diagonal cone | Forbidden => \|delta\|<=2dB-3 in 1,153 forbid-mode geometries | Computer-assisted theorem | Evaluate every bad placement. |
| Interval grammar | <=2 contiguous forbidden intervals per active diagonal | Computer-assisted theorem | Run interval decomposition. |
| Projection locality | All edge endpoints within 4 bishop steps of projection | Computer-assisted theorem | Normalize segment endpoints. |
| Pawn surface | Only delta=-1,+1,+3; 703 geoms | Computer-assisted theorem | Surface-restricted enumeration. |
| King surface leaf count | ~78 exact leaves | Compression observation | Depends on feature representation / tree algorithm. |
## 15.1 What “proof” means here
The finite universal statements are proofs conditional on the implementation matching the model. Their logical form is finite and exhaustive, not statistical. The remaining proof obligation is software correctness and reproducibility: an independent implementation should regenerate the same counts, or the production implementation should emit sufficient certificates (state hashes, counterexample-free scans, and independent cross-checks) to make accidental implementation error unlikely.
No claim in this report establishes a theorem about all FIDE chess positions or about the initial chess position. The static arena includes positions that may not be reachable from ordinary game history, and it omits rule counters. The correct interpretation is: “within this explicitly defined finite game graph, the stated set identities and implications were exhaustively verified.”
# 16. Superseded numbers and chronology of corrections
The interactive nature of the pilot produced several interim figures that were later corrected. This section exists to prevent a future agent from accidentally mixing incompatible baselines.
| Interim figure | Status | Authoritative treatment |
| --- | --- | --- |
| KPK 28,616 wins / 13,003 draws | Superseded | Initial KPK solver omitted h2-h4. Final: 29,520 wins / 12,099 draws. |
| Corrected basin 309,650 | Superseded by final KPK correction | Final reconstructed corrected basin: 308,810. |
| 89 masks / 5,260 bad placements | Superseded | Final reconstructed residual: 91 masks / 5,623 bad placements. |
| 5,590 bad placements | Superseded | Pre-h2-h4 KPK correction; final 5,623. |
| 18,147 original mixed states disappearing | Superseded | Final reconstructed value: 18,404. |
| Intermediate 290,404 “corrected predecessor” figure | Do not use | Came from an earlier correction pass before the full reconstructed terminal semantics; final authoritative total is 308,810 safe / 286,802 beyond h8 seed. |
The original h8-only layer histogram (29,001, 20,034, …, 441) remains authoritative for the conservative original model. The corrected model has a different layer structure and should not be inferred by modifying those original counts.
# 17. Frozen conclusions of Pilot 1
Pilot 1 began with the speculative idea that backward non-loss regions might admit symbolic stepping stones. In this arena, the state cloud did not remain an arbitrary collection of FENs. It repeatedly collapsed under better representations: from state membership to non-bishop geometry; from geometry to two exact race surfaces; from bishop square to a diagonal cone; from diagonal masks to one/two contiguous intervals; and, on the pawn surface, to a small base-mask plus blocker grammar.
The strongest positive statement is therefore not that “the endgame has one simple rule.” It is that a large exact attractor has a hierarchical representation with low-dimensional critical manifolds and local geometric grammars. That is precisely the sort of representation a proof-oriented solver would need if it were ever to escape raw enumeration.
The strongest negative statement is equally important: the king-only surface did not collapse to a handful of lemmas under the attempted feature language. Even in this four-man geometry, a mobile opposing king creates dozens of local topologies. Symbolic complexity is real and appears as soon as the adversarial resource becomes two-dimensional.
| Frozen Pilot 1 verdict<br>STRONG POSITIVE SIGNAL, WITH A REAL COMPLEXITY WARNING. The experiment demonstrates the existence of exact machine-discoverable symbolic structure in a backward chess attractor, while also demonstrating that the structure is hierarchical and can fragment on more mobile adversarial boundaries. |
| --- |
This technical report intentionally ends with that frozen verdict. Proposed follow-on experiments, replication targets, scaling tests, and decision gates are documented separately.
# Appendix A. State encoding and solver pseudocode
## A.1 Four-man validity
| valid4(WK, WB, WP, BK, stm):<br>reject if any pieces overlap<br>reject if kings are adjacent<br>if stm == WHITE:<br>reject if WP attacks BK<br>reject if WB attacks BK through current blockers<br>otherwise accept as static-valid |
| --- |
## A.2 Four-man attractor update
| A = safe_seed<br>repeat synchronously:<br>add = {}<br>for every static-valid state s not in A:<br>if BLACK to move:<br>if exists legal successor in A, or an exact safe terminal exit:<br>add s<br>else:  # WHITE to move<br>if at least one legal move exists and every legal move stays in A,<br>with no unsafe terminal exit:<br>add s<br>if s is a draw terminal (stalemate under corrected semantics):<br>add s<br>A = A union add<br>until add is empty |
| --- |
## A.3 KPK solver
| W = set of White-winning KPK states<br>repeat:<br>White node enters W if promotion is legal OR exists successor in W<br>Black node enters W if there is at least one legal move,<br>no legal pawn-capture draw exit,<br>and every legal successor is in W<br>until fixed point<br>all static-valid KPK states outside W are classified drawn for Black |
| --- |
## A.4 Neutralisation attractor
Inside the corrected safe basin, a non-bishop geometry is universal if every legal wrong-coloured bishop placement is corrected-safe. All states in universal geometries are neutralisation rank 0; safe terminal states are also rank 0. The same exists/forall recurrence is then applied inside the corrected-safe set. Final result: all 308,810 safe states receive a neutralisation rank; maximum rank 13.
# Appendix B. Exact original layer counts
| n | \|Bn\| | \|Dn\| cumulative |
| --- | --- | --- |
| 1 | 29001 | 51009 |
| 2 | 20034 | 71043 |
| 3 | 35802 | 106845 |
| 4 | 24224 | 131069 |
| 5 | 34406 | 165475 |
| 6 | 18593 | 184068 |
| 7 | 25765 | 209833 |
| 8 | 7895 | 217728 |
| 9 | 10045 | 227773 |
| 10 | 523 | 228296 |
| 11 | 441 | 228737 |
| 12 | 0 | 228737 |
Original fixed point: D11 = 228,737; B12 is empty. Total predecessor states beyond D0: 206,729.
# Appendix C. Pawn-surface base-mask vocabulary
For convenience, the thirteen base masks are repeated here in diagonal order. They are square masks, not necessarily single contiguous segments before blocker/correction processing.
| Mask | Squares |
| --- | --- |
| M1 | {h7} |
| M2 | {a2,b3,c4,d5,e6,f7,h7} |
| M3 | {b1,c2,d3,f7,e8,g8} |
| M4 | {a2,b3,c4,d5,e6,h7} |
| M5 | {f7,e8,g8} |
| M6 | {e8} |
| M7 | {b1,c2,d3,e4,f7,e8,g8} |
| M8 | {e8,g8} |
| M9 | {b1,c2,f7,e8,g8} |
| M10 | {b1,c2} |
| M11 | {b1,c2,d3} |
| M12 | {b1,c2,d3,e4} |
| M13 | {h7,e8,g8} |
The mask vocabulary should be treated as a frozen reconstruction artifact. A future implementation should derive these from data and then compare the derived vocabulary to this list, rather than hard-code them as assumed chess truths.
# Appendix D. Reproduction checklist and certificate schema
1.  Enumerate all 1,572,864 raw states and confirm exactly 1,182,440 static-valid.
2.  Confirm exactly 22,008 h8 seed states.
3.  Recompute the original conservative attractor and match every original layer count through rank 11.
4.  Build independent KPK solver; with h2-h4 enabled confirm 41,619 valid, 29,520 White wins, 12,099 draws.
5.  Recompute corrected four-man basin and confirm 308,810 total, 286,802 beyond h8, max rank 15.
6.  Recompute universal non-bishop geometries and neutralisation ranks; confirm 256,639 neutral targets, 8,798 universal geometries, 263 extra terminals, all 308,810 ranked, max neutral rank 13.
7.  Recreate old mixed set: 2,354 geometries / 37,456 old-safe states. Confirm 18,404 become universal and 19,052 survive across 1,181 geometries.
8.  Emit residual placement CSV and confirm 33,461 legal placements, 27,838 corrected-safe, 5,623 bad.
9.  Check race-surface identity and 703/261/217 split.
10.  Check mechanism counts 2,646 / 2,262 / 496 / 219.
11.  Check diagonal cone, interval component counts, edge-ray counts, projection-offset bounds.
12.  Reconstruct pawn-surface 13-mask grammar and 683/703 blocker-rule success; enumerate the remaining 20 correction geometries explicitly.
13.  Hash all generated state-membership bitsets and CSVs; store the hash, compiler/interpreter versions, and deterministic code revision in the final certificate.
14.  Cross-check a random and boundary-focused sample with a separate legal-move implementation (for example python-chess where representable) before publication.
| Recommended certificate contents (for reproduction, not a new experiment)<br>state-model version; move-semantics version; raw/static-valid counts; bitset SHA-256 for original and corrected attractors; per-rank histograms; KPK bitset hash; residual CSV hash; zero-counterexample logs for each exact lemma; and a list of every superseded configuration flag. |
| --- |
