# R1 Scaling Results

**Session:** R1 — Scaling and Lifting Audit  
**Prospective authority:** `REVIEW/R1_SCALING_HYPOTHESIS.md` at commit `29d3946a056ca6033f3be58fd2e152286aca8d20`  
**Outcome inspection began only after that freeze.**

## 1. Reproducibility context

The R1 finite-game harness was compiled with:

- `g++ (Debian 14.2.0-19) 14.2.0`
- `-O3 -std=c++17 -march=native`
- Linux x86_64, kernel 6.18.44

Final source SHA-256:

`dcf4260e4779d6274a07013541714b475760ef6c49694b8405fcb1c6c54af245`

Final executable SHA-256:

`47c9248e6385ff0b772c5241cd66b1ee0a6712797bc2ab683ff2cbabd0171a9d`

The producer computes least fixed-point White-win truth with lower-material capture dependencies. The verifier runs as a separate process, recomputes validity and Bellman conditions, and requires a strictly descending rank witness for every nonterminal winning claim so self-supporting winning cycles cannot pass.

### Harness correction before final timings

The first implementation generated each reverse predecessor and then regenerated all forward moves to prove that inverse candidate. This was semantically correct but needlessly quadratic in local move generation and caused wrapper/hostile timeouts.

R1 did **not** shrink or alter any arena. Instead the inverse generator was replaced by direct chess-legal inverse moves. The repair was accepted only after:

- P0 again reproduced the historical G5 bishop checksum exactly: 1,180,148 states / 1,094,908 wins / 373,545 strict target attractor;
- P1/P2/P3/H2 exact truth and proof-object populations matched the pre-repair runs where those runs had completed;
- the separate verifier passed every accepted state.

The final results below use the repaired harness. The abandoned timeouts are an engineering alarm, not evidence against the scientific ladder.

## 2. Experiment A — truth-production scaling

| ID | dependency states | largest live signature | dep/active | producer | producer RSS | verifier | verifier RSS | V/P |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| P0 | 1,625,276 | 1,180,148 | 1.377× | 0.259 s | 13.5 MiB | 0.225 s | 9.9 MiB | 0.871× |
| P1 | 3,158,830 | 1,180,148 | 2.677× | 0.742 s | 17.1 MiB | 0.566 s | 12.9 MiB | 0.763× |
| P2 | 6,126,627 | 1,180,148 | 5.191× | 1.201 s | 21.2 MiB | 0.833 s | 16.4 MiB | 0.693× |
| P3 | 13,532,888 | 4,191,884 | 3.228× | 2.814 s | 63.6 MiB | 1.914 s | 46.8 MiB | 0.680× |
| H1 | 29,734,058 | 12,602,226 | 2.359× | 6.656 s | 168.1 MiB | 4.410 s | 120.4 MiB | 0.663× |
| H2 | 13,043,648 | 4,048,418 | 3.222× | 3.215 s | 63.4 MiB | 2.044 s | 46.9 MiB | 0.636× |

All producer truths independently passed the rank/Bellman verifier.

### Normalized producer cost

Producer seconds per million dependency states:

- P0: 0.159;
- P1: 0.235;
- P2: 0.196;
- P3: 0.208;
- H1: 0.224;
- H2: 0.246.

The median P0–P2 rate is 0.196 s/M. P3 is 0.208 s/M = **1.061×** that median, well inside the preregistered 3× limit.

A log-log fit to the four ordered P0–P3 points gives a descriptive runtime exponent of approximately **1.09** against dependency-state count. This is a useful finite-harness observation, not an extrapolation law for chess.

### Truth-production gate

1. P0–P3 all solved and verified: **PASS**.
2. All are far below 300 s / 3 GiB: **PASS**.
3. P3 normalized runtime <=3× P0–P2 median: **PASS**.
4. P2/P3 dependency-to-active ratio >=2: **PASS**.
5. P2/P3 verifier <=1.5× producer: **PASS**.
6. No semantic weakening: **PASS**.

**Experiment A result: SURVIVED.**

## 3. Experiment B — proof/discovery leverage

The target and strategy palette were frozen before truth inspection.

