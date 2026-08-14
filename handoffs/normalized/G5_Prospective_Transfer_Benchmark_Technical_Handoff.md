<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G5_Prospective_Transfer_Benchmark_Technical_Handoff.docx
original_sha256: 4cc3ffaf7b13400c28d5ea0f636fd5b3a8944bdb53fff283e8bc0bd5a977b2bd
derivative_filename: G5_Prospective_Transfer_Benchmark_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

# G5: Prospective Transfer Benchmark
Frozen proof-language transfer across K+N+d-pawn vs K and K+B+d-pawn vs K
STATUS: G5 FROZEN — MIXED / SCIENTIFIC PASS. PROSPECTIVE TARGET + CRITICAL-MANIFOLD TRANSFER SUCCEEDS; INHERITANCE AND PURE UNION-BRIDGE TRANSFER FAIL.
Frozen research handoff generated from the G5 prospective-transfer benchmark session.
11 August 2026
# Executive summary
G5 changed the methodology from retrospective compression to prospective transfer. Before inspecting new outcome truth, the operation library and semantic vocabulary were frozen. Two new arenas were then solved under the same declared frame: White king + knight + d-pawn versus Black king (Arena N), and White king + bishop + d-pawn versus Black king (Arena B), with the pawn restricted to d5–d7, unrestricted king/minor squares, both sides to move, promotion as a White win, ordinary mate/stalemate, and exact KPK classification after capture of the minor.
The result is deliberately mixed. The strongest positive transfer is TARGET → strict ATTRACTOR plus critical-manifold localization. The same semantic target formula works in both unseen movement topologies, attracting 366,763 knight wins and 373,545 bishop wins with zero draw false positives. The same frozen one-move promotion/interception slab contains 99.03% of knight and 96.06% of corrected bishop WK-sensitive mixed geometries. The strongest negative transfer is equally clear: projected KPK wins are not restored monotonically after adding the minor, and the failures are not reducible to a tiny stalemate family. Predicate-union BRIDGE also produces zero pure bridge states in either arena. Finally, the off-surface tails are semantically separable but cross the predeclared description-cost stopping threshold: 15 leaves / 25 knight geometries and 46 / 87 bishop geometries.
G5 therefore passes as a prospective scientific benchmark but does not pass the stronger hypothesis that every previously successful proof operation transfers. The fixed language predicts robust interior and where exact complexity concentrates, while simultaneously predicting its own limits badly enough to falsify universal inheritance/bridge reuse. Those failures are frozen rather than retuned away.
| Quantity | Arena N: K+N+P vs K | Arena B: K+B+P vs K |
| --- | --- | --- |
| Static-valid states | 1,211,042 | 1,180,148 |
| White wins | 1,106,864 | 1,094,908 |
| Draws | 104,178 | 85,240 |
| Max win rank | 24 | 21 |
| WK-sensitive mixed geometries | 2,572 | 2,207 |
| Direct common target | 214,344 wins | 208,717 wins |
| Strict common-target attractor | 366,763 wins | 373,545 wins |
| Two-target union attractor | 368,023 wins | 374,097 wins |
| Pure union-bridge increment | 0 | 0 |
| One-move critical slab | 2,547/2,572 = 99.03% | 2,120/2,207 = 96.06% |
| Off-surface tail | 25 geometries | 87 geometries |
| Tail WK placements | 1,450 = 1,400 W + 50 D | 5,036 = 4,882 W + 154 D |
| Exact local grammar | 15 leaves / 25 geoms | 46 leaves / 87 geoms |
# 1. Research question and prospective discipline
The G5 north-star question was whether a proof language frozen before seeing a new arena’s outcome table can discover exact certified regions whose coverage grows materially faster than description cost, while also predicting where compression fails. The methodological burden was stronger than G4: arena restrictions, operations, feature atoms, strict reachability semantics, critical-slab width, and the lookup-scale stopping convention were fixed prospectively.
- Operations frozen: PROJECT, INHERITS, TARGET, ATTRACTOR, BRIDGE, RESIDUAL, GROUP_OUT, LOCALIZE, STOP, CERTIFY.
- Vocabulary frozen: tempo-adjusted promotion clocks; king interception to current fronts and moving paths; support/contact; relative file/rank orientation; lower-material truth; piece mobility/access distance; symmetry-relative coordinates; one-move equality slabs; blockade-conversion template.
- No arena-specific absolute-square patches were admitted during the final local audit.
# 2. Frozen arenas and terminal semantics
Arena N contains WK, WN and a White d-pawn against BK. Arena B replaces WN with a light- or dark-square bishop as permitted by the unrestricted minor-square encoding. In both arenas the pawn occupies d5, d6 or d7; kings and minor range over legal board squares; both sides to move are represented. Promotion is a White-winning terminal. If BK captures the minor, the resulting KPK state is classified by the exact lower-material solver. Ordinary checkmate and stalemate are represented. Static validity, rather than proof of historical reachability, defines the finite universe. Repetition, en passant, and move-count claim state are outside this benchmark.
# 3. Harness certification and correction ledger
The local-tail continuation independently reconstructed the declared static-valid universes exactly: 1,211,042 states for N and 1,180,148 for B. Arena N also reproduced the provisional solve exactly at 1,106,864 wins / 104,178 draws, maximum rank 24. The common KPK regression reproduced the Pilot-2 central-file checksum 28,853 wins / 12,505 draws in the corresponding full-rank KPK model.
The bishop baseline did not reproduce the provisional session count. The audited solve is 1,094,908 wins / 85,240 draws, maximum rank 21, superseding the earlier provisional 1,093,936 / 86,212. This changes the bishop WK-sensitive mixed count from 2,223 to 2,207 and the off-surface tail from 90 to 87. The semantic target/attractor counts reproduce unchanged. All provisional bishop baseline, 2,223-mixed, 95.95%-slab, and 90-tail figures are therefore superseded and must not be reused.
# 4. PROJECT / INHERITS: transfer failure
Deleting the minor projects each full state to exact KPK truth. The natural restoration hypothesis—if the projected KPK position is White-winning, restoring a friendly minor preserves the win—fails in both topologies. The provisional exhaustive scan found 1,086 knight restoration failures and 1,557 bishop restoration failures. Only 131 knight and 395 bishop failures are immediate stalemates. The remaining failures are genuine interference/tactical effects rather than one compact terminal exception family.
Frozen conclusion: no restoration theorem is promoted. Enumerating the residual failures as square catalogues would violate the prospective description-cost discipline. This is a clean negative transfer relative to Pilot 2 and G4.
# 5. TARGET / ATTRACTOR: common exact transfer
The first frozen support/contact candidate was falsified because it admitted draws. The prospective template sweep then found the same largest zero-counterexample target in both arenas using only the frozen vocabulary: pawn on d6 or d7; WK within four king-steps of d8; BK at least five king-steps from d8.
| Result | Knight | Bishop |
| --- | --- | --- |
| Direct target | 214,344 / 214,344 wins | 208,717 / 208,717 wins |
| Strict attractor | 366,763 wins | 373,545 wins |
| Draw false positives | 0 | 0 |
| Share of complete win basin | 33.14% | 34.12% |
Strict means actual entry into the semantic target is required: promotion and material-reduction exits are failures for this objective. Thus the large increments beyond direct membership are genuine adversarial stepping-stone values, not terminal shortcuts.
# 6. BRIDGE: exact but non-compositional
A second independently exact target from the same frozen family was combined with the primary target. The union attractor contains 368,023 knight wins and 374,097 bishop wins with zero draws. However, the number of pure bridge states—states that can force the union but cannot force either constituent target individually—is exactly zero in both arenas. G3 and G4’s distinctive predicate-union return bridge therefore does not prospectively transfer here.
# 7. Critical-manifold audit
After subtracting the strict target-union basin, the frozen clock vocabulary was applied without alteration. The one-move slab is the union of the predeclared promotion-race, direct-front interception, and moving-path interception near-equality surfaces. Arena N reproduces 2,547 / 2,572 mixed geometries = 99.03% inside the slab. The corrected Arena B result is 2,120 / 2,207 = 96.06%.
This is the strongest G5 transfer result. A language frozen before solving two unseen minor-piece topologies predicts where nearly all White-king-sensitive complexity concentrates. It also improves on the conceptual generality of G4: the same critical-manifold template works across a leaper and a slider, not merely another pawn-race variant.
# 8. Off-surface singularities
## 8.1 Knight tail
Exactly 25 mixed geometries remain off all frozen one-move clock slabs. Every one is Black to move; the pawn is on d6 or d7; BK is three or four files from the d-file; 20 place BK on rank 1 and five on rank 8. They contain 1,450 legal WK placements: 1,400 wins and 50 draws.
## 8.2 Bishop tail
Exactly 87 corrected mixed geometries remain. Every one is Black to move and every pawn is on d6 or d7. Seventy-seven of 87 place BK three or four files from the d-file. The tail contains 5,036 legal WK placements: 4,882 wins and 154 draws. All 87 place bishop and BK on opposite colour complexes, so direct bishop/BK contact has disappeared; the surviving distinction is conversion topology involving WK.
# 9. Bounded local grammar and STOP
The frozen local DSL included pawn rank and move order; BK corridor/rank relations; WK distances to BK, pawn, promotion/front squares and minor; minor-piece access distances; support/contact relations; and relative file/rank orientation. No absolute-square identifiers or newly invented topology-specific atoms were introduced.
The representation is information-complete: after the frozen relative-orientation features are included, neither tail contains opposite-outcome states with identical semantic vectors. Exact separability therefore does not require a missing atom. But exact description cost crosses the predeclared lookup-scale threshold.
| Tail | Geometries | Placements | W / D | Exact leaves | Leaf / geometry |
| --- | --- | --- | --- | --- | --- |
| Knight | 25 | 1,450 | 1,400 / 50 | 15 | 0.600 |
| Bishop | 87 | 5,036 | 4,882 / 154 | 46 | 0.529 |
| Combined | 112 | 6,486 | 6,282 / 204 | 70 | 0.625 |
The G5 convention was to stop when exact representation needs more than roughly half as many leaves/templates as residual geometries unless a clearly reusable parameterized family appears. Both individual arenas cross that threshold; the combined grammar is worse. High shallow-tree accuracy does not alter the verdict because classifier accuracy is not proof compression. STOP is therefore triggered.
# 10. Cross-arena operation scorecard
| Operation | Prospective result | Verdict |
| --- | --- | --- |
| PROJECT | Exact KPK projections available in both arenas | Transfers mechanically |
| INHERITS | 1,086 N and 1,557 B restoration failures; mostly non-stalemate | FAILS as compact theorem |
| TARGET | Same exact semantic target formula in both arenas | STRONG PASS |
| ATTRACTOR | 366,763 N / 373,545 B; zero draws | STRONG PASS |
| BRIDGE | Exact union attractors but zero pure bridge states | FAILS as added composition |
| RESIDUAL | Exact subtraction preserves truth semantics | PASS |
| GROUP_OUT | 2,572 N / 2,207 B mixed geometries | PASS |
| LOCALIZE | 99.03% N / 96.06% B in same one-move slab | STRONG PASS |
| STOP | 15/25 and 46/87 trigger predeclared threshold | PASS |
| CERTIFY | Static universes reconstructed; bishop provisional truth corrected | PARTIAL / improved |
# 11. G5 advance/failure criteria audit
| Criterion | Outcome |
| --- | --- |
| Two arenas under same harness | Met: knight and bishop prospective arenas. |
| At least one inheritance/restoration rule transfers compactly | Not met. |
| Semantic target in each arena works under strict reachability | Met strongly. |
| At least one arena gains pure predicate-union bridge states | Not met: zero in both. |
| Frozen critical slab localizes substantial majority in new topology | Met strongly in both. |
| Certified coverage grows faster than description cost | Met for target/attractor interior; fails at final singularity by design. |
| Preserve at least one clean negative without retuning | Met: inheritance and bridge failures. |
| Stop local grammar at predeclared lookup threshold | Met. |
The failure criteria are also informative. The vocabulary did not need arena-by-arena rewriting; strict target reachability remained valuable; the critical region did not remain high-dimensional; and the arena restrictions were not changed after outcome inspection. Two negative signals did fire: restoration exceptions are too heterogeneous for a compact inheritance theorem, and union bridges cease to add meaningful compositional coverage.
# 12. Frozen G5 verdict
FROZEN G5 VERDICT: MIXED / SCIENTIFIC PASS, FULL-OPERATION TRANSFER FAILS. The prospective methodology succeeds: a fixed language discovers the same exact semantic stepping stone in two unseen minor-piece arenas and localizes 96–99% of their WK-sensitive frontiers to the same one-move clock manifold. It also exposes a repeatable description-cost floor at the remaining conversion singularity. But the stronger universal-proof-language hypothesis is falsified in two places: lower-material restoration is not compactly monotone once a mobile minor is restored, and predicate-union bridging supplies no pure compositional increment.
This is stronger evidence than another high-coverage post-hoc compression result because both successes and failures were obtained under a frozen prospective protocol. The reusable core is now narrower and better specified: exact projection as information, semantic TARGET, strict ATTRACTOR, residualization, grouping/localization, and explicit STOP transfer robustly; INHERITS and BRIDGE are conditional operations whose usefulness depends on arena semantics.
# 13. Evidence ledger
| Claim | Frozen result | Status |
| --- | --- | --- |
| N static universe | 1,211,042 | Exact reconstruction |
| B static universe | 1,180,148 | Exact reconstruction |
| N truth | 1,106,864 W / 104,178 D; rank 24 | Exact solve |
| B truth | 1,094,908 W / 85,240 D; rank 21 | Corrected exact solve |
| Common target | 214,344 N / 208,717 B; zero exceptions | Computer-assisted theorem |
| Strict target attractor | 366,763 N / 373,545 B; zero draws | Computer-assisted theorem |
| Union attractor | 368,023 N / 374,097 B | Computer-assisted theorem |
| Pure bridge | 0 N / 0 B | Exact negative |
| Critical slab | 99.03% N / 96.06% B | Exact structural count |
| Off-surface tails | 25 N / 87 B | Exact count |
| Tail populations | 1,450 N / 5,036 B | Exact count |
| Local grammar cost | 15/25 N; 46/87 B; 70/112 combined | Compression observation / STOP |
# 14. Superseded figures
- Bishop provisional truth 1,093,936 W / 86,212 D — superseded by 1,094,908 W / 85,240 D.
- Bishop provisional 2,223 mixed geometries — superseded by 2,207.
- Bishop provisional slab 2,133/2,223 = 95.95% — superseded by 2,120/2,207 = 96.06%.
- Bishop provisional off-surface tail 90 — superseded by 87.
# 15. Proof discipline and remaining certification scope
All exact statements are finite-universe claims conditional on the stated move semantics and implementation. Decision-tree leaf counts are representation observations rather than mathematical invariants. The benchmark uses static validity and omits repetition, en passant and move-count claims. A publication-grade repository rerun should persist deterministic state bitsets, rank histograms, residual tables, feature tables, zero-counterexample logs, software revisions and SHA-256 hashes, and should independently reproduce the earlier G3/G4 full checksum suites inside the generic harness. That repository engineering obligation does not change the frozen experimental verdict above.
# Appendix A. Reproduction checklist
1. Recreate N and B static universes and confirm 1,211,042 / 1,180,148.
1. Resolve N and confirm 1,106,864 W / 104,178 D, rank 24.
1. Resolve B and confirm corrected 1,094,908 W / 85,240 D, rank 21.
1. Reproduce the KPK regression and all lower-material projection counts.
1. Rescan restoration failures and classify immediate-stalemate versus genuine tactical failures.
1. Flatten the common target predicate and verify zero counterexamples in both arenas.
1. Recompute strict target and two-target union attractors with promotion/material reduction forbidden as shortcuts.
1. Confirm zero pure bridge states.
1. Group out WK and reproduce 2,572 N / 2,207 B mixed geometries.
1. Recompute frozen clocks and confirm 2,547/2,572 and 2,120/2,207 one-move slab counts.
1. Regenerate 25 N and 87 B tails and their placement W/D splits.
1. Re-run frozen DSL collision audit and exact-tree description-cost audit.
1. Persist deterministic artifacts, hashes, model flags and superseded-configuration ledger.
