# G8 Proof Language v0.4 — Frozen Closeout Specification

**Date:** 11 August 2026  
**Status:** FROZEN AT G8 CLOSEOUT

## 1. Compatibility rule
G8 v0.4 is backward-compatible with the frozen G7 v0.3 proof language. G8 does not change the semantics of any G7 core object.

## 2. Universal/core operations retained unchanged

- `STRICT_ATTRACTOR`
- `ROLE_DUAL_SANCTUARY_ATTRACTOR`
- `BRANCH_KERNEL`
- `FINITE_N_HYPERKERNEL`
- `FILTERED_ATTRACTOR(F)`
- `FILTER_PIVOT_FACTORIZATION`
- `DEPENDENCY_DAG_AND_SUBSUMPTION_SEMANTICS`

Reusable schemas/diagnostics remain `PROJECT_EXACT_LOWER_TRUTH`, `RESOURCE_SAFE_TARGET`, `RESIDUAL`, `GROUP_OUT`, `LOCALIZATION_LIFT`, `STOP`, and `CERTIFY`.

## 3. G8 compiled composition schema

### `ORDERED_FILTER_SWITCH(F -> G; T)`
Within a declared ordinary domain A and target T, let:

`C_G = FILTERED_ATTRACTOR(G, T)`

Then:

`ORDERED_FILTER_SWITCH(F -> G; T) = FILTERED_ATTRACTOR(F, C_G)`

with the same target-entry exemption, defender semantics, terminal typing and dependency rules as the underlying filtered-attractor nodes.

**Classification:** canonical compiled composition schema / proof-DAG node. It is **not** a new primitive theorem: it reduces exactly to nested `FILTERED_ATTRACTOR`.

G8.6 establishes the first canonical destination x strategy product certificate:

`typed endpoints -> FINITE_N_HYPERKERNEL -> irreducible closure -> STRICT_ATTRACTOR -> MOBILE_PIECE_ONLY phase -> CHECK->MOBILE switch`.

In F02 the final ordered switch covers 23,327 / 23,327 states of the derived basin.

## 4. Strategy-language algebra
The frozen finite semantic palette tested in G8 is:

- `CHECK`
- `CAPTURE`
- `FORCING = CHECK union CAPTURE`
- `KING_ONLY`
- `PAWN_ONLY`
- `MOBILE_PIECE_ONLY`

`CHECK_OR_PROMOTION_THREAT` remains uninstantiated because no exact move-local definition was frozen before outcome inspection.

### Typed quotient relations
The following are **typed empirical equalities**, not universal chess identities:

- On the G8 brink/seven-man material-endpoint target type, `FORCING == CHECK`.
- On F01/F02/F03/F04/F06/F07/F08, `PAWN_ONLY == CAPTURE` because the fixed brink pawn has no ordinary internal non-promotion move.
- F09 breaks the second equality: `PAWN_ONLY` contains 822,815 more states than `CAPTURE` because its pawn rank varies and internal pushes exist.

Thus language equivalence is parameterized by arena/target type.

## 5. Certificate layer
G8 adds repository-level compilation, not new game semantics:

- `G8.CERT.v0.1` — canonical certificate manifest format.
- `G8DV1` — sorted raw-code delta ULEB128 sparse-state payload encoding.
- `G8.PRODUCT.CERT.v0.1` — product-DAG manifest for destination x strategy composition.

Truth dependencies, arena declarations, semantic versions, source hashes and payload hashes are explicit. Producer work queues are never proof payload.

## 6. Material-signature dependency typing
Capture, promotion and lower-material transitions are explicit dependency edges. Each child signature is solved/certified once and addressed by deterministic identity/hash. Packed validity membership may be reused for successor validation because it is itself part of the certified signature state layer; this changes representation cost, not legal-move semantics.

## 7. Conditional guards retained
The frozen G6/G7 conditional theorems and guards remain conditional, including FAR domains, conversion-safe restoration sharpening, faithful wrong-colour sanctuary, and sanctuary-access guarding. F10's full G8 truth strengthens the access-destruction evidence but does not create a new primitive object type.

## 8. Non-promotions
G8 does **not** promote:

- any absolute-square strategy predicate;
- any bespoke F09 fortress language;
- `FORCING == CHECK` as a universal theorem;
- `PAWN_ONLY == CAPTURE` as a universal theorem;
- ordered switching as a primitive beyond nested `FILTERED_ATTRACTOR` semantics.

## 9. Frozen classification
The central G8 language advance is therefore compositional rather than ontological: destination-choice kernels and nested semantic strategy phases can be represented in one deterministic proof DAG without expanding the primitive theorem inventory.
