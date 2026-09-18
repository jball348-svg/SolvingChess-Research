# Independent viability review

This directory is a frozen audit room for the Solving Chess research programme at the post-G14 snapshot. It is outside the numbered G lifecycle: it is not G15 and does not consume a programme number.

The review asks three questions:

1. Does the existing mathematics and exact computation support a defensible route from the standard initial position to a machine-checkable White-non-loss proof?
2. If the current G10-G42 roadmap is not defensible as written, is there enough genuine leverage to justify a reboot around a bridge-first mechanism?
3. If neither is true, should the current method stop while preserving its valid restricted results?

While `REVIEW/REVIEW_STATUS.json` is `OPEN`, do not start a new G programme or repair blockers merely to resume the old sequence unless the user explicitly overrides the hold.

## Start here

1. `REVIEW_SCOPE.md`
2. `CHESS_TRUTH_SNAPSHOT.md`
3. `CLAIM_INVENTORY.md`
4. `GLOBAL_PROOF_ARCHITECTURE.md`
5. `DEPENDENCY_GRAPH.md`
6. `COMPUTATIONAL_EVIDENCE.md`
7. `OPEN_OBLIGATIONS.md`
8. `AUDIT_ISSUES.md`
9. `REBOOT_CRITERIA.md`
10. `REVIEWER_GUIDE.md`
11. `SESSION_TEMPLATE.md`
12. `LEDGER.md`
13. `VERDICT.md`

## Review phases

- R0: reconstruct claims and provenance.
- R1: audit scaling and verification economics.
- R2: audit the endgame-to-middlegame bridge.
- R3: audit start reachability and all-reply closure.
- R4: construct and attack the strongest reboot candidate.
- R5: adversarial synthesis and verdict.

Allowed verdicts: `CONTINUE_CURRENT_ROADMAP`, `REBOOT`, `STOP_CURRENT_METHOD`, or `INCONCLUSIVE`.

A verdict about the current method is not a theorem about whether chess can be weakly solved by some future method.
