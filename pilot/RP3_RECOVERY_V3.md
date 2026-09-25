# RP3-MR1 immutable-generation rerun

The second recovery attempt is preserved as `attempt-2`; four records failed the
post-run completeness audit even though their child envelopes exited cleanly.
Its 72-process expense is retained and excluded from the decisive comparison.

The final rerun changes persistence only. Query checkpoints are written as
immutable generation files. At completion, one final report is written, read
back, and hard-linked to `report.json`; validation also checks the final link and
completion digests. The RP3 solver, cohorts, arm order, libraries, budgets,
controls, repetitions and accounting gates remain unchanged. This is the last
RP3 recovery attempt; after R4 no acquisition or later pilot stage is run.
