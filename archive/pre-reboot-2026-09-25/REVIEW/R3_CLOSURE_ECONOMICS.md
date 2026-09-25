# R3 Closure Economics

**Session:** R3 — Start-Reachable All-Reply Closure Audit

## Accepted clean-run resource results

Each accepted branch run is inside the prospective 180 s / 2 GiB budget.

| branch | workload | wall | peak RSS |
|---|---|---:|---:|
| D king-pawn | competent raw exact forward baseline | 9.2827 s | 738,716 KiB |
| D king-pawn | frozen semantic-policy DAG | 3.20535 s | 192,688 KiB |
| H queen-pawn | competent raw exact forward baseline | 7.88406 s | 644,688 KiB |
| H queen-pawn | unchanged semantic-policy DAG | 3.09398 s | 189,100 KiB |

Empirical `CLOSURE_COST_RATIO` using construction wall:

- D: **0.34530x** raw baseline;
- H: **0.39243x** raw baseline.

These ratios are implementation/hardware observations, not a chess scaling law.

## State burden

At ply 5:

| branch | raw path leaves | raw unique exact full states | policy unique unresolved frontier |
|---|---:|---:|---:|
| D | 808,373 | 496,086 | 13,064 |
| H | 690,301 | 411,566 | 13,181 |

The raw exact-forward implementation already uses competent exact transposition handling. The policy is therefore not being compared to an intentionally naive no-transposition baseline.

## Discovery/evaluation accounting

R3 can separate the scientific workloads but the audit-local harness did not independently time every micro-component:

| component | R3 accounting |
|---|---|
| raw forward-search cost | separately measured above |
| exact full-state canonicalization cost | included in both raw and policy wall; not separately instrumented |
| semantic feature cost | included in policy wall; not separately instrumented |
| candidate generation | six frozen candidates; no outcome labels; not separately timed |
| candidate selection | exact ply-2 D structure only; 40 states / 1,199 edges; not separately timed |
| proof-domain construction | separately measured policy wall above |
| verifier/replay | deterministic clean reruns reproduced the same counts; no structurally independent R3 verifier wall was isolated |
| labelled/proven information used for strategy selection | **0 W/D/L labels** |

The missing component-level and independent-verifier timing is preserved as an R3 limitation. It prevents using the favorable construction ratio as publication-grade verification economics.

## Verification/replay status

The audit-local generator reproduced the frozen G11 standard-start perft anchors through depth 4. Separate clean process runs reproduced the previously observed branch counts and history multipliers exactly.

However, R3 did **not** build a second independently authored full-state move generator/verifier. The inherited G11 dual-generator conformance evidence supports the semantic implementation target, but does not convert the R3 policy experiment itself into an independent replay certificate.

Therefore:

- construction economics: favorable at tested shallow scope;
- deterministic replay: successful;
- independent verifier economics: **not established**.

## Economic interpretation

The large reduction is mainly semantic White-choice reduction, not raw full-state transposition. Exact history makes the raw transposition ratio worse by ply 5, while the policy avoids generating most of those histories.

That is encouraging for a strategy-DAG architecture but is not yet evidence that a **certified non-loss** policy can be selected this cheaply. Certifying the White choices is the unresolved economic question.
