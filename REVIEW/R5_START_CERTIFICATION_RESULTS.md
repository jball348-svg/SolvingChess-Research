# R5 Start Certification Results

**Session:** R5  
**Discovery family:** D — king-pawn first move `e2-e3` or `e2-e4`  
**Frozen target:** FERL-4  
**Coverage gate:** >=20%  
**Observed result:** **5 / 1,024 = 0.48828125%**

## 1. Exact START_REACHABLE frontier

The frozen one-phase six-literal White program was generated from the real standard initial position through ply 6 under exact theorem-state identity.

D produced:

- raw policy histories at ply 6: **9,547,374**;
- unique exact full theorem states: **3,903,222**;
- distinct board placements: **1,556,742**;
- full-state / board `HISTORY_MULTIPLIER = 2.50730178796x`;
- maximum exact theorem states sharing one board placement: **264**.

Every admitted state has an explicit legal path from the standard initial position.

## 2. Frozen cohort

The prospectively declared cohort contains:

- **1,024** exact White-to-move theorem states;
- **512** with `FORCING_MOVE_AVAILABLE=true`;
- **512** quiet;
- material range **30–32 pieces**.

Selection used canonical full-state identity only and no outcome labels.

## 3. Direct and attracted certification

Direct FERL-4 membership:

- **1 / 1,024 = 0.09765625%**.

After the frozen one White/Black attraction pair:

- exact certified roots: **5 / 1,024**;
- `CERTIFIED_POLICY_COVERAGE = 0.48828125%`;
- `CERTIFICATION_RESIDUAL = 99.51171875%`.

This is nonzero exact proof coverage, unlike R4's 0 / 1,024 result, but it misses the frozen >=20% discovery survival threshold by a factor of about **40.96x**.

## 4. Universal Black closure

For each of the five accepted roots:

- White existence is restricted by the frozen semantic program;
- every legal Black reply at a certified Black node is represented;
- each branch either reaches an exact draw or satisfies the FERL-4 exact return theorem.

The separate replay verifier reproduced the same five roots in aggregate count.

`CERTIFIED_BLACK_CLOSURE = 100%` for the accepted proof objects.

## 5. Exact search work

Policy certification wall:

**27.789252083 s**

Recorded policy work:

- direct target calls: 29,274;
- direct-cache hits: 11,438;
- attraction White candidates: 27,165;
- attraction Black replies: 27,226;
- first-cycle White candidates: 443,602;
- first-cycle Black replies: 315,027;
- repetition-barrier kills: 718,197;
- second White candidates: 3,093,251;
- second Black replies: 2,291,643;
- exact repetition returns encountered: 69,356;
- exact draw branches: 166.

A compact target certificate may exist once found, but finding accepted roots remains an exact multi-million-edge computation.

## 6. Competent unrestricted-White baseline

The same proposition was solved on the same 1,024 roots with all legal White attraction moves admitted.

Baseline certified:

**5 / 1,024** — exactly the same number as the semantic policy.

Thus the tiny coverage is not explained by the semantic policy accidentally excluding a large population of nearby FERL-4 entries. Under the frozen one-pair proposition, the target itself is sparse.

## 7. Truth leakage and exceptions

- complete outcome-labelled truth used before freeze: **0**;
- `LOCAL_TRUTH_LEAKAGE = 0%`;
- engine evaluation: **none**;
- square/state-ID exceptions: **none**;
- absolute opening-line exceptions: **none**;
- post-inspection target repair: **none**.

## 8. Discovery conclusion

D establishes a real high-material exact target but **not a material start-side bridge**.

The named survival gate fails on coverage before any favorable payload claim can rescue the candidate.
