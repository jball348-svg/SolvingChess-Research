# R1 Ascent Evidence Reconstruction

**Session:** R1 — Scaling and Lifting Audit  
**Purpose:** reconstruct the G6→G7→G8/R01/R02 ascent quantitatively while separating solve engineering from discovery leverage.

## 1. Controlling distinction

The historical stack contains four different phenomena that must not be merged:

1. **exact finite truth production** — enumerate/solve a declared arena;
2. **engineering leverage** — reduce solve memory/time for the same declared arena;
3. **proof/discovery leverage** — explain new exact truth using reusable targets, composition operators or strategy languages without arena-by-arena outcome fitting;
4. **restriction relaxation / relevance** — move toward broader topology rather than merely increasing state count or piece count.

R0 correctly identified that G8 strongly established (1) and (2), established some restricted-scope instances of (3), and did not establish a repeated law for (4).

## 2. G5 prospective baseline needed by R1

G5 is the cleanest historical prospective target-transfer control and supplies the target reused unchanged in the new R1 ladder.

Two arenas were frozen before outcome truth: K+N+d-pawn vs K and K+B+d-pawn vs K, pawn on d5–d7, unrestricted legal king/minor placement, board-only historical semantics.

The same target formula transferred exactly in both:

- d-pawn on d6 or d7;
- WK within four king steps of d8;
- BK at least five king steps from d8.

Historical exact results:

| Quantity | Knight | Bishop |
|---|---:|---:|
| static-valid states | 1,211,042 | 1,180,148 |
| White wins | 1,106,864 | 1,094,908 |
| direct target | 214,344 | 208,717 |
| strict target attractor | 366,763 | 373,545 |
| win-basin coverage | 33.14% | 34.12% |
| target false positives | 0 | 0 |
| pure two-target bridge | 0 | 0 |
| lookup-like tail | 15 leaves / 25 geometries | 46 / 87 |

This is simultaneously positive and negative evidence: a frozen semantic target transfers, while restoration/BRIDGE do not universally transfer and the final local tail crosses the predeclared lookup threshold.

Source: `handoffs/normalized/G5_Prospective_Transfer_Benchmark_Technical_Handoff.md`.

## 3. G6 — reusable operators plus topology-dependent scaling

G6 strengthened the universal graph layer and widened topology coverage.

### Exact reusable/core results

- Strict attractor semantics.
- Branch-Kernel factorization.
- Finite-n Hyperkernel factorization.
- Typed dependency/subsumption semantics.
- Conditional resource-safe TARGET construction.
- Large guarded restoration domains: FAR5 15,251,718 antecedents / 0 violations; FAR3 sliders 20,880,614 / 0; knight FAR3 has an exact 96-state exception family.

### Composition leverage

The bishop c-file Branch kernel contains 4,302 states and generates a 117,430-state strict pure bridge, a 27.2966× kernel-to-derived-region amplification **after the constituent basins exist**.

That is genuine proof/certificate leverage. It is not evidence that the constituent truth or target predicates were cheap to discover.

### G6 nested scaling experiment

Widening the pawn rank band from 5–7 to 2–7 roughly doubled state space while the TARGET_SAFE description remained unchanged and exact:

| Topology | state growth | target-attractor exponent | target share of win basin |
|---|---:|---:|---:|
| Knight | ≈2.0008× | 0.4207 | 33.135% → 22.471% |
| Bishop | ≈2.0014× | 0.6480 | 34.117% → 26.884% |
| Rook | ≈2.0003× | 0.9923 | 90.649% → 90.706% |

The target description cost stayed constant, but coverage did not scale uniformly. In N/B, new winning mechanisms appeared faster than the frozen proof object absorbed them; Rook behaved much better.

### Negative regimes preserved by G6

- G4/G5 lookup-like tails remain.
- Critical-manifold selectivity is not universal; double-brink timing slabs become tautological.
- An alternative 10-leaf tactical grammar works on double-brink held-out states, showing that proof regime is topology-dependent rather than uniformly absent.

Source: `handoffs/normalized/G6_Final_Technical_Handoff.md`.

## 4. G7 — higher material, real scale holds, new strategy-language factorization

G7 prospectively selected a higher-tree portfolio.

### Exact and held arenas

| Arena | Material / role | scale | G7 status |
|---|---|---:|---|
| F01 | K+B+P vs K+B+P, opposite-colour | 5,105,749 full states / 23,728,925 graph states later reported by G8 | exact |
| F02 | K+B+P vs K+B+P, same-colour | 4,761,076 / 22,770,972 | exact |
| F03 | K+B+P vs K+N+P | 48,028,628 graph states | hold |
| F04 | K+R+P vs K+B+P | 44,820,777 | >180 s hold |
| F06 | K+Q+P vs K+B+P | 40,499,052 | >180 s hold |
| F07 | K+B+2P vs K+B+P | 45,823,238 | seven-man hold |
| F08 | same-colour matched F07 | 43,334,293 | seven-man hold |
| F09 | higher wrong-colour fortress | 16,557,288 | exact |
| F10 | sanctuary-access control | 33,305,146 | full-table hold; terminal falsification available |

