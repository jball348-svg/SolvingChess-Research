# R2 Discovery Cost Audit

**Session:** R2 — Topology-Adaptive Proof Discovery Audit

## 1. Accounting rule

R2 separates:

- legal/static graph construction;
- exact lower-dependency production;
- semantic feature/candidate work;
- complete top W/D/L acquisition;
- proof-object verification.

The prospectively frozen economic gate is:

`DISCOVERY_COST_RATIO = discovery wall / complete exact-truth acquisition wall <= 1.0`.

This is deliberately demanding because R2 asks whether proof discovery is economically competitive with simply solving the arena.

## 2. D1 discovery cost

Accepted discovery-freeze run:

| Component | Wall |
|---|---:|
| Static-valid / top indexing | 0.5639 s |
| Exact lower signatures | 11.7188 s |
| Top graph + semantic metadata | 13.0138 s |
| A4 certified basin | 0.2773 s |
| Target generation/ranking | 5.6778 s |
| 55 strategy classes | 0.4168 s |
| 36 ordered one-switch programs | 1.3289 s |
| Ordinary/filtered recomputation + rank checks + overhead | remainder |
| **Total discovery** | **33.9099 s** |

Peak RSS on a later identical-object discovery replay:

**924,500 KiB (~903 MiB).**

The replay completed in 28.23 s external wall, showing some wall-time variance but no change to selected objects.

## 3. Complete D1 exact truth cost

First accepted validation acquisition:

| Component | Wall |
|---|---:|
| Static-valid / top indexing | 0.5256 s |
| Exact lower signatures | 11.1897 s |
| Top graph | 9.1102 s |
| Complete top W/D/L solve | 5.7094 s |
| **Complete exact-truth acquisition** | **26.5349 s** |

A later instrumented replay measured:

- acquisition: 27.4093 s;
- full command including frozen proof-object application/validation: 32.9666 s;
- peak RSS: **850,844 KiB (~831 MiB)**.

All are far inside the 180 s / 2 GiB arena budget.

## 4. Discovery cost ratio

Using the accepted discovery freeze and first complete acquisition:

`33.9099 / 26.5349 = 1.2780`.

Thus the frozen <=1.0 economic threshold **FAILS**.

A later timing replay places the two workloads much closer to parity (external discovery 28.23 s versus 27.4093 s acquisition), but still does not establish a robust <1 advantage. R2 does not replace the preregistered failure with the more favorable rerun.

This is the decisive reason the overall R2 proposition is not `SURVIVED`.

## 5. Outcome-truth consumption

Top-domain labelled truth used during candidate generation/selection:

**0 states.**

`TRUTH_LEAKAGE = 0 / 5,004,008 = 0.000000`.

Exact lower-material truth consumed by discovery:

**18,293,044 states.**

This lower truth is not counted in the defined top-domain leakage ratio, but its production cost **is** counted in discovery cost. The selected target explicitly uses that dependency through `WHITE_CERTIFIED_LOWER_CAPTURE_EXIT_EXISTS`.

## 6. Description versus lookup cost

Selected target:

- 3 literals / 2 clauses.

Selected program:

- 2 move literals / 1 switch.

Residual exact D1 wins outside composite proof object:

- 1,125 / 2,377,388 = 0.0473208%.

Thus representation cost is dramatically below a raw top-state lookup table. The economic failure is **compute**, not description size.

## 7. Held-out acquisition economics

H1 instrumented replay:

- complete acquisition: 28.0783 s;
- full command including unchanged proof-object application/validation: 32.4128 s;
- peak RSS: **875,576 KiB (~855 MiB)**.

No H1 candidate search/retraining was performed.

## 8. Comparison to R1 and historical economics

R1 showed exact producer cost can be very cheap in controlled material-signature families. R2 inherits that strength. Because exact truth acquisition remains inexpensive at ~26–28 seconds for ~5M top states plus ~18M lower dependency states, even a compact zero-label miner has difficulty beating the solver.

This is strategically important:

> R2 succeeds at **information discipline** (zero top-label discovery) and **proof compression**, but not at **discovery economics**.

Opposing mobile material does not make exact solving hard enough, in this arena, for discovery to gain an economic advantage. Instead the broader candidate/feature search adds overhead on top of an already efficient exact solver.

## 9. Cost verdict

- candidate generation/selection cost: bounded and modest;
- complete truth acquisition: cheaper;
- verifier/proof application: exact and within budget;
- description cost: far below lookup scale;
- frozen discovery-economic threshold: **FAILED**.

This failure is preserved in the overall `PARTIAL` classification.
