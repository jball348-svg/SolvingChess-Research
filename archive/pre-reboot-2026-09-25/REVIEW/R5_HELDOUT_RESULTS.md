# R5 Held-Out Results

**Session:** R5  
**Hostile family:** H — first White move by a knight from original b1/g1  
**Mechanism changes after D:** **none**  
**Frozen H coverage gate:** >=10%

## 1. Exact START_REACHABLE frontier

Under the unchanged R5 state model and six-literal one-phase White program, H reaches at ply 6:

- raw policy histories: **8,822,889**;
- unique exact full theorem states: **3,004,564**;
- board placements: **1,281,334**;
- `HISTORY_MULTIPLIER = 2.34487182889x`;
- maximum exact theorem states per board: **217**.

## 2. Frozen held-out cohort

The unchanged deterministic rule yields:

- cohort: **1,024**;
- forcing-contact stratum: **512**;
- quiet stratum: **512**;
- material range: **30–32 pieces**.

No target atom, strategy literal, guard, depth or cohort rule was changed after D.

## 3. Exact held-out certification

Direct FERL-4 targets:

**6 / 1,024 = 0.5859375%**

Total certified after the unchanged one-pair attraction:

**7 / 1,024 = 0.68359375%**

Therefore:

- `CERTIFIED_POLICY_COVERAGE = 0.68359375%`;
- `CERTIFICATION_RESIDUAL = 99.31640625%`.

The >=10% held-out coverage gate fails by a factor of about **14.63x**.

## 4. Transfer

The residual ratio is:

`99.31640625 / 99.51171875 = 0.9980372915x`.

Thus there is no adverse residual degradation from D to H. The exact target transfers unchanged and remains nonempty.

This is **transfer of a sparse mechanism**, not successful held-out survival.

## 5. Universal Black closure and replay

All legal Black replies are required by the accepted FERL-4 objects.

The separate replay verifier reproduced:

- direct target count: **6**;
- policy-certified count: **7**;
- unrestricted-baseline count: **7**.

No target-exactness violation or omitted Black reply was observed in accepted certificates.

## 6. Hostile work profile

Policy certification wall:

**27.599330099 s**

Recorded work:

- direct calls: 28,851;
- direct-cache hits: 9,704;
- attraction White candidates: 26,699;
- attraction Black replies: 26,803;
- first-cycle White candidates: 543,338;
- first-cycle Black replies: 403,524;
- repetition-barrier kills: **1,039,312**;
- second White candidates: 3,000,647;
- second Black replies: 2,225,575;
- exact repetition returns encountered: 31,249;
- exact draw branches: 26.

The hostile family therefore preserves exactness but exposes even more pressure from irreversible reply branches.

## 7. Competent unrestricted baseline

Allowing all legal White attraction moves certifies:

**7 / 1,024**

— again exactly the policy count.

The held-out failure is therefore not repaired by removing semantic White pruning inside the frozen local proposition.

## 8. Held-out conclusion

FERL-4 genuinely transfers unchanged across the knight-first family, but its density remains far below the required material bridge threshold.

R5 cannot classify transfer alone as survival when both D and H coverage gates fail by large margins.
