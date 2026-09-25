# G8 Certificate Format v0.1 — Freeze B

**Status:** frozen for G8.2 deterministic replay.

## 1. Logical contract

The certificate format compiles the frozen G7 proof language without changing its semantics. A certificate identifies an arena, exact truth dependencies, proof-object type, semantic parameters, object dependencies, sparse generating payload (when needed), and canonical expected membership hash. Producer work queues and mutable frontier state are not certificate data.

## 2. State identity

A state is identified by `(arena_signature, canonical_raw_code)`. Canonical raw-code semantics are arena-declared. The verifier reconstructs the move relation for that arena and consumes only exact lower-material/truth dependencies whose SHA-256 hashes are declared in the manifest.

## 3. Sparse payload encoding: G8DV1

Payloads are strictly increasing 32-bit canonical raw codes. The first code is stored as an unsigned LEB128 integer and later codes as unsigned deltas. The file begins with an 8-byte `G8DV1` magic/version field and an unsigned 64-bit count. Payload SHA-256 and byte count are declared in the manifest.

This encoding is a representation choice, not a chess theorem.

## 4. Object verification

- **BRANCH_KERNEL:** verifier independently derives constituent attractors/proper union, checks the supplied kernel exactly against local defender-choice obligations, and reconstructs the irreducible bridge by residual closure.
- **FINITE_N_HYPERKERNEL:** verifier independently derives all proper subunions, checks the supplied defender Hyperkernel, then reconstructs the irreducible n-way region by residual closure.
- **STRICT_ATTRACTOR:** verifier independently regenerates the least fixed point from the declared exact target and typed external transitions.
- **FILTERED_ATTRACTOR:** same graph and defender semantics; only attacker pre-target admission is restricted by the declared semantic filter, with target-entry exemptions explicit.
- **FILTER_PIVOT_FACTORIZATION:** verifier independently derives ordinary and filtered attractors, computes the strategy complement and exact pivot set, requires equality with the sparse payload, then reconstructs the complement from those pivots.
- **ROLE_DUAL_SANCTUARY_ATTRACTOR:** verifier reverses goal/ownership semantics and accepts external safe exits only when explicitly declared.

## 5. Hash hierarchy

The manifest declares hashes for exact G8.1 truth dependencies, producer and verifier sources, every sparse payload, and every canonical derived membership stream used as a deterministic replay fingerprint. The manifest itself has a SHA-256 sidecar.

## 6. Current frozen payloads

| Object | Seeds | Payload bytes |
|---|---:|---:|
| F01 Branch kernel | 152 | 248 |
| F02 Hyperkernel | 1,641 | 2,135 |
| F02 derived Filter-Pivots | 239 | 460 |
| F09 Filter-Pivots | 517,120 | 530,753 |

Combined sparse payload: **533,596 bytes**.

## 7. Independence boundary

The verifier sources do not include producer sources. They independently reconstruct move relations/fixed points and use the frozen truth tables only as explicitly hashed dependencies. Producer audit masks are not required to verify the certificate. A replay succeeds only if independently reconstructed canonical membership streams match the hashes in the manifest.

## 8. Known engineering boundary

Certificate bytes are compact, but the current F01/F02 standalone verifier caches a large reverse graph and peaks around 0.55–0.62 GB RSS. That is an implementation cost to attack later; it is not hidden inside the certificate economics. F09 verifies on the fly at roughly 84 MB peak RSS.
