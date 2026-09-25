# R2 Discovery Hypothesis — prospective freeze

**Session:** R2 — Topology-Adaptive Proof Discovery Audit  
**Freeze status:** PROSPECTIVE — frozen before either R2 arena is exactly solved or its full-domain W/D/L truth is inspected  
**Review mode:** independent viability review; G15 remains forbidden  
**Result vocabulary:** `SURVIVED`, `FAILED`, `PARTIAL`, `NO_CANDIDATE`

## 1. Primary falsifiable proposition

R2 tests, without weakening after outcome inspection:

> There exists an outcome-independent discovery mechanism, compatible with the existing strict-attractor / Branch / Hyperkernel / Filter-Pivot algebra, that can generate or select compact exact semantic targets and strategy languages on a transition-rich opposing-material arena, with materially useful exact coverage, no square-level fitting, low raw-truth leakage, and unchanged held-out transfer.

The discovery mechanism must be evaluated separately from full exact truth production.

## 2. Rules and reachability model

R2 uses the same historical board-state finite-game semantics as the G7/G8 brink laboratories, not G10/G12 full-history chess:

- standard 8×8 board;
- both sides to move;
- kings may occupy any statically legal square;
- bishops occupy a prospectively declared colour complex and otherwise move normally;
- one fixed brink pawn per side;
- legal king/bishop/pawn moves;
- pawn promotion is an immediate win for the promoting side;
- checkmate is a win for the mating side;
- stalemate and unresolved cycles are draws;
- captures are represented by exact lower-material signatures inside the same capture-closed graph;
- no castling, en-passant, repetition history or halfmove clock.

All states are **ARENA_ADMISSIBLE** only. No START_REACHABLE claim is permitted.

## 3. Prospectively frozen arenas

### D1 — discovery arena

`R2D1_BB_SAME_F7_D2`

Material: K+B+f7-pawn versus K+B+d2-pawn.

- White bishop: colour complex 0 under the repository's 0-based `(file+rank) mod 2` convention.
- Black bishop: the same colour complex 0.
- White pawn fixed initially at f7; Black pawn fixed initially at d2.
- Kings unrestricted.
- Captures remove material and enter exact lower signatures.
- Both bishops are on the same complex, so direct bishop-for-bishop captures are live where geometry permits.
- The White bishop can interact directly with the d2 pawn; king captures and both promotion races remain live.

### H1 — held-out hostile arena

`R2H1_BB_OPP_F7_D2`

Same material, pawn squares and rules as D1, except:

- White bishop remains colour complex 0.
- Black bishop is colour complex 1.

This changes line interference, direct bishop-exchange availability and which mobile piece can attack the f7 pawn while preserving the same material count and promotion resources.

H1 is not used to select target predicates, strategy classes, program depth or thresholds. Objects selected on D1 are applied unchanged.

## 4. Why these arenas answer the R2 question

D1 materially exceeds the R1 one-sided laboratory:

- at least one White and one Black mobile non-pawn piece;
- both sides have an irreversible promotion resource;
- genuine captures by both sides;
- multiple live lower-material destinations;
- checking resources for both sides;
- quiet king/bishop moves;
- direct line interference and exchange choices;
- two competing promotion fronts.

The pair is intentionally much smaller than ordinary middlegame chess so complete exact truth can be withheld during discovery and produced later for validation.

## 5. Discovery/validation separation

### Discovery phase — full W/D/L forbidden

Allowed:

- legal graph structure and static validity;
- material identities/signatures;
- relative geometry and attack/access maps;
- checks/captures/promotion distance;
- mobility and line blocking;
- king-safety descriptors;
- pawn-resource accessibility;
- exact lower-material truth;
- exact bounded-horizon attractor membership derived from certified terminal/lower-material exits;
- exact ordinary/filtered attractors to a frozen discovered target.

Forbidden:

- D1 full-domain W/D/L labels;
- H1 full-domain W/D/L labels;
- any outcome-derived exception list;
- manual patching after held-out validation;
- square IDs as target/strategy features.

The planned full-domain labelled-state budget during candidate generation/selection is **zero**.

### Validation phase

Only after target and strategy objects are frozen may complete D1/H1 W/D/L be solved and inspected for:

- false positives;
- win-basin coverage;
- residual raw truth;
- exact held-out transfer;
- discovery/full-solve economics.

## 6. Frozen target-discovery mechanism

### 6.1 Certified seed

Construct an exact `CERTIFIED_EXIT` seed using only:

- legal promotion wins;
- legal captures entering an already exact lower-material signature whose resulting state is a win for the capturing side.

No top-signature W/D/L label is used.

Compute a bounded local attractor `A4 = Attr_{≤4 plies}(CERTIFIED_EXIT)` in the full capture-closed graph. Membership in A4 is a proof object derived from semantics/lower truth, not a full-domain W/D/L table.

### 6.2 Semantic target atoms

The frozen state atom grammar contains only relative/resource predicates:

- side to move;
- own/enemy pawn present;
- in check;
- own/enemy direct promotion legal;
- own/enemy promotion distance class;
- own king Chebyshev distance to own/enemy promotion square in bins 1,2,3,4+;
- enemy king distance to own promotion square in bins 1,2,3,4,5+;
- own/enemy bishop attacks own/enemy pawn;
- own/enemy bishop controls own/enemy promotion square;
- own/enemy pawn defended by king;
- own/enemy pawn defended by bishop;
- own/enemy pawn blocked;
- bishops aligned on a common diagonal;
- own bishop attacks enemy bishop;
- enemy bishop attacks own bishop;
- own/enemy legal mobility in frozen bins 0–3, 4–7, 8+;
- own/enemy checking-move availability;
- certified winning capture exit exists;
- certified promotion exit exists.

