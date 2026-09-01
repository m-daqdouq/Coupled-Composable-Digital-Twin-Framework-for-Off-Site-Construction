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

"""Reproducible manufactured-housing CCDT demonstration."""

from ccdt import (
    build_reference_system,
    effective_factory_capacity,
    evaluate_schedule_sync,
    forecast_assembly_start,
    hidden_interaction_information,
    infer_logistics_state,
    late_delivery_probability,
    rework_induced_delay,
)


def main() -> None:
    system = build_reference_system()

    # DT-DT: field schedule drifts two days behind a stale master schedule.
    sync = evaluate_schedule_sync(
        master_value=20.0,
        field_value=22.0,
        time_since_master_update=10.0,
    )

    # PT-DT: Module #8 truck evidence indicates a high chance of delay.
    logistics_posterior = infer_logistics_state(
        prior={"on_time": 0.8, "delayed": 0.2},
        transition={
            "on_time": {"on_time": 0.9, "delayed": 0.1},
            "delayed": {"on_time": 0.3, "delayed": 0.7},
        },
        sensor_likelihood={"on_time": 0.15, "delayed": 0.85},
    )
    predicted_start = forecast_assembly_start(
        planned_start=30.0,
        logistics_posterior=logistics_posterior,
        delay_by_state={"on_time": 0.0, "delayed": 2.0},
    )

    # Mutual-information detector for a sensor-driven hidden interaction.
    information_bits, active = hidden_interaction_information(
        {
            ("normal", "on_time"): 0.45,
            ("normal", "late"): 0.05,
            ("delay_signal", "on_time"): 0.10,
            ("delay_signal", "late"): 0.40,
        },
        threshold=0.1,
    )

    # DT-PT: assembly rework diverts factory capacity and raises ripple risk.
    capacity = effective_factory_capacity(
        10.0,
        rework_command=True,
        capacity_reduction=2.0,
    )
    factory_delay = rework_induced_delay(
        rework_workload=40.0,
        available_slack_time=4.0,
        effective_capacity=capacity,
    )
    late_risk = late_delivery_probability(
        manufacturing_posterior={"on_time": 0.55, "delayed": 0.45},
        late_probability_by_state={"on_time": 0.1, "delayed": 0.8},
    )

    system.log_event("LG", "module_8_transit_update", posterior=logistics_posterior)
    system.log_event("AS", "module_8_forecast_shift", predicted_start=predicted_start)

    print("CCDT reference twins:", ", ".join(system.twins))
    print("Schedule divergence:", round(sync.divergence, 3))
    print("Master outdated probability:", round(sync.master_outdated_probability, 3))
    print("Logistics posterior:", logistics_posterior)
    print("Predicted Module #8 assembly start:", round(predicted_start, 3))
    print("Sensor/outcome mutual information (bits):", round(information_bits, 3))
    print("Hidden PT-DT interaction active:", active)
    print("Rework-induced factory delay:", round(factory_delay, 3))
    print("Late-delivery ripple probability:", round(late_risk, 3))


if __name__ == "__main__":
    main()
