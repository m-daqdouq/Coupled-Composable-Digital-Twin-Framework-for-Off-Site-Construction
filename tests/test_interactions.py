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

import math

from ccdt import (
    effective_factory_capacity,
    evaluate_schedule_sync,
    forecast_assembly_delay,
    forecast_assembly_start,
    hidden_interaction_information,
    infer_logistics_state,
    late_delivery_probability,
    physical_coupling_prediction,
    rework_induced_delay,
)
from ccdt.interactions import evolve_schedule_divergence


def test_schedule_divergence_and_reconciliation():
    assert evolve_schedule_divergence(3.0, 1.0) == 4.0
    assert evolve_schedule_divergence(
        3.0,
        1.0,
        master_correction=3.0,
        is_master_update_day=True,
    ) == 1.0

    result = evaluate_schedule_sync(
        master_value=10.0,
        field_value=13.0,
        time_since_master_update=14.0,
    )
    assert result.divergence == 3.0
    assert result.out_of_sync


def test_sensor_filter_and_assembly_cross_update():
    posterior = infer_logistics_state(
        prior={"on_time": 0.8, "delayed": 0.2},
        transition={
            "on_time": {"on_time": 0.9, "delayed": 0.1},
            "delayed": {"on_time": 0.3, "delayed": 0.7},
        },
        sensor_likelihood={"on_time": 0.15, "delayed": 0.85},
    )
    assert math.isclose(sum(posterior.values()), 1.0)
    assert posterior["delayed"] > posterior["on_time"]

    expected_delay = forecast_assembly_delay(
        {"on_time": 0.3, "delayed": 0.7},
        {"on_time": 0.0, "delayed": 2.0},
    )
    assert math.isclose(expected_delay, 1.4)
    assert math.isclose(
        forecast_assembly_start(
            20.0,
            {"on_time": 0.3, "delayed": 0.7},
            {"on_time": 0.0, "delayed": 2.0},
        ),
        21.4,
    )


def test_mutual_information_detects_dependency():
    information, active = hidden_interaction_information(
        {
            ("normal", "on_time"): 0.45,
            ("normal", "late"): 0.05,
            ("delay_signal", "on_time"): 0.10,
            ("delay_signal", "late"): 0.40,
        },
        threshold=0.1,
    )
    assert information > 0.1
    assert active


def test_pt_pt_and_dt_pt_ripple_models():
    assert math.isclose(
        physical_coupling_prediction(
            2.0,
            coupling_coefficient=0.75,
            residual=0.25,
        ),
        1.75,
    )

    capacity = effective_factory_capacity(
        10.0,
        rework_command=True,
        capacity_reduction=2.0,
    )
    assert capacity == 8.0
    assert math.isclose(
        rework_induced_delay(
            rework_workload=40.0,
            available_slack_time=4.0,
            effective_capacity=capacity,
        ),
        1.0,
    )

    risk = late_delivery_probability(
        {"on_time": 0.55, "delayed": 0.45},
        {"on_time": 0.1, "delayed": 0.8},
    )
    assert math.isclose(risk, 0.415)
