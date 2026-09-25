# R5 Certification Economics

**Session:** R5  
**Question:** does the exact nonterminal target provide materially favorable certification economics for the same proposition?

## 1. Competent baseline

The baseline answers exactly the same bounded proposition as the semantic certifier:

- identical D/H cohorts;
- identical exact full-rule state identity;
- identical FERL-4 target;
- identical four-ply target theorem;
- identical one White/Black attraction pair;
- every legal Black reply;
- but **all legal White moves** are admitted at the attraction White node.

This is not a stronger complete-chess W/D/L task.

Unlike R4's raw baseline, both R5 baselines complete inside the frozen 2 GiB budget.

## 2. Wall-clock cost

| Family | Policy certification | Unrestricted exact baseline | `CERTIFICATION_COST_RATIO` |
|---|---:|---:|---:|
| D | 27.789252083 s | 34.375237343 s | **0.8084090244** |
| H | 27.599330099 s | 33.018857092 s | **0.8358657001** |

The frozen strong-survival threshold is <=0.75.

Both families therefore **fail the economic gate**.

## 3. Exact-work proxy

Using recorded examined candidate/reply work for the same proposition:

D:
- policy examined work proxy: **6,197,914**;
- baseline: **8,105,879**;
- ratio: **0.7646196051**.

H:
- policy: **6,226,586**;
- baseline: **7,781,785**;
- ratio: **0.8001488090**.

This independent accounting reaches the same conclusion as wall time: semantic restriction saves work, but not enough to cross the <=0.75 strong-survival gate robustly.

## 4. Coverage-adjusted interpretation

The economic miss is more damaging because coverage is tiny:

- D: **0.48828125%**;
- H: **0.68359375%**.

The unrestricted baseline certifies exactly the same root counts: 5 and 7.

Therefore there is no evidence that paying the remaining baseline cost would reveal a materially larger local FERL-4 basin. The target is sparse under the frozen proposition.

## 5. Proof payload

Accepted producer witness-edge totals are extremely small:

- D: **13 witness edges** across five accepted roots;
- H: **7 witness edges** across seven accepted roots.

As an edge-work proxy against the exact baseline search:

- D: 13 / 8,105,879 = **0.0001603774%**;
- H: 7 / 7,781,785 = **0.0000899537%**.

This is strong evidence that **individual accepted FERL-4 certificates are compact**.

However, the frozen `PROOF_PAYLOAD_RATIO` was defined against complete exact baseline **state burden**, while the accepted instrumentation records proof witness edges and baseline examined-edge work rather than a canonical unique-state burden in the same unit.

Accordingly:

`PROOF_PAYLOAD_RATIO = NOT EXACTLY AVAILABLE IN THE FROZEN STATE-BURDEN UNIT`.

R5 does not launder the tiny edge proxy into the preregistered state-ratio metric. The strong survival gate receives no formal payload pass from this proxy.

## 6. Discovery versus certificate compression

R5 reproduces a pattern already visible historically:

- once an exact proof object exists, it can be very small;
- finding the object still requires substantial exact exploration.

FERL-4 therefore improves **certificate compactness** without demonstrating the required **discovery leverage**.

## 7. Resource budget

Accepted full producer run:

- peak RSS: **1,260,500 KiB** (~1.20 GiB);
- all individual D/H frontier/certification/baseline components completed inside their frozen 180 s budget.

The combined instrumented D+H run took 181 s overall, but the freeze specifies per-component budgets; no component exceeded 180 s.

The separate verifier also completed inside its 180 s target.

## 8. Economic conclusion

R5 does not pass the favorable-economics requirement:

- wall ratios fail <=0.75 on both D and H;
- exact-work proxy ratios also fail or marginally exceed the gate;
- compact proof payload does not compensate for negligible certified coverage;
- no material exact frontier is retired.

This is a **negative economic result**, not merely an unresolved measurement.
