# R4 Certification Economics

**Session:** R4

## 1. Accounting boundary

R4 compares:

- prospective start-frontier generation, deterministic cohort selection and exact policy certification; versus
- complete bounded all-White target-reachability truth on the identical cohort, target grammar and depth.

The baseline proposition is exact but local: “Can White force one of the frozen exact non-loss targets within five remaining plies?” It is not complete-chess W/D/L.

## 2. Policy-side cost

Accepted R4 policy runs:

| branch | work | result | elapsed process wall | peak RSS |
|---|---|---:|---:|---:|
| D | frontier + cohort + prospective depths 1/3/5 | 0/1,024 certified | **3.56 s** | **140,972 KiB (~137.7 MiB)** |
| H | frontier + cohort + unchanged depth 5 | 0/1,024 certified | **9.09 s** | **389,824 KiB (~380.7 MiB)** |

The inner depth-5 certification solver itself used:

- D: 17,872 memo configurations / 18,013 explored edges / 0.4263 s;
- H: 9,459 memo configurations / 9,441 explored edges / 0.2920 s.

These costs are small because failing branches can be rejected early.

## 3. Complete bounded all-White baseline

The frozen baseline allows every legal White move and universal Black replies, with the same exact full-state identity, targets, cohort and depth.

Both baselines fail the frozen 2 GiB memory budget before producing complete bounded truth.

### D

Hard virtual-memory cap: 2 GiB.

- outcome: **std::bad_alloc**, exit 134 / signal 6;
- elapsed: **69.06 s**;
- peak RSS reported: **2,081,320 KiB**;
- complete bounded truth: **not acquired**.

### H

Hard virtual-memory cap: 2 GiB.

- outcome: **std::bad_alloc**, exit 134 / signal 6;
- elapsed: **71.58 s**;
- peak RSS reported: **2,024,280 KiB**;
- complete bounded truth: **not acquired**.

A prior uncapped D attempt was terminated once RSS visibly exceeded the declared budget; it is not used as the accepted baseline result.

## 4. Certification-cost ratio

Because the denominator did not complete, an exact `CERTIFICATION_COST_RATIO` cannot be reported.

Using time-to-budget-failure only gives upper bounds:

- D: complete-baseline cost >69.06 s, so 3.56 / complete cost **< 0.0516**;
- H: complete-baseline cost >71.58 s, so 9.09 / complete cost **< 0.1270**.

These bounds are **not positive reboot evidence**. The policy computation is cheap because it certifies zero states. A low cost for an empty proof object is not proof leverage.

## 5. Proof payload

Accepted R4 non-loss proof objects: **0**.

Therefore a numerical proof-payload/full-truth ratio would be vacuous. R4 explicitly does **not** score an empty proof payload as satisfying the <=25% payload gate.

## 6. Economic interpretation

R4 exposes a two-sided problem:

1. complete bounded local target truth with unrestricted White choices already exceeds the declared memory budget;
2. the cheap semantic policy avoids that cost but reaches no exact target and certifies nothing.

This is stronger negative evidence than a simple “solver too expensive” result. It shows that the R3 branching advantage does not automatically buy useful exact truth.

The architecture needs an exact intermediate target that is both reachable under compressed policy and cheaper to certify than raw local minimax. R4 did not find one inside its frozen grammar.
