# G7.8 Complexity and Certificate Economics — Freeze F

## Exact-solve wall-time baselines

| Arena | Static-valid states | Completed wall time | Approx. static states/s |
|---|---:|---:|---:|
| F01 BB opposite | 23,728,925 | 28.829 s | 823,092 |
| F02 BB same | 22,770,972 | 27.198 s | 837,230 |
| F09 fortress ascent | 16,557,288 | 20.750 s | 797,942 |

## High-branch complexity-floor controls

| Arena | Static-valid | Mean branch (prospective scan) | Check density | Exact result within 180 s |
|---|---:|---:|---:|---|
| F04 R+B | 44,820,777 | 13.454 | 6.673% | No W/D/L emitted |
| F06 Q+B | 40,499,052 | 14.897 | 15.823% | No W/D/L emitted |

Both controls passed sampled predecessor soundness/completeness audits with zero errors. The 180-second holds are execution/certificate boundaries; no partial propagation is accepted as outcome truth.

## New multi-level verifier engineering cost

F02 multi-level proof-DAG reconstruction:

- wall clock: **2.96 s**
- user CPU: **2.36 s**
- system CPU: **0.59 s**
- peak RSS: **526,588 kB**
- raw byte-mask width: **35,684,352 bytes/mask**

The high RSS is mostly the deliberately simple collection of byte-per-encoding masks. It should not be interpreted as an intrinsic proof-language cost.

## Seed payload estimates

Using sparse 64-bit state encodings solely as a descriptive comparison:

- F02 deep chain: 1,641 Hyperkernel seeds + 239 second-order Filter-Pivot seeds = **15,040 bytes** for seeds; final derived strict-attractor region 23,327 states; **0.645 seed bytes/final state**.
- F09: 517,120 Filter-Pivot seeds = **4,136,960 bytes**; ordinary target attractor 8,295,062 states; **0.499 seed bytes/final state**.

These are not standalone proof-file sizes. Semantic target/filter declarations, lower-material dependencies, move generator and terminal semantics remain required by the verifier.
