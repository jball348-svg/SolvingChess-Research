# Current pilot status

Updated: 2026-09-25.

**RP2 COMPLETE — BOUNDED_POSITIVE_ACQUISITION; NO_R1_COST_ADVANTAGE.**

The previous tracked tree is archived without changes at
`archive/pre-reboot-2026-09-25/`. Its source commit is
`3eba1a0c60e8ffca63a85763d176e1da9f904141`.

| Part | State | Result |
|---|---|---|
| 1 — Benchmark and baseline | COMPLETE | Reference reproduced; exact baseline/checker usable; protocol v1 frozen. |
| 2 — Discover reusable proofs | COMPLETE | Eight exact donor objects; one internal R1 application; 16/16 checked in every arm; no first-use advantage. |
| 3 — Cumulative reuse | NOT_STARTED | No amortization or scaling measurements yet. |
| 4 — Transfer and connections | NOT_STARTED | No new connected strategy certificate yet. |
| 5 — Replay and decision | NOT_STARTED | No pilot viability conclusion yet. |

**Next action, only when requested:** execute RP3 under the unchanged protocol.
Reuse RP2's R1 measurements as the first prefix. Acquire from the separate R1
training cohort for G/C before R2, then follow the frozen R2–R4 schedule and
R3/R4 ablation/order checks. Carry the donor acquisition and all R1 costs in
`pilot/evidence/rp2/summary.json` forward; shared setup is charged once. Do not
regenerate R1 as unseen evidence. RP3–RP5 remain unstarted.

**RP2 result:** [consolidated results, limitations and exact commands](pilot/RESULTS.md#rp2-complete--bounded-positive-acquisition-no-r1-cost-advantage).
All arms checked 16/16 R1 queries (five true, eleven false), with no unknowns or
timeouts. Eight short, single-branch geometry objects were acquired reproducibly.
One transferred proof discharged an internal negative-query search obligation,
but contributed to no final R1 root certificate. F/G saved only two of 915
fallback expansions and failed every practical cost-advantage gate.

Median first-use CPU seconds, including donor construction and R1 but before
shared environment setup: B 0.795, C 2.582, F 1.318, G 1.261. All setup, failed
applications, candidate attempts and repetition costs are retained. This bounded
positive acquisition result establishes neither useful scaling nor cumulative
benefit. F/G have identical donor knowledge at this stage.

**Published donor/source freeze:**
[`2736e3cf00e0696520c3d8fe1203f28087ed3db6`](https://github.com/jball348-svg/SolvingChess-Research/commit/2736e3cf00e0696520c3d8fe1203f28087ed3db6),
verified on the remote before R1 generation. The [manifest](pilot/evidence/rp2/donor-freeze.json),
actual objects, donor/evaluation certificates and raw ledgers are preserved.
No R1 training, R2–R4 evaluation, held-out counterplay/history work or old conveyor
was run. The active protocol, original source manifest and archive are unchanged.

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
