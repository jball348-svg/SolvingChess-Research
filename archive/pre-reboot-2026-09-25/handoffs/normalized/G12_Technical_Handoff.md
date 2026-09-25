<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G12_Technical_Handoff.docx
original_sha256: 958367f224467efc439217ac7a546249915e7a596717e8ad0c2131349e50eff3
derivative_filename: G12_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

# G12 Full-Rule Small-Arena Certification
Technical Handoff — Frozen Closeout
12 August 2026 | G12.R1
| FROZEN VERDICT — PASS UNDER THE AUTHORISED SUPERSEDING-ARTIFACT BRANCH<br>G12 closes the G11 provenance/identity seam without pretending the missing G10 machine payload was recovered. G10.RULES.v1.0 remains the semantic rules authority. A new versioned canonical artifact profile, G12.STATE.SERIAL.v2, is frozen for forward work; a new conformance corpus passes; compact final-rule reference arenas are solved and independently replayed; exact history-sensitive controls and a nontrivial exact DEAD family are certified. Historical G11 remains HOLD against the unavailable original G10 payload. |
| --- |
# 0. Executive freeze
| Gate / object | Frozen result | Claim class |
| --- | --- | --- |
| Programme number | G12 | Sequential programme identity |
| Original G10 bundle recovery | FAILED: exact payload not retrievable | Historical provenance failure; preserved |
| Authorised fallback | G12.STATE.SERIAL.v2 + G12.CONFORMANCE.v2 | New forward artifact contract; G10 rules unchanged |
| New conformance gate | PASS; zero accepted A/B mismatches | Deterministic conformance under v2 |
| KQK clean roots | 368,452 = 345,404 W + 23,048 D; max rank 20 | Exact finite-arena truth |
| KRK clean roots | 399,112 = 376,868 W + 22,244 D; max rank 32 | Exact finite-arena truth |
| a-file KPK clean roots | 41,619 = 27,430 W + 14,189 D; max rank 36 | Exact finite-arena truth |
| Same-colour K+2B vs K | 5,938,848 admissible states; 0 checkmates | Exact DEAD theorem in declared arena |
| Standalone replay | 809,183 table states; 0 Bellman/rank mismatches | Independent target-centric verifier |
| Fresh rerun | 7/7 principal outputs byte-identical | Deterministic reproduction |
# 1. Authority, programme numbering and source precedence
The immediately preceding completed programme is G11, so the sequential programme is G12. The permanent roadmap assigns G12 the mission “Full-Rule Small-Arena Certification”: re-solve a compact but varied portfolio under the complete final state semantics and freeze truth hashes, independent move-generation agreement and certificate replay. G11 amended the order of work by making conformance/provenance closure the first mandatory G12 substage.
| Priority | Artifact | Use in G12 |
| --- | --- | --- |
| 1 | G9_G10_Onwards_Long_Range_Plan.docx | Permanent dependency map and G12/G13 mission authority. |
| 2 | G11_Technical_Handoff.docx | Immediate frozen technical state and binding G12 Successor Contract. |
| 3 | G10 semantic statements quoted/frozen in G11 | Chess-rule/state semantics; not a substitute for missing original machine bytes. |
| 4 | G7_4_Interim_Evidence_Freeze_B.md / ledger | Retrieved only because G12 deliberately chose KPK as a historical regression anchor. |
No Pilot–G6 or G8 handoff was retrieved for historical completeness. The older G7 artifact was recovered only after the KPK regression arena was selected, because it contains the exact continuation-aware 41,619-state KPK checksum used for an independent historical cross-check.
# 2. Inherited frozen state from G11
G11 had already established a strong local legality/state implementation result but stopped correctly at a formal provenance gate. Its accepted evidence included two structurally distinct move/state implementations, 27 curated controls with zero mismatch, 11 fixed perft anchors, exhaustive differential testing over 98,623 states and 889,808 legal edges, 256,000 attack queries, 5,000 mixed states, 2,000 en-passant cases, 5,000 malformed mutations and 1,536 reachable full-state transitions, all with zero known A/B mismatch. G11 did not promote this to the original G10 conformance certificate because the exact G10 vector corpus and canonical raw-byte payload were unavailable.
## 2.1 Semantic state inherited unchanged
| Field / rule | Frozen meaning retained in G12 |
| --- | --- |
| Board + turn | 64-square placement plus side to move. |
| Castling | Four monotone KQkq historical rights; home king/rook occupancy required; false rights never restore. |
| En passant | Only effective EP is stored: a target exists only when at least one EP capture is legally available including own-king safety. |
| Halfmove clock | Exact count since pawn move or capture; 50-move claims from 100; automatic 75-move draw at 150 subject to mate precedence. |
| Repetition | Occurrence-count map inside the current exact barrier epoch; REP identity is board + turn + castling + effective EP. |
| Barriers | Pawn move, capture or permanent castling-right reduction clears the prior repetition epoch. |
| Claims | Valid threefold and 50-move claims are explicit actions, including intended-move claims. |
| Terminal order | CHECKMATE, STALEMATE, DEAD, FIVEFOLD, 75-MOVE, then ACTIVE. |
| DEAD | No finite legal continuation can reach checkmate by either player; insufficient-material shorthand is not the definition. |
| Reachability typing | ARENA_ADMISSIBLE is distinct from START_REACHABLE. |
## 2.2 Frozen negative constraints
- Do not identify a state by board placement plus side to move alone.
- Do not store only the current repetition count or an unbounded full move-history tape.
- Do not retain a nominal but legally unusable en-passant target.
- Do not replace exact DEAD by an “insufficient material” helper.
- Do not label locally legal endgame states START_REACHABLE without a reachability certificate.
- Do not absorb clocks, resignation, agreement or arbiter administration into the abstract legal-play graph.
# 3. G12.0 — mandatory G10 artifact recovery and provenance decision
G11 required G12 to attempt exact recovery before any final-rule solve. G12 searched the File Library by the exact bundle name, exact vector/component names and recorded hashes. The searches returned the G10/G11 handoffs and checksum references, but not the standalone byte payloads. The session filesystem likewise contained no recoverable original G10 payload.
| Missing artifact | Recorded original SHA-256 | G12 result |
| --- | --- | --- |
| G10_Semantics_Contract_Bundle.zip | a0c5c2df8f8f61d8f6365ae8750491e3d64df821d060f9d24edb6ad9342b0793 | NOT RECOVERED |
| G10_Conformance_Vectors_v1.json | 317a192513f99b467b2afb888a74e9607950aa2c50b90848a98c1feb2aedbb4d | NOT RECOVERED |
| G10_Rules_Contract_v1.json | c0e2430e6dabf029193897e6c621e614914963290f07ecb8946049543a13edca | NOT RECOVERED |
| PROVENANCE RULING<br>The original G10 artifact chain is frozen as broken/unrecoverable in this programme. No G12 artifact is called the original G10 vector set or original G10 canonical bytes. No G11 HOLD is retroactively converted into an original-G10 PASS. This is an artifact-lineage failure, not evidence of a chess-rule mismatch. |
| --- |
# 4. G12.1 — authorised superseding serialization/vector contract
The G11 Successor Contract explicitly authorised a failure branch if the G10 payload proved permanently unrecoverable: freeze a new versioned serialization/vector contract, record the broken original chain, rerun conformance under the new version, and only then solve. G12 follows that branch literally.
| Frozen object | Meaning | SHA-256 |
| --- | --- | --- |
| G12.STATE.SERIAL.v2 | Forward canonical full-state/repetition byte profile. Semantic rules remain G10.RULES.v1.0. | 73ef6660d98c1aa072feb8a04764b26cf4c69b9d545abdb2f4d8f105965d06a8 |
| G12.CONFORMANCE.v2 | New vector corpus. Explicitly NOT a reconstruction of G10 vectors. | ed972a06e6d855ec47077a90dc81e8c49db6ba1a21562f44cd684a600b6534d8 |
| Pre-outcome freeze ledger | Hashes both new contract/vector files before accepted G12 arena outcomes. | 10f69cd3d7e97c2154e545253059cb687f33a61f491cc81e0154977907a2a42c |
## 4.1 Canonical identity profile
G12.STATE.SERIAL.v2 preserves G10 state semantics but supplies a new raw-byte identity profile. Repetition keys use magic G12R2 followed by length-delimited board64, turn, sorted castling rights and effective EP. Full-state bytes use magic G12S2 followed by those fields, canonical decimal halfmove clock, then a lexicographically sorted repetition map with raw repetition-key bytes and bounded counts. Canonical payload bytes, not their hashes, define equality; hashes are transport/integrity addresses.
## 4.2 New conformance gate
The new corpus was declared from inherited G10/G11 obligations before accepting any G12 tablebase truth. It exercises the initial position, both castlings, castling through/into check, legal and pinned en passant, four-way and capture promotion, check evasion, mate, stalemate, rights loss by rook move/capture, claim/history controls and mate-over-75 precedence. Two separately implemented serializers emit byte-identical canonical v2 payloads on the frozen controls.
| Representative control | Accepted result |
| --- | --- |
| Initial | 20 legal moves; A/B exact set equality. |
| Clear castling | Both e1-g1 and e1-c1 legal. |
| Through/into check | Kingside castle rejected when f1/g1 respectively is attacked. |
| Legal EP | e5xd6 generated; effective EP remains d6. |
| Pinned EP | e5xd6 rejected; nominal d6 canonicalizes to null. |
| Promotions | Four a7-a8 choices; capture-promotion control has eight a7 promotion moves. |
| Mate / stalemate | Both zero-move cases distinguished by check status. |
| Rook rights | h1-h2 -> Qkq; a1xa8 -> Kk. |
| Canonical state | Independent serializers equal on accepted controls. |
| Gate ledger | FAIL=0. |
Important boundary: the G12 producer/verifier sources are new artifacts written in G12. The original G11 source bundle was not byte-recovered in this session, so G12 does not claim source identity with G11. It relies on G11’s frozen broad zero-mismatch evidence as inherited evidence and creates a new self-contained forward artifact chain.
# 5. G12.2 — final-rule reference portfolio design
After the v2 gate passed, G12 selected a deliberately small but semantically varied portfolio. The point was not to inflate piece count; it was to create independently replayable anchors that exercise final-state semantics and prove where restricted board-only truth does and does not survive history decoration.
| Arena / control | Role | Declared metadata / boundary |
| --- | --- | --- |
| KQK | Fast mating reference; captures, check/mate/stalemate; history-safety by bounded rank. | No castling/EP; halfmove=0; current rep count=1. |
| KRK | Second slider reference with different geometry and capture/stalemate structure. | Same clean metadata. |
| a-file KPK | Pawn move, double push, capture, four promotions into exact Q/R children; B/N promotion dead exits. | Same clean metadata; promotion continues semantically. |
| K+2 same-colour bishops vs K | Nontrivial exact DEAD classification via no-mate reachability, not material helper. | Both turns; unordered same-colour bishop pair. |
| History-decorated KQK controls | Show repetition/50/75 metadata can change W/D truth for the identical board. | ARENA_ADMISSIBLE history examples; not claimed START_REACHABLE. |
| Special-right corpus | Castling, effective EP, rights loss and promotion transition checks. | Conformance/certificate controls rather than full W/D tables. |
# 6. Exact solver, certificate and verifier architecture
## 6.1 Producer
The accepted producer builds each finite graph once, then computes the White-win attractor with priority-ordered retrograde propagation. Black checkmate states are rank 0. A White-to-move state is winning when at least one successor is winning; its rank is one plus the minimum winning child rank. A Black-to-move state is winning for White only when every legal successor is winning for White; its rank is one plus the maximum child rank. Captures into certified dead lower material remain drawing exits and therefore correctly block an all-successor White-win classification.
## 6.2 Frozen certificates
Each table emits a compact raw-index certificate: 8-byte magic, array length, then valid flag, White-win flag and exact rank for every encoding. This is intentionally simple so later proof-store and raw-truth stages can ingest it without reverse engineering a producer-specific object model.
## 6.3 Standalone target-centric replay
A separate C++20 verifier loads the three certificates, regenerates legal moves with the target-centric Engine-B path, and checks every Bellman equation and every winning rank. It also independently repeats the same-colour-bishop mate scan. The verifier contains no producer Engine-A source-centric attack/move implementation. Both programs were authored in the same research programme, so this is structural software independence, not organizational independence; G15 still owns trusted-core hardening.
# 7. Exact quantitative results
| Arena | Valid | White win | Draw | Max rank | Legal edges | Verifier mismatches |
| --- | --- | --- | --- | --- | --- | --- |
| KQK | 368,452 | 345,404 | 23,048 | 20 | 4,891,672 | 0 |
| KRK | 399,112 | 376,868 | 22,244 | 32 | 4,469,208 | 0 |
| a-file KPK | 41,619 | 27,430 | 14,189 | 36 | 285,758 | 0 |
The independent verifier replayed 809,183 table states with zero Bellman/rank mismatch. Its independently generated edge counts and FNV graph checksums exactly match the producer for all three tables. A fresh-directory rerun reproduced seven principal output artifacts byte-for-byte.
| Arena | Truth FNV64 | Edge FNV64 A/B |
| --- | --- | --- |
| KQK | d0b275b8cb22e29d | 52d331cd50ac23e9 |
| KRK | 2b2148e736f682c1 | 0b1b0d9d0d047838 |
| KPK | 5096d7ac7945bdc8 | 0d85f51438a4ddd7 |
# 8. Why the clean-root tables are final-rule truths, not merely old-style board tables
| G12.CLEAN-RANK-SAFETY<br>For a clean root with halfmove_clock=0 and current repetition count 1, if the certified White-winning strategy strictly decreases an exact attractor rank and the maximum winning rank is below 100 plies, then neither threefold repetition nor the 50/75-move rules can preempt the certified mate. Strict rank decrease forbids a repeated full repetition key; the path is too short to reach a 50-move claim threshold. This is a reusable sufficient condition, not a claim about arbitrary history-decorated copies of the same board. |
| --- |
All three accepted clean-root arenas satisfy this condition: maximum ranks are 20, 32 and 36 plies respectively. On White winning states, White chooses a lower-rank child; on Black turns every legal child is winning and has rank at most the parent rank minus one. Therefore rank decreases on every ply against every Black reply. KPK pawn moves only reset the halfmove clock further. Promotions continue into the exact Q/R tables; bishop/knight promotion exits are exact dead draws, not automatic wins.
# 9. Historical KPK regression without rewriting history
The a-file KPK table was chosen in part because an older exact G7 dependency provides a meaningful checksum. After file reflection, G12 reproduces the continuation-aware G7 result exactly: 41,619 states = 27,430 White wins + 14,189 draws. G7 also recorded 29,520 / 12,099 when promotion alone was treated as an immediate White-winning terminal. G12 does not call that historical number erroneous; it remains exact under its declared promotion-terminal diagnostic model. The G12 final-rule anchor uses semantic continuation through promoted material and therefore matches the continuation-aware split.
# 10. History-sensitive exact controls: identical board, different truth
G12 deliberately constructs history-decorated controls to falsify any temptation to reuse board-only truth as full-state truth. These are arena-admissible state tests; no claim is made that every seeded repetition map is reachable from the standard initial position.
| Control | Clean board truth | History decoration | Exact full-rule consequence |
| --- | --- | --- | --- |
| Threefold now | 8/8/8/8/8/8/8/QK1k4 b - - 0 1 | Black to move; current REP count = 3 | Black has CLAIM_3_NOW; DRAW instead of forced White win. |
| 50-move now | 8/8/8/8/8/8/8/QK1k4 b - - 0 1 | Black to move; halfmove=100 | Black has CLAIM_50_NOW; DRAW. |
| 75-move boundary | 8/8/8/8/8/8/8/QK1k4 w - - 0 1 | White to move; halfmove=149; 16 legal moves; clean rank 9 | No mate in one; every move is a draw by higher terminal or automatic 75-move rule; root DRAW. |
| Intended claims | same KQK control | a1a2 with target count 2 / halfmove 99 | Threefold-by-move and 50-by-move claims both available. |
| Fivefold | same KQK control | a1a2 with target prior count 4 | Successor count 5; automatic DRAW_FIVEFOLD. |
| Mate at 150 | 7k/5Q2/7K/8/8/8/8/8 w - - 149 1 | f7g7 | Successor halfmove=150 but move is checkmate; CHECKMATE wins by precedence. |
| KEY NEGATIVE RESULT<br>Board-only W/D identity is definitively unsafe under the final rules. G12 contains explicit states whose board placement is a certified clean KQK White win but whose legal history metadata gives Black an immediate draw claim or forces an automatic draw. This supports, rather than weakens, the G10 state model. |
| --- |
# 11. Exact DEAD certification: same-colour K+2B vs K
G12’s dead-position obligation is met with a family that cannot be discharged merely by calling a library “insufficient material” helper. The arena contains White king, Black king and two indistinguishable White bishops constrained to the same colour complex. Both turns are represented.
| Quantity | Producer | Independent verifier |
| --- | --- | --- |
| Arena-admissible states | 5,938,848 | 5,938,848 |
| Black-to-move checked states | 783,048 | 783,048 |
| Checked-state evasion edges | 3,715,916 | 3,715,916 |
| Bishop-capture evasion edges | 217,432 | 217,432 |
| Checkmates | 0 | 0 |
| Audit FNV64 | 632a491855434b4b | 632a491855434b4b |
## 11.1 Deadness proof object
1. Exhaustively enumerate every locally legal same-colour K+2B vs K placement with Black to move that is in check. Both independent attack/move paths find zero checkmate positions.
1. White bishops can never change colour complex under a legal bishop move. Therefore every non-capture continuation with two bishops remains inside the enumerated no-mate family.
1. If Black captures a bishop, material reduces to K+B vs K; if both bishops eventually disappear, it reduces to K vs K. Those are exact dead dependencies.
1. Black has only a king. Legal king separation means Black cannot checkmate White in this material family.
1. Thus no legal continuation from any state in the declared family can reach checkmate by either player. Every state is DEAD by the extensional G10 definition.
| G12.DEAD-CLOSURE<br>Reusable pattern: prove a material/topology family is closed except for exits into already-certified DEAD dependencies; exhaustively prove the closed family contains no checkmate terminal; conclude every state in the family is DEAD. This is exact reachability-to-mate reasoning, not a material heuristic. |
| --- |
# 12. Proof and verification status
| Claim | Status | Boundary |
| --- | --- | --- |
| G10 semantic rules used by G12 | Inherited frozen contract | Not re-derived; unchanged from G10/G11. |
| Original G10 byte/vector replay | FAILED / historically unresolved | Payload absent; no reconstruction claim. |
| G12 v2 canonical profile | Frozen deterministic artifact | New forward identity profile. |
| Special-move/state conformance | Deterministic A/B conformance PASS | New v2 corpus plus inherited G11 broad evidence. |
| KQK/KRK/KPK W/D | Computer-assisted exact finite-arena theorem | Clean-metadata roots; not arbitrary histories. |
| Certificate replay | Independent structural verifier PASS | Same-session authorship; formal TCB hardening deferred G15. |
| Same-colour KBB DEAD | Exact finite theorem: exhaustive zero-mate + invariant closure | Declared arena only. |
| History decorated examples | Exact local full-rule outcomes/actions | ARENA_ADMISSIBLE; not START_REACHABLE. |
| Initial-position theorem | NOT ESTABLISHED | No G12 result connects these arenas to the standard initial state. |
# 13. Corrections, supersessions, negative results and discarded provisional outputs
- Original G10 machine artifacts: unrecoverable. This is preserved as a historical provenance exception; G12 does not fabricate a cryptographic chain.
- G11 historical verdict: remains HOLD against the original G10 replay gate. The new G12 forward contract supersedes the missing artifact profile only; it does not rewrite G11 history.
- Early provisional rank computation: an initial in-place relaxation pass reached the same W/D sets but emitted inflated order-dependent rank maxima (KQK 44, KRK 50, KPK 50). Those rank figures were discarded before freeze. Priority-ordered retrograde produced 20/32/36 and the independent verifier checks every rank equation with zero mismatch.
- A pre-acceptance conformance assertion encoded the Qkq castling-right bit mask as decimal 10 instead of the correct 14. The conformance run caught the assertion failure; the harness was corrected before any accepted ledger or certificate was frozen.
- The KBB audit initially used an ambiguous “legal_edges” label for checked-state evasions. It was renamed to “checked_state_evasion_edges” before freeze; no chess result changed.
- Historical promotion-terminal KPK 29,520/12,099 is not superseded as a historical restricted-model result. G12’s continuation-aware 27,430/14,189 is the final-rule clean-root anchor.
# 14. New reusable capabilities and proof operations created by G12
| Object / capability | What is new | Likely downstream use |
| --- | --- | --- |
| G12.STATE.SERIAL.v2 | Self-contained forward canonical raw-byte profile after the G10 artifact-chain break. | G13 manifests/checkpoints; G14 proof-store identities; G20 history scaling. |
| G12.CLEAN-RANK-SAFETY | Bounded strictly decreasing exact rank proves clean-root wins cannot be preempted by repetition or move-count draws. | Certifying board-table anchors under final rules without exploding history state where the sufficient condition applies. |
| G12.DEAD-CLOSURE | Zero-mate exhaustive scan + closure into dead dependencies yields exact DEAD families. | General small/material deadness certification and later raw-truth dependencies. |
| Raw valid/win/rank certificate v2 | Simple content-addressable table certificate with standalone Bellman replay. | G14 store schema and G18 raw exact-truth carrier. |
| History truth-flip controls | Concrete exact examples where identical boards differ by repetition/halfmove metadata. | G20 regression anchors and verifier anti-shortcut tests. |
| Fresh-process deterministic suite | Producer + verifier + checksum manifest + byte-identical rerun. | G13 distributed/checkpoint acceptance baseline. |
# 15. Implications for the G9 roadmap
G12 meets its natural advance criterion under the exact failure branch authorized by G11. The original G10 artifact chain is not repaired; instead, the project now has a new explicit forward canonical profile plus independently replayed final-rule anchors. This is sufficient to move forward without silently skipping the provenance failure.
| Roadmap stage | G12 close implication |
| --- | --- |
| G13 distributed/checkpointed compute | Sequential next programme. It can now use the G12 frozen suite as its deterministic kill/restart regression baseline. |
| G14 proof store | Must preserve both the historical broken G10 identity references and the new G12 forward profile; never alias them as the same byte contract. |
| G15 verifier hardening | Still required. G12 verifier is structurally distinct but same-session authored. |
| G16-G22 scale/breadth | Now have final-rule small anchors and a reusable raw certificate format; scaling must retain v2 identity and full-rule boundaries. |
| G20 history scaling | G12 gives exact truth-flip and intended-claim controls; large history-state economics remain open. |
| G35 initial-position connection | Still untouched. ARENA_ADMISSIBLE anchors do not constitute reachability from the initial position. |
# 16. Current position at G12 close
| FROZEN CLOSE POSITION<br>The foundation now contains: frozen final chess semantics; strong independent move/state conformance evidence; an explicit new canonical artifact chain after the old byte payload became unrecoverable; exact final-rule clean-root KQK/KRK/KPK anchors; history-state counterexamples that enforce full identity; a nontrivial exact dead-position theorem; standalone certificate replay; and deterministic reproduction. It still does not contain distributed exact computation, durable proof storage, a formally minimized trusted verifier core, large history-aware arenas, or any certified connection from the standard initial position. |
| --- |
No new “road to 100%” percentage is frozen in G12. Increasing a handful of exact small arenas is a foundation-quality improvement, not a meaningful solved-state fraction of chess.
# 17. Successor Contract — G13
| Successor item | Frozen instruction |
| --- | --- |
| Programme number | G13 — Distributed and Checkpointed Exact-Compute Platform. |
| Immediate mission | Make exact solving resumable, deterministic and multi-machine before larger state growth makes one-session runs fragile. |
| Roadmap questions | Partition material/signature jobs without semantic drift; define checkpoints, retries, work ownership and deterministic merge; reproduce complete runs from immutable manifests. |
| Required inherited semantics | G10.RULES.v1.0 remains chess-rule authority. G12.STATE.SERIAL.v2 is the forward canonical artifact profile unless a later explicitly versioned contract supersedes it. |
| Required machine dependency | G12_Final_Rules_Reference_Bundle.zip — SHA-256 7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c. |
| Mandatory acceptance baseline | Run the G12 reference suite through the checkpoint/distributed machinery. Worker kill/restart, repartitioning and retry must reproduce identical truth/certificate hashes and canonical artifacts. |
| Blocking rule | Stop on nondeterministic merge, hidden global state, non-content-addressed dependency identity, or checkpoint resume that changes any accepted result. |
| Provenance rule | Do not try to “heal” the missing G10 payload by calling G12 v2 the original G10 bytes. Preserve the break as explicit history. |
| G14 coordination | Design G13 manifests/checkpoints so G14 can store immutable semantic version, source hash, truth hash, certificate hash and dependency identity without lossy translation. |
| Older artifacts genuinely needed | None by default. Read the G9 roadmap + this handoff + the G12 machine bundle. Retrieve G7 only if a deliberately chosen G13 scale benchmark requires its exact old payload. |
| Advance condition | Content-addressed manifests, checkpoint format, deterministic scheduler and retry/recovery protocol exist; a reference distributed run survives worker kill/restart with identical truth/certificate hashes. |
| What G13 unlocks | G17 onward directly; in the dependency spine it supports durable compute/proof-store closure before G15 and scale/breadth. |
# 18. Frozen G12 artifact inventory
| Artifact | SHA-256 | Role |
| --- | --- | --- |
| G12_Superseding_State_Contract_v2.json | 73ef6660d98c1aa072feb8a04764b26cf4c69b9d545abdb2f4d8f105965d06a8 | Superseding v2 canonical serialization/state artifact profile. |
| G12_Conformance_Vectors_v2.json | ed972a06e6d855ec47077a90dc81e8c49db6ba1a21562f44cd684a600b6534d8 | New frozen semantic/conformance corpus; not G10 reconstruction. |
| g12_suite.cpp | d759ccf161637a4b612a48f04f7ecab26b1fcab4204711030fe1c304ac40dfec | Producer + source-centric reference implementation and v2 controls. |
| g12_verifier.cpp | 99cd9a3466169d558128df49a31416c54e380d10133740cb9c8f44fa00ed34ef | Standalone target-centric Bellman/deadness verifier. |
| G12_Arena_Ledger.json | 6cd144db4dd8e5416f7dc41e2b29ddc5be76d15aa0350db10b70adf16cc7689d | Authoritative exact arena counts and producer checksums. |
| G12_Verification_Ledger.json | 792ea0b9a427f9d77a97b50888f8eb7b6c47c9df0fc65b89945b72e5c83b78d4 | Independent replay counts, edge hashes and zero mismatch ledger. |
| G12_History_Rules_Ledger.json | c8a374bd5237cab0372bd9ad0ddff0a166cebe6c23f82c14a452687f6b7432eb | History-sensitive claim/automatic-draw and mate-precedence controls. |
| G12_KQK_Certificate_v2.bin | e01dd995e050542e63d2f7c3f6fe1a9ef05a1ce065d64704e743907f8a0c9127 | KQK valid/win/rank certificate. |
| G12_KRK_Certificate_v2.bin | badc392dbdd13b96862c4e5859cf50468f65cd65a72f40747d9300ebcc110793 | KRK valid/win/rank certificate. |
| G12_KPK_Certificate_v2.bin | b515ae01fa2c23669b00d967d9a86d921534874f90d3d53e8bef1f1155359eba | KPK valid/win/rank certificate. |
| G12_Freeze_Manifest.json | 9252e1d3c2fb1af2a7cf2597e48f820aec2d5204b1cbf030ab894cca8bd7e1d6 | Machine-readable closeout authority/provenance/results manifest. |
| G12_SHA256SUMS.txt | 0ea65a5cea38867670f06a265afe016a30fb4e06952c1accba14258783226da3 | Checksum ledger for machine artifacts. |
| G12_Final_Rules_Reference_Bundle.zip | 7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c | Portable frozen machine reference bundle. |
# 19. Final frozen conclusion
G12 PASSES. The pass is deliberately qualified by provenance rather than hidden by it: the original G10 byte/vector payload was not recovered, so its chain remains broken and G11 remains historically HOLD against that exact replay. The explicit G11 fallback branch was exercised instead. G12 freezes a new forward canonical artifact profile, passes the new conformance gate, produces independently replayed final-rule small-arena anchors, proves a nontrivial exact DEAD family, and demonstrates with exact counterexamples why history metadata must remain part of state identity. The sequential programme may proceed to G13.
