# Computational evidence map

This file separates exact chess computation from engineering fixtures and from proof/certificate compression.

| Programme | Evidence | Domain | Supports | Does not by itself support |
|---|---|---|---|---|
| G6 | Large exact finite campaigns and counterexample families | Declared restricted domains | Exact local/restricted propositions and proved universal operators | Start reachability or global scaling |
| G7 | Exact restricted six/seven-man higher-tree arenas | Declared arenas | Exact arena truth and reusable propositions at proved scope | Ordinary middlegame coverage |
| G8 | Recovered large scale holds; restricted eight-man dependency graphs above 80M states; compact certificates | Prospectively frozen restricted arenas | Exact restricted truth and solver/certificate economics | General eight-piece tablebases or higher-material discovery compression |
| G12 | KQK/KRK/a-file KPK tables, same-colour K+2B deadness, history controls, 809,183-state replay | Small final-rule arenas | Full-state semantic anchors | Reachability of arbitrary decorated states from the initial position |
| G13 | 65,536-state checkpoint/repartition campaign | Synthetic game graph | Distributed engineering | New chess truth |
| G14 | Proof-store/mutation/offline verification | Synthetic/preservation fixture | Preservation and integrity engineering | New chess truth or bridge progress |

## Required audit measurements

For each meaningful ascent reconstruct where possible:

- full/static/dependency state counts;
- edge/branching counts;
- wall time and peak memory;
- verifier wall time and peak memory;
- certificate/raw-truth bytes;
- degree of prospective geometric/material restriction;
- whether speedup avoids truth discovery or merely implements the same discovery more efficiently;
- whether solved truth composes upward without re-solving most parent states.

The primary question is not whether a current arena is fast. It is whether the mechanism has a scaling law compatible with many ascents toward ordinary 32-piece chess.
