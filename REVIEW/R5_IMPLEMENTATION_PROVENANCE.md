# R5 Implementation and Reproduction Provenance

**Session:** R5

## 1. Prospective scientific freeze

The R5 target/program/domain/budget/threshold hypothesis was committed before decisive target-membership inspection:

`305b154642f99e5a8c52e8248743615acfb6a956`

File:

`REVIEW/R5_NONTERMINAL_TARGET_HYPOTHESIS.md`

## 2. Accepted producer

Audit-local source SHA-256:

`b8978d1bfacc2f46b2b1818f2d481cbb8809ef58be82ea03073fd60799a671e8`

Executable SHA-256:

`295e240def874ba10489e6872c19647d826d099541b412013451564176ac269a`

Compiler:

`g++ (Debian 14.2.0-19) 14.2.0`

Flags:

`-O3 -std=c++20 -march=native`

Standard-start perft reproduced:

- 20;
- 400;
- 8,902;
- 197,281;
- 4,865,609.

## 3. Representation-only failed attempt

The first implementation used a larger in-memory exact-state representation.

Under the frozen 2 GiB cap it reached:

- D ply 1: 2;
- ply 2: 40;
- ply 3: 839;
- ply 4: 13,844;
- ply 5: 272,731;

then failed with `std::bad_alloc` while constructing ply 6 at roughly 2 GiB RSS.

This was treated as an engineering representation failure, not a scientific result.

No target theorem, target depth, policy, cohort rule, D/H family, threshold or budget was changed.

The accepted rerun used a compact exact serialization of the same theorem state.

## 4. Accepted producer run

Result output SHA-256:

`88a96eb1dd55c9dce47d75137684d401f100d8de240ed25b494171b4343fdb87`

Accepted peak RSS:

**1,260,500 KiB**

Combined instrumented D+H run elapsed:

**181 s**

All prospectively budgeted individual frontier/certification/baseline components completed below 180 s.

## 5. Frozen cohort dumps

D cohort:

- 1,024 exact states;
- SHA-256: `3b0e3fb8ad6af01f57eda39f82940caec9b62b18a877046ac966fa38c6bd0f2e`.

H cohort:

- 1,024 exact states;
- SHA-256: `33078078fcd5bad52c5b45516c633d77bf9d96bf9db2a094f8639137d025215b`.

These cohort dumps were generated from the frozen canonical selection rule.

## 6. Separate target/certification replay

Verifier source SHA-256:

`38500f5568a2cb8d6176fd1cc9b0a3f1bd05c798a286863dc10e815a8da2da88`

Verifier executable SHA-256:

`b113e06cc424751b612104d9b95f5629974f9514c6f10e3e4a3e38ba2f13e607`

Verifier output SHA-256:

`373d7787a68a4a7398e70cd6b58f54d54f1576cc594c2819f1dff8052cb86651`

The verifier uses a separately written bottom-up `exists/forall/exists/forall` FERL implementation over the frozen cohort states.

It shares the audit-local move generator/state parser, so it is structurally separate at the theorem/certificate algorithm level rather than a fully independent chess implementation.

It reproduced:

- perft 20 / 400 / 8,902 / 197,281 / 4,865,609;
- D direct/policy/baseline = **1 / 5 / 5**;
- H = **6 / 7 / 7**.

The replay completed inside the frozen verifier wall target.

## 7. Independence limitation

R5 has stronger replay separation than R4 at the target theorem level, but it does not claim organizationally independent verification or a second legal-move implementation.

The exact target result is supported by:
- prospective freeze;
- complete legal-reply quantifiers;
- exact identity checks;
- perft regression;
- separately implemented target/certification quantifier replay.

## 8. Artifact policy

Large frontier/cohort/runtime bytes are not committed to ordinary Git history merely to demonstrate existence.

This provenance file and the machine-readable R5 run summary record the identities required to reproduce/audit the result.
