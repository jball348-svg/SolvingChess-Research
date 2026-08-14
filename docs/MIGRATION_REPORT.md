# Migration report

**Document status:** completed migration evidence; final Git binding is supplied by the
bootstrap freeze

**Generated:** 2026-08-13T00:00:00Z

**Migration tool/version:** solving-chess immutable corpus migration 1.0.0, with
solving-chess-stdlib-ooxml-to-markdown 1.0.0

**Source root:** the verified 129-file flat staging set at C:\Solving_Chess

**Destination commit:** assigned by the final bootstrap content freeze; the byte identities
below do not depend on that Git identifier

This report is derived from state/ARTIFACT_REGISTRY.json, the per-document conversion
audits and independent post-relocation checks. File movement has no scientific effect.

## Outcome

- Migration result: PASS
- Original source occurrences inventoried: 129
- Unique content identities: 124
- Original bytes copied without transformation: 59,994,517 across all 129 occurrences
- Archive members inventoried without exploding the archives: 334
- Artifact registry SHA-256:
  482199338b76d8c3e0a67f162cfb7324e0b7186508cfdc929651dd1f21cf476c
- Normalized human derivatives produced: 29 Markdown files, each with a conversion audit
- Document-conversion exceptions: all 29 are
  LOSS_AUDITED_WITH_LIMITATIONS; no unsupported body element was observed
- Missing expected artifacts: 63 checksum references were expected-only in the supplied
  historical input; none is reported as corruption or as a newly lost migration byte
- Exact recovered artifacts: the required G10, G11 and G12 bundles are present at their
  frozen expected SHA-256 identities

## Authority placement

| Authority class | Original destination | Normalized destination | Identity status |
|---|---|---|---|
| G9 permanent roadmap | roadmap/originals/G9_G10_Onwards_Long_Range_Plan.docx | roadmap/normalized/G9_G10_Onwards_Long_Range_Plan.md | Original and derivative hashes verified |
| Technical handoffs | handoffs/originals (14 occurrences) | handoffs/normalized (14 derivatives) | Original occurrences and derivative provenance verified |
| Other inherited primary files | legacy/originals (111 occurrences) | legacy/normalized (11 DOCX derivatives; native machine/archive files not normalized) | Original occurrences and applicable derivative provenance verified |

The recovered G12 reference bundle is retained only at
legacy/originals/G12_Final_Rules_Reference_Bundle.zip. It is not duplicated under
artifacts/bundles.

## Duplicate and naming policy

The registry preserves five identical-byte duplicate groups as ten distinct source
occurrences. They are the paired names for the G4 technical handoff, G5 kickoff memo, G5
technical handoff, G6 interim certificate bundle A and G6 kickoff memo. Parenthesized
`(1)` names are retained, so no outcome-dependent disambiguation or overwrite occurred.

Archives remain immutable outer objects. Their 334 members are separately inventoried for
inspection and checksum resolution but are not extracted into authoritative repository
paths. JSON, checksum, source, archive and binary files are intentionally not normalized.

## DOCX normalization

Every derivative audit binds the original path, size and SHA-256; derivative path, size and
SHA-256; conversion method, tool version and timestamp; visible-text sequence identity;
structure statistics; and the controlling-original/non-authoritative-derivative boundary.

Across the 29 conversions, the recorded documentary losses are:

- 43 header/footer text occurrences retained in audit metadata but not repeated in body
  Markdown, across 27 documents;
- 5,331 character-run formatting simplifications across all 29 documents.

The audits report zero pictures, drawings, math objects, content controls, tracked changes,
nested tables, merged cells or unsupported body elements. The immutable DOCX remains
controlling wherever presentation or structure differs.

## Recovered historical bundles

### G10 semantics bundle

- Expected SHA-256:
  a0c5c2df8f8f61d8f6365ae8750491e3d64df821d060f9d24edb6ad9342b0793
- Observed SHA-256:
  a0c5c2df8f8f61d8f6365ae8750491e3d64df821d060f9d24edb6ad9342b0793
- Current bytes status: RECOVERED_EXACT_BYTES
- Integrity status: VERIFIED
- Required original conformance replay: NOT_PERFORMED
- Historical G11 verdict: remains HOLD as frozen

