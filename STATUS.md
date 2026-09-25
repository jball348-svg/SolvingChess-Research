# Current pilot status

Updated: 2026-09-25.

**SETUP COMPLETE. PART 1 NOT STARTED.**

The previous tracked tree is archived without changes at
`archive/pre-reboot-2026-09-25/`. Its source commit is
`3eba1a0c60e8ffca63a85763d176e1da9f904141`.

| Part | State | Result |
|---|---|---|
| 1 — Benchmark and baseline | NOT_STARTED | No experimental protocol or new baseline yet. |
| 2 — Discover reusable proofs | NOT_STARTED | No pilot proof library yet. |
| 3 — Cumulative reuse | NOT_STARTED | No amortization or scaling measurements yet. |
| 4 — Transfer and connections | NOT_STARTED | No new connected strategy certificate yet. |
| 5 — Replay and decision | NOT_STARTED | No pilot viability conclusion yet. |

**Next action:** run only Part 1 using [its prompt](pilot/PART_1_PROMPT.md).
Its endpoint is a reproducible baseline, a frozen feasible experiment and a clear
readiness result. It must not run the decisive Part 2–4 campaigns.

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
