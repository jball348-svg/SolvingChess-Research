# G8.3 Interim Evidence Freeze C — Six-Man Scale-Hold Recovery

**Date:** 11 August 2026  
**Stage:** G8.3 — Recover six-man scale holds  
**Status:** **CLOSED — PASS VERY STRONGLY. F03, F04 AND F06 ALL RECOVERED UNCHANGED.**

## 1. Authority and freeze rule

G8.3 attacks the prospectively frozen G7 holds without shrinking or changing their semantics. The authoritative G7 declarations are:

- **F03 `BN_opp_d7_e2`** — K+B+P vs K+N+P; White bishop on its frozen colour complex, Black knight unrestricted, pawns d7/e2; exact frozen static-valid universe **48,028,628**; G7 accepted no W/D/L.
- **F04 `RB_c7_f2`** — K+R+P vs K+B+P; rook unrestricted, Black bishop on its frozen colour complex, pawns c7/f2; exact static-valid **44,820,777**; G7 high-branch control, no W/D/L within 180 s.
- **F06 `QB_d7_e2`** — K+Q+P vs K+B+P; queen unrestricted, Black bishop on its frozen colour complex, pawns d7/e2; exact static-valid **40,499,052**; G7 high-branch control, no W/D/L within 180 s.

Terminal semantics remain the G7 brink model: ordinary mate/stalemate; no repetition/en-passant/move-count state; promotion by either side is an immediate win for the promoting side; captures transition into exact lower-material signatures.

No outcome-guided arena restriction was introduced.

## 2. Superseded reconstruction attempt

An initial G8.3 reconstruction mistakenly interpreted the phrase `bishop colour invariant` as an unrestricted 64-square bishop. That changed the arena: the frozen raw width **70,287,360** itself factors as `4096 * 2 * 4 * 33 * 65`, proving one 32-square bishop colour complex plus absence (33 slots) paired with an unrestricted mobile piece plus absence (65 slots).

The original frozen G7 source declaration was then recovered and confirmed the exact colour parameters:

- F03: `mk("BN_opp_d7_e2","B","N",0,0,"d7","e2")`
- F04: `mk("RB_c7_f2","R","B",0,1,"c7","f2")`
- F06: `mk("QB_d7_e2","Q","B",0,1,"d7","e2")`

All outputs from the over-broad reconstruction are **discarded and superseded**. No W/D/L from that run is part of this freeze.

## 3. Engine changes admitted in G8.3

Two representation/execution changes were made after G8.1/G8.2, with no change to move or terminal semantics:

1. **Packed-valid predecessor reuse.** Same-signature predecessor candidates are filtered against the already-computed packed `valid` membership rather than re-running the complete static legality/attack predicate for every predecessor.
2. **Packed-valid successor reuse.** Generated successor candidates are encoded into the current/child signature and tested against that signature's already-computed packed `valid` table rather than re-running full static legality for every edge.

The second change was prospectively regression-tested on frozen F01/F02 before use as evidence on F03/F04/F06. It reproduced, exactly:

- F01 graph **23,728,925 = 7,282,421 W + 8,205,091 B + 8,241,413 D**; full **5,105,749 = 2,506,683 W + 2,519,613 B + 79,453 D**; capture vector **255,368 / 231,650 / 981,578 / 214,347**.
- F02 graph **22,770,972 = 7,043,319 W + 7,043,319 B + 8,684,334 D**; full **4,761,076 = 2,321,127 W + 2,321,127 B + 118,822 D**; capture vector **784,233 / 784,233 / 811,070 / 811,070**.

Measured producer wall times on that regression binary were approximately **4.46 s F01 / 4.36 s F02**.

## 4. Recovered F03 exact truth

### Entire capture-closed dependency graph

**48,028,628 = 15,988,090 White wins + 16,147,057 Black wins + 15,893,481 draws.**

### Full-material SIG15

**10,631,072 = 5,381,419 W + 5,055,467 B + 194,186 D.**

Full-material percentages:

- White wins: **50.620%**
- Black wins: **47.554%**
- Draws: **1.827%**

Direct full-material capture transitions:

- SIG7: **964,540**
- SIG11: **1,204,532**
- SIG13: **1,108,688**
- SIG14: **554,624**
- total: **3,832,384**

Producer wall time: **7.81 s**  
Producer peak RSS: **81,980 kB**

This converts the G7 tractability hold into complete exact W/D/L without altering the frozen arena.

## 5. Recovered F04 exact truth

### Entire capture-closed dependency graph

**44,820,777 = 18,876,467 W + 13,279,606 B + 12,664,704 D.**

### Full-material SIG15

**9,956,314 = 5,170,590 W + 4,640,695 B + 145,029 D.**

Full-material percentages:

- White wins: **51.933%**
- Black wins: **46.611%**
- Draws: **1.457%**

Direct full-material capture transitions:

- SIG7: **1,204,113**
- SIG11: **1,411,402**
- SIG13: **485,335**
- SIG14: **1,483,432**
- total: **4,584,282**

Producer wall time: **9.65 s**  
Producer peak RSS: **77,952 kB**

G7's same unchanged arena emitted no W/D/L within 180 s. Relative to that 180 s floor, the new producer completes in less than 1/18.65 of the old floor time.

