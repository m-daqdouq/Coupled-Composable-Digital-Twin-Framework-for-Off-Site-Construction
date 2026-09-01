# CCDT Open-Source Roadmap

This roadmap is aligned with the current CCDT Rev10 study and distinguishes **implemented software**, **research prototypes**, and **planned extensions**.

**Status as of August 31, 2026:** the first executable CCDT engine is implemented on `main`. The six-twin system-of-systems foundation is operational, and initial algorithms for all four hidden-interaction classes have been added. The next major technical milestone is an integrated temporal PGM/DBN workflow across `t-1`, `t`, and `t+1`.

### Status legend

- ✅ **Implemented** — available in the repository and covered by the current implementation/tests.
- 🟡 **Prototype / partial** — an initial research implementation exists, but additional modeling, integration, or validation is required.
- ⬜ **Planned** — not yet implemented.

## v0.1 — Executable research foundation

- ✅ Research README aligned with CCDT Rev10
- ✅ Python package configuration (`pyproject.toml`)
- ✅ Core twin registry and coupled fleet/system-of-systems abstraction
- ✅ Six reference twins:
  - Planning (`PL`)
  - Procurement (`PR`)
  - Components Fabrication (`CF`)
  - Modules Manufacturing (`MM`)
  - Logistics (`LG`)
  - Assembly (`AS`)
- ✅ Generalized state tuple `X_i(t) = {D, P, S, A, R, E}`
- ✅ State updates and UTC timestamps
- ✅ Timestamped event history
- ✅ System snapshots
- ✅ Four interaction types: PT–PT, DT–DT, PT–DT, DT–PT
- ✅ Designed/hidden interaction flag and interaction filtering
- ✅ Programmatic 50-home / 200-module manufactured-housing reference configuration
- ✅ Reference project metadata for manufacturing and logistics assumptions
- ✅ Runnable manufactured-housing example
- ✅ Unit tests
- ✅ GitHub Actions CI for Python 3.10, 3.11, and 3.12
- ✅ Apache License 2.0, `NOTICE`, and source-header template
- ✅ `CITATION.cff`

## v0.2 — Hidden-interaction detection and synchronization

- 🟡 Designed-versus-inferred interaction model
  - Current implementation stores whether a connection is designed or hidden.
  - Automated inference of previously unknown graph edges is still planned.
- ✅ Planning/Assembly schedule-divergence calculation
- ✅ Discrete schedule divergence evolution/reconciliation prototype
- ✅ Probabilistic outdated-master schedule flag using divergence and update staleness
- ⬜ Calibrated Bayesian outdated-master model using empirical/project data
- ⬜ Interaction strength/confidence metadata
- ⬜ Co-evolution analysis across twin state histories
- ⬜ Event-log dependency discovery
- ⬜ Hidden-interaction alert interface
- ⬜ Graph-level visualization of designed versus inferred dependencies

## v0.3 — Temporal probabilistic inference layer **(next major milestone)**

- 🟡 Basic probability utilities and discrete Bayesian filtering
- ✅ Sensor-derived Logistics posterior update
- ✅ Probability-weighted Logistics → Assembly delay propagation
- ✅ Assembly start-shift calculation from logistics posterior and factory delay
- ✅ Mutual-information hidden-dependency detector
- ⬜ Explicit PGM/DBN abstraction linking twin states across `t-1`, `t`, and `t+1`
- ⬜ State-transition layer integrated with `TwinState`
- ⬜ Cross-twin conditional dependency graph
- ⬜ Reusable conditional probability table (CPT) objects
- ⬜ Event/process interpretation layer for `E_i(t)`
- ⬜ Decision/action layer for `A_i(t)`
- ⬜ Reward/KPI evaluation layer for `R_i(t)`
- ⬜ Automatic posterior propagation across multiple connected twins
- ⬜ Parameter-learning/calibration workflow from historical or sensor data
- ⬜ Temporal inference tests using multi-step scenarios

## v0.4 — Physical ripple-risk and mitigation modeling

- ✅ PT–PT physical coupling prototype for off-site disruption → on-site deviation
- ✅ DT–PT rework-command model
- ✅ Effective factory-capacity calculation under rework
- 🟡 Rework-induced downstream delay model
  - Current implementation models workload, available slack, and effective capacity.
  - A full discrete-event factory queue is not yet implemented.
- ✅ Downstream late-delivery probability from manufacturing posterior states
- ✅ Assembly start-shift estimation
- ⬜ Factory queue/resource simulation
- ⬜ Resource-buffer mitigation controls
- ⬜ Overtime / additional-truck mitigation controls
- ⬜ Expected delay-cost / penalty comparison
- ⬜ Risk-aware mitigation selection
- ⬜ Multi-twin ripple propagation beyond one downstream link

## v0.5 — Interoperability and Common Data Environment

- ⬜ Common Data Environment (CDE) abstraction
- ⬜ JSON schemas for twin state, event, interaction, and provenance records
- ⬜ Data validation and versioned schemas
- ⬜ BIM/IFC adapter concepts and examples
- ⬜ GIS integration examples
- ⬜ GPS/RFID/IoT event adapters
- ⬜ Message/event interface for cross-twin synchronization
- ⬜ Import/export interface for external DT platforms
- ⬜ uGRIDD-compatible data exchange examples where licensing and access permit

## v0.6 — Reproducibility, validation, and open-source ecosystem

- ✅ Reproducible Python demonstration example
- ✅ Automated test suite and CI foundation
- ✅ Apache-2.0 licensing foundation
- ✅ Citation metadata
- ⬜ Public synthetic module-level dataset
- ⬜ Public synthetic event-log dataset
- ⬜ Reproducible notebooks for the four interaction scenarios
- ⬜ Comparison of modeled results against the Rev10 case-study outputs
- ⬜ Sensitivity analysis for demonstration/calibration parameters
- ⬜ Contribution guidelines (`CONTRIBUTING.md`)
- ⬜ Governance model (`GOVERNANCE.md`)
- ⬜ Security policy (`SECURITY.md`)
- ⬜ Code of Conduct
- ⬜ Issue and pull-request templates
- ⬜ Release/versioning policy
- ⬜ Documentation site/API reference
- ⬜ Archived DOI release through Zenodo or an equivalent repository

## Public-release readiness

The repository is currently a research-development repository. Before the first formal public release:

- ✅ Include Apache License 2.0
- ✅ Include `NOTICE`
- ✅ Include `CITATION.cff`
- ✅ Add automated tests and CI
- ⬜ Confirm the appropriate copyright owner/name for the Apache source-file header
- ⬜ Add contribution, governance, security, and conduct documents
- ⬜ Confirm that no proprietary, restricted, confidential, or credential-bearing files are included
- ⬜ Clearly label synthetic/reference data and demonstration parameters
- ⬜ Create a tagged `v0.1.0` release
- ⬜ Change repository visibility from private to public when release checks are complete

## Validation boundary

The current software should be treated as a **research prototype**. The implemented algorithms reproduce the structure and interaction logic of the CCDT Rev10 framework, but demonstration probabilities, coefficients, thresholds, and scenario parameters are not presented as empirically calibrated values unless supporting validation data are added to the repository.

## Future research extensions

The current Rev10 study places the following beyond the core hidden-interaction-management contribution, so they are not presented as completed capabilities:

- system resilience under disruptions;
- broader multi-objective optimization;
- advanced autonomous control;
- large-scale empirical validation across multiple projects;
- production-grade cyber-physical actuation;
- production-grade security, privacy, and deployment hardening.
