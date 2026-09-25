# G7.7 Interim Evidence Freeze E — Backward Fire

**Date:** 11 August 2026  
**Status:** **G7.7 CLOSED — STRONG PASS. G7 remains open for G7.8/G7.9.**

## 1. Stage rule

The G7.6 objects were frozen before this audit. CHECK was not retuned, target-entry exemption was unchanged, and Filter-Pivot was not altered to fit G6. Type-inapplicability and missing implementation-level source were recorded as holds rather than reverse-engineered.

## 2. Same-side all-file backward fire

The canonical G6 same-side target is `TARGET_SAFE`. G7.7 independently reconstructed its exact strict-attractor quantities; d-file N/B counts reproduce 366,763 / 373,545 and the bishop c-file whole target attractor reproduces 795,768. The backward CHECK/filter-pivot sweep then covered all **24** rank5-7 N/B/R pawn-file arenas a-h. Every Filter-Pivot residual reconstruction was exact: **0 missing / 0 extra in 24/24**.

Aggregate advanced-pawn results:

| Piece | Ordinary attr total a-h | CHECK total | Aggregate retained | Quiet-required | Pivots | Pivot amp |
|---|---:|---:|---:|---:|---:|---:|
| N | 5,216,274 | 2,860,796 | 54.844% | 2,355,478 | 252,912 | 9.313x |
| B | 5,828,716 | 2,782,282 | 47.734% | 3,046,434 | 251,552 | 12.111x |
| R | 8,148,388 | 2,676,768 | 32.850% | 5,471,620 | 264,788 | 20.664x |

CHECK retained-share ranges: N 45.618-88.893%; B 37.623-85.008%; R 29.838-34.492%. The strategy language is therefore useful but materially topology-dependent.

## 3. Nested scaling reinterpretation

On d-file rank expansion 5-7 -> 2-7:

- Knight ordinary attr grows **1.3388x**, CHECK **1.0000x**, quiet-required **4.0504x**.
- Bishop ordinary attr grows **1.5677x**, CHECK **1.0016x**, quiet-required **4.7777x**.
- Rook ordinary attr grows **1.9896x**, CHECK **1.0001x**, quiet-required **2.4104x**.

The old fixed-target scaling growth is therefore largely growth of the **quiet-required strategy complement**, not expansion of the all-check corridor. This is an exact retrospective decomposition, but not yet a universal scaling theorem.

## 4. Faithful fortress backward fire

The G6 faithful one-bishop fortress was reconstructed under the same promotion-continuation semantics and reproduces **1,182,440 = 825,269 W + 357,171 D**, direct target **103,451**, and ordinary strict target attractor **585,732**.

CHECK-filtered target attraction: **178,642 / 585,732 = 30.4989%**, with **0 non-wins**. The quiet-required complement **407,090** factors exactly through **39,790 pivots**, amplification **10.2310x**, 0 missing / 0 extra. This is backward transfer across a different terminal model and fortress topology.

## 5. Interaction with G6 BRIDGE

G6 split TARGET_SAFE by **Black-king side of the pawn file**. G7.7 reproduced the frozen ordinary pure-bridge counts and then measured CHECK overlap:

| Arena | Ordinary pure BRIDGE | In CHECK corridor | Overlap | Filtered pure |
|---|---:|---:|---:|---:|
| N-d | 3,486 | 2,156 | 61.847% | 5,538 |
| B-d | 9,756 | 4,734 | 48.524% | 5,481 |
| B-c | 117,430 | 3,190 | **2.717%** | 6,028 |

The bishop c-file result is decisive against subsumption: destination-choice Branch-Kernel structure can be enormous while almost entirely outside the CHECK strategy corridor. G6 Branch/Hyperkernel and G7 Filter-Pivot describe different compositional axes.

## 6. Restoration-guard backward result

The conversion-safe White-mobile guard was fired backward into the original G5 d-file N/B rank5-7 arena. Because there is no opponent pawn there, the frozen guard reduces to `restored mobile piece is not on White's promotion square`.

- Knight: raw projected-win restoration failures **1,086**; guard leaves **535**. It explains **551** historical failures.
- Bishop: raw failures **1,557**; guard leaves **1,048**. It explains **509**.

Thus the guard captures a genuine conversion-interference mechanism but is strictly weaker than the G6 FAR-domain theory. It is retained as a conditional sharpening, not promoted as a replacement theorem.

## 7. Source-bounded holds

The frozen G6 record names and hashes implementation sources for two-sided and double-brink experiments, but the source contents were not retrievable as active files through the present File Library search. The opposing-minor edge implementation was likewise not recovered. Since an edge-filtered strategy certificate cannot be computed from aggregate W/D/attr counts alone, **no CHECK or pivot counts are invented for those families**.

G4 remains under its explicit frozen historical optional-pawn/capture implementation exception. No clean-room graph is substituted for G7.7 backward-fire numbers.

These are provenance/source holds, not failures of the factorization theorem.

## 8. G7.7 promotions

1. **`G7.FILTER_PIVOT.v0.2` — PROMOTED to universal/core proof-language factorization.**
2. **`G7.FILTERED_ATTRACTOR.v0.2` — PROMOTED as a universal typed strategy-language reachability field/operator.** CHECK is a reusable first instantiation, not a universal compression guarantee.
3. **Conversion-safe restoration guard — sharpening only.**
4. **Sanctuary access guard — retained conditional guard family, existing restoration object envelope.**

## 9. Stage verdict

**G7.7 STRONG PASS.** The G7.6 strategy-language architecture fires backward across a broad, symmetry-complete G6 same-side corpus and the faithful fortress, survives scale expansion, and remains distinct from G6 destination-choice composition. Its only serious negative is useful: the particular CHECK language loses coverage in quiet/rook/deeper-rank topologies, while the universal Filter-Pivot factorization remains exact.
