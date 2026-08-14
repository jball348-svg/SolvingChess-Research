# G8.5 Strategy-Language Algebra — Interim Evidence Freeze E

**Date:** 11 August 2026  
**Status:** **CLOSED — PASS VERY STRONGLY. G8.6 AUTHORISED.**

## 1. Frozen stage contract

G8.5 evaluates the predeclared semantic palette `CHECK`, `CAPTURE`, `FORCING = CHECK ∪ CAPTURE`, `KING_ONLY`, `PAWN_ONLY`, and `MOBILE_PIECE_ONLY`. No filter was added or edited after outcome/filter inspection. Target-entry edges retain the frozen G7 exemption.

For F01–F06 the target is the frozen G7 material-endpoint union `{SIG7,SIG11,SIG14}`. F07/F08 use the direct seven-man single-resource-exit analogue `{SIG15,SIG23,SIG30}`, frozen before filter results. F09 uses the frozen faithful safe-conversion TARGET. `CHECK_OR_PROMOTION_THREAT` is not instantiated because no exact move-local prospective definition was frozen. F10 is not retrofitted with a strategy target.

One-switch composition is frozen as `S(F→G) = Attr_F(C_G)`, where `C_G = Attr_G(T)` is treated as the certified next-phase target and the usual target-entry exemption applies.

## 2. Exact single-language transfer matrix

| Arena | Ordinary A | CHECK | CAPTURE | FORCING | KING_ONLY | PAWN_ONLY | MOBILE |
|---|---:|---:|---:|---:|---:|---:|---:|
| F01 | 146,068 | 146,044 (99.984%) | 143,710 (98.386%) | 146,044 (99.984%) | 144,179 (98.707%) | 143,710 (98.386%) | 145,599 (99.679%) |
| F02 | 612,427 | 582,247 (95.072%) | 557,375 (91.011%) | 582,247 (95.072%) | 560,379 (91.501%) | 557,375 (91.011%) | 603,816 (98.594%) |
| F03 | 623,638 | 581,914 (93.310%) | 568,146 (91.102%) | 581,914 (93.310%) | 586,792 (94.092%) | 568,146 (91.102%) | 594,708 (95.361%) |
| F04 | 3,089,492 | 2,484,665 (80.423%) | 1,761,987 (57.032%) | 2,484,665 (80.423%) | 1,816,124 (58.784%) | 1,761,987 (57.032%) | 2,877,371 (93.134%) |
| F06 | 4,896,620 | 4,843,717 (98.920%) | 2,357,434 (48.144%) | 4,843,717 (98.920%) | 2,385,133 (48.710%) | 2,357,434 (48.144%) | 4,846,005 (98.966%) |
| F07 | 1,186,903 | 1,093,512 (92.132%) | 983,658 (82.876%) | 1,093,512 (92.132%) | 1,000,035 (84.256%) | 983,658 (82.876%) | 1,149,297 (96.832%) |
| F08 | 927,338 | 883,585 (95.282%) | 799,827 (86.250%) | 883,585 (95.282%) | 804,157 (86.717%) | 799,827 (86.250%) | 913,843 (98.545%) |
| F09 | 8,295,062 | 2,461,867 (29.679%) | 2,460,362 (29.661%) | 2,461,867 (29.679%) | 3,288,923 (39.649%) | 3,283,177 (39.580%) | 2,502,224 (30.165%) |

All **48 / 48** filter rows pass the exhaustive local fixed-point audit and exact Filter-Pivot residual reconstruction: `fixedBad=0`, `missing=0`, `extra=0`.

## 3. Typed algebra discovered without adding predicates

