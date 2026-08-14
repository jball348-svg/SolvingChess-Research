<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G11_Technical_Handoff.docx
original_sha256: 6c52873dcf9ceda157ac954f73374340038f635ff85ececbc21b239fcfc5db89
derivative_filename: G11_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

G11
Independent Move-Generation and
State-Conformance Suite
Technical Handoff
Solving Chess research project
Frozen closeout | 11 August 2026
| CLOSED AT NATURAL FRONTIER — STRONG LOCAL CONFORMANCE PASS; ROADMAP G11 GATE ON HOLD<br>Original G12 full-rule solving is not yet authorised. |
| --- |
Permanent authority: G9_G10_Onwards_Long_Range_Plan.docx
Immediate technical authority: G10_Technical_Handoff.docx
# 1. Frozen verdict and programme identity
Programme: G11 — Independent Move-Generation and State-Conformance Suite.
Roadmap mission: build two genuinely independent implementations of the G10 state and move rules and force them to agree.
Programme close verdict: the new local conformance stack is a strong zero-known-mismatch result, but the formal roadmap advance condition is not fully met because the exact frozen G10 conformance-vector payload and canonical byte serialization bundle were not retrievable in this session. This is a blocking artifact boundary, not a discovered chess-rule mismatch.
| Gate item | Verdict | Meaning |
| --- | --- | --- |
| Two structurally independent move/state implementations | MET locally | Different board representations and attack-generation algorithms; neither engine imports the other. |
| Curated special-move/history suite | MET locally | All completed controls agree with zero A/B mismatches. |
| Exhaustive small-domain conformance | MET locally | 98,623 locally valid states and 889,808 legal edges, zero mismatches. |
| Adversarial/fuzz conformance | MET locally | Attack maps, mixed boards, EP constructions, reachable games and malformed mutations all returned zero mismatches. |
| Exact frozen G10 vector replay | BLOCKED | The named G10 vector file was not retrievable as a standalone File Library artifact. |
| Byte-identical G10 canonical serialization | BLOCKED | G10 says canonical raw bytes are equality authority; G11LC1 is only a local differential profile. |
| General exact DEAD predicate | DEFERRED BY CONTRACT | Only sound positive hooks are present; G12 is explicitly responsible for exact small-arena deadness. |
| Roadmap G11 advance condition | NOT FULLY MET | Therefore the original G12 solve must begin with a conformance-closure pre-gate. |
No unexplained legality or state-transition mismatch was found. The hold is provenance/identity-level: the missing frozen G10 payload prevents claiming that the suite actually replayed the exact corpus and bytes that G10 froze.
# 2. Authority and reconstructed starting state
| Authority level | Source | Frozen use in G11 |
| --- | --- | --- |
| 1 — permanent programme map | G9_G10_Onwards_Long_Range_Plan.docx | Defines G11 mission, advance gate, dependencies and G12 successor mission. |
| 2 — immediate technical state | G10_Technical_Handoff.docx | Authoritative G10.RULES.v1.0 / G10.STATE.v1 semantics, open conformance seam, artifact hashes and G11 Successor Contract. |
| 3 — G10 named machine artifacts | Bundle/vector files named and hashed by G10 | Required for exact frozen-vector and canonical-byte replay; not independently retrievable in this session. |
G10 closed as a PASS and explicitly unlocked G11, while forbidding authoritative larger final-model solves until independent move/state conformance was established. Its unresolved blocking items assigned to G11 were independent move generation, effective en-passant computation including king-safety pins, and a stronger local state-admissibility/rejection corpus. Exact general dead-position execution was shared between G11 and G12, with G12 owning exact small-arena truth.
## 2.1 Inherited state semantics that G11 did not change
| Field / rule | Inherited G10 meaning |
| --- | --- |
| board64 | 64-square piece placement, a1 through h8; one king per side plus legality constraints. |
| turn | Side to move: White or Black. |
| castling_rights | Monotone KQkq historical rights; true rights require home king/rook occupancy and never restore. |
| ep_effective | EP square exists only if at least one EP capture is actually legal now, including king-safety legality; unusable nominal EP canonicalizes to null. |
| halfmove_clock | Exact count since the last pawn move or capture; claims at 100, automatic draw at 150 subject to mate precedence. |
| rep_counts | Occurrence-count map for repetition keys within the current exact barrier epoch; active counts are bounded. |
| REP1 | Piece placement + turn + castling rights + effective EP; halfmove and repetition map are not part of same-position identity. |
| Full state identity | Board + turn + castling + effective EP + halfmove + repetition map, serialized canonically. |
- Pawn moves, captures and permanent castling-right reductions are exact repetition barriers; old occurrence counts are discarded after a barrier.
- Within a barrier epoch, occurrence counts are sufficient; a full ordered move-history tape is unnecessary.
- Claim actions are explicit: threefold now/by intended legal move and 50-move now/by intended non-pawn non-capture move.
- Post-move terminal precedence is CHECKMATE, STALEMATE, DEAD POSITION, FIVEFOLD, 75-MOVE, then active.
- DEAD means no finite legal continuation can ever reach checkmate by either player. “Insufficient material” is not accepted as a definition.
- ARENA_ADMISSIBLE and START_REACHABLE remain distinct. Local legality does not silently certify historical reachability from the initial position.
## 2.2 Frozen negative constraints inherited from G10
- Do not collapse identity to board placement + side to move.
- Do not store only the current repetition count.
- Do not use an unbounded full move history when the exact barrier/count quotient suffices.
- Do not preserve a nominal FEN EP target when no legal EP capture exists.
- Do not replace DEAD with an insufficient-material helper.
- Do not label every locally sensible endgame state start-reachable.
- Do not absorb clocks, arbiter sanctions or other event-administration rules into the abstract legal-play graph.
# 3. G11 mission, advance criterion and actual programme shape
The G9 roadmap required a reference move generator, an independently written conformance generator, a differential corpus, fuzz/property tests, state serialization, successor/predecessor round trips and a zero-unexplained-mismatch ledger. Any unexplained legality mismatch was blocking. G10 sharpened this: G11 had to compare full state identity and history transitions, not merely board legal moves.
| Substage | Work actually performed | Frozen result |
| --- | --- | --- |
| G11.0 — authority reconstruction | Resolved programme number; retrieved G9 roadmap and G10 handoff; searched exact G10 bundle/vector names. | G11 confirmed. Missing standalone G10 payload became an explicit potential gate risk, not an excuse to stop. |
| G11.1 — implementation A | Built flat 0..63 board generator with source-centric attack scans, special moves and G10 metadata transitions. | Reference engine A64-source-rays. |
| G11.2 — implementation B | Built sparse coordinate-map generator with target-centric attack queries and separately implemented transitions/validation/serialization. | Conformance engine Bmap-target-rays. |
| G11.3 — semantic corpus | Encoded castling, EP, promotion, checks, mate/stalemate, claims, automatic draws, barriers, deadness controls and malformed states. | 27 curated controls; zero mismatches. |
| G11.4 — external-count move regression | Ran fixed perft anchors through both engines. | 11 depth/position anchors reproduced by both. |
| G11.5 — exact small-domain differential | Exhaustive K v K plus locally valid a-file K+R v K and K+P v K slices. | 98,623 states; 889,808 legal edges; zero mismatches. |
| G11.6 — adversarial differential | Attack-map fuzz, mixed-piece boards, effective-EP constructions and malformed mutations. | 256,000 attack queries; 5,000 mixed states; 2,000 EP cases; 5,000 malformed mutations; zero mismatches. |
| G11.7 — reachable/full-state fuzz | Deterministic games from the normal start; full state transitions, local serializer round trips, terminal and undo spot checks. | 1,536 states/transitions; zero mismatches. |
| G11.8 — gate audit | Compared achieved local evidence with the exact frozen G10 artifact requirement. | Strong local PASS, but formal G11 gate HOLD because exact G10 vector/byte payload is unavailable. |
# 4. New conformance architecture
## 4.1 Engine A — A64-source-rays
- Flat 64-element board indexed a1=0 through h8=63.
- Source-centric attack detection: enumerate attacking pieces and trace whether each attacks a target.
- Independent pseudo-move generation for pawns, leapers, sliders and king moves; legal moves filtered by own-king safety.
- Explicit castling checks for right, home rook, clearance, current check and attacked transit/destination squares.
- EP simulation removes the captured pawn before king-safety validation; pinned EP is therefore rejected.
- G10 history transition logic separately updates rights, barriers, halfmove clock, effective EP and repetition counts.
## 4.2 Engine B — Bmap-target-rays
- Sparse map keyed by (file, rank) coordinates, converted to/from neutral board64 only at the interface.
- Target-centric attack detection: inspect pawn/knight/king origins and ray outward from the target to the first slider blocker.
- Separately written move generation, castling, EP, promotion, rights loss, history updates, claims and terminal handling.
- No import of Engine A. The test harness is the only component that sees both implementations.
## 4.3 Independence boundary
This is genuine structural/software independence in the narrow sense relevant to differential testing: different board representations, different attack-direction logic and separately implemented transition code with no producer-source import. It is not organizational independence: both implementations were authored within the same research session. The handoff therefore treats zero differential mismatch as strong implementation evidence, not as a proof that both cannot share a conceptual misunderstanding of G10.
## 4.4 Local serialization profile
Both engines independently serialize and deserialize the full local state with length-delimited fields, sorted repetition entries and deterministic bytes. The harness verifies byte equality after normalizing the engine marker and round-trips each serializer. This profile is frozen as G11LC1 for conformance engineering only.
G11LC1 is explicitly NOT the G10 canonical serialization. Because the frozen G10 byte profile is unavailable, matching G11LC1 cannot satisfy G10’s statement that canonical raw bytes are the equality authority.
# 5. Verification results and quantitative evidence
| Evidence class | Completed volume | A/B mismatches | Status |
| --- | --- | --- | --- |
| Curated semantic controls | 27 controls | 0 | PASS |
| Fixed perft regression | 11 depth/position anchors | 0; both equal expected counts | PASS |
| Exhaustive small domains | 98,623 states; 889,808 legal edges | 0 | PASS |
| Attack-map adversarial fuzz | 256,000 target/side queries | 0 | PASS |
| Mixed-board fuzz | 5,000 valid states; 2,000 sampled transitions | 0 | PASS |
| EP adversarial construction | 2,000 cases | 0 | PASS |
| Reachable-game fuzz | 1,536 states; 1,536 transitions | 0 | PASS |
| Malformed mutation fuzz | 5,000 mutations | 0 | PASS |
## 5.1 Fixed perft anchors
| Position | Depth | Expected | A | B |
| --- | --- | --- | --- | --- |
| start | 1 | 20 | 20 | 20 |
| start | 2 | 400 | 400 | 400 |
| start | 3 | 8,902 | 8,902 | 8,902 |
| start | 4 | 197,281 | 197,281 | 197,281 |
| perft_position_3 | 1 | 14 | 14 | 14 |
| perft_position_3 | 2 | 191 | 191 | 191 |
| perft_position_3 | 3 | 2,812 | 2,812 | 2,812 |
| perft_position_3 | 4 | 43,238 | 43,238 | 43,238 |
| perft_position_5 | 1 | 44 | 44 | 44 |
| perft_position_5 | 2 | 1,486 | 1,486 | 1,486 |
| perft_position_5 | 3 | 62,379 | 62,379 | 62,379 |
These counts are regression anchors for move generation. They are not by themselves a proof of G10 compliance, because standard perft does not encode the project’s full repetition/claim/dead-position state contract.
## 5.2 Exhaustive small-domain agreement
| Domain | Declared scope | States | Legal edges | Mismatch |
| --- | --- | --- | --- | --- |
| K v K | all non-adjacent king placements, both turns | 7,224 | 44,352 | 0 |
| K+R v K | extra piece on a-file; locally valid positions only; both turns | 49,780 | 559,698 | 0 |
| K+P v K | extra piece on a-file; locally valid positions only; both turns | 41,619 | 285,758 | 0 |
“Exact” here means exhaustive over these declared finite conformance domains. It does not mean a theorem about chess generally, nor does it establish game-theoretic W/D/L truth.
## 5.3 Adversarial and fuzz evidence
| Campaign | Frozen quantitative result | Interpretation |
| --- | --- | --- |
| Attack-map fuzz | 2,000 synthetic boards × 64 squares × 2 attacking sides = 256,000 queries; 0 mismatches | Directly cross-checks the two fundamentally different attack algorithms. |
| Mixed-board fuzz | 5,000 locally valid mixed-piece states from 7,992 attempts; 2,000 sampled transitions; 0 mismatches | Adds bishops, knights, rooks and queens beyond the exact K/R/P slices. |
| EP adversarial fuzz | 2,000 constructions: 1,569 effective; 431 null; 1,468 locally admissible states compared; 0 mismatches | Exercises the load-bearing effective-EP/pin rule prospectively. |
| Reachable-game fuzz | 24 games × up to 64 plies; 1,536 states/transitions; 90 terminal and 80 undo spot checks; 0 mismatches | Exercises full metadata transitions on states actually generated from the normal initial position. |
| Malformed mutation fuzz | 5,000 deterministic mutations; 0 A/B classification mismatches | Checks deterministic rejection of obvious local/history impossibilities. |
## 5.4 Reachable fuzz move classes actually encountered
| Class | Observed transitions |
| --- | --- |
| castle | 7 |
| ep | 2 |
| pawn | 448 |
| promotion | 1 |
The reachable campaign is not claimed as statistical coverage of chess. Its purpose is to expose history-state divergence under ordinary legal play; rare special cases remain primarily covered by the adversarial/curated corpus.
# 6. Special-move, history and terminal conformance
| Control | Frozen result | Classification |
| --- | --- | --- |
| Castling clear | Both engines allow White O-O and O-O-O in the declared clear-rights control. | Deterministic conformance |
| Castling through check | Kingside castling rejected when f1 is attacked. | Deterministic conformance |
| Castling into check | Kingside castling rejected when g1 is attacked. | Deterministic conformance |
| Rights loss on rook move | h1-h2 converts KQkq → Qkq and creates a repetition barrier. | Deterministic conformance |
| Rights loss on rook capture | a1xa8 converts KQkq → Kk: White Q and Black q are both lost. | Deterministic conformance |
| Legal EP | e5xd6 EP retained and generated in the legal control. | Deterministic conformance |
| Pinned EP | Nominal d6 EP canonicalizes to null when e5xd6 would expose White king on the e-file. | Deterministic conformance |
| Promotion | All four q/r/b/n promotions are generated; capture-promotion control produces all eight a7 move variants. | Deterministic conformance |
| Check evasion | Only king-safe evasions survive legal filtering. | Deterministic conformance |
| Mate / stalemate | Both engines distinguish no-legal-move + check from no-legal-move + no check. | Deterministic conformance |
| Threefold now / by move | Current count ≥3 creates CLAIM_3_NOW; seeded legal successor with prior count 2 creates intended-move claim. | G10 metadata conformance |
| 50-move now / by move | Halfmove ≥100 creates NOW claim; halfmove 99 + quiet legal move creates by-move claims. | G10 metadata conformance |
| Fivefold | Seeded successor count 4 becomes automatic FIVEFOLD on quiet repetition-producing move. | G10 metadata conformance |
| 75 move | Quiet move from halfmove 149 reaches 150 and auto-draws when no higher terminal applies. | G10 metadata conformance |
| Mate precedence at 150 | Qf7-g7# from halfmove 149 is CHECKMATE, not 75-move draw. | Load-bearing precedence control |
| History barrier | Pawn move resets halfmove and repetition epoch; quiet non-barrier move preserves prior counts. | G10-L1/L2 conformance |
## 6.1 Dead-position handling — deliberately conservative
Each engine has a sound positive hook that returns DEAD for K v K, K+B v K and K+N v K. K+N+N v K is deliberately returned UNKNOWN, not “not dead”, because G11 does not substitute a material checklist for the extensional G10 predicate. Any state whose exact deadness is not established by the hook remains ACTIVE_DEADNESS_UNRESOLVED for conformance purposes.
| Control | Hook result | Claim level |
| --- | --- | --- |
| K v K | DEAD | Exact positive control |
| K+B v K | DEAD | Exact positive control |
| K+N v K | DEAD | Exact positive control |
| K+N+N v K | UNKNOWN | Conservative non-claim; not classified by material shortcut |
This is a boundary, not a failure of the G11 local move generator. G10 explicitly assigned general dead-position execution to G11/G12 and required G12 small-arena certification to exercise nontrivial exact deadness.
# 7. State-admissibility and provenance typing
Both implementations independently reject obvious malformed or history-inconsistent states using the same G10-derived invariants, while preserving the distinction between local admissibility and global start reachability.
| Rejected control | Frozen reason |
| --- | --- |
| Missing black king | king_count plus castling inconsistencies inherited from the initial-rights mutation. |
| Adjacent kings | adjacent_kings. |
| Castling right without home rook | castling_inconsistent_K. |
| Pawn on first/eighth rank | pawn_backrank. |
| Pinned nominal EP retained as “effective” | HISTORY_INCONSISTENT: ineffective_ep. |
| Non-moving side king already in check | nonmoving_king_in_check; cannot arise as an active legal turn state. |
| Promoted material impossible with all eight pawns still present | promotion_material_infeasible. |
G11 does not attempt the G35 problem of proving START_REACHABLE for arbitrary states. A locally valid state can remain ARENA_ADMISSIBLE without any claim that it is reachable from the normal start.
# 8. Claim taxonomy and what has actually been proved
| Statement | Status | Why |
| --- | --- | --- |
| A and B agree on every state in the declared exhaustive K/K, a-file KRK and a-file KPK conformance domains. | Exact finite computation | Every locally valid state in those explicitly declared domains was enumerated and compared. |
| A and B reproduce the fixed perft counts listed in this handoff. | Independently duplicated computation vs fixed anchors | Two code paths match each other and the encoded expected counts. |
| A and B agree on the completed adversarial/fuzz corpus. | Deterministic empirical / property evidence | The sampled/synthetic corpus is large but not exhaustive over chess. |
| The new engines implement all of G10 correctly. | NOT CLAIMED | Both could share a conceptual error; more importantly the exact frozen G10 vector payload was not replayed. |
| G11LC1 equals the G10 canonical byte serialization. | NOT CLAIMED | The exact G10 packing payload was unavailable. |
| The general G10 DEAD predicate is implemented. | NOT CLAIMED | Only sound positive hooks exist; exact small-arena deadness is G12 work. |
| Any historical Pilot–G8 result is now full-rule truth. | REJECTED | Old results remain attached to their frozen restricted models until explicitly re-solved. |
# 9. Negative results, holds and failed shortcuts
| Item | Frozen disposition | Consequence |
| --- | --- | --- |
| Over-wide exhaustive a–d file K+R/K+P conformance workload | HOLD_NO_RESULT after >300 s run budget; no partial output accepted. | A-file exact slice was selected only on runtime grounds before inspecting mismatch outcomes. This is an engineering workload adjustment, not a scientific arena shrink. |
| 120 games × 80 plies reachable-fuzz stress run | HOLD_NO_RESULT after combined command budget was exceeded; no partial output accepted. | Accepted 24×64 corpus is separately seeded and frozen; stress-run partials are not evidence. |
| Single-process monolithic replay in this container | Resource-throttling/timeout observed after sustained CPU work. | Final evidence ledger merges only completed deterministic phases; `g11_run_phase.py` supports fresh-process replay. |
| Use “insufficient material” for DEAD | REJECTED. | Only sound positive hooks; unknown stays unknown. |
| Invent G10 canonical bytes from prose | REJECTED. | Would silently change the equality authority and defeat the conformance gate. |
| Reconstruct the missing G10 frozen vector payload from similar tests | REJECTED. | Semantically similar controls are useful evidence but not a replay of the frozen corpus. |
# 10. Blocking artifact boundary
The immediate G10 handoff names and hashes a machine bundle containing the JSON rules contract, executable metadata layer, contract tests, frozen G11 conformance vectors, README and checksum ledger. Exact-name semantic search and navigational File Library search for the bundle and key components returned the G10 handoff itself, not standalone retrievable payloads. G11 therefore knows what should exist and its hashes, but cannot execute or byte-compare the payload.
| G10 artifact | Frozen SHA-256 | G11 status |
| --- | --- | --- |
| G10_Conformance_Vectors_v1.json | 317a192513f99b467b2afb888a74e9607950aa2c50b90848a98c1feb2aedbb4d | Named/hash-frozen by G10; not retrievable here |
| G10_README.md | 1c71e7b5cd41041d67f3275cdbbc1491c8fb6cd73bc3aaa0a5817bfad0aa69bb | Named/hash-frozen by G10; not retrievable here |
| G10_Rules_Contract_v1.json | c0e2430e6dabf029193897e6c621e614914963290f07ecb8946049543a13edca | Named/hash-frozen by G10; not retrievable here |
| G10_Semantics_Contract_Bundle.zip | a0c5c2df8f8f61d8f6365ae8750491e3d64df821d060f9d24edb6ad9342b0793 | Named/hash-frozen by G10; not retrievable here |
| g10_contract.py | 1aeea039ea9b46f10a189bcf968543009558a88d8a36ca362c854a96de045062 | Named/hash-frozen by G10; not retrievable here |
| test_g10_contract.py | 806806622a8015515c88f30999618e223d10ca2b8e61686a80d35fc717c2d36e | Named/hash-frozen by G10; not retrievable here |
Why this blocks: G10 made canonical raw bytes the state-equality authority and G10’s Successor Contract required replay of its frozen vectors. A newly invented equivalent serializer or reconstructed test suite would be a new artifact, not verification of the frozen one.
# 11. New reusable capabilities created by G11
- Two non-importing full legal-move implementations covering ordinary moves, special moves and own-king safety.
- Two independently written effective-EP computations that canonicalize nominally present but legally unusable targets to null.
- Full G10-style history metadata transition logic in both engines: castling-right barriers, pawn/capture barriers, halfmove clock and bounded repetition counts.
- Explicit valid claim-action generation for threefold and 50-move rules, including intended-move claims.
- Deterministic terminal precedence implementation with checkmate-over-75 control.
- Sound exact deadness positive hooks with an explicit UNKNOWN channel, preventing heuristic overclaim.
- Independent local state validators for obvious malformed/history-inconsistent inputs and promotion-material feasibility.
- Deterministic local full-state serializer/deserializer pair per engine with cross-engine byte comparison under G11LC1.
- Exact exhaustive conformance harnesses plus fixed-anchor, adversarial, reachable and malformed property campaigns.
- Fresh-process phase runner and content-addressed frozen artifact bundle for successor replay.
# 12. Corrections and supersessions made during G11
- An initially attempted “Kiwipete” FEN/count pairing was found not to match the remembered reference count and was excluded rather than reverse-fitted. No result from that candidate entered the frozen ledger.
- The first broad a–d exhaustive slice and large reachable-fuzz stress campaign exceeded runtime budgets; partials were explicitly discarded and replaced by separately frozen, runtime-bounded workloads.
- Local validation was strengthened after adversarial review to reject a non-moving king already in check and materially impossible promotion surplus with all pawns still present.
- Move generators were hardened to never emit a move that captures the opposing king even on malformed raw placements.
- The G11 ledger label was changed from an early “pass with artifact gap” working description to the final HOLD verdict, because the roadmap gate requires exact frozen G10 replay rather than merely similar tests.
These are G11 implementation/test-harness corrections. They do not amend G10.RULES.v1.0 and do not alter any earlier frozen chess result.
# 13. Implications for the G9 roadmap
The roadmap’s dependency logic remains correct, but the transition from G11 to the original G12 mission must be gated more explicitly than forecast because the G10 machine payload is not currently retrievable. No downstream dependency is skipped.
| Roadmap item | G11 close implication |
| --- | --- |
| G12 — Full-Rule Small-Arena Certification | Not yet authorised as the first action. G12 must begin with conformance closure: recover/verify G10 bundle, replay exact vectors, and prove canonical byte alignment. Only then continue the original G12 arena mission. |
| G13 — Distributed platform | Architectural design may be discussed later, but no final-model exact computation should be treated as authoritative until G11’s artifact gate closes and G12 establishes full-rule anchors. |
| G14 — Proof store | Must preserve the exact G10 contract/version and canonical raw bytes; the present artifact gap demonstrates why immutable payload retention is load-bearing. |
| G15 — Verifier hardening | The same-session authorship caveat remains useful motivation for later shrinking/independence of the trusted core. |
| G20 — History-dependent scaling | G11 provides working dual transition implementations, but scaling should use the certified G10 identity after byte-profile closure. |
| G35 — Initial-position connection | Reachable fuzz confirms the full-state machinery can be propagated from the initial state; it is not a substitute for G35 reachability proof. |
# 14. Current position at G11 close
The project now has substantially stronger move/state infrastructure than at G10 close: two distinct legal-move implementations, dual history-state transitions, deterministic state validation, full-state local serialization, exact exhaustive conformance slices and adversarial property campaigns. Across every completed accepted G11 test there are zero known A/B mismatches.
However, this is not promoted to final G10 conformance certification. The missing exact G10 payload prevents two load-bearing checks: replaying the frozen vector corpus and proving byte-identical canonical state identity. G11 therefore closes at a genuine artifact/provenance frontier rather than forcing a PASS.
Frozen close position: strong local conformance capability exists; formal G11 roadmap gate remains open. The next programme is G12, but its first mandatory substage is conformance closure, not full-rule W/D/L solving.
# 15. Successor Contract — G12
| Successor item | Frozen instruction |
| --- | --- |
| Programme number | G12. |
| Immediate mission | Close the one remaining G11 provenance/identity seam, then — and only then — execute the original roadmap G12 Full-Rule Small-Arena Certification mission. |
| G12.0 mandatory artifact recovery | Recover `G10_Semantics_Contract_Bundle.zip` and verify SHA-256 a0c5c2df…9342b0793. Recover its frozen vector and rules/serialization components without reconstructing them from prose. |
| G12.1 exact conformance closure | Run both G11 engines against the exact `G10_Conformance_Vectors_v1.json`; compare legal moves, full successor states, claim/terminal behavior and rejection typing. Implement/read the exact G10 canonical byte profile and require byte identity or explain every mismatch. |
| Blocking rule | Any unexplained legality, full-state, castling, EP, history, claim, terminal, rejection or canonical-byte mismatch blocks the original G12 solve. Do not “fix” vectors to suit the engines. |
| If G10 bundle is permanently unrecoverable | Do not pretend reconstructed bytes/vectors are original. Freeze an explicit superseding state-serialization/vector contract with a new version and record that the original G10 artifact chain is broken; rerun the conformance gate under the new version before solving. |
| G12.2 original roadmap mission | After G12.1 PASS, re-solve a compact varied final-rules portfolio that actually exercises repetition, move-count claims, exact dead positions, captures, promotions and special rights. |
| Deadness obligation | Build exact small-arena dead-position truth/reachability-to-mate, not an insufficient-material heuristic. |
| Historical result discipline | Pilot–G8 truths remain historical under their frozen models unless explicitly re-solved under the final G10/G11/G12 semantics. |
| What G12 inherits directly | G9 roadmap; this G11 handoff; G11 conformance bundle and checksums; all G10 semantic statements quoted here. |
| Older/supplementary artifact genuinely required | The exact G10 semantics bundle is required despite the normal two-document successor rule because this handoff records that its payload could not be recovered and its canonical bytes/vectors are themselves the unresolved dependency. |
| No other earlier G handoff required | Do not retrieve G1–G9 technical history merely for completeness. Older restricted artifacts are needed only if a chosen G12 regression arena explicitly references them. |
# 16. Frozen G11 artifact inventory
| Artifact | SHA-256 | Role |
| --- | --- | --- |
| engine_a.py | 13c51f414ec842c4ce3e8ff8a665037875d2a079d4d9c03748c24f6600341368 | Reference A: flat-board/source-centric engine. |
| engine_b.py | 9ff5b42d6b642b499969521785f81d162f4b87e4ce103935fb9eaac4143a45e5 | Independent B: sparse-map/target-centric engine. |
| g11_conformance.py | 608ec9a05d33e1bfc138faa038bf58625610b0d868ba2745cc39c267712342b0 | Differential, exhaustive, perft and fuzz harness. |
| g11_run_phase.py | b7288e5e0fbf8d83d7573366132d8bdbcf6a490b281400b229e779a54ef1db77 | Fresh-process deterministic phase runner. |
| G11_Conformance_Ledger.json | 9662e5c4b3503b7d1cf9062920cf4477118c7831072bc05a8abce6cf4c7970ce | Authoritative quantitative/gate ledger. |
| G11_Freeze_Manifest.json | 7cd15e99f2ae1991ad268440e58f9df1b072bebf1cd8426f85501dcf0459e37f | Machine-readable authority, artifact-gap and hash manifest. |
| G11_Artifact_README.md | f74ee81f85cd6d4ab4fe794058504a974f6767a3353e108ccd45a9d361003d87 | Bundle boundary, reproduction notes and limitations. |
| G11_Conformance_Bundle.zip | 874c69b11d6e2d1aa5d4f5de96c3ef96a8e9307c49cd5f53e7b5c4a3849aab5c | Frozen bundle of source, ledger, manifest and completed phase provenance. |
## 16.1 Integrity and equality rule
The hashes above identify the G11 artifacts. They do not replace semantic equality. In particular, G10’s canonical raw state bytes remain the intended final identity authority once the missing G10 bundle is recovered. The G11 bundle must not be used to silently redefine that authority.
# Appendix A — Frozen curated controls
| Control | Recorded result |
| --- | --- |
| initial | ep_effective=None; in_check=False; moves=20 |
| castle_both_clear | ep_effective=None; in_check=False; moves=26 |
| castle_through_check | ep_effective=None; in_check=False; moves=12 |
| castle_into_check | ep_effective=None; in_check=False; moves=14 |
| ep_legal | ep_effective=d6; in_check=False; moves=5 |
| ep_pinned_canonical_null | ep_effective=None; in_check=False; moves=6 |
| promotion_four | ep_effective=None; in_check=False; moves=7 |
| capture_promotions_eight | ep_effective=None; in_check=False; moves=11 |
| check_evasion | ep_effective=None; in_check=True; moves=4 |
| checkmate | ep_effective=None; in_check=True; moves=0 |
| stalemate | ep_effective=None; in_check=False; moves=0 |
| K_vs_K | dead_hook=DEAD |
| KB_vs_K | dead_hook=DEAD |
| KN_vs_K | dead_hook=DEAD |
| KNN_vs_K_unknown | dead_hook=UNKNOWN |
| rook_move_right_loss | rights=Qkq |
| rook_capture_double_right_loss | rights=Kk |
| claim_controls | fifty_by_move=True; fifty_now=True; threefold_by_move=True; threefold_now=True |
| automatic_draw_controls | fivefold=True; mate_precedence_150=True; seventyfive=True |
| history_barriers | pawn_reset=True; quiet_preserve=True |
| missing_black_king | issues=['castling_inconsistent_k', 'castling_inconsistent_q', 'king_count']; status=MALFORMED |
| adjacent_kings | issues=['adjacent_kings']; status=MALFORMED |
| castling_without_rook | issues=['castling_inconsistent_K']; status=MALFORMED |
| pawn_backrank | issues=['pawn_backrank']; status=MALFORMED |
| ineffective_ep | issues=['ineffective_ep']; status=HISTORY_INCONSISTENT |
| nonmoving_king_in_check | issues=['nonmoving_king_in_check']; status=MALFORMED |
| promotion_material_infeasible | issues=['promotion_material_infeasible']; status=MALFORMED |
# Appendix B — Perft position definitions
| Name | FEN | Frozen depths/counts |
| --- | --- | --- |
| start | rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 | d1 20; d2 400; d3 8,902; d4 197,281 |
| perft_position_3 | 8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1 | d1 14; d2 191; d3 2,812; d4 43,238 |
| perft_position_5 | rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8 | d1 44; d2 1,486; d3 62,379 |
# Appendix C — Reproduction protocol
Preferred resource-bounded replay is one fresh process per phase:
python g11_run_phase.py curated --out phase_curated.json
python g11_run_phase.py perft --out phase_perft.json
python g11_run_phase.py exhaustive_kings --out phase_kings.json
python g11_run_phase.py exhaustive_three_piece_slices --out phase_slices.json
python g11_run_phase.py attack_map_fuzz --out phase_attack.json
python g11_run_phase.py mixed_board_fuzz --out phase_mixed.json
python g11_run_phase.py ep_adversarial_fuzz --out phase_ep.json
python g11_run_phase.py reachable_fuzz --out phase_reachable.json
python g11_run_phase.py mutation_fuzz --out phase_mutation.json
A replay is evidentially successful only if it preserves the declared domain definitions and returns zero unexplained A/B mismatch. Timing is not part of the theorem. The two `HOLD_NO_RESULT` stress runs remain excluded unless rerun to completion under their original wider scopes.
# Appendix D — Evidence taxonomy at freeze
| Category | G11 examples | Promotion rule |
| --- | --- | --- |
| Exact finite computation | Exhaustive declared small-domain A/B move-set agreement. | May be stated exactly only over the declared finite domain. |
| Duplicated computation vs fixed anchor | Perft depth counts reproduced by both engines. | Strong regression evidence; does not cover full G10 metadata semantics. |
| Deterministic empirical/property evidence | Attack, mixed-board, EP, reachable and malformed fuzz. | Supports correctness but is not an exhaustive chess theorem. |
| Sound partial theorem/hook | K v K, K+B v K, K+N v K are returned DEAD. | Unknown cases remain UNKNOWN; no completion by heuristic analogy. |
| Blocked certification | Frozen G10 vector and canonical byte replay. | No promotion until exact payload is recovered and replayed. |
| Negative/hold | Over-wide stress runs that timed out. | No partial results count; preserve as holds. |
END OF FROZEN G11 TECHNICAL HANDOFF
