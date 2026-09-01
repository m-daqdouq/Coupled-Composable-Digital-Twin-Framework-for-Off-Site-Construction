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

"""Manufactured-housing reference configuration from CCDT Rev10."""

from __future__ import annotations

from .models import InteractionType
from .system import CCDTSystem


def build_reference_system() -> CCDTSystem:
    """Create the six-twin, 50-home / 200-module CCDT reference system."""
    system = CCDTSystem.manufactured_housing_reference(timestep=0)

    system.twins["PL"].metadata.update(
        homes=50,
        modules_per_home=4,
        total_modules=200,
        context="flood-prone Louisiana",
    )
    system.twins["MM"].metadata.update(
        average_module_production_days=5.0,
        production_std_days=0.5,
    )
    system.twins["LG"].metadata.update(
        modules_per_truck=2,
        estimated_truck_trips=100,
        target_modules_per_week=10,
    )

    system.connect(
        "MM", "AS", InteractionType.PT_PT,
        description="Physical module flow from factory to site through logistics",
        mediator="Logistics",
    )
    system.connect(
        "PL", "AS", InteractionType.DT_DT,
        description="Master schedule and field schedule synchronization",
    )
    system.connect(
        "LG", "AS", InteractionType.PT_DT,
        description="GPS/RFID transit evidence updates assembly forecast",
        mediator="GPS/RFID/IoT",
    )
    system.connect(
        "AS", "MM", InteractionType.DT_PT,
        description="Assembly rework command reprioritizes physical factory queue",
        mediator="human/actuator",
    )
    return system
