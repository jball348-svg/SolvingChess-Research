<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: Pilot_2_G3_Technical_Handoff.docx
original_sha256: 117258872ce0066427b5a0787e5cf16da87b6448b946049b7ff688fc913c9b27
derivative_filename: Pilot_2_G3_Technical_Handoff.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

# Pilot 2 - G3 Technical Handoff
Bounded local-grammar test and third exact compositional bridge in K+2P vs K
STATUS: G3 FROZEN - PASSED VIA PRINCIPLED COMPLEXITY BOUNDARY; EXACT COVERAGE 98.94%
10 August 2026
# Executive summary
G3 was the bounded follow-on to Pilot 2. It asked whether the final 214 White-king-sensitive blockade geometries admit a compact reusable local-access grammar, and whether a third exact compositional layer can be obtained before changing material.
Every load-bearing Pilot 2 checksum was independently reconstructed before new inference. A strict reachability target equal to the union of KPK inheritance and the rank-gap-1 cooperative predicate certifies another 2,852 previously unexplained wins, with zero draws admitted. Exact symbolic coverage rises from 223,230 / 228,500 = 97.69% to 226,082 / 228,500 = 98.94%.
The surviving 214 mixed geometries do not collapse to a small exact grammar under the bounded access-region DSL. Semantic features become exact after adding one blockade-orientation atom, but an exact semantic tree still requires roughly 200 leaves for 214 geometries. Under the predeclared stopping rule, this is a principled local-topology complexity floor rather than a reason to fit square-specific exceptions.
| Quantity | Frozen G3 value |
| --- | --- |
| Pilot 2 wins / draws | 228,500 / 8,476 |
| Certified before G3 | 223,230 wins = 97.69% |
| Post-two-lemma residual | 13,736 = 5,270 wins + 8,466 draws |
| New bridge-certified wins | 2,852 |
| Combined certified | 226,082 / 228,500 = 98.94% |
| Post-bridge residual | 10,884 = 2,418 wins + 8,466 draws |
| Post-bridge geometries | 272 = 16 universal win + 214 mixed + 42 universal draw |
| Mixed placements after bridge | 8,580 = 1,776 wins + 6,804 draws |
| Exact grammar cost | ~200 leaves / 214 mixed geometries |
# 1. Research question and stopping rule
The G3 programme explicitly allowed two advance signals: either a small parameterized access/blockade vocabulary exactly generates most of the 214, or a bounded search establishes a principled complexity boundary while exact compositional mechanisms continue to remove robust interior. It prohibited treating high classifier accuracy or arbitrary absolute-square masks as success.
# 2. Independent reconstruction
A fresh minimal move generator was used for this material class. Before any G3 inference, the following frozen Pilot 2 checksums were recovered.
| Checksum | Recovered value |
| --- | --- |
| KPK(d) | 41,358 valid = 28,853 wins + 12,505 draws |
| KPK(e) | 41,358 valid = 28,853 wins + 12,505 draws |
| KPK inheritance | 197,118 antecedents; 197,108 wins; 10 stalemates |
| Cooperative residual | 39,858 = 31,392 wins + 8,466 draws |
| Rank-gap-1 target | 14,382 states / 504 geometries |
| Strict rank-gap-1 reachability | 26,122 wins |
| Final Pilot 2 residual | 13,736 states / 520 geometries / 214 mixed |
# 3. Terminal-semantics certificate note
The independent reconstruction initially returned 228,502 White wins. Exactly two mirror-symmetric static-valid checkmate positions account for the difference: Kd6, Pd7, Pe7 versus Kd8 with Black to move, and its d/e reflection. Treating ordinary checkmate as White-winning adds those states. The frozen Pilot 2 convention leaves these no-move states outside the White-win attractor. G3 preserved the frozen convention. A repository certificate should make this explicit.
# 4. Third compositional layer: return bridge
Define the target T as the union of the two already-certified semantic regions: KPK-inheritance-certified states OR the rank-gap-1 cooperative target. Terminalize T as success. Promotion and material-reduction exits are failures for this reachability objective. Therefore a newly certified state must force the board into an already-proved predicate under adversarial play.
| Bridge rank | New wins |
| --- | --- |
| 1 ply | 346 |
| 2 plies | 2,408 |
| 3 plies | 52 |
| 4 plies | 46 |
| Total | 2,852 |
There are zero false-positive draws and the maximum bridge depth is four plies. The proof hierarchy now certifies 226,082 / 228,500 wins = 98.94%.
- Layer 1: KPK inheritance certifies 197,108 wins.
- Layer 2: strict reachability to rank-gap-1 certifies another 26,122 wins.
- Layer 3: strict reachability back into the union of Layers 1 and 2 certifies another 2,852 wins.
- Residual: 2,418 wins and 8,466 draws remain outside all three certified mechanisms.
# 5. Effect on the residual
The bridge mainly removes another robust shell. Of the 2,852 newly certified wins, 2,638 come from post-two-lemma universal-win geometries and 214 from winning placements inside mixed geometries.
| Reduced class | Before bridge | After bridge |
| --- | --- | --- |
| Universal win | 264 | 16 |
| Mixed | 214 | 214 |
| Universal draw | 42 | 42 |
All 214 mixed geometries survive. Their legal White-king population becomes 8,580 placements: 1,776 wins and 6,804 draws. The compositional interior and the genuinely king-sensitive boundary are therefore cleanly separated.
# 6. Bounded access-region DSL
- Pawn-pair frame: advanced/rear pawn, rank gap, leader file and support relation.
- BK blockade frame: corridor distance, rank relative to each pawn, front/side/rear sector.
- Critical support/contact squares around each pawn.
- Frozen-board WK/BK access distances to critical squares.
- Tempo and route-parity comparisons.
- Pawn contact/protection atoms.
- d/e reflection and pawn-order canonicalization.
# 7. Missing orientation atom
The initial semantic representation was almost information-complete: only two mirror pairs shared identical feature vectors but opposite W/D truth.
- WK b8 / Pd2 Pe7 / BK e8 / Black -> win; WK h8 with the same other pieces -> draw.
- Mirror: WK a8 / Pd7 Pe2 / BK d8 / Black -> draw; WK g8 with the same other pieces -> win.
The missing distinction is whether WK lies on the rear-pawn side of the advanced-pawn/BK blockade or on the outside. Adding this orientation atom resolves the collisions without introducing a raw WK-square identifier.
# 8. Description-length result
Exact separability does not imply useful compression. With the enriched semantic DSL, an exact decision tree still requires approximately 200 leaves over 214 mixed geometries. The frontier is local and chess-semantic, but template reuse is too weak to justify continued fitting. This reproduces the complexity warning seen in Pilot 1's mobile-king boundary.
# 9. G3 gate decision
G3 PASSES VIA THE PRINCIPLED-COMPLEXITY-BOUNDARY BRANCH. It does not claim a tiny grammar for the 214. It establishes that a bounded topology-first language reaches near lookup-scale at the surviving critical boundary while a new strict compositional operation continues to compress the solved basin.
# 10. Evidence ledger
| Claim | Result | Status |
| --- | --- | --- |
| Pilot 2 checksums | Recovered | Exact reconstruction |
| Two-checkmate discrepancy | Exactly two mirror states | Certificate finding |
| Union bridge | 2,852 wins; zero draws; max depth 4 | Computer-assisted theorem |
| Combined coverage | 98.94% | Exact composition |
| Post-bridge residual | 10,884 states | Exact count |
| Mixed boundary | 214 geometries; 1,776 wins + 6,804 draws | Exact grouping |
| Semantic collision audit | Two mirror pairs before orientation atom | Exact audit |
| Enriched DSL | Exact separability | Representation result |
| Grammar complexity | ~200 leaves | Compression observation |
# 11. Frozen conclusion
FROZEN G3 VERDICT: PASS. A third exact compositional layer raises coverage to 98.94%, while the bounded access-region search establishes the surviving king/blockade frontier as a principled complexity floor under the tested representation. Do not continue polishing the 214 with square-specific exceptions. The next scientific test is cross-arena reuse of the proof architecture.
# Appendix A. Reproduction checklist
- Reproduce both KPK checksums and all Pilot 2 decomposition counts.
- Explicitly test and document the two mirror checkmate terminal-semantics cases.
- Terminalize the union of KPK inheritance and rank-gap-1; forbid promotion/material-reduction shortcuts.
- Confirm bridge ranks 346 / 2,408 / 52 / 46, total 2,852 and zero draw false positives.
- Confirm post-bridge residual 10,884 and 272 reduced geometries.
- Recreate the two semantic collision pairs and orientation-atom resolution.
- Persist bitsets, bridge ranks, residual/feature tables, zero-counterexample logs and hashes.
