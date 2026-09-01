# CCDT Open-Source Roadmap

This roadmap is aligned with the current CCDT Rev10 study and distinguishes implemented research foundations from future extensions.

## v0.1 — Research-faithful open-source foundation

- [x] Public-facing research README aligned with Rev10
- [ ] Core twin registry and coupled fleet abstraction
- [ ] Six reference twins: Planning, Procurement, Components Fabrication, Modules Manufacturing, Logistics, Assembly
- [ ] State tuple `X_i(t) = {D, P, S, A, R, E}`
- [ ] Timestamped event history
- [ ] Four interaction types: PT–PT, DT–DT, PT–DT, DT–PT
- [ ] Synthetic 50-home / 200-module reference scenario
- [ ] Unit tests and CI

## v0.2 — Hidden-interaction detection

- [ ] Designed-versus-inferred interaction graph
- [ ] Planning/Assembly schedule-divergence detector
- [ ] Outdated-master Bayesian flag
- [ ] Interaction strength metadata
- [ ] Co-evolution/event-log analysis
- [ ] Hidden-interaction alert interface

## v0.3 — Probabilistic inference layer

- [ ] PGM/DBN abstraction
- [ ] State-transition layer
- [ ] Event/process interpretation layer
- [ ] Decision/reward layer
- [ ] Conditional probability table support
- [ ] Bayesian filtering for sensor-derived logistics state
- [ ] Posterior propagation from Logistics to Assembly
- [ ] Mutual-information interaction detector

## v0.4 — DT→PT ripple-risk modeling

- [ ] Rework-command model
- [ ] Factory capacity and queue effects
- [ ] Downstream late-delivery probability
- [ ] Assembly start-shift estimation
- [ ] Mitigation controls such as resource buffers/overtime
- [ ] Expected penalty/risk comparison

## v0.5 — Interoperability and common data environment

- [ ] Common Data Environment abstraction
- [ ] JSON schemas and provenance metadata
- [ ] BIM/IFC adapter concepts
- [ ] GIS integration examples
- [ ] IoT/GPS/RFID event adapters
- [ ] Message/event interface for cross-twin synchronization
- [ ] uGRIDD-compatible data export/import examples where licensing permits

## v0.6 — Reproducibility and community ecosystem

- [ ] Reproducible benchmark notebooks/examples
- [ ] Public synthetic datasets
- [ ] Contribution guidelines
- [ ] Governance model
- [ ] Security policy
- [ ] Citation metadata
- [ ] Release/versioning policy
- [ ] Documentation site

## Future research extensions

The current Rev10 study explicitly places the following beyond the core interaction-management contribution, so they are not presented as completed capabilities:

- system resilience under disruptions;
- broader multi-objective optimization;
- advanced autonomous control;
- large-scale empirical validation across multiple projects;
- production-grade cyber-physical actuation.
