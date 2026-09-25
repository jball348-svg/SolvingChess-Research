# Current pilot status

Updated: 2026-09-25.

**RP2 IN_PROGRESS — DONOR_FREEZE_READY.**

The previous tracked tree is archived without changes at
`archive/pre-reboot-2026-09-25/`. Its source commit is
`3eba1a0c60e8ffca63a85763d176e1da9f904141`.

| Part | State | Result |
|---|---|---|
| 1 — Benchmark and baseline | COMPLETE | Reference reproduced; exact baseline/checker usable; protocol v1 frozen. |
| 2 — Discover reusable proofs | IN_PROGRESS | Eight donor proof geometries acquired reproducibly; R1 not yet generated or evaluated. |
| 3 — Cumulative reuse | NOT_STARTED | No amortization or scaling measurements yet. |
| 4 — Transfer and connections | NOT_STARTED | No new connected strategy certificate yet. |
| 5 — Replay and decision | NOT_STARTED | No pilot viability conclusion yet. |

**Next action:** publish the donor freeze in `pilot/evidence/rp2/donor-freeze.json`,
then execute only the 16 reserved R1 test queries with the already recorded
measurement driver. This is the authorized continuation of RP2. No R1 training,
R2–R4 evaluation, compounding or held-out transfer has run.

**RP2 donor evidence:** [consolidated record](pilot/RESULTS.md#rp2--donor-acquisition-and-freeze-2026-09-25).
The nine acquisition runs reproduce all 24 checked donor certificates; F/G's
six runs reproduce the same eight geometries and 7,628-byte library. C's three
runs reproduce a 357-entry, 685,523-byte geometry cache. R1 remains unopened.

**RP1 evidence:** [consolidated results and replay commands](pilot/RESULTS.md).
G12's producer/verifier reproduced seven frozen artifacts; the verifier checked
809,183 table states with zero mismatches. The new bounded baseline agrees with
the full development-arena reference on all eight smoke queries, and fourteen
targeted controls pass. This is readiness, not a new discovery/scaling success.

**Protocol freeze:**
[`ccf3a1c18ac9f92250bb94576a9d3f010fab80f3`](https://github.com/jball348-svg/SolvingChess-Research/commit/ccf3a1c18ac9f92250bb94576a9d3f010fab80f3).
The follow-up status record does not change protocol or executable source.

**Current evidence:** the [post-mortem](archive/POST_MORTEM_2026-09-24.md) and
[archive guide](archive/README.md). Historical positives and limitations are
inputs for experiment design, not pilot successes.

**Known availability risk:** the archived late-review R2/R4/R5 provenance records
source hashes for programs not found in the inspected tracked files or bundled
archives. Part 1 must not depend on those source bytes being present. The G12
reference bundle does contain source and certificates and was replayed during
the post-mortem.

After each part, update this file in place with its bounded conclusion, links to
the consolidated results and the next action. Keep experiment measurements in
`pilot/`, not duplicated here.
