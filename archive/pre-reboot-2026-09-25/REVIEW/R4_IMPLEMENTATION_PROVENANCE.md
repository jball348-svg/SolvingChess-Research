# R4 Implementation and Reproduction Provenance

**Session:** R4

## Audit-local implementation

Accepted source SHA-256:

`b4344cd2ab3502c3efb87c855267a75853aa5f0f5a55a793e55124dd9fab169a`

Accepted executable SHA-256:

`d4d68185246ec82b81ca719da55829536c25c529e18250d7324846fd6242cd49`

Compiler:

`g++ (Debian 14.2.0-19) 14.2.0`

Flags:

`-O3 -std=c++20 -march=native`

The implementation carries board, turn, castling rights, effective en-passant, halfmove clock and a bounded repetition-count map. Program phase is strategy memory and is not substituted for chess-state identity.

## Move-generator regression

Standard-start legal path counts reproduced:

- depth 1: 20;
- depth 2: 400;
- depth 3: 8,902;
- depth 4: 197,281;
- depth 5: 4,865,609.

## Direct R3 regression

A diagnostic replay of the frozen one-phase R3 policy `ANSWER_CHECK OR CENTER_PAWN` reproduced the frozen R3 counts exactly.

D:

- ply 1: 2 paths / 2 exact states;
- ply 2: 40 / 40;
- ply 3: 281 / 281;
- ply 4: 6,243 / 4,714;
- ply 5: **38,824 / 13,064**.

Historical R3 H queen-pawn control:

- ply 1: 2 / 2;
- ply 2: 40 / 40;
- ply 3: 281 / 281;
- ply 4: 6,248 / 4,719;
- ply 5: **38,916 / 13,181**.

This links the R4 generator directly to the exact R3 structural mechanism under audit.

## Target implementation boundary

The G12 table payloads were not loaded by the R4 local certifier. This does not weaken the R4 result because the cohort minimum is 30 pieces and only five remaining plies are permitted. No legal line can reach a 3–4-piece G12 target inside the test.

## Baseline resource enforcement

The accepted D/H complete bounded baselines were run under a 2 GiB virtual-memory ceiling and 180-second wall ceiling.

Both terminated with `std::bad_alloc` before complete truth was acquired.

A prior D attempt without a hard virtual-memory limiter was terminated as soon as observed RSS exceeded the prospective 2 GiB budget. That preliminary run is preserved as an engineering alarm and not used for the accepted baseline figures.

## Independence limitation

R4's move/path regressions are strong deterministic checks, including exact reproduction of R3 counts, but R4 does not contain a separately authored second policy-certification implementation.

The result is therefore exact computation with deterministic regression evidence, not organizationally independent replay.
