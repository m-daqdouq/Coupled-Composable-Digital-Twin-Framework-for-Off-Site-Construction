# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""First hidden-interaction algorithms described in CCDT Rev10."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Mapping

from .probability import bayesian_filter_step, expected_value, mutual_information, sigmoid


@dataclass(frozen=True, slots=True)
class ScheduleSyncResult:
    divergence: float
    out_of_sync: bool
    master_outdated_probability: float


def schedule_divergence(
    master_value: float,
    field_value: float,
    *,
    tolerance: float = 1.0,
) -> float:
    """Magnitude of Planning-vs-field DT schedule mismatch."""
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    return abs(field_value - master_value)


def evolve_schedule_divergence(
    previous_divergence: float,
    local_update: float,
    *,
    master_correction: float = 0.0,
    is_master_update_day: bool = False,
) -> float:
    """Discrete divergence drift/reconciliation model from the DT-DT case."""
    new_value = previous_divergence + local_update
    if is_master_update_day:
        new_value -= master_correction
    return new_value


def master_outdated_probability(
    divergence: float,
    time_since_master_update: float,
    *,
    beta0: float,
    beta_divergence: float,
    beta_staleness: float,
) -> float:
    """Logistic hidden-inconsistency flag probability."""
    score = (
        beta0
        + beta_divergence * abs(divergence)
        + beta_staleness * max(0.0, time_since_master_update)
    )
    return sigmoid(score)


def evaluate_schedule_sync(
    master_value: float,
    field_value: float,
    time_since_master_update: float,
    *,
    tolerance: float = 1.0,
    threshold: float = 0.7,
    beta0: float = -3.0,
    beta_divergence: float = 0.9,
    beta_staleness: float = 0.15,
) -> ScheduleSyncResult:
    divergence = schedule_divergence(master_value, field_value, tolerance=tolerance)
    probability = master_outdated_probability(
        divergence,
        time_since_master_update,
        beta0=beta0,
        beta_divergence=beta_divergence,
        beta_staleness=beta_staleness,
    )
    return ScheduleSyncResult(
        divergence=divergence,
        out_of_sync=(divergence > tolerance or probability >= threshold),
        master_outdated_probability=probability,
    )


def infer_logistics_state(
    prior: Mapping[Hashable, float],
    transition: Mapping[Hashable, Mapping[Hashable, float]],
    sensor_likelihood: Mapping[Hashable, float],
) -> dict[Hashable, float]:
    """PT->DT: infer logistics status from GPS/RFID/telematics evidence."""
    return bayesian_filter_step(prior, transition, sensor_likelihood)


def forecast_assembly_delay(
    logistics_posterior: Mapping[Hashable, float],
    delay_by_state: Mapping[Hashable, float],
) -> float:
    """PT->DT cross-update: probability-weighted expected assembly delay."""
    return expected_value(logistics_posterior, delay_by_state)


def forecast_assembly_start(
    planned_start: float,
    logistics_posterior: Mapping[Hashable, float],
    delay_by_state: Mapping[Hashable, float],
    *,
    factory_delay: float = 0.0,
) -> float:
    return (
        planned_start
        + max(0.0, factory_delay)
        + forecast_assembly_delay(logistics_posterior, delay_by_state)
    )


def hidden_interaction_information(
    joint_sensor_outcome_distribution: Mapping[tuple[Hashable, Hashable], float],
    *,
    threshold: float = 0.0,
) -> tuple[float, bool]:
    """PT->DT hidden-interaction detector using mutual information."""
    information = mutual_information(joint_sensor_outcome_distribution)
    return information, information > threshold


def physical_coupling_prediction(
    offsite_deviation: float,
    *,
    coupling_coefficient: float,
    residual: float = 0.0,
) -> float:
    """PT-PT prototype: on-site deviation induced by off-site disruption."""
    return coupling_coefficient * offsite_deviation + residual


def effective_factory_capacity(
    base_capacity: float,
    *,
    rework_command: bool,
    capacity_reduction: float,
) -> float:
    """DT->PT: capacity left for the normal queue after a rework command."""
    if base_capacity <= 0:
        raise ValueError("base_capacity must be positive")
    if capacity_reduction < 0:
        raise ValueError("capacity_reduction must be non-negative")
    effective = base_capacity - (capacity_reduction if rework_command else 0.0)
    if effective <= 0:
        raise ValueError("Rework consumes all available capacity")
    return effective


def rework_induced_delay(
    rework_workload: float,
    available_slack_time: float,
    effective_capacity: float,
) -> float:
    """Delay imposed on the next factory job by rework."""
    if rework_workload < 0 or available_slack_time < 0:
        raise ValueError("workload and slack must be non-negative")
    if effective_capacity <= 0:
        raise ValueError("effective_capacity must be positive")
    residual_workload = max(
        0.0,
        rework_workload - available_slack_time * effective_capacity,
    )
    return residual_workload / effective_capacity


def late_delivery_probability(
    manufacturing_posterior: Mapping[Hashable, float],
    late_probability_by_state: Mapping[Hashable, float],
) -> float:
    """DT->PT ripple: total probability of the next module arriving late."""
    value = expected_value(manufacturing_posterior, late_probability_by_state)
    if not 0.0 <= value <= 1.0:
        raise ValueError("Conditional late probabilities must be in [0, 1]")
    return value
