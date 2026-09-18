# R2 Strategy-Language Discovery Results

**Session:** R2 — Topology-Adaptive Proof Discovery Audit

## 1. Frozen meta-language

The concrete R2 move-effect language contains ten positive semantic atoms:

- gives check;
- captures;
- captures mobile piece;
- captures pawn;
- moves White king closer to White promotion;
- moves White king farther from Black promotion;
- attacks Black pawn after move;
- defends White pawn after move;
- attacks Black bishop after move;
- enters exact lower White win.

No atom reads top-signature W/D/L. No square/state ID is available.

The candidate set consists of every one-atom and every two-atom conjunction:

**55 candidate move classes.**

The six best D1 single classes, selected only by exact filtered coverage of the unlabeled composite target attractor, enter the frozen one-switch search. All 36 ordered pairs are evaluated. No second switch is allowed.

## 2. D1 class discovery

Ordinary D1 composite target attractor:

**2,376,263 states.**

Top six generated classes:

| Rank | Class | Exact filtered states | Coverage |
|---|---|---:|---:|
| 1 | ATTACKS_BLACK_PAWN_AFTER_MOVE | 2,348,285 | 98.8226% |
| 2 | GIVES_CHECK | 2,335,054 | 98.2658% |
| 3 | ATTACKS_BLACK_BISHOP_AFTER_MOVE | 2,330,600 | 98.0784% |
| 4 | ATTACKS_BLACK_PAWN_AFTER_MOVE AND ATTACKS_BLACK_BISHOP_AFTER_MOVE | 2,321,940 | 97.7139% |
| 5 | DEFENDS_WHITE_PAWN_AFTER_MOVE | 2,321,665 | 97.7024% |
| 6 | MOVES_WHITE_KING_CLOSER_TO_WHITE_PROMOTION | 2,318,980 | 97.5894% |

Class search wall: **0.416816 s**.

## 3. Frozen strategy program

Best prospectively selected ordered program:

> **GIVES_CHECK -> ATTACKS_BLACK_PAWN_AFTER_MOVE**

Machine masks:

- F_req = 1;
- G_req = 64.

D1 selected-program membership:

**2,370,207 / 2,376,263 = 99.7451%.**

Program membership hash:

`10500123484221588853`.

Pair-search wall: **1.32885 s**.

Description complexity:

- two move literals;
- one ordered switch;
- no exceptions;
- within the frozen four-literal / one-switch budget.

Rank/graph verifier:

- inner filtered attractor violations: 0;
- final program violations: 0.

## 4. D1 validation against withheld truth

After complete W/D/L production:

- program false positives: **0**;
- program / exact composite proof basin: **99.7451%**;
- program membership states are exact White wins.

The frozen >=75% D1 strategy threshold passes.

This directly addresses R1 H2's weakness: R2 did not simply reuse CHECK/KING/PAWN/MOBILE. It generated a larger semantic meta-language, ranked it without top W/D/L, and selected an exact topology-adaptive phase program.

## 5. Held-out H1 application

No strategy atom, class, phase or order is changed.

H1 composite target attractor:

**2,470,802.**

Same D1 program:

**2,460,358 / 2,470,802 = 99.5773%.**

- program false positives: 0;
- pre-W/D/L rank/graph violations: 0;
- held-out >=60% threshold: PASS.

The transfer survives despite a large structural shift in mobile-piece capture traffic and bishop colour geometry.

## 6. Composition with existing proof algebra

The discovered program uses only existing exact graph machinery:

1. exact typed lower-material endpoints;
2. selected semantic top target;
3. strict/composite attractor;
4. filtered attractor for `ATTACKS_BLACK_PAWN_AFTER_MOVE`;
5. outer filtered attractor for `GIVES_CHECK`;
6. rank witness / Bellman validation.

No new primitive graph theorem is required. The novelty is automated selection of the chess-semantic inputs to the existing machinery.

The program is therefore compatible with Filter-Pivot/ordered-filter-switch semantics and can be represented as the same type of finite proof DAG used in G7/G8.

## 7. Interpretation

R2 gives strong evidence that the H2 lesson was not “strategy semantics cannot be discovered.” In this six-piece opposing-bishop pair, a simple frozen semantic meta-language automatically finds a high-coverage exact program and transfers unchanged.

The result is still narrow:

- both pawns are brink resources;
- the selected second phase attacks the immediately promotable enemy pawn;
- only one switch is tested;
- no quiet middlegame plan or broad pawn structure is present;
- discovery compute is not economically favorable versus exact solving.

Thus strategy discovery succeeds technically and prospectively, but does not by itself establish scalable middlegame proof discovery.