1. **`FORCING ≡ CHECK` on all eight evaluated target contracts.** This is a typed degeneracy, not a universal chess theorem: under these particular target/domain semantics, CAPTURE adds no admissible pre-target same-domain edge beyond target-entry exits, and target-entry is already exempt.
2. **`PAWN_ONLY ≡ CAPTURE` on F01/F02/F03/F04/F06/F07/F08.** Their brink pawns have no internal non-promotion same-domain attacker move. F09 breaks the equivalence: `PAWN_ONLY` certifies 3,283,177 states versus 2,460,362 for CAPTURE, a difference of **822,815**.
3. **There is no universal best single language.** MOBILE is strongest on F02/F03/F04/F06/F07/F08, CHECK on F01, and KING_ONLY on F09. The operator transfers; coverage remains topology-dependent.
4. **Nesting is typed, not total.** PAWN/CAPTURE is a base subcorridor of CHECK/KING/MOBILE throughout the brink/seven-man endpoint families. CHECK and MOBILE are generally incomparable (exactly nested only in F01 among these tests). In F09, CHECK is exactly nested inside KING_ONLY.

## 4. One-switch strategy composition

| Arena | Best single | Best one-switch | One-switch coverage | Residual outside switch |
|---|---:|---|---:|---:|
| F01 | CHECK 99.984% | `KING_ONLY->CHECK` | **100.000%** | 0 |
| F02 | MOBILE_PIECE_ONLY 98.594% | `MOBILE_PIECE_ONLY->CHECK` | **99.676%** | 1,984 |
| F03 | MOBILE_PIECE_ONLY 95.361% | `KING_ONLY->CHECK` | **99.156%** | 5,261 |
| F04 | MOBILE_PIECE_ONLY 93.134% | `MOBILE_PIECE_ONLY->CHECK` | **99.772%** | 7,055 |
| F06 | MOBILE_PIECE_ONLY 98.966% | `CHECK->MOBILE_PIECE_ONLY` | **99.983%** | 852 |
| F07 | MOBILE_PIECE_ONLY 96.832% | `MOBILE_PIECE_ONLY->CHECK` | **99.946%** | 639 |
| F08 | MOBILE_PIECE_ONLY 98.545% | `CHECK->MOBILE_PIECE_ONLY` | **99.763%** | 2,201 |
| F09 | KING_ONLY 39.649% | `CHECK->PAWN_ONLY` | **55.498%** | 3,691,481 |

The recovered hostile families show a very strong reusable phase-switch structure:

- F03: **99.156%** with `KING_ONLY→CHECK`.
- F04: **99.772%** with `MOBILE_PIECE_ONLY→CHECK`, versus only 80.423% CHECK and 93.134% MOBILE separately.
- F06: **99.983%** with `CHECK→MOBILE_PIECE_ONLY`.
- F07: **99.946%** with `MOBILE_PIECE_ONLY→CHECK`.
- F08: **99.763%** with `CHECK→MOBILE_PIECE_ONLY`.

F09 is the deliberately valuable negative control. Its best tested one-switch certificate is only **55.498%** (`CHECK→PAWN_ONLY`), leaving **3,691,481** ordinary-attractor states outside the two-phase corridor. No bespoke fortress language is added after seeing this.

## 5. Switching is not merely set union

Every nontrivial arena shows positive dynamic gain over the static union of its two single-language corridors. Examples:

- F04 `MOBILE→CHECK`: **+198,155** states beyond `MOBILE ∪ CHECK`; `CHECK→KING`: **+543,519**.
- F06 `CHECK→MOBILE`: **+43,949**.
- F07 `MOBILE→CHECK`: **+36,528**.
- F09 `CHECK→PAWN`: **+1,319,918** despite the final corridor remaining incomplete.

Thus the switch object is capturing ordered strategy phases, not simply overlap/nesting of two filtered attractors.

## 6. G8.5 freeze verdict

**PASS VERY STRONGLY.** The predeclared palette transfers across eight materially/topologically distinct exact arenas. Filter-Pivot remains exact on every one of 48 filter rows. The most important new empirical structure is ordered phase switching: a single semantic handoff lifts every recovered six-/seven-man brink family to at least 99.156% of its ordinary target basin, while the faithful fortress F09 remains a sharp counterexample at 55.498%.

No new universal chess theorem is promoted in G8.5. The correct promotion is narrower: **strategy-language composition supports a finite typed algebra with quotient/equivalence relations determined by arena/target type, and ordered switching is a reusable proof-DAG operation worth compiling in G8.6.**

G8.6 is therefore authorised to compile destination × strategy product DAGs, with F02 as the existing Hyperkernel anchor and the newly measured ordered strategy phases as the second axis.
