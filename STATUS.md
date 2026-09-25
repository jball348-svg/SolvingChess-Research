# Current pilot status

Updated: 2026-09-25.

**RP3 BLOCKED — ORIGINAL_MEASUREMENT_LEDGER_LOSS.**

| Part | State | Result |
|---|---|---|
| 1 — Benchmark and baseline | COMPLETE | Exact baseline/checker and protocol v1 frozen. |
| 2 — Discover reusable proofs | COMPLETE | Eight donor objects; complete R1 coverage; no first-use cost advantage. |
| 3 — Cumulative reuse | BLOCKED | 24 processes through R2 training preserved; one R2 evaluation ledger is incomplete. R3/R4 and controls unrun. |
| 4 — Transfer and connections | NOT_STARTED | No held-out cohort or anchor generated. |
| 5 — Replay and decision | NOT_STARTED | No final pilot decision. |

**Blocker:** `pilot/evidence/rp3/evaluate-r2-primary-3-F/report.json` retains only
14 of 16 per-query measurement rows and lacks final search counters. Its
application log also ends early. All sixteen certificates and the complete
original process envelope survive, but they cannot recover the lost measurements.
No cost or work was filled in from another repeat and no primary run was replaced.
A separate acquisition checkpoint was reconstructed from original surviving
ledgers, with missing subphase measurements explicitly unavailable.

**Preserved result:** G grew 8 → 16 → 24 objects through donor/R1/R2 training.
R2 used sixteen objects and all arms checked 16/16 queries (six true, ten false).
Complete first-repeat ledgers show twelve internal G applications, with four
objects contributing to four final root certificates. This does not establish
compounding. Median cumulative CPU through R1/R2: B 0.795/2.867 seconds,
C 2.582/39.191, F 1.318/3.589, G 1.261/4.662, before the unchanged shared setup.
No observed break-even. R3/R4 economics, ablation and order controls are unavailable.

**Next action:** recover an authentic copy of the missing original measurement
and event tail, or explicitly specify a labelled replacement comparison retaining
all original costs. Then finish RP3. Do not silently replay and substitute a
primary run. RP4 is not ready: its frozen-library counterplay/history and local
anchor tests await a sound RP3 endpoint and a request to execute RP4.

[Consolidated RP3 findings, failure evidence and exact reconciliation commands](pilot/RESULTS.md#rp3--blocked-incomplete-original-measurement-ledgers-2026-09-25).
[Compact raw evidence](pilot/evidence/rp3/raw-evidence.tar.gz) and
[full cost carry-forward](pilot/evidence/rp3/summary.json).
Run `python pilot/src/rp3_unpack.py` to verify/materialize the original paths.

**Published RP3 source freeze:**
`35d409bf67198340446bd7021c95e8c1dc1f5cfc` (before any R1 training).
**RP2 publication:** `984b427eb4054c7eb11968b4f871a1e4f73d5836`.
**RP2 donor freeze:** `2736e3cf00e0696520c3d8fe1203f28087ed3db6`.
**RP1 protocol/source freeze:** `ccf3a1c18ac9f92250bb94576a9d3f010fab80f3`.
All frozen experimental source and inherited RP2 evidence remain unchanged.

The previous tracked programme is archived unchanged under
`archive/pre-reboot-2026-09-25/`, source commit
`3eba1a0c60e8ffca63a85763d176e1da9f904141`. Archived instructions do not govern
the pilot. The original source availability limitations and reproduced G12
reference remain in the consolidated results. No old conveyor was restarted.
