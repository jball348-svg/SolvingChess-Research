# G7.4 Interim Evidence Freeze B

**Programme:** G7 Higher-Tree Position Discovery  
**Stage:** G7.4 — Seven-man / fortress-imbalance wave  
**Date:** 11 August 2026  
**Status:** G7.4 complete as an interim freeze; G7 remains open.

## 1. Authority and stage contract

G7.4 inherits the frozen Pilot1 → Pilot2 → G3 → G4 → G5 → G6 history and the G7 prospective ascent memo. It is not permitted to retune a candidate after outcome inspection. Terminal semantics are part of every proof-object domain.

This freeze records two distinct outcomes:

1. the prospectively frozen seven-man triple-brink matched pair reaches the present exact-solve/certificate boundary before any W/D/L output; and
2. the predeclared fortress-imbalance branch succeeds exactly one material level above the faithful G6 wrong-colour bishop sanctuary.

## 2. Seven-man wave: frozen scale boundary, no outcome claim

### G7F07 — BB_opp_a7c7_b2
- Material: `K+B+2P vs K+B+P` (7 men)
- White bishop: wrong-colour relative to a8; Black bishop opposite colour
- White brink pawns: a7, c7
- Black brink pawn: b2
- Raw encodings: **71,368,704**
- Exact static-valid states: **45,823,238**
- Structural sample: mean legal branch **12.116**, capture density **1.818%**, checking density **4.103%**, promotion-available state rate **48.743%**
- Predecessor audit: **115,563** reverse edges, **0 unsound**; **116,006** forward edges, **0 missing**
- Exact W/D/L: **NOT PRODUCED**. Full solve crossed the declared execution/certificate budget before outcome output.

### G7F08 — BB_same_a7c7_b2
- Same pawn geometry and White bishop complex; Black bishop moved to same colour complex
- Raw encodings: **71,368,704**
- Exact static-valid states: **43,334,293**
- Structural sample: mean legal branch **11.939**, capture density **4.629%**, checking density **3.609%**, promotion-available state rate **50.320%**
- Predecessor audit: **114,494** reverse edges, **0 unsound**; **114,669** forward edges, **0 missing**
- Exact W/D/L: **NOT ATTEMPTED AFTER F07 SCALE HOLD** under the same full-closure engine.

### Seven-man verdict

The seven-man pair is preserved as a **scale-boundary certificate**, not shrunk after truth inspection. No W/D/L number from either family is asserted. The next implementation-level route, if revisited, should solve material signatures as a dependency DAG rather than materializing the whole optional-material closure in one retrograde arena.

## 3. Faithful fortress dependency regression

Before the higher-material fortress experiment, G7 reconstructed the faithful four-man G6 arena:

`K + wrong-colour B + h-pawn vs K`, pawn h2–h7, both turns, full legal king/bishop/pawn motion, h2–h4 allowed, capture exits typed through exact lower material, promotion continued semantically rather than treated as an unconditional win.

Exact regression:

- Static-valid: **1,182,440**
- White wins: **825,269**
- Draws: **357,171**
- `BK=h8` states: **22,008**
- White wins with `BK=h8`: **0**
- G6 fortress target direct states: **103,451**, **0** failures
- Strict White target attractor: **585,732**, **0** failures

These reproduce the frozen G6 faithful-fortress quantities, including the published 585,732 target-attractor count.

### Terminal-model diagnostic

The continuation-aware h-file KPK helper used inside the faithful model gives **27,430 W / 14,189 D** on 41,619 states. A diagnostic changing only promotion to an immediate terminal White win reproduces the historical Pilot-style **29,520 W / 12,099 D** split. This is recorded as a deliberate terminal-model distinction, not a move-generation discrepancy.

## 4. Higher-material fortress ascent

### G7F09 — TWO_WRONG_BISHOPS_HPAWN

Prospective family encoded before its first outcome solve:

- Material: **K + 2B + h-pawn vs K** (5 men)
- Both White bishops are restricted to the colour complex opposite h8.
- Bishops are identical and canonicalized as an unordered pair.
- Pawn ranks: h2–h7; h2–h4 enabled.
- Black capture of one bishop exits into the exact faithful G6 four-man dependency.
- Black capture of the pawn exits to same-colour `K+2B vs K`, a draw.
- Promotion continuation is typed by the resulting promoted material, immediate king capture and stalemate/checkmate status; it is not an unconditional terminal win.
- No repetition, 50/75-move counter or en-passant state is included, matching the declared finite-model contract.

Structural/certification quantities:

- Raw full-material encodings: **24,379,392**
- Static-valid states: **16,557,288**
- Predecessor audit: **118,745** reverse edges, **0 unsound**; **121,885** forward edges, **0 missing**
- Exhaustive Bellman audit: **16,557,288 / 16,557,288 checked, 0 mismatches**

Exact truth:

