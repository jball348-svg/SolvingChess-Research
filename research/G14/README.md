# G14 - Proof Store and Content-Addressed Dependency Graph

G14 closed with an engineering/preservation PASS. Its content-addressed reference store
resolves typed immutable dependencies, retains superseded bytes, separates model and
solution identity from execution attestations, and exports a deterministic portable
closure for offline verification.

The result is deliberately bounded:

- the G13 fixture remains `G13.TEST.SEMANTICS.v1`, an `ENGINEERING_TEST`, not chess;
- G10 and G12 remain inherited authority context, not the fixture's solved model;
- no initial-position reachability or new chess truth is claimed;
- the exact G12-through-G13 kill/restart/repartition replay remains `NOT_PERFORMED`;
- G15 and G17 remain blocked by that inherited G13 gate.

Primary artifacts:

- `G14_Proof_Store_Contract_v1.json` - frozen storage, identity, lineage and bundle contract;
- `G14_Prospective_Acceptance_v1.json` - pre-outcome 14-positive/30-hostile acceptance set;
- `g14_proof_store.py` - standard-library producer/importer reference implementation;
- `g14_independent_verifier.py` - structurally separate offline verifier;
- `g14_reference_campaign.py` - deterministic producer, replay and hostile campaign;
- `test_g14_proof_store.py` - regression tests for defects found during hostile review;
- `G14_Portable_Proof_Store_Bundle.zip` - deterministic, self-contained portable closure;
- `G14_Reference_Campaign_Ledger.json` - positive campaign ledger;
- `G14_Hostile_Mutation_Ledger.json` - hostile mutation ledger;
- `G14_Independent_Verification_Ledger.json` - independent offline verification ledger;
- `G14_G13_G12_PreGate_Ledger.json` - inherited replay pre-gate diagnostic;
- `G14_Technical_Handoff.md` and `G14_Freeze_Manifest.json` - closeout authorities.

Replay commands and exact interpretation are frozen in `G14_Technical_Handoff.md`.