Promotion squares are represented relationally as the promotion square of a declared pawn, not as literal square IDs.

### 6.3 Candidate grammar and ranking

Generate:

- every single atom;
- conjunctions of up to three atoms;
- disjunctions of at most two conjunction clauses, with at most four total literals.

A candidate is admissible only if every matching D1 state is inside A4. Thus candidate exactness is established without top W/D/L.

Rank admissible candidates lexicographically by:

1. larger D1 A4 coverage;
2. fewer literals;
3. larger material-signature diversity;
4. larger side-to-move diversity;
5. deterministic lexical atom order.

Select exactly one target. No manual tie-break based on chess interpretation is allowed.

Maximum target description complexity: **4 semantic literals in at most 2 clauses**, no exceptions.

## 7. Frozen strategy-language discovery mechanism

### 7.1 Move-effect atoms

Generate move classes from these move-local semantic effects:

- gives check;
- captures;
- captures mobile piece;
- captures pawn;
- promotes;
- creates direct promotion threat;
- answers an existing check;
- moves king closer to own promotion square;
- moves king farther from enemy promotion square;
- attacks enemy pawn after the move;
- defends own pawn after the move;
- attacks enemy mobile piece after the move;
- defends own mobile piece after the move;
- newly blocks an enemy bishop line to own pawn/promotion square;
- newly unblocks own bishop line to enemy pawn/promotion square;
- simplifies material;
- moves into an exact lower-material win;
- nondecreasing own legal mobility;
- nonincreasing enemy checking-move availability.

No atom may read W/D/L of the top signature.

### 7.2 Candidate classes and finite programs

Candidate move classes are:

- every single move atom;
- every conjunction of two move atoms.

Discovery computes the ordinary strict attractor of the frozen selected target and exact filtered attractors for every candidate class.

Rank classes by exact coverage of the ordinary target attractor, then by fewer literals and deterministic lexical order.

The strategy program search is limited to:

- one phase; or
- one ordered switch `F -> G`.

No second switch is allowed in R2.

The best program is selected only from D1 target-attractor membership and graph semantics. No D1 full W/D/L is available.

Maximum strategy description complexity: **4 move literals total plus one switch**.

## 8. Frozen cost and leakage measures

`TRUTH_LEAKAGE = full-domain W/D/L-labelled states consumed during candidate generation/selection / total exact states in the target top signature`.

Because R2 is preregistered as zero-label discovery, the planned value is **0**. Any top-signature W/D/L use before object freeze is a protocol deviation and prevents `SURVIVED`.

`DISCOVERY_COST_RATIO = discovery wall time / complete exact-solve wall time`.

Discovery wall time includes:

- graph/static-valid enumeration needed by discovery;
- semantic feature generation;
- exact lower-signature production used by discovery;
- A4 construction;
- candidate generation/ranking;
- target ordinary attractor;
- strategy-class/program search.

It excludes the later complete top-signature W/D/L validation solve.

`RESIDUAL_RAW_RATIO = exact top-signature White-winning states not certified by the frozen discovered target attractor / exact top-signature White-winning states`.

A separate strategy residual is reported relative to the ordinary discovered-target attractor.

## 9. Frozen budgets

Per arena hard resource budget:

- 180 s wall time for the complete exact solve;
- 2.0 GiB peak RSS.

Discovery-side search budget on D1:

- at most 100,000 target candidates;
- at most all one/two-atom move classes from the frozen move grammar;
- at most the best 12 single/class candidates may enter ordered-pair program search;
- one switch maximum;
- no adaptive grammar extension after candidate outcomes.

## 10. Frozen positive thresholds

For **SURVIVED**, all must hold:

1. full-domain truth leakage during discovery is **0%**;
2. one exact semantic target is selected by the frozen procedure;
3. no target false positives on D1 validation;
4. D1 strict target-attractor coverage is at least **15%** of exact White wins;
5. a discovered strategy class/program covers at least **75%** of the D1 ordinary target attractor;
6. the target and strategy descriptions stay within the frozen literal budgets;
7. no square-level or state-ID exceptions;
8. discovery cost ratio is **≤1.0**;
9. the frozen target transfers to H1 with zero false positives;
10. H1 strict target-attractor coverage is at least **10%** of exact White wins;
11. the frozen strategy program transfers unchanged and covers at least **60%** of H1 ordinary target attractor;
12. selected objects verify under exact graph semantics;
13. the D1 residual raw ratio is **< 0.67**, improving on the approximately 67% unexplained main-ladder residual recorded in R1;
14. no post-validation mutation.

If useful exact discovery occurs but one or more of coverage, economics, residual improvement or held-out thresholds fail, classify `PARTIAL`.

If the mechanism requires essentially full truth, lookup-scale descriptions, square patches, or held-out exactness collapses, classify `FAILED`.

If the frozen mechanism cannot produce an admissible target/program at all, classify `NO_CANDIDATE`.

## 11. Strike discipline

An individual target/program failure is not itself a strike.

A strike is warranted only if R2 fails to formulate/test the central mechanism, collapses discovery into post-hoc full-truth explanation, or completes without retiring/sharpening the discovery obligation.

## 12. Freeze declaration

This file freezes the arenas, semantic grammars, candidate generation, ranking, label budget, complexity limits, strategy depth, search budget and pass/fail thresholds **before D1/H1 complete W/D/L truth is inspected**.

Implementation defects may be repaired only if semantics and all frozen scientific choices remain unchanged. Any affected preliminary output is discarded and preserved as negative/engineering evidence.

**R2 discovery objects are not yet selected. Full-domain validation has not begun.**
