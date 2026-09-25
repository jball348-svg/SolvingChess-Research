# RP3-MR1 final recovery rerun

The first RP3-MR1 measurement attempt completed its child processes, but seven
durability checks found that the on-disk report had reverted to a pre-final
checkpoint while the completion marker described a complete report.  Those
records remain preserved as `attempt-1`; their expense is included in the
recovery accounting and none of their measurements is used as a conclusion.

This final rerun keeps the approved amendment unchanged: the original blocked
R2 record remains blocked, the R1 prefix is unchanged, R2 is a balanced
four-arm three-repetition replacement block using the frozen 8-object F and
16-object G libraries, and R3/R4 use the prescribed primary, ablation and
reverse-order schedule.  The R2-trained libraries are frozen before R3, the
new R3 C/G acquisitions are frozen before R4, and there is no acquisition after
R4.

The rerun changes persistence only.  Each JSON generation uses a unique
temporary file, fsyncs the file and containing directory, atomically replaces
the destination, and reads the destination back before returning.  The final
report is emitted again after the frozen RP2 finish returns; a completion
manifest is written only after two complete validations.  `validate()` checks
row order and completeness, search-counter conservation, certificate hashes,
event-tail counts, the append-only row journal, and the completion digests.

All first-attempt directories are retained in the compact `attempt-1` archive.
The final rerun is stored separately under `pilot/evidence/rp3-recovery-v2/`;
its compact archive and validation manifest are the authoritative RP3-MR1
measurement record.  Original expense, first-attempt expense and final-rerun
expense are reported separately and together.  Missing original counters are
still unavailable; final-rerun counters do not repair the blocked report.

The fixed replay command is:

```text
PYTHONPATH=pilot/src:<pinned-site-packages> python pilot/src/rp3_recovery_campaign_v2.py run --output pilot/evidence/rp3-recovery-v2 --commit <published-source-commit>
```

The campaign is bounded to the RP3 schedule and stops after the R4 controls.
Held-out counterplay/history cohorts, RP4, RP5 and any archived-programme
restart remain outside this amendment.
