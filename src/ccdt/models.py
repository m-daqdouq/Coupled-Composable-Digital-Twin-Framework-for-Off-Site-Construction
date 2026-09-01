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

"""Core state and interaction models for CCDT."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class TwinKind(str, Enum):
    PLANNING = "planning"
    PROCUREMENT = "procurement"
    COMPONENTS_FABRICATION = "components_fabrication"
    MODULES_MANUFACTURING = "modules_manufacturing"
    LOGISTICS = "logistics"
    ASSEMBLY = "assembly"


class InteractionType(str, Enum):
    PT_PT = "PT-PT"
    DT_DT = "DT-DT"
    PT_DT = "PT-DT"
    DT_PT = "DT-PT"


@dataclass(slots=True)
class TwinState:
    """State tuple X_i(t) = {D, P, S, A, R, E} from the CCDT study."""

    timestep: int
    digital: dict[str, Any] = field(default_factory=dict)
    physical: dict[str, Any] = field(default_factory=dict)
    sensors: dict[str, Any] = field(default_factory=dict)
    actions: dict[str, Any] = field(default_factory=dict)
    rewards: dict[str, float] = field(default_factory=dict)
    events: dict[str, Any] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def patch(
        self,
        *,
        digital: dict[str, Any] | None = None,
        physical: dict[str, Any] | None = None,
        sensors: dict[str, Any] | None = None,
        actions: dict[str, Any] | None = None,
        rewards: dict[str, float] | None = None,
        events: dict[str, Any] | None = None,
    ) -> None:
        for target, values in (
            (self.digital, digital),
            (self.physical, physical),
            (self.sensors, sensors),
            (self.actions, actions),
            (self.rewards, rewards),
            (self.events, events),
        ):
            if values:
                target.update(values)
        self.updated_at = datetime.now(timezone.utc)


@dataclass(slots=True)
class DigitalTwin:
    twin_id: str
    kind: TwinKind
    state: TwinState
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Interaction:
    source_twin: str
    target_twin: str
    interaction_type: InteractionType
    description: str = ""
    designed: bool = True
    mediator: str | None = None


@dataclass(slots=True)
class EventRecord:
    timestep: int
    twin_id: str
    event: str
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