- White wins: **12,115,187**
- Draws: **4,442,101**
- Win share: **73.1713%**
- Draw share: **26.8287%**

## 5. Sanctuary preservation result

The G6 direct corner sanctuary survives the extra attacking bishop exactly:

> **Finite G7.4 preservation result:** In the declared `K+2 wrong-colour bishops+h-pawn vs K` faithful arena, `BK=h8 ⇒ draw`.

Certificate:

- `BK=h8` antecedents: **330,264**
- White wins among antecedents: **0**
- Draws among antecedents: **330,264**

This is approximately 15× the number of direct sanctuary states in the four-man G6 arena, but the exact statement is the zero-counterexample implication above; no simple multiplicative theorem is asserted.

## 6. Role-dual sanctuary attractors

Two defender certificates were measured.

### Strict target-only defender attractor

Treat every shortcut/external material transition as a failure for the narrow objective “reach the direct `BK=h8` target”.

- Direct sanctuary: **330,264**
- Strict defender attractor: **3,133,058**
- False White wins: **0**
- Exact draw-basin coverage: **70.5310%**
- Amplification over direct seed: **9.4865×**

### Typed safe-exit defender attractor

Allow exact drawing exits already certified by the dependency graph (lower-material faithful draw after bishop capture, same-colour two-bishop draw after pawn capture, and stalemate) as safe defender terminals.

- Direct sanctuary: **330,264**
- Safe-exit seeds outside direct target: **843,760**
- Stalemate seeds: **10,438**
- Defender attractor: **4,437,719**
- Certified draws: **4,437,719**
- False White wins: **0**
- Exact draw-basin coverage: **99.9014%**
- Exact draw residual outside this certificate: **4,382**

The residual is preserved rather than patched. It contains no h7-pawn states in the current exact scan and is concentrated mainly on pawn ranks 4–6 with Black king away from h8, but no new grammar is promoted at G7.4.

## 7. Resource-safe TARGET upward fire

The unchanged G6 faithful-fortress safe target form was fired into G7F09:

`pawn rank >= 6 ∧ WK Chebyshev distance to h8 <= 4 ∧ BK Chebyshev distance to h8 >= 5`

In this topology the two extra wrong-colour bishops cannot occupy h8, there is no opposing promotion race or opposing mobile access resource, and the faithful terminal model is already typed.

Results:

- Direct target states: **1,448,464**
- Direct non-wins: **0**
- Strict White target attractor: **8,295,062**
- Attractor non-wins: **0**
- Coverage of exact White-win basin: **68.4683%**
- Attractor amplification over direct target: **5.7268×**

For regression, the same target in the reconstructed four-man faithful arena gives **103,451** direct states and **585,732** strict-attractor states, both with zero failures. Thus the typed TARGET + STRICT ATTRACTOR machinery survives this one-level fortress ascent unchanged.

## 8. Supersession / audit ledger

The following quantities are explicitly **not evidence**:

1. No seven-man W/D/L value was emitted by the timed-out G7F07 solve; none is inferred.
2. An early post-analysis defender-attractor run reported 5,462,806 states including 1,024,496 White wins. It is discarded. The post-analysis executable had instantiated, but not solved/loaded, the exact F4 dependency, so lower-material bishop captures were mis-typed as draws. Re-running with F4 initialized gives the certified 4,437,719 / 0-false-win result.
3. A corresponding “873,735 Bellman mismatches” diagnostic is also discarded as an audit-harness dependency-initialization error. The actual F5 truth mask, audited with F4 loaded, has **0 exhaustive Bellman mismatches**.
4. The F5 W/D split itself was never changed by those post-analysis errors and is now accepted because the exhaustive dependency-aware Bellman audit is zero-error.

## 9. G7.4 scientific verdict

**G7.4 PASS WITH A SEVEN-MAN SCALE HOLD.**

- The seven-man portfolio reaches a reproducible current implementation boundary without outcome-driven shrinking.
- A higher-material fortress family is solved exactly under a faithful terminal model whose four-man dependency reproduces G6.
- The G6 corner sanctuary survives one attacker-material level upward: **330,264/330,264 draws**.
- The role-dual sanctuary machinery remains highly effective, reaching **99.9014%** of the exact draw basin when typed exact draw exits are allowed.
- The unchanged G6 faithful-fortress TARGET remains exact and its strict attractor certifies **8,295,062** White wins.
- No genuinely new G7 proof-object type is promoted yet. Under the G7 programme order, new abstraction discovery remains reserved for G7.6 after the broader unchanged-G6 upward-fire matrix in G7.5.

## 10. Next gate

G7.5 should now fire the full type-compatible G6 library upward across the frozen G7 families without retuning: PROJECT/restoration where domains type-check, TARGET, attacker/defender strict attractors, Branch/Hyperkernel, localization-lift and STOP. The G7.4 preservation theorem should be treated as a candidate higher-tree object for later G7.6/G7.7 promotion and backward-fire, not generalized yet.