### G11 conformance bundle

- Expected SHA-256:
  874c69b11d6e2d1aa5d4f5de96c3ef96a8e9307c49cd5f53e7b5c4a3849aab5c
- Observed SHA-256:
  874c69b11d6e2d1aa5d4f5de96c3ef96a8e9307c49cd5f53e7b5c4a3849aab5c
- Current bytes status: RECOVERED_EXACT_BYTES
- Integrity status: VERIFIED
- Replay implication: recovery does not retroactively rewrite G11

### G12 final rules reference bundle

- Expected SHA-256:
  7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c
- Observed SHA-256:
  7641e0f8a4e621efb90b75cd3ce99b44e96c07a2f3541114611126a076d5695c
- Canonical path: legacy/originals/G12_Final_Rules_Reference_Bundle.zip
- Current bytes status: RECOVERED_EXACT_BYTES
- Integrity status: VERIFIED
- Mandatory G13 acceptance replay: NOT_PERFORMED
- G13 core engineering result: PASS
- G13 roadmap gate: HOLD

Byte recovery and archive inspection are not the pending scientific/acceptance replays.

## Reference projects

| Project | Identity | Storage | Authority | Status |
|---|---|---|---|---|
| Decision Coordinates | eadf71ef1d0562b18124959c63b4a8a2613c6c4c | pinned submodule | NON_AUTHORITATIVE_REFERENCE | Reproducible |
| Structural Invariants in Chess Endgames | manifest 5b62101a73bfa85277f7246ee2b304921921828e2f0b1bb50d618d917512a1ca over base ade9f4e51ed3048e915386d82e0b53d28ed7e3ab | ignored local-private snapshot plus tracked manifest | NON_AUTHORITATIVE_REFERENCE | Exact local snapshot materialized; durable private hosting and licensing unresolved |
| jball348-svg/SolvingChess | 1861f4a8ea4978b1599a042809f9f7cd53345151 | pinned submodule | NON_AUTHORITATIVE_REFERENCE | Reproducible |

The structural per-file manifest covers 138 files and 262,213,060 bytes. Its deterministic
local-private ZIP is 52,608,393 bytes with SHA-256
71ed9950df89c9d61e04c08895c28596c7c1964cb3615478008061b15bfc5be3.
The unlicensed tree and ZIP are ignored and must not enter main Git.
The complete reference registry SHA-256 is
6507a501831c7498c8cadb2c2afb68627668feafbe64d36e67a8b0eb23142fe1.

## Validation

The migration application command was:

```powershell
python scripts/migration/migrate_corpus.py --apply --finalize-relocation
```

Post-relocation acceptance checked:

- all 129 registry occurrences exist at their declared repository paths with exact size
  and SHA-256;
- placement cardinalities are exactly 4 roadmap, 14 handoff and 111 legacy originals;
- all 29 derivatives and audits exist and match their registered hashes;
- 192 outer checksum references resolve as 129 exact and 63 expected-only, with zero
  mismatches;
- 11 internal archive checksum manifests contain 152 references, all 152 exact;
- the G12 target bundle occurs exactly once;
- all 334 archive-member identities validate;
- both pinned submodule commits and the structural private-snapshot identities match;
- no G14 handoff, freeze manifest or scientific output exists.

The independent acceptance audit reported zero errors. Final bootstrap acceptance reruns
the repository validator and full test suite before creating the immutable Git tag.

## Exceptions and residual work

- The 63 expected-only historical checksum targets were absent from the supplied migration
  input. They remain explicit registry records and are not silently treated as recovered.
- DOCX character formatting and header/footer placement have the audited limitations above.
- The structural snapshot lacks project-wide redistribution authority and durable private
  hosting.
- Required G10/G11 conformance and G12-through-G13 acceptance replays remain NOT_PERFORMED.
- The final bootstrap commit/tag identity is supplied after this content is accepted.

## Claim boundary

- No G14 research was performed.
- No G14 handoff or freeze was created.
- No new chess truth was claimed.
- Historical PASS/HOLD/BLOCKED wording was preserved.
- G14 remains started=false.