### Material-transition composition

F02 contains a three-way exact material-endpoint attractor of 612,427 states. A 1,641-state Hyperkernel generates the 7,195-state irreducible three-way region; that region is then reused as a target for a 23,327-state second-order attractor.

This proves that lower exact material signatures can act as reusable typed destinations.

### Strategy language

G7 adds FILTERED_ATTRACTOR and FILTER_PIVOT. The operator is graph-general, but the first concrete CHECK language is strongly topology-dependent:

- F01 CHECK retention: 99.9836%;
- F02: 95.0721%;
- F09: 29.6787%.

Filter-Pivot reconstructs the missing residual exactly even where CHECK coverage is poor. Again, exact factorization of a supplied language is not the same as automatic discovery of a useful language.

### G7 scaling interpretation

G7's main exact-solve limitation was real and prospectively preserved: F04/F06 and F07/F08 did not produce accepted W/D/L within the declared implementation budget. The session explicitly described this as an implementation/certificate boundary, not a universal state-count law.

Source: `handoffs/normalized/G7_Higher_Tree_Position_Discovery_Technical_Handoff.md`.

## 5. G8 — decisive engineering recovery, restricted re-ascent

G8 changes the exact-solve economics through material-signature decomposition, packed validity/outcome membership and validity reuse.

### Matched recovery of G7 holds

| Arena | graph states | G8 producer | G8 verifier | G7 |
|---|---:|---:|---:|---|
| F03 | 48,028,628 | 7.81 s | 4.58 s | hold |
| F04 | 44,820,777 | 9.65 s | 5.38 s | >180 s |
| F06 | 40,499,052 | 12.22 s | 6.03 s | >180 s |
| F07 | 45,823,238 | 10.76 s | 4.08 s | hold |
| F08 | 43,334,293 | 10.49 s | 3.76 s | hold |
| F10 | 33,305,146 | 9.77 s | 14.08 s | hold |

This is strong evidence that the G7 scale wall was substantially implementation-specific.

### Restricted eight-man re-ascent

R01/R02 were frozen before truth inspection as K+B+3P vs K+B+P with White pawns fixed on a7/c7/e7, Black pawn fixed on b2, and only the bishop-colour relation changed. Each arena has 64 capture-closed material signatures.

| Arena | dependency states | full states | capture exits | solve | verify |
|---|---:|---:|---:|---:|---:|
| R01 opposite | 88,363,292 | 4,420,922 | 1,801,481 | 19.46 s | 6.58 s |
| R02 same | 82,547,870 | 3,880,569 | 3,722,402 | 18.64 s | 6.22 s |

These are substantial exact finite results and a genuine prospective one-step material ascent. They are also strongly geometrically restricted: four pawns are fixed on specific squares and topology variation is narrow.

### G8 proof-object / strategy coverage

Sparse proof payload examples:

- F01 Branch kernel: 152 generators / 248 B;
- F02 Hyperkernel: 1,641 / 2,135 B;
- F02 CHECK pivots: 239 / 460 B;
- F09 CHECK pivots: 517,120 / 530,753 B;
- F02 full product generating payload: 2,599 B for the 23,327-state derived product basin.

The frozen six-language one-switch palette performs extremely well on recovered brink/seven-man families, but F09 remains the negative control:

- F01 100%;
- F02 99.676%;
- F03 99.156%;
- F04 99.772%;
- F06 99.983%;
- F07 99.946%;
- F08 99.763%;
- F09 55.498%.

Thus certificate compression and supplied-language factorization are impressive; universal language discovery is not demonstrated.

### Verifier economics

G8 also disproves a universal “verification is cheaper” rule:

- F09 verifier/producer = 1.651×;
- F10 = 1.441×;
- R01/R02 ≈0.338× / 0.334×.

Certificate bytes and verification compute are separate scaling variables.

Source: `handoffs/normalized/G8_Certificate_Engine_and_Reascent_Final_Technical_Handoff.md`.

## 6. Historical R1 synthesis

### What historical evidence does support

- Exact material-signature solving can be much cheaper than the prior monolithic implementation.
- Lower-material exact truth can be reused as typed dependencies.
- Strict attractors, Branch/Hyperkernel and Filter-Pivot are real reusable game-graph operations.
- Some semantic targets transfer prospectively across multiple related topologies.
- Sparse proof objects can represent large derived memberships compactly.
- A one-step prospective ascent to restricted eight-man truth was achieved.

### What historical evidence does not support

- a three-or-more-step law under progressively weaker chess restrictions;
- automatic semantic target discovery;
- automatic useful strategy-language discovery;
- a decreasing raw/unexplained residual as material rises;
- favorable verifier economics on every topology;
- any claim that R01/R02 are close to ordinary middlegame topology;
- any START_REACHABLE connection.

The historical record therefore justifies R1's prospective test, but does not itself close the scaling/lifting dependency.
