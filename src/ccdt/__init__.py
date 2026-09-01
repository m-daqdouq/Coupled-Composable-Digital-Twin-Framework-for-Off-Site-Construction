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

"""CCDT: Coupled-Composable Digital Twin framework."""

from .case_study import build_reference_system
from .interactions import (
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
from .models import DigitalTwin, Interaction, InteractionType, TwinKind, TwinState
from .system import CCDTSystem

__all__ = [
    "CCDTSystem",
    "DigitalTwin",
    "Interaction",
    "InteractionType",
    "TwinKind",
    "TwinState",
    "build_reference_system",
    "effective_factory_capacity",
    "evaluate_schedule_sync",
    "forecast_assembly_delay",
    "forecast_assembly_start",
    "hidden_interaction_information",
    "infer_logistics_state",
    "late_delivery_probability",
    "physical_coupling_prediction",
    "rework_induced_delay",
]

__version__ = "0.1.0"
