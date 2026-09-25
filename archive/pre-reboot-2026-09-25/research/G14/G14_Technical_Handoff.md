# G14 Technical Handoff

## Freeze identity and result

- Programme: `G14 - Proof Store and Content-Addressed Dependency Graph`
- Run ID: `G14-a01-d02c7f5da9fe`
- Authorized base commit: `ce50d28f552b91b0441e6eea701d87ac6501d512`
- Controller prompt SHA-256: `a74546731d81b829b63e01491bed789701404ec7a664efddd0b493de9fa79584`
- Close result: **PASS**
- Claim scope: engineering and preservation only
- Successor started: **no**

G14 satisfies its roadmap advance condition for the declared reference store: every
admitted proof object resolves its complete typed dependency closure by immutable identity
and reproduces the exact declared model from a portable offline bundle. This is not a new
chess result. The inherited mandatory G12-through-G13 acceptance replay remains
`NOT_PERFORMED`; G13's core engineering result remains PASS, its roadmap gate remains HOLD,
and G15/G17 remain blocked.

## Controlling authority and reconstructed inherited state

The permanent authority is
`roadmap/originals/G9_G10_Onwards_Long_Range_Plan.docx`, SHA-256
`2ccb06fad1d9cbe42631e40861f8982bffdeefe8c981ecda5b7c2f470fdd77b9`.
The predecessor authority is
`handoffs/originals/G13_Technical_Handoff.docx`, SHA-256
`34cc4caea8fdf9902bd04f14701660f5942c6f12ef3901d50164523330302194`.

The active inherited contracts remain distinct:

- `G10.RULES.v1.0`, controlled by the G10 handoff at
  `41267d308be04d79f078fbc3f41aa47add8d0a085bfe7b9cad1587edca7787be`;
- `G12.STATE.SERIAL.v2` and `G12.CLEAN-RANK-SAFETY`, controlled by the G12
  handoff at
  `958367f224467efc439217ac7a546249915e7a596717e8ad0c2131349e50eff3`;
- `G13.COMPUTE.CONTRACT.v1`, controlled by the G13 handoff above; its embedded
  compute-contract bytes hash to
  `030930d52931d8d9346d1feace8756a5edaf1a43495ed3b7a8991bb9146a8dc8`.

The exact recovered G10, G11, G12 and G13 bytes do not retroactively change historical
verdicts. The G10-to-G11 conformance replay remains not performed, historical G11 remains
HOLD, and `G12.STATE.SERIAL.v2` is not an alias for G10. G13 passed only its synthetic
engineering workload. These exceptions remain append-only historical facts.

No indexed external reference was materially required for G14. No
`NON_AUTHORITATIVE_REFERENCE` result was imported.

## Prospectively frozen acceptance

Before outcome inspection, G14 froze:

- contract `G14.PROOFSTORE.v1`, SHA-256
  `d0d36fd32cdc7470642c4f91a4f894891cad9e5c4291fb5348fa2be0da729825`;
- acceptance set `G14.ACCEPTANCE.v1`, SHA-256
  `3bc06d60462044169cd396433ee174bf1d2a365f850de14bb51d83aa46fedcd5`;
- 14 mandatory positive checks;
- 30 mandatory hostile mutations, all required to be rejected;
- zero accepted failures or unexplained mismatches;
- a 300-second whole-campaign bound and offline/no-network execution.

The acceptance document permits implementation corrections only if they are recorded and
the complete campaign is rerun from empty stores. The acceptance criteria and contract
were not weakened or rewritten after outcome inspection. Producer and verifier sources
were finalized after hostile review, then hash-pinned in the executed campaign and frozen
by the closeout inventory.

## Frozen design

### Identity layers

G14 separates identities that must not be conflated:

1. Raw bytes use a SHA-256 content address and exact byte length.
2. `MODEL` and `ARENA` records identify declared semantics and problem domain.
3. `SOLUTION_CORE` identifies model, arena, source set, truth, certificate and immutable
   solution dependencies; it deliberately contains no partition/worker plan.
4. `ATTESTATION` records bind execution plans, checkpoints, merge/verification evidence
   and gate status to a solution core.
5. `CATALOG` and `RELEASE` records pin an active snapshot without mutating older objects.

