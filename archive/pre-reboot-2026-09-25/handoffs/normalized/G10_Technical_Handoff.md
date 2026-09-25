<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G10_Technical_Handoff.docx
original_sha256: 41267d308be04d79f078fbc3f41aa47add8d0a085bfe7b9cad1587edca7787be
derivative_filename: G10_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

G10 Final Chess Ruleset and
State-Semantics Contract
TECHNICAL HANDOFF | G10.0-G10.6 FROZEN CLOSEOUT
11 August 2026
| FINAL STATUS | CLOSED - PASS; G11 UNLOCKED |
| --- | --- |
| FREEZE | G10.RULES.v1.0 \| 11 August 2026 |
Mission achieved: freeze one unambiguous full legal-play chess state and transition contract before the programme scales again.
# 1. Executive synthesis
G10 is the first programme after the G9 strategic reset. Its job was not to solve a larger arena. It was to remove a foundational ambiguity: exactly what game, state, history and draw semantics the eventual initial-position proof is supposed to certify. The G9 roadmap explicitly makes this a blocking dependency for G11, G12, G20 and the later initial-position connection work.
G10 closes that dependency at the specification level. It freezes G10.RULES.v1.0: a standard-chess legal-play state containing piece placement, side to move, persistent castling rights, effective en-passant state, the 50/75-move halfmove counter, and a bounded repetition-history summary. It also freezes legal claim actions, automatic terminal precedence, exact dead-position semantics, reachability typing, canonical identity and versioning rules.
The most useful new result is not another chess outcome. It is a small exact history calculus. G10 proves that after a pawn move, capture, or permanent loss of castling rights, no earlier FIDE-repetition position can recur. Repetition history before that barrier can therefore be discarded without changing any future threefold/fivefold draw semantics. Within a barrier epoch, only occurrence counts matter, not order. Together with the automatic 75-move draw, this makes the history component finite and directly representable in an exact state graph.
G10 does not claim that move generation is independently correct. That is deliberately left to G11. Nor does it replace exact dead-position classification with an insufficient-material heuristic: deadness is frozen as the global FIDE condition that no legal continuation can ever reach checkmate. G11/G12 must implement and certify that semantics rather than weakening it.
# 2. Authority, predecessor seam and source precedence
The sequential kickoff requested the G9 roadmap plus the technical handoff of the immediately preceding G. There is no G9 technical handoff in the File Library, for a non-accidental reason: G9 was a planning/review programme whose frozen closeout contract required exactly three principal documents and explicitly said not to create a G10 kickoff memo. G10 therefore does not fabricate a missing G9 handoff.
| Authority level | Artifact / source | How G10 uses it |
| --- | --- | --- |
| 1 - permanent programme map | G9_G10_Onwards_Long_Range_Plan.docx | Authoritative mission, dependency order and G10 advance condition. |
| 2 - immediate planning baseline | G9_Road_to_100_Assessment.docx | Authoritative G9 capability gap: rules/model completeness remained low and disconnected from the initial position. |
| 3 - latest frozen technical truth | G8_Certificate_Engine_and_Reascent_Final_Technical_Handoff.docx | Latest technical state: restricted-eight-man exact solving, typed dependencies, compact certificates, independent replay; not full-rule semantics. |
| 4 - rules authority | FIDE Laws of Chess taking effect 1 January 2023, current FIDE Handbook listing checked 11 Aug 2026 | Primary external authority for legal moves, castling/en-passant, mate/stalemate/dead position, threefold/50 claims and fivefold/75 automatic draws. |
Frozen G6 historical certification exceptions remain untouched. G10 has no need to inspect or repair them because they do not determine the final rules contract.
# 3. G10 mission and advance criteria
Roadmap mission: "Freeze the exact game that 100% is supposed to prove." The programme must make every state variable and outcome convention explicit before any larger final-model computation is allowed.
| Roadmap question | G10 frozen answer |
| --- | --- |
| Castling rights? | Four monotone historical rights K,Q,k,q are explicit state. A true right requires the corresponding home king/rook occupancy; false rights never restore. |
| En-passant rights? | State stores only effective en-passant: a target exists only when at least one en-passant capture is actually legal. Nominal but legally unusable targets canonicalize to null. |
| Repetition identity? | Piece placement + side to move + castling rights + effective en-passant. Halfmove and repetition counters are not part of the same-position key. |
| 50/75-move state? | Exact halfmove counter since last pawn move or capture. Claims begin at 100 halfmoves; automatic draw at 150, with checkmate precedence on the 150th move. |
| Threefold/fivefold history? | Bounded occurrence-count map over repetition keys since the last exact repetition barrier. |
| Dead positions? | Exact global no-checkmate-reachable condition, not insufficient-material shorthand. |
| Historical reachability? | Separated by type: arena-admissible truth is not silently called start-reachable. Final proof use requires a reachable entry edge or explicit reachability certificate. |
| Canonical identity? | Full state = board, turn, castling, effective EP, halfmove, repetition counts. Canonical raw bytes define identity; hashes are transport addresses only. |
# 4. What game is being solved
## 4.1 Core theorem scope
The 100% target is frozen as the adversarial legal-play game of standard chess: from the normal initial position, prove by a machine-checkable certificate that White has a strategy whose outcome is never BLACK_WIN against every legal Black reply. The external outcome vocabulary is absolute: WHITE_WIN, DRAW, BLACK_WIN. Implementations may use turn-relative encodings internally only if the certificate states the conversion.
## 4.2 Included in the core graph
- All ordinary legal piece moves, captures, checks, check evasions, promotions and underpromotions.
- Standard castling, including persistent historical rights and attacked/transit-square restrictions.
- En-passant with its one-move historical availability and king-safety legality.
- Checkmate, stalemate and exact dead-position termination.
- Claimable threefold repetition and 50-move draws as player actions, including claims based on an intended legal move.
- Automatic fivefold repetition and 75-move draws, including checkmate precedence on the last 75-move-rule move.
## 4.3 Deliberately outside the core proof graph
| Feature | Reason for exclusion | Effect on White-non-loss theorem |
| --- | --- | --- |
| Draw by agreement | Requires opponent consent; tournament/event rules may also restrict offers. | Removing a bilateral option does not remove a unilateral forced non-loss strategy against an adversarial opponent. |
| Resignation | Voluntary concession, not a forced board outcome. | A non-losing strategy never needs to resign. |
| Clock forfeits / time controls | Depend on event-specific clock parameters rather than the abstract legal-move graph. | The theorem is about legal-play chess, not a guarantee of human clock performance. |
| Conduct penalties / arbiter sanctions | Competition administration, not chess-position transition semantics. | Outside the game-theoretic state graph. |
| Move notation / fullmove number | Needed for records, not for legality or board-game outcome. | Omitted from canonical state identity. |
This is a scope declaration, not a claim that the omitted competition procedures do not exist. It fixes an unambiguous mathematical game suitable for weak solution. If the project later decides that a different competition-layer theorem is desired, that is a breaking rules-contract change.
# 5. Canonical full-state schema - G10.STATE.v1
| Field | Canonical meaning | Active-state constraints |
| --- | --- | --- |
| board64 | 64-square piece placement in a1..h8 order using .PNBRQKpnbrqk. | Exactly one king of each colour; all further legality checked by G11. |
| turn | Side to move: w or b. | Exactly one value. |
| castling_rights | Sorted subset of KQkq. Historical and monotone. | A true right requires home king/rook occupancy; rights never reappear. |
| ep_effective | Square or null. Retained only if at least one legal EP capture exists now. | Null if no legal EP capture exists, including pinned pseudo-EP cases. |
| halfmove_clock | Halfmoves since last pawn move or capture. | 0..149 for an active state; reset on pawn move/capture. |
| rep_counts | Sorted map from raw canonical repetition keys to occurrence counts within current barrier epoch. | Each active count 1..4; current repetition key must be present. |
Full state identity includes every field above. Two positions with the same board can therefore be different exact game states if castling, en-passant, 50/75-move or repetition history changes the future legal outcome.
# 6. Repetition identity and bounded-history calculus
## 6.1 Repetition key
The canonical FIDE same-position key is:
```text
REP1 := board64 | turn | castling_rights | ep_effective
```
The halfmove clock and repetition count map are deliberately excluded from this key: they affect whether a draw may/must be declared, but they do not change whether two positions are the "same position" for repetition purposes.
## 6.2 G10-L1 - History Barrier Lemma
The following move types are exact repetition barriers: pawn move; capture; permanent castling-right reduction. After such a move, no repetition key from before the move can ever recur, so all earlier repetition counts may be discarded.
| Barrier | Why an earlier same-position key cannot return |
| --- | --- |
| Pawn move | Pawn progress is irreversible. Pawns do not move backward and promotions remove pawns rather than recreate an earlier pawn placement. |
| Capture | The total number of pieces decreases and chess has no operation that recreates a captured piece as an additional piece. |
| Castling-right reduction | Castling rights are monotone. Once a king/rook move has removed a right, an earlier position requiring that right cannot be the same FIDE position again. |
## 6.3 G10-L2 - Count Sufficiency Lemma
Inside one barrier epoch, the future threefold/fivefold rules depend only on how many times each repetition key has occurred. The order of those occurrences is irrelevant. Therefore an ordered history trace can be quotiented exactly to a sorted key->count map. On each non-barrier move, increment exactly the successor key; on a barrier move, replace the map with {successor key: 1}.
## 6.4 Finiteness
No active repetition count can exceed 4 because the fifth occurrence is an automatic draw. The 75-move rule also bounds a no-pawn/no-capture period at 150 halfmoves. A castling-right barrier can only shorten the relevant repetition epoch. History-sensitive chess therefore remains a finite-state game under this contract; G20 may scale the representation without inventing an unbounded move-history tape.
# 7. Claim actions and automatic terminal semantics
## 7.1 Claimable draws are actions
| Action | Availability | State transition |
| --- | --- | --- |
| CLAIM_3_NOW | Current repetition key count >= 3. | Immediate DRAW; no board move. |
| CLAIM_3_BY_MOVE(m) | m is legal and its resulting repetition key would be at least the third occurrence. | Immediate DRAW before m is executed. |
| CLAIM_50_NOW | halfmove_clock >= 100. | Immediate DRAW; no board move. |
| CLAIM_50_BY_MOVE(m) | m is a legal non-pawn, non-capture move and would bring the clock to >=100. | Immediate DRAW before m is executed. |
Incorrect real-world claims and their clock penalties are not graph actions: the exact solver enumerates only valid claim actions. This removes an administrative error path without changing the legal strategic choices available to a perfect player.
## 7.2 Post-move terminal precedence
1. CHECKMATE - win for the mover.
1. STALEMATE - draw.
1. DEAD POSITION - draw.
1. FIVEFOLD REPETITION - draw when successor key count reaches 5.
1. 75-MOVE RULE - draw when successor halfmove clock reaches 150.
1. Otherwise the successor is active.
The order encodes the load-bearing FIDE exception that if the 150th non-resetting halfmove gives checkmate, checkmate takes precedence over the automatic 75-move draw. Stalemate/dead/fivefold are all draws, so their mutual order does not change the absolute outcome but is kept deterministic for certificate replay.
# 8. Dead-position semantics - exact, not heuristic
G10 freezes the FIDE dead-position concept extensionally: a position is DEAD iff there exists no finite sequence of legal moves from that position that reaches checkmate by either player. This is a reachability-to-mate property of the underlying legal move graph, not merely a material checklist.
Consequences for later programmes:
- K vs K, K+B vs K and K+N vs K are useful positive dead-position controls, but they do not define the whole predicate.
- An "insufficient material" library helper may be used only as a sound subset/optimization if independently proved sound for that use; it cannot stand in for DEAD by assertion.
- G12 small-arena certification must include positions where board geometry, blocking or history makes deadness nontrivial, so the exact predicate is exercised rather than bypassed.
- Any old Pilot-G8 arena that used a weaker terminal model remains historically valid only under its frozen model; G10 does not retroactively relabel it full-rule truth.
# 9. Legal historical reachability versus arena admissibility
G10 explicitly separates board/state truth from provenance. This prevents a common error: treating a locally sensible reconstructed endgame state as though it had already been proved reachable from the normal start.
| Type | Meaning | Permitted use |
| --- | --- | --- |
| ARENA_ADMISSIBLE | Satisfies the arena/state invariants declared by a solver; may be historically unreachable. | Exact finite-arena science, regression tests and lower-basin truth. |
| START_REACHABLE | There exists a legal path from the standard initial full state under G10.RULES.v1.0. | Required for nodes that occur on the final initial-position proof path. |
| REACHABLE_ENTRY_CERTIFIED | An ARENA_ADMISSIBLE basin state entered by a legal edge from an already START_REACHABLE parent, or accompanied by a reachability certificate. | Allows a broad lower table to be reused without proving every table row start-reachable. |
This separation is deliberately economical. A lower exact table may contain unreachable rows. The final proof need only demonstrate that each row it actually enters is a matching full G10 state reached from a certified parent. No global historical-reachability solve is required merely to store unused rows.
# 10. Canonical serialization, hashes and versioning
Semantic equality is defined by canonical raw state bytes, not by a cryptographic digest. A SHA-256 digest may be used as a content address, as in G8, but implementations must treat the canonical payload as the equality authority if a digest collision is ever observed. This preserves exact semantics while retaining the practical economics of a content-addressed proof store.
- Castling rights serialize in KQkq order.
- Repetition-count entries serialize lexicographically by the raw repetition-key bytes.
- Every field is length-delimited; no parser may infer field boundaries from punctuation that can appear in a payload.
- Any change to state identity, legal actions, claim rules, terminal precedence, deadness or reachability typing is a breaking major version.
- Pure implementation/packing optimizations that preserve canonical bytes and transitions are non-breaking implementation revisions.
# 11. Work actually performed - G10.0 to G10.6
| Substage | Work | Frozen result |
| --- | --- | --- |
| G10.0 - Authority freeze | Resolved G9 predecessor seam; froze G9 roadmap/assessment + G8 technical truth + current FIDE Laws as source precedence. | No invented G9 handoff; no historical repair. |
| G10.1 - Scope freeze | Separated adversarial board-game legal play from event administration. | Declared exact theorem scope and outcome vocabulary. |
| G10.2 - State construction | Enumerated all history-sensitive state needed by castling, EP, repetition and 50/75 rules. | G10.STATE.v1 schema. |
| G10.3 - Repetition calculus | Derived barrier, count-sufficiency, active-count and finiteness lemmas. | Finite exact history representation. |
| G10.4 - Terminal/claim contract | Specified claim actions and automatic terminal precedence, including exact deadness. | Deterministic transition/terminal contract. |
| G10.5 - Reachability + serialization | Separated arena admissibility from start reachability; froze raw canonical identity and hash policy. | Safe reuse rule for lower basins. |
| G10.6 - Machine artifacts + tests | Wrote JSON contract, executable metadata layer, frozen G11 conformance vectors and 11 unit tests; hashed bundle. | 11/11 metadata tests pass; artifacts frozen. |
# 12. Verification status and quantitative evidence
The executable G10 layer tests only the history/metadata semantics owned by this programme. It intentionally does not contain a chess move generator; therefore these are contract tests, not G11 independent-conformance evidence.
| Check | Result |
| --- | --- |
| Metadata unit tests | 11 / 11 PASS |
| Castling-right monotonicity | Restoration attempt rejected |
| Pawn/capture barrier behavior | PASS; history reset and halfmove reset |
| Castling-right barrier behavior | PASS; history reset without halfmove reset |
| Threefold now / by intended move | PASS |
| 50-move now / by intended move | PASS |
| Fivefold automatic draw | PASS |
| 75-move automatic draw | PASS |
| Checkmate precedence at halfmove 150 | PASS |
Frozen conformance vectors additionally cover legal versus pinned-illegal en-passant, stalemate, checkmate, elementary dead/non-dead controls, castling-right identity and intended-claim edge cases. Those board-legality vectors remain PENDING until G11 runs them through two independent move/state implementations.
# 13. Frozen artifact inventory
| Artifact | SHA-256 | Role |
| --- | --- | --- |
| G10_Rules_Contract_v1.json | c0e2430e6dabf029193897e6c621e614914963290f07ecb8946049543a13edca | Machine-readable rules/state contract. |
| g10_contract.py | 1aeea039ea9b46f10a189bcf968543009558a88d8a36ca362c854a96de045062 | Executable metadata/reference layer; no move generation. |
| test_g10_contract.py | 806806622a8015515c88f30999618e223d10ca2b8e61686a80d35fc717c2d36e | 11 contract tests. |
| G10_Conformance_Vectors_v1.json | 317a192513f99b467b2afb888a74e9607950aa2c50b90848a98c1feb2aedbb4d | Frozen G11 edge-case vectors. |
| G10_README.md | 1c71e7b5cd41041d67f3275cdbbc1491c8fb6cd73bc3aaa0a5817bfad0aa69bb | Bundle boundary and usage note. |
| G10_Semantics_Contract_Bundle.zip | a0c5c2df8f8f61d8f6365ae8750491e3d64df821d060f9d24edb6ad9342b0793 | Frozen bundle of the above files plus checksum ledger. |
# 14. Negative results, rejected shortcuts and corrections
- REJECTED: using board placement + side-to-move alone as canonical position identity. It loses castling/en-passant and history-dependent draw semantics.
- REJECTED: storing only the current repetition count. Future claims depend on counts of other keys that may recur before the next barrier.
- REJECTED: storing an unbounded full move history. The barrier/count lemmas give an exact finite quotient.
- REJECTED: treating a raw FEN en-passant target as repetition-significant when no legal en-passant capture exists. G10 stores only effective legal EP.
- REJECTED: "insufficient material" as the definition of dead position. The final contract uses no-checkmate-reachable semantics.
- REJECTED: silently calling all locally valid endgame rows historically reachable. Reachability is explicitly typed.
- REJECTED: absorbing tournament clock/arbiter procedures into the state graph without a fixed competition specification. G10 freezes the legal-play board game instead.
# 15. What remains unresolved
| Open item | Status at G10 close | Owner |
| --- | --- | --- |
| Independent move generation | No independent implementation pair yet. | G11 - blocking. |
| Effective EP computation | Semantics frozen; must be computed by legal move generator, including king-safety pins. | G11. |
| Static/local state admissibility | Schema/invariants frozen; exact conformance rejection corpus not yet exhaustive. | G11. |
| Exact dead-position engine | Definition frozen; no general implementation certified here. | G11/G12, with G12 exact small-arena truth. |
| Full-rule arena regression | Historical truths not retroactively re-solved. | G12. |
| Large history-state economics | Finite representation proved; scaling behavior not yet measured. | G20. |
| Formal proof assistant core | No mechanized theorem-prover encoding in G10. | G15. |
| Initial-position reachability/canonical forward graph | Type contract exists but no forward canonicalizer yet. | G35. |
# 16. Implications for the G9 roadmap
No roadmap renumbering is justified. G10 succeeds on the exact dependency the G9 plan assigned to it and therefore unlocks G11. It also sharpens several later stages:
- G11 must compare two implementations on full state identity and history transitions, not merely board legal moves.
- G12 must certify exact deadness and claim/automatic-draw behavior in small arenas; old restricted-model W/D/L hashes remain historical where semantics differ.
- G14 proof-store keys must version the G10 contract and preserve canonical raw payloads behind hashes.
- G20 inherits the History Barrier and Count Sufficiency lemmas as the preferred exact representation for history-dependent draw scaling.
- G35 forward canonicalization must generate the complete G10 full state, not FEN-like board state with history dropped.
G9 scored rules/model completeness at only 20/100 and total programme readiness at 24%. G10 materially closes the specification portion of that gap, but no new overall percentage is frozen here: independent conformance (G11) and full-rule exact anchors (G12) are still missing, so rescoring now would risk rewarding a paper contract as though it were verified implementation.
# 17. G10 advance / failure gate
| Gate | Verdict | Evidence |
| --- | --- | --- |
| One unambiguous ruleset stated | MET | G10.RULES.v1.0 declares core legal-play scope and exclusions. |
| Every history-sensitive state variable explicit | MET | Castling, effective EP, halfmove, repetition map all in machine schema. |
| Canonical position and full-state identity explicit | MET | REP1 and G10.STATE.v1 defined separately. |
| Claim semantics explicit | MET | Threefold/50 now and intended-move actions frozen. |
| Automatic terminals explicit | MET | Mate/stalemate/dead/fivefold/75 semantics and precedence frozen. |
| Historical reachability safely separated | MET | ARENA_ADMISSIBLE vs START_REACHABLE / certified entry typing. |
| Machine-readable artifacts and tests | MET | JSON contract + executable layer + vectors; 11/11 metadata tests. |
| No hidden implementation-conformance claim | MET | Move generation explicitly deferred to G11; deadness execution to G11/G12. |
FINAL G10 VERDICT: PASS. The programme may advance to G11. No larger "final-model" exact solve should be treated as authoritative until G11 resolves move/state conformance.
# 18. Successor Contract - G11
G11 immediate mission: build two genuinely independent implementations of G10.RULES.v1.0 state identity and legal transition semantics, then force them to agree on a frozen conformance corpus.
| Successor item | Frozen instruction |
| --- | --- |
| Programme number | G11 - Independent Move-Generation and State-Conformance Suite. |
| Inherits | G10.RULES.v1.0, G10.STATE.v1, REP1, G10-L1..L4, claim/terminal precedence, reachability typing, frozen conformance vectors. |
| Immediate deliverables | Reference generator; independently written conformance generator; full-state serializer; predecessor/successor round trips; fuzz/property corpus; zero-unexplained-mismatch ledger. |
| Blocking rule | Any unexplained legality, state-identity, castling, EP, claim, terminal or history-transition mismatch blocks G12. |
| Required special cases | Castling through/into check; rights loss and rook capture; legal/pinned EP; promotion/underpromotion; check evasions; mate/stalemate; threefold/fivefold; 50/75; exact deadness hooks; malformed/unreachable state rejection typing. |
| Independence requirement | The second implementation must not call the first generator, reuse its move list, or replay producer queues. Shared test vectors and the frozen G10 contract are allowed. |
| Older artifacts genuinely needed? | None for semantic authority. G11 can proceed from the permanent G9 roadmap + this G10 handoff + G10 bundle. G8 may be consulted only as optional engineering regression context, not to define full-rule semantics. |
| Natural close | Zero unexplained mismatches across the frozen suite plus exhaustive small-domain and adversarial/fuzz coverage sufficient to unlock G12. Preserve every mismatch and correction in the G11 handoff. |
# 19. Source and rule reference ledger
- FIDE Handbook, FIDE Laws of Chess taking effect from 1 January 2023 (current Laws entry verified in the official Handbook on 11 August 2026). Relevant areas: Article 3 (moves, en-passant, castling), Article 5 (checkmate, stalemate, dead position), Article 9 (threefold/fivefold repetition and 50/75-move rules).
- G9_G10_Onwards_Long_Range_Plan.docx - authoritative dependency map and G10 mission/advance condition.
- G9_Road_to_100_Assessment.docx - authoritative G9 progress baseline and rules/model gap.
- G8_Certificate_Engine_and_Reascent_Final_Technical_Handoff.docx - latest pre-G9 frozen technical truth; restricted-model results remain historically scoped.
G10 CLOSED - RULES/STATE CONTRACT FROZEN - G11 UNLOCKED