| ID | exact White wins | direct target | target false positives | strict target attractor | target / wins | best frozen one-switch | switch / target basin | full-win residual |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| P0 | 1,094,908 | 208,717 | 0 | 373,545 | 34.117% | KING_ONLY→PAWN_ONLY | 93.291% | 65.883% |
| P1 | 1,112,076 | 199,890 | 0 | 359,310 | 32.310% | KING_ONLY→PAWN_ONLY | 93.271% | 67.690% |
| P2 | 1,043,686 | 191,112 | 0 | 344,420 | 33.000% | KING_ONLY→PAWN_ONLY | 93.390% | 67.000% |
| P3 | 4,188,474 | 765,360 | 0 | 1,379,448 | 32.934% | KING_ONLY→PAWN_ONLY | 93.354% | 67.066% |
| H1 | 12,594,284 | 1,724,571 | 0 | 3,727,570 | 29.597% | KING_ONLY→PAWN_ONLY | 89.813% | 70.403% |
| H2 | 4,044,431 | 728,876 | 0 | 2,993,272 | **74.010%** | PAWN_ONLY→KING_ONLY | **43.504%** | 25.990% |

No arena-specific target or strategy predicate was introduced.

### Main-ladder proof gate

- zero target false positives P0–P3: **PASS**;
- P2/P3 target coverage >=20%: **PASS**;
- P3 coverage drop from P0 = 1.183 percentage points, <15 pp: **PASS**;
- P1–P3 best frozen one-switch >=90%: **PASS**;
- full-win residual worsens only 1.183 pp P0→P3, <15 pp: **PASS**;
- new predicates = 0: **PASS**.

**Main-ladder proof/discovery result: SURVIVED.**

Important limitation: “survived” here means transfer of already-supplied proof objects. R1 did not demonstrate automatic target or strategy-language invention.

## 4. Hostile controls

### H1 — wider pawn mobility

H1 widens all three pawn bands while retaining bishop topology.

- exact truth completes and verifies;
- target false positives: 0;
- target coverage: 29.597% >=15%;
- frozen one-switch coverage: 89.813% >=75%;
- no new predicates.

**H1: PASS.**

### H2 — rook mobility/checking

H2 holds the P3 pawn bands fixed but replaces bishop with rook.

Structural change relative to P3:

- mean branching 9.571 → 10.881;
- p95 branching 19 → 23;
- maximum 24 → 25;
- White-move checking density 3.765% → 7.577%.

Truth production remains easy and the unchanged target becomes exceptionally large: 74.010% of all White wins with zero false positives.

But the **best** ordered pair from the entire frozen one-switch palette reaches only:

`1,302,190 / 2,993,272 = 43.504%`

of the ordinary strict target basin, versus the hostile threshold of 75%.

No new move language was invented to rescue it.

**H2 proof-language hostile control: FAIL.**

### Hostile gate

Because H2 fails the prospectively frozen strategy-transfer threshold:

**Hostile gate: FAIL.**

## 5. Analysis/discovery-evaluation cost

Wall time for evaluating the frozen target plus all 16 one-switch combinations:

| ID | analysis wall | peak RSS |
|---|---:|---:|
| P0 | 1.42 s | 22.1 MiB |
| P1 | 1.52 s | 23.1 MiB |
| P2 | 1.55 s | 28.7 MiB |
| P3 | 6.22 s | 92.4 MiB |
| H1 | 18.61 s | 252.2 MiB |
| H2 | 7.56 s | 91.4 MiB |

This is evaluation cost for a fixed vocabulary, not automatic discovery cost.

## 6. Raw / unexplained residual

The main P0–P3 ladder does **not** show the unexplained exact-win residual shrinking:

- P0 65.883%;
- P1 67.690%;
- P2 67.000%;
- P3 67.066%.

Thus the unchanged target explains a stable roughly one-third of full truth, not an increasing share.

H1 worsens to 70.403%. H2 improves sharply to 25.990%, but then the frozen strategy palette explains only 43.504% of that target basin. There is no monotone residual-compression law.

## 7. Scaling-law statement allowed by R1

R1 can defensibly state only:

> In this prospectively frozen, board-only, one-sided material family, material-signature exact solving and rank/Bellman verification scale approximately with dependency-state count across the tested 1.6M–29.7M dependency-state range, while a fixed semantic target retains substantial exact coverage across the bishop ladder.

R1 **cannot** defensibly state:

- a law for unrestricted chess;
- a law for opposing mobile material;
- a law for full history-aware state;
- a law that the unexplained residual shrinks with ascent;
- a law that one frozen strategy palette transfers across topology.

## 8. Frozen R1 result

- Truth-production scaling: **SURVIVED**.
- Main-ladder proof/discovery leverage: **SURVIVED at the fixed-object transfer scope**.
- Hostile held-out transfer: **FAILED on H2 strategy-language coverage**.
- Overall R1 scaling/lifting proposition: **PARTIAL**.
