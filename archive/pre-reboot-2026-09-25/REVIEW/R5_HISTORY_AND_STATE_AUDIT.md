# R5 History and State Audit

**Session:** R5  
**State model:** exact board, turn, castling rights, effective EP, halfmove clock and repetition-count map.

## 1. History-state multiplication

At the frozen ply-6 R5 policy frontier:

| Family | Exact full states | Board placements | HISTORY_MULTIPLIER | Max full states / board |
|---|---:|---:|---:|---:|
| D | 3,903,222 | 1,556,742 | **2.50730178796x** | **264** |
| H | 3,004,564 | 1,281,334 | **2.34487182889x** | **217** |

Board-only merging would therefore collapse many theorem-distinct states and is not admissible.

## 2. Comparison with R4

R4 at ply 6 reported:

- D: 1.34595x, max 15 theorem states per board;
- H: 1.48250x, max 15.

R5's broader one-phase policy produces substantially more history splitting:

- D multiplier rises to **2.50730x**;
- H to **2.34487x**;
- maximum same-board theorem multiplicity rises to **264 / 217**.

This does not mean history alone causes the FERL coverage failure. It does mean that adding semantic freedom to search for a richer bridge spends a large amount of the transposition advantage.

## 3. Policy-surface expansion

R4's two-phase policy frontier at ply 6 contained:

- D: 158,947 exact states;
- H: 449,623.

R5's broader prospectively frozen policy contains:

- D: **3,903,222**;
- H: **3,004,564**.

The increase is approximately:

- D: **24.56x** R4's exact frontier;
- H: **6.68x**.

This is important negative evidence. R5 gained enough White semantic freedom to produce a nonempty high-material exact target, but the price was a much larger exact start-side surface.

## 4. FERL-4 and exact history

FERL-4 itself is history-safe because it demands exact return of the FIDE repetition identity, not merely board placement.

The theorem deliberately permits halfmove/repetition counters to advance; those counters can only move the state toward an exact draw condition while the same REP identity preserves ordinary move legality.

No accepted target was invalidated by:
- castling-right mismatch;
- effective-EP mismatch;
- turn mismatch;
- board mismatch.

Such branches simply fail target membership.

## 5. Target splitting

The same board placement can correspond to hundreds of distinct theorem states in the R5 frontier.

Although FERL-4 membership is driven by REP identity, start-side certification and claim legality still require the exact theorem state. R5 therefore cannot safely store or certify the frontier by board placement alone.

History does not destroy FERL-4 exactness, but it **materially increases the number of exact start-side objects that must be distinguished**.

## 6. State-audit conclusion

R5 strengthens the adverse history prior:

> the semantic freedom needed to search for high-material exact bridge objects can enlarge both the policy frontier and the full-history splitting burden faster than it enlarges certified coverage.

No safe quotient is introduced in R5.
