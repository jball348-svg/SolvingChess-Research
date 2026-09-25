<!--
SOLVING CHESS NORMALIZED DERIVATIVE
original_filename: G7_Proof_Language_Specification_v0_3.docx
original_sha256: 2f99ee91e476f95a669747cbaf5f3cca9de693b3b6fd42e16b839c57464cfc41
derivative_filename: G7_Proof_Language_Specification_v0_3.md
conversion_method: solving-chess-stdlib-ooxml-to-markdown
conversion_tool_version: 1.0.0
conversion_timestamp: 2026-08-13T00:00:00Z
authority: This Markdown is a derivative; the immutable DOCX is controlling authority.
-->

> **Derivative notice:** This Markdown is an agent-facing extraction. The immutable DOCX named above remains controlling authority.

G7 Proof Language Specification v0.3
Frozen after G7.9 cross-level synthesis
11 August 2026
| STATUS | FROZEN G7 CLOSEOUT SPECIFICATION |
| --- | --- |
This specification supersedes G7 proof-language v0.2 for classification and packaging. It preserves G6 object IDs and historical provenance while adding strategy-language fields and Filter-Pivot factorization. It separates universal game-graph operations, reusable schemas, conditional chess theorems and representation-dependent metrics.
# 1. Type discipline
- Every proof object is typed by game graph, side-to-move ownership, target semantics, terminal/shortcut semantics, material-signature dependencies and rank convention where ranks are used.
- A graph-general theorem may be reused across chess arenas only when the concrete arena satisfies the theorem input contract.
- A chess theorem remains finite/domain-specific unless quantified and independently certified beyond that domain.
- New names do not create new proof objects: dependency/subsumption must be checked before promotion.
- Exact membership is primary; learned classifiers, local grammars and heuristic features are proposal mechanisms until exhaustively certified.
# 2. Universal/core operations
## STRICT_ATTRACTOR(T)
Least fixed point containing exact target T. Attacker-owned state enters when at least one legal successor is in the set; defender-owned state enters only when it has a legal continuation and every legal successor is in the set. External transitions follow the declared typed shortcut/terminal contract.
## ROLE_DUAL_SANCTUARY_ATTRACTOR(S)
Same fixed-point machinery with roles/goal reversed to certify defender force into an exact draw/sanctuary set S. Terminal exits are accepted only when explicitly typed as safe defender outcomes.
## BRANCH_KERNEL(A,B)
For two alternative exact target attractors A and B, identify defender-owned states outside their separate explanations whose legal replies lie within A∪B and genuinely branch between alternatives. Residual backward closure produces the irreducible union-only BRIDGE population.
## FINITE_N_HYPERKERNEL(A1…An)
Generalizes Branch-Kernel to n alternatives. Proper-subunion explanations are removed first; defender states whose replies are covered only by the full alternative family seed the irreducible n-way region; residual closure reconstructs it.
## FILTERED_ATTRACTOR(T,F)
Strict attractor with the original game graph retained and a semantic attacker-edge filter F. Attacker existential admission requires an F-admissible edge; defender universal admission is unchanged. Optional target-entry exemptions are declared explicitly. The object certifies a strategy-language-constrained forcing proof.
## FILTER_PIVOT_FACTORIZATION(T,F)
Let A=Attr(T), C=Attr_F(T), Q=A\C. Define K_F as attacker-owned states in Q with an F-excluded edge into C. Then Q≠∅ iff K_F≠∅, and Q is exactly the ordinary residual backward closure of K_F outside C. This factors the first necessary departure from a strategy language.
## DEPENDENCY_DAG / SUBSUMPTION
Proof objects may depend on lower-material truths or other derived objects. The dependency graph must remain acyclic by semantic/material/object version. Candidate abstractions are rejected when a weaker dependency set proves a strictly broader theorem under the same guards.
# 3. Reusable schemas and diagnostics
## PROJECT
Map a full state to an exact lower-material/subgame state under a declared deletion/exchange projection. PROJECT itself transfers truth only as a counterfactual observation; restoration requires a separate theorem/guard.
## RESOURCE_SAFE_TARGET
Construct semantic targets from conversion possibility plus resource guards required by the arena: promotion/terminal validity, conversion path, opponent race, opponent access/check/capture resources, and lower-material target typing.
## RESIDUAL
Subtract already certified proof objects from an exact outcome population before searching for additional structure.
## GROUP_OUT
Quotient/group residual states by declared variables or symmetries to expose dependency on omitted resources without claiming a theorem.
## LOCALIZATION_LIFT
Measure whether a geometric/race slab adds discriminatory information beyond its ambient residual prevalence; saturated 100% slabs with zero lift are negative diagnostics, not compression.
## STOP
Bound local grammar fitting when description cost, held-out transfer or residual structure becomes lookup-scale. Preserve the floor rather than encoding square tables.
## CERTIFY
Flatten the proposed proof object on its stated finite domain and scan exhaustively; record hashes, dependency versions, terminal semantics, and all counterexamples.
# 4. Conditional finite theorems / guards retained at G7 closeout
| Object / family | Classification | Frozen meaning |
| --- | --- | --- |
| G6 FAR5 | Conditional finite theorem | Exact restoration theorem on its frozen same-side domain. |
| G6 FAR3 sliders / knight exception | Conditional finite theorem | Exact finite restoration laws with preserved exception domain. |
| Faithful wrong-colour sanctuary | Conditional chess theorem | Under faithful continuation, lower wrong-colour h8 sanctuary is exact. |
| G7 RESTORE.CONVERSION_SAFE_WHITE_MOBILE | Conditional sharpening | Blocks promotion-square / promotion-capture-cone interference; does not subsume FAR3/FAR5. |
| G7 SANCTUARY_ACCESS_GUARD | Conditional guard family | F09 preservation when added resource cannot access critical corner; F10 exact terminal destruction when it can. |
# 5. Representation-dependent strategy fields and metrics
- CHECK is the first certified attacker-edge language: every pre-target attacker move gives check, with an explicitly declared target-entry exemption where used.
- strategy_retention = |Attr_F(T)| / |Attr(T)|. This is descriptive and topology-dependent.
- pivot_amplification = |Attr(T)\Attr_F(T)| / |K_F|. This measures compression of the strategy-language complement.
- Local critical-manifold/clock/grammar representations remain arena-sensitive and are not promoted merely because their generating features recur.
# 6. Multi-level proof DAG composition
Derived objects may be reused as typed targets. G7 validates the chain: exact lower-material endpoints → finite-n Hyperkernel → irreducible derived region → strict attractor to the derived region → filtered attractor under a strategy language → Filter-Pivot factorization of the strategy complement. Each node retains its own object ID, domain, dependency hashes and certificate semantics.
Destination composition and strategy-language composition are orthogonal dimensions. Branch/Hyperkernel factors defender choice among destinations. Filter-Pivot factors the attacker’s first necessary departure from a move language. One object must not be substituted for the other merely because their certified populations overlap.
# 7. Explicit non-promotions
| Candidate label | Disposition | Reason |
| --- | --- | --- |
| Exchange Funnel | Not a new object | Reduces to Branch-Kernel once material endpoints are typed as exact targets. |
| Transition Hyperkernel | Not a new object | Reduces exactly to finite-n Hyperkernel. |
| Multi-Projection Consistency | Rejected by subsumption | Guarded single projection is strictly broader; second projection adds no proof power. |
| CHECK corridor as universal chess law | Not promoted | The operator transfers, but CHECK retention varies strongly by topology. |
| Sanctuary Lift as new class | Not promoted | Preservation/destruction is naturally represented as guarded RESTORE/sanctuary typing. |
# 8. Certification package requirements
- Object version and semantic type signature.
- Exact target/sanctuary/filter definition in code or canonical predicate form.
- Dependencies on lower-material truth/proof objects, with hashes.
- State-domain manifest and exact membership counts.
- Verifier/replay command and independent fixed-point or predecessor audit where feasible.
- Counterexample set for any rejected/conditional candidate.
- Sparse kernel/pivot payload plus reconstruction rule for compositional certificates.
- No accepted result may depend on incomplete retrograde propagation or a helper whose dependency truth was not loaded.
# 9. Version transition
v0.3 promotes FILTER_PIVOT to the universal/core layer after G7.7 backward fire; retains FILTERED_ATTRACTOR as a universal typed strategy-language reachability operator; demotes Multi-Projection Consistency by subsumption; keeps restoration/sanctuary access results conditional; and formalizes mixed destination × strategy proof DAGs demonstrated in G7.8.