This makes the five G13 4/4/7/11/13-partition plans five distinct attestations over one
solution-core identity rather than five competing proof identities.

### G13 semantic boundary

The imported G13 workload is exactly the 65,536-state synthetic engineering fixture:

- semantic profile: `G13.TEST.SEMANTICS.v1`;
- rules profile: `engineering-reference-only-not-chess`;
- serialization profile: `component:u32,node:u16,outcome:u8,rank:u16`;
- problem SHA-256:
  `08f4960faf6b2d5e4d0a93c620373566226dea436318a6da3b5e2022656c9a0d`;
- producer SHA-256:
  `251989338b314ab3804b4fdf8f7a1fd7a90bcbd1e3a576708ea16588dc1feb00`;
- truth SHA-256:
  `00dde19eddcdf236cad2ce5fbfe115c1951d84b52e7224d230095c904bd03d85`;
- certificate SHA-256:
  `5594391149c4464d63811741d90969d1bbe5bbc43a20c39a2e47eb30eb687da7`.

`G10.RULES.v1.0` and `G12.STATE.SERIAL.v2` are inherited authority context only. They
are not relabelled as the solved semantics of this fixture. The lossless G13 projection
maps semantic rules to `model.rules_profile`, state serialization to
`model.serialization_profile`, problem/truth/certificate/source identities to immutable
object references, dependency hashes to the present-empty solution dependency list, and
execution/gate fields to attestations.

### Dependency, lineage and retention rules

- Typed references carry algorithm, digest, size and expected kind.
- Canonical JSON is NFC, integer-only, sorted-key compact UTF-8 with one LF; duplicate
  keys, floats and noncanonical bytes are rejected.
- Proof local edges must exactly equal the dependency edges of referenced solution cores.
- Supersession and withdrawal are append-only, non-retroactive lineage events.
- Active resolution is by a pinned catalog snapshot. Historical releases remain valid
  under their earlier snapshots; later catalogs may not reuse superseded or withdrawn
  targets.
- Every admitted release closure, including shared and superseded lineage subjects, is
  retained. G14's GC implementation is dry-run only and performs zero deletion.
- CAS publication uses an atomic no-clobber hard-link after fsync, followed by exact-byte
  comparison if another writer wins the address.

### Portable format

The portable format is a deterministic `ZIP_STORED` closure with fixed 1980 timestamp,
regular-file mode 0644, safe ordered POSIX member paths, exact inventory, exact rooted
typed closure, frozen contract binding and fixed resource limits. Export validates the
completed temporary ZIP with the same offline inspector used by importers before atomic
publication. Import validates completely into staging and publishes no partial root on
failure.

## Execution results

The final campaign produced:

- bundle SHA-256
  `2b2a80269211e8b87bfd2b076f79ffe7f41b4582acf0dfeaf6865fd267b96269`;
- bundle size 2,390,623 bytes;
- 75 inventoried objects: 41 raw and 34 typed records;
- 222 typed edges and two roots;
- 14/14 mandatory positive checks PASS;
- 30/30 prospectively frozen hostile mutations rejected;
- 10/10 structurally separate verifier checks PASS;
- 17/17 additional regression tests PASS;
- exact G13 independent replay over 65,536 synthetic states with zero Bellman/index and
  truth/certificate mismatch;
- two complete fresh-store campaign runs with byte-identical bundle and three ledgers;
- a separate fresh verifier process that reproduced the frozen independent ledger
  byte-for-byte.

The structurally separate verifier imports no producer, store or campaign module. It
recomputes ZIP/CAS identities, record shapes, typed closure, proof DAG obligations,
catalog/lineage/retention rules, the nine-field G13 projection, claim boundaries and GC
closure.

## Development failures and hostile-review corrections

The following pre-PASS failures are preserved; neither was averaged away or converted
into evidence:

1. Development campaign run 1 stopped before publication because catalog entries were
   not in canonical order.
2. Development campaign run 2 reached the independent verifier, which rejected the
   bundle because three acceptance-bound raw authorities were inserted into transient CAS
   storage but omitted from the portable release closure.

