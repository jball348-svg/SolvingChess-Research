# G6 Interim Evidence Freeze C

**Date:** 11 August 2026  
**Status:** Interim synthesis checkpoint; G6 remains open.

## What changed since Freeze B

- Added a closed two-sided pawn-race family (BCF discovery, CDG translation held-out, ABE edge held-out). `TARGET_RACE_CLEAR` transfers exactly and strict pure BRIDGE remains nonzero, but one-move critical-slab coverage is scientifically weak because the slab covers almost all residual geometry.
- Completed corrected nested scaling at ranks 5–7, 4–7, 3–7, 2–7. Fixed proof descriptions persist while coverage growth is topology-dependent: rook target-attractor growth is almost linear in state count; knight/bishop growth is sublinear.
- Added paired adversarial double-brink controls. Their promotion race slab is 100% saturated and non-informative; non-race contact slabs are not enriched for mixed truth. Yet their off-contact tails admit a 10-leaf exact semantic grammar shared by knight and bishop. The frozen grammar transfers with zero error to translated c7/e2 N+B and to a non-translation b7/e2 knight held-out.
- Completed an exhaustive all-files full-rank restoration scan under the corrected double-push predecessor implementation. FAR5 is zero-counterexample across 15,251,718 N/B/R antecedents. FAR3 is zero-counterexample for 20,880,614 bishop/rook antecedents; knight has exactly 96 failures, and those 96 are exactly one compact relative-coordinate exception family.
- Canonicalized the corrected same-side harness as `g6_lab_corrected_v2.cpp`. Its G5 regression reproduces all load-bearing truth/count quantities; only the historical max-rank label convention remains different.

## New methodological rule: localization lift

Raw slab coverage is no longer sufficient evidence of a critical manifold. G6 now records **localization lift = mixed-geometry slab coverage − all-residual slab coverage**. Opposing-minor and fortress arenas show strong positive lift; dense two-sided races show only ~1–3 percentage points; double-brink promotion parity is exactly 0. This prevents a broad/slack-saturated surface from masquerading as compression.

## Cross-arena theory map at this freeze

**Universal/mathematical:** strict attractor semantics; Branch-Kernel Factorization; three-way Hyperkernel Factorization; certificate dependency semantics.

**Strong reusable schema:** semantic target construction, but only with explicit resource guards (terminal safety, conversion-path availability, opponent race/access constraints).

**Conditional:** restoration/inheritance. FAR5 is exact across the full N/B/R board portfolio; FAR3 is exact for B/R and for N outside one exact edge family.

**Conditional localization:** thin clock manifolds are real in advanced-pawn, opposing-minor and fortress topologies, but fail as a discriminating representation when resource clocks saturate.

**Local/representation-dependent:** final grammar complexity. Some tails hit lookup-like floors (G4/G5), opposing-minor tails compress compactly but do not transfer exactly, while double-brink tails admit a tiny exact cross-topology grammar.

**Model-level theorem:** terminal semantics belong in the proof-object domain. The faithful wrong-bishop fortress changed by 274,296 White wins relative to the historical immediate-promotion shortcut and restored the exact 22,008-state `BK=a8 => draw` theorem.

## Still open

1. Full G4 implementation-level optional-pawn/capture graph reconstruction. The prose handoff remains authoritative but insufficient to invent missing encoding details; the File Library search endpoint errored during this pass.
2. Historical G5 rank-label convention (membership truth and all load-bearing counts match).
3. Final G6.9 synthesis, proof-language specification, technical handoff and G7 strategy memo.

G6 is **not closed** by this freeze.
