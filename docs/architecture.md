# CCDT Architecture

## System-of-Systems View

CCDT models a construction project as a network of semi-independent digital twins coordinated through a coupled fleet layer. Each twin retains local state and domain responsibility, while the fleet layer supports cross-twin synchronization, probabilistic inference, and detection of hidden dependencies.

## Reference Twin Set

The manufactured-housing case contains six twins:

- Planning
- Procurement
- Components Fabrication
- Modules Manufacturing
- Logistics
- Assembly

## State Representation

For twin `i` at timestep `t`:

```text
X_i(t) = { D_i(t), P_i(t), S_i(t), A_i(t), R_i(t), E_i(t) }
```

- `D`: digital state
- `P`: physical state
- `S`: sensor observations
- `A`: actions
- `R`: reward/performance
- `E`: event/process of interest

The model evolves across `t-1`, `t`, and `t+1`, which allows synchronous, baseline-to-current, and predictive relationships to be represented.

## Hidden Interaction Layer

CCDT distinguishes four interaction classes:

### PT–PT
Physical processes influence other physical processes, sometimes through mediators such as transportation or shared resources.

### DT–DT
Digital states or models influence other digital twins through shared schedules, databases, algorithms, or message exchange.

### PT–DT
Physical conditions or sensor observations update a digital model, potentially in another domain.

### DT–PT
A digital decision changes a physical process, such as a rework command changing factory capacity or a logistics decision changing a truck route.

## Probabilistic Graphical Model

The CCDT research architecture uses a Bayesian/PGM perspective to represent conditional dependencies among state variables and events.

The implementation is organized into three logical layers:

1. **State transition** — how local and cross-twin state evolves over time.
2. **Event interpretation** — how digital states imply events/processes of interest.
3. **Decision/reward evaluation** — how states, events, observations, and actions influence performance outcomes.

A dynamic Bayesian network is an appropriate computational representation when temporal dependencies are explicitly modeled.

## Example Cross-Twin Pathways

```text
Factory physical disruption
        |
        v
Manufacturing state
        |
        v
Logistics risk posterior
        |
        v
Assembly forecast shift
```

```text
Assembly defect detected
        |
        v
Digital rework command
        |
        v
Factory physical queue/capacity change
        |
        v
Downstream delivery risk
```

```text
Assembly daily field updates
        |
        v
Planning/Assembly schedule divergence
        |
        v
Outdated-master probability
        |
        v
Potential Logistics misalignment
```

## Common Data Environment

The CDE is treated as a shared information layer for project data, event logs, model states, and probabilistic parameters. A mature implementation should maintain provenance, timestamps, identifiers, schema versions, and access controls.

## Design Principle

The objective is not a single monolithic twin. The architectural goal is **composability with explicit coupling**: twins remain replaceable and domain-specific, while interdependencies are represented, measured, and governed at the system level.