Independent hostile review then found and caused correction of: optional-empty open
exceptions; incomplete GC protection; synthetic reachability promotion; unchecked G13
mapping targets; non-resolving inspector behavior; incomplete ZIP metadata checks;
unbound acceptance/verifier execution; wrong fresh-run evidence mapping; partial output
publication; iterable-root consumption; a concurrent CAS overwrite race; globally
retroactive supersession semantics; duplicate-root publication; proof/solution edge
disagreement; active withdrawn targets; and absent whole-run resource enforcement.
All affected code was rerun from empty stores after correction.

Post-run independent review then found one further counterexample: the verifier rejected
direct inactive catalog targets but initially failed to reject a superseded solution hidden
as an added node inside a catalog-active proof. The producer correctly rejected it. PASS
was paused, the verifier was hardened to traverse each active proof/solution dependency
graph under its pinned lineage snapshot, the counterexample then failed with
`CATALOG_INACTIVE_ACTIVE`, historical catalogs excluding the later event still passed,
and the complete campaign was rerun twice from empty stores.

Two test-harness errors were also preserved during validation: an initial package-style
`unittest` invocation could not resolve the sibling module, and one regression constant
initially named the G13 baseline-status hash instead of the fresh-reproduction hash. The
direct script invocation and corrected exact frozen hash then passed all 17 tests. These
were harness errors, not accepted scientific mismatches.

## Negative results and retained limitations

### Frozen G12-through-G13 interface gap - BLOCKED

`G14_G13_G12_PreGate_Ledger.json` independently verifies both recovered archives, all
15 G12 and 22 G13 internal ledger entries, safe/unique paths, and the frozen adapter's
`READY` output. It also proves that `READY` means input-integrity readiness only:

- `g13_g12_adapter.py` validates archive members but does not construct or execute a G12
  workload;
- `g13_reference_campaign.py` is hard-wired to the synthetic 2,048-by-32 workload and has
  no bundle/adapter hook;
- the G12 producer/verifier exposes a whole-suite interface, not shard/checkpoint/resume;
- therefore no frozen command performs the mandated G12 kill/restart/repartition replay.

The current Windows environment also lacks Linux GCC/Clang/MinGW, WSL and containers;
the frozen G12 source uses `<bits/stdc++.h>` and its exact historical build was Linux GCC.
A Linux/GCC standalone replay could reproduce G12 bytes but still would not establish the
missing G13 distributed acceptance interface. A new explicitly versioned, governed
G12-specific G13 execution adapter/campaign is required. Frozen originals must not be
modified.

### Snapshot-status limitation - CONDITIONAL

`G14.PROOFSTORE.v1` deliberately freezes the current G13 HOLD/open-exception snapshot.
Its reference record vocabulary cannot truthfully encode a later successful G13 replay by
mutating these v1 records. A future status change must preserve this bundle and introduce
a new versioned contract/record schema, lineage event and release. G14 does not claim that
v1 alone represents every future status transition.

### Explicit non-claims

- No chess truth is newly proved or computed.
- No formal proof of SHA-256 collision resistance is claimed.
- No start-position reachability is claimed.
- No G10/G11/G12 pending conformance or acceptance replay is claimed performed.
- No G15 work, research output or authorization is created.
- No production-scale bulk CAS service, erasure coding, remote replication or automatic
  deletion is claimed.

## Claim ledger

| ID | Class | Domain and statement | Evidence |
|---|---|---|---|
| G14.C1 | ENGINEERING_TEST | The reference proof store satisfies all 14 frozen positive checks for its declared synthetic/preservation fixture. | `G14_Reference_Campaign_Ledger.json` |
| G14.C2 | ENGINEERING_TEST | All 30 prospectively declared hostile mutations were rejected. | `G14_Hostile_Mutation_Ledger.json` |
| G14.C3 | INDEPENDENTLY_REPLAYED | A structurally separate offline verifier passed all 10 obligations on the exact portable bundle, and a fresh process reproduced its ledger bytes. | `G14_Independent_Verification_Ledger.json` |
| G14.C4 | EXACT | The frozen bundle and ledger byte identities below were reproduced by a second complete empty-store run. | bundle and ledgers; `G14_SHA256SUMS.txt` |
| G14.C5 | ENGINEERING_TEST | Seventeen targeted regressions reject defects found during hostile review, including non-retroactive snapshot coexistence. | `test_g14_proof_store.py`; validation report |
| G14.C6 | BLOCKED | The mandatory exact G12-through-G13 acceptance replay has no executable path in the frozen G13 bundle and remains `NOT_PERFORMED`. | `G14_G13_G12_PreGate_Ledger.json` |
| G14.C7 | NOT_CLAIMED | The G13 fixture is not chess truth and no initial-position reachability or successor progress is claimed. | contract, acceptance, release claim boundary |

