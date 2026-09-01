# Coupled–Composable Digital Twin (CCDT) Framework for Off-Site Construction

An open-source research implementation of a **Coupled–Composable Digital Twin (CCDT)** framework for construction project management, with an initial manufactured-housing use case.

The framework treats multiple digital twins as a **system-of-systems (SoS)**: each twin operates as a semi-independent module, while a coupled coordination layer manages cross-twin data flows, hidden interactions, probabilistic inference, and system-wide decision support.

> **Status:** Early research prototype / open-source foundation (v0.1).
>
> This repository is aligned with the current **CCDT Rev10** study manuscript. The implementation will evolve as research algorithms, datasets, and validation materials are released.

## Research problem

Construction digital twins are frequently implemented as siloed models. In off-site construction, however, planning, procurement, fabrication, module manufacturing, logistics, and field assembly are interdependent. Changes in one subsystem can propagate physically or digitally into others, even when the dependency is not explicitly modeled.

CCDT focuses on detecting, representing, and managing these **hidden interactions** so that multi-DT systems can operate as an integrated whole rather than as isolated twins.

## Case-study digital twins

The reference manufactured-housing system uses six composable digital twins:

| ID | Digital Twin | Primary scope |
|---|---|---|
| PL | Planning | BIM, master schedule, sequencing, baselines |
| PR | Procurement | materials, suppliers, orders, availability |
| CF | Components Fabrication | prefabricated component production and quality |
| MM | Modules Manufacturing | module assembly, factory throughput, rework, capacity |
| LG | Logistics | routing, shipment status, GPS/RFID, delivery risk |
| AS | Assembly | site readiness, crane/installation sequence, field progress |

The initial scenario represents **50 modular homes**, each composed of **four prefabricated modules** (200 modules total), in a flood-prone Louisiana context.

## CCDT state model

Each twin is modeled at timestep `t` using the generalized state tuple:

```text
X_i(t) = { D_i(t), P_i(t), S_i(t), A_i(t), R_i(t), E_i(t) }
```

where:

- `D` = digital state
- `P` = physical state
- `S` = sensor observations
- `A` = actions
- `R` = reward / performance state
- `E` = event or process of interest

The coupled fleet layer coordinates these local states across twins and across timesteps (`t-1`, `t`, `t+1`).

## Four hidden-interaction classes

CCDT explicitly represents four interaction categories:

1. **PT–PT** — Physical-to-Physical
2. **DT–DT** — Digital-to-Digital
3. **PT–DT** — Physical-to-Digital
4. **DT–PT** — Digital-to-Physical

Examples include factory disruption propagating to field operations, schedule divergence between Planning and Assembly twins, GPS/RFID updates shifting assembly forecasts, and digital rework commands changing physical factory capacity.

## Probabilistic reasoning

The research framework uses a **Probabilistic Graphical Model (PGM)** / **Dynamic Bayesian Network (DBN)** perspective to:

- update posterior beliefs as new sensor and project data arrive;
- identify conditional dependencies across twins;
- detect hidden cross-twin interactions;
- propagate delay/risk information;
- infer unobserved states;
- evaluate the effects of actions and mitigation decisions.

The software roadmap separates three main probabilistic layers:

1. **State transition layer** — evolution of digital/physical states across time;
2. **Event interpretation layer** — mapping state into events/processes of interest;
3. **Decision/reward layer** — evaluating performance effects and response actions.

## KPI domains

The reference study monitors six KPI domains:

- Cost
- Time
- Quality
- Sustainability
- Risk
- Safety

## Repository structure

```text
.
├── src/ccdt/               # Core CCDT package
├── examples/               # Reproducible demonstrations
├── data/                   # Synthetic/public benchmark data
├── tests/                  # Automated tests
├── docs/                   # Architecture, methodology, and use-case docs
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── SECURITY.md
├── ROADMAP.md
├── CITATION.cff
├── LICENSE
└── pyproject.toml
```

## Planned open-source implementation

The first implementation milestones are:

- composable twin registry and lifecycle model;
- six-twin manufactured-housing reference configuration;
- state tuple and timestamped event history;
- interaction graph for PT–PT, DT–DT, PT–DT, and DT–PT links;
- Planning/Assembly schedule-divergence detector;
- sensor-to-logistics Bayesian update;
- logistics-to-assembly probabilistic cross-update;
- manufacturing rework/ripple-risk model;
- mutual-information based hidden-interaction detector;
- common data environment (CDE) abstractions;
- reproducible synthetic case-study data;
- automated tests and continuous integration.

## What is not claimed yet

This repository should be treated as a **research prototype**, not a production control system. The public implementation will distinguish clearly between:

- algorithms implemented in code;
- synthetic/reference demonstrations;
- empirical validation material that can legally and ethically be released; and
- future capabilities.

In particular, system resilience under disruptions and broader multi-objective optimization are treated as future extensions unless reproducible implementation and validation artifacts are added.

## Open-source ecosystem direction

The project is being structured to support a sustainable open-source digital-twin ecosystem through modular interfaces, public contribution workflows, reproducible examples, governance, security practices, and interoperability with BIM/GIS/IoT data sources.

This makes CCDT-Offsite a concrete construction and next-generation manufacturing use case for broader open-source digital-twin ecosystem research.

## License

Apache License 2.0 (planned for the initial public release).

## Maintainer

**Mohannad Daqdouq**  
Ph.D. Student, Construction Management  
Louisiana State University

**Yongcheol Lee**  
Associate Professor, Construction Management  
Louisiana State University

## Citation

Citation metadata will be provided through `CITATION.cff` and updated when the associated manuscript/repository release is finalized.

---

**Disclaimer:** CCDT is an academic research prototype. Outputs should not be used as the sole basis for safety-critical, contractual, engineering, or operational decisions.