## 6. Recovered F06 exact truth

### Entire capture-closed dependency graph

**40,499,052 = 27,773,901 W + 8,530,120 B + 4,195,031 D.**

### Full-material SIG15

**8,787,241 = 5,210,861 W + 3,476,720 B + 99,660 D.**

Full-material percentages:

- White wins: **59.300%**
- Black wins: **39.566%**
- Draws: **1.134%**

Direct full-material capture transitions:

- SIG7: **1,039,257**
- SIG11: **1,556,350**
- SIG13: **1,380,393**
- SIG14: **1,539,467**
- total: **5,515,467**

Producer wall time: **12.22 s**  
Producer peak RSS: **73,236 kB**

G7's unchanged high-mobility queen control emitted no W/D/L within 180 s. Relative to that 180 s floor, the new producer completes in less than 1/14.73 of the old floor time.

## 7. Independent exhaustive verification

A separate verifier implementation consumes only the frozen arena declaration plus the packed truth bundle. It independently implements:

- state decoding/encoding;
- colour-complex restrictions;
- static legality and attack geometry;
- king, knight, bishop, rook and queen moves;
- capture-to-child-signature transitions;
- promotion legality and terminal outcome semantics;
- Bellman W/D/L obligations.

It first independently recomputes static validity over **every raw encoding**, then checks the Bellman equation over **every valid state**.

| Arena | Static-valid | Static mismatches | Bellman checked | Bellman mismatches | Verifier wall | Peak RSS |
|---|---:|---:|---:|---:|---:|---:|
| F03 | 48,028,628 | **0** | 48,028,628 | **0** | 4.58 s | 29,320 kB |
| F04 | 44,820,777 | **0** | 44,820,777 | **0** | 5.38 s | 29,320 kB |
| F06 | 40,499,052 | **0** | 40,499,052 | **0** | 6.03 s | 29,320 kB |

The independently recomputed W/D/L and full-material counts exactly equal the producer counts in all three arenas.

## 8. Packed truth hashes

Canonical G8.3 packed truth dependencies:

- F03 `BN_opp_d7_e2`: `686bdf95d6d2ec16ed22868fed9269e92c94ab2b4476728341103354ce41ad34`
- F04 `RB_c7_f2`: `a9af726992d8ec8eded325ada4d41458edb959d3cfc0967c0535207e863b4717`
- F06 `QB_d7_e2`: `fa93c352b9a0e489b323612710bc062ef27b25e08c751ce2ef98571f78e6f508`

Each packed file stores all 16 signature validity and 2-bit outcome tables and is approximately 26 MiB.

## 9. Source and binary fingerprints

Final G8.3 producer source:

`g8_3_sig_brink.cpp`  
SHA-256 `7f95ba8adc1d9eed7c6c596a8d8d42e2b7990402e6f8771a4e865c8c1291505d`

Producer binary:

SHA-256 `f4f0a592187ea3744c07157a3501d0213dd5ea33cb97904dfc362d02343d0645`

Truth-dump producer source:

SHA-256 `7717b37d8c71ec41d86e9b66afaaf0b54614676b831112650cc8cf9600e30604`

Independent verifier source:

SHA-256 `e2f5002d9d81822677f1720bd82c04e4985c024f5f0974ddfb4bba00355e9948`

Independent verifier binary:

SHA-256 `e67549aae9075a46d69b2e122ade0016cec200c9dab235e394a56600f8a27d79`

## 10. Engineering interpretation

The G7 frontier was principally an implementation frontier, not a state-count impossibility. Material-signature decomposition mattered, but G8.3 shows that **eliminating repeated legality work across already-certified signature membership** is at least as important on high-branch topologies.

The strongest evidence is F06: the queen control had fewer static-valid states than F04 but much higher branching/check density and was still a >180 s hold under the monolith. Once child/current validity becomes a reusable certified dependency instead of a repeatedly recomputed predicate, that same topology completes in ~12 s while retaining exact semantics.

This is not parallel brute force: the accepted runs are single-process/single-core in the recorded measurements.

## 11. G8.3 gate

G8 advance criterion relevant here required recovery of full exact W/D/L for at least two frozen holds, including at least one high-branch F04/F06 or seven-man F07/F08 arena.

**G8.3 exceeds the criterion:** all three scheduled six-man holds F03/F04/F06 are recovered unchanged, and both hostile high-branch controls are recovered.

## 12. Frozen verdict

**G8.3 PASS VERY STRONGLY.**

- F03: recovered unchanged — complete exact W/D/L.
- F04: recovered unchanged — complete exact W/D/L.
- F06: recovered unchanged — complete exact W/D/L.
- Static universe agreement with frozen G7: exact on all three.
- Exhaustive independent static verification: 0 mismatches on all three.
- Exhaustive independent Bellman verification: 0 mismatches on all three.
- No partial propagation accepted.
- No arena shrinking or terminal-model change.
- The erroneous over-broad bishop reconstruction is explicitly superseded and excluded.

**Next authorised stage: G8.4 — recover the seven-man wave F07/F08 unchanged, and attempt F10 full faithful truth if economically feasible.**