## Frozen artifact identities

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `G14_Proof_Store_Contract_v1.json` | 16,415 | `d0d36fd32cdc7470642c4f91a4f894891cad9e5c4291fb5348fa2be0da729825` |
| `G14_Prospective_Acceptance_v1.json` | 6,808 | `3bc06d60462044169cd396433ee174bf1d2a365f850de14bb51d83aa46fedcd5` |
| `g14_proof_store.py` | 57,145 | `fca4b222e356e5d7795005bfc51b921c5d862ca86026409189c496b201ebac9c` |
| `g14_reference_campaign.py` | 49,879 | `8175b046c00ee57106a36485c46803291e360a99347aaba104732bc316581f59` |
| `g14_independent_verifier.py` | 73,721 | `887eca1987c4c1c2f60147486a5e94313f38b61b9a35c52bf011411d0718d128` |
| `G14_Portable_Proof_Store_Bundle.zip` | 2,390,623 | `2b2a80269211e8b87bfd2b076f79ffe7f41b4582acf0dfeaf6865fd267b96269` |
| `G14_Reference_Campaign_Ledger.json` | 4,123 | `7a2b6c42223ebf7f6982ecaa0675f692cb7e001ab98ec5e1ae4d171b7e556bf9` |
| `G14_Hostile_Mutation_Ledger.json` | 6,014 | `8d3d7f0d177d1ba8bc3263cfa330efcd6a584d4c81b45c0e1e26b0f483a18aab` |
| `G14_Independent_Verification_Ledger.json` | 1,860 | `eb8296e54e4f708d2b85ab680cd031f17114dd061c7b278988518061d1823083` |
| `g14_g13_replay_pregate.py` | 21,561 | `33645426fb2dcd82078aad06a6fdc232f6b8c67746ab9c3178eab0a107872f23` |
| `G14_G13_G12_PreGate_Ledger.json` | 14,444 | `03bd9dcb7d45fc5ef9cc85ab5469d016c41e4e1863b7e60ddd4b128c00128e41` |

The checksum ledger also binds the README, regression source, handoff, validation report
and updated programme state. The freeze manifest intentionally does not self-hash.

## Replay and validation instructions

Use Python 3.12 or later; the G14 implementation is standard-library only. Commands are
relative to the repository root and require no network:

```powershell
python -B research/G14/g14_g13_replay_pregate.py --out research/G14/G14_G13_G12_PreGate_Ledger.json
python -B research/G14/g14_reference_campaign.py --output-dir research/G14 --work-parent .run/g14-campaign-work --verifier research/G14/g14_independent_verifier.py
python -B research/G14/test_g14_proof_store.py
python -B research/G14/g14_independent_verifier.py research/G14/G14_Portable_Proof_Store_Bundle.zip --ledger .run/G14_Independent_Replay.json --expected-contract-sha256 d0d36fd32cdc7470642c4f91a4f894891cad9e5c4291fb5348fa2be0da729825
python -B research/G14/g14_proof_store.py inspect-bundle research/G14/G14_Portable_Proof_Store_Bundle.zip
```

The final campaign must report 14 positives and 30 rejections. The regression script must
report 17 tests. The independent replay must report 10 checks, 75 objects and 34 records;
its output must hash to
`eb8296e54e4f708d2b85ab680cd031f17114dd061c7b278988518061d1823083`.

## Roadmap and successor contract

G14's own engineering/preservation gate passes. Its proof-store dependency is available
to future work, but this does not override the inherited G13 roadmap HOLD.

The only sequential successor candidate is
`G15 - Verifier Hardening and Formal Core`. It is **not authorized**, **not started**, and
must not be launched while `G13_MANDATORY_G12_REPLAY_OPEN` remains binding. G17 remains
blocked as well. A future controller may authorize G15 only after a governed resolution
updates programme state without rewriting this G14 snapshot. G15 must consume
`G14.PROOFSTORE.v1` read-only, preserve all claim boundaries, and require a new versioned
contract for any later replay-status transition.

This process stops here and creates no G15 research output.
