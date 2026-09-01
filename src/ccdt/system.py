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

"""Coupled-composable twin registry and coordination layer."""

from __future__ import annotations

from copy import deepcopy

from .models import DigitalTwin, EventRecord, Interaction, InteractionType, TwinKind, TwinState


REFERENCE_TWINS: tuple[tuple[str, TwinKind], ...] = (
    ("PL", TwinKind.PLANNING),
    ("PR", TwinKind.PROCUREMENT),
    ("CF", TwinKind.COMPONENTS_FABRICATION),
    ("MM", TwinKind.MODULES_MANUFACTURING),
    ("LG", TwinKind.LOGISTICS),
    ("AS", TwinKind.ASSEMBLY),
)


class CCDTSystem:
    """System-of-systems coordination layer for composable digital twins."""

    def __init__(self) -> None:
        self.twins: dict[str, DigitalTwin] = {}
        self.interactions: list[Interaction] = []
        self.events: list[EventRecord] = []

    @classmethod
    def manufactured_housing_reference(cls, timestep: int = 0) -> "CCDTSystem":
        system = cls()
        for twin_id, kind in REFERENCE_TWINS:
            system.register_twin(
                DigitalTwin(
                    twin_id=twin_id,
                    kind=kind,
                    state=TwinState(timestep=timestep),
                )
            )
        return system

    def register_twin(self, twin: DigitalTwin) -> None:
        if twin.twin_id in self.twins:
            raise ValueError(f"Twin {twin.twin_id!r} already exists")
        self.twins[twin.twin_id] = twin

    def connect(
        self,
        source_twin: str,
        target_twin: str,
        interaction_type: InteractionType,
        *,
        description: str = "",
        designed: bool = True,
        mediator: str | None = None,
    ) -> Interaction:
        self._require_twin(source_twin)
        self._require_twin(target_twin)
        interaction = Interaction(
            source_twin=source_twin,
            target_twin=target_twin,
            interaction_type=interaction_type,
            description=description,
            designed=designed,
            mediator=mediator,
        )
        self.interactions.append(interaction)
        return interaction

    def update_state(self, twin_id: str, **patches: dict) -> TwinState:
        twin = self._require_twin(twin_id)
        twin.state.patch(**patches)
        return twin.state

    def advance(self, timestep: int) -> None:
        for twin in self.twins.values():
            if timestep < twin.state.timestep:
                raise ValueError("Cannot move a twin backward in time")
            twin.state.timestep = timestep

    def log_event(self, twin_id: str, event: str, **payload: object) -> EventRecord:
        twin = self._require_twin(twin_id)
        record = EventRecord(
            timestep=twin.state.timestep,
            twin_id=twin_id,
            event=event,
            payload=dict(payload),
        )
        self.events.append(record)
        twin.state.events[event] = dict(payload)
        return record

    def snapshot(self) -> dict[str, object]:
        return {
            "twins": deepcopy(self.twins),
            "interactions": deepcopy(self.interactions),
            "events": deepcopy(self.events),
        }

    def interactions_for(
        self,
        *,
        twin_id: str | None = None,
        interaction_type: InteractionType | None = None,
        hidden_only: bool = False,
    ) -> list[Interaction]:
        items = self.interactions
        if twin_id is not None:
            items = [
                i for i in items
                if i.source_twin == twin_id or i.target_twin == twin_id
            ]
        if interaction_type is not None:
            items = [i for i in items if i.interaction_type == interaction_type]
        if hidden_only:
            items = [i for i in items if not i.designed]
        return list(items)

    def _require_twin(self, twin_id: str) -> DigitalTwin:
        try:
            return self.twins[twin_id]
        except KeyError as exc:
            raise KeyError(f"Unknown twin: {twin_id}") from exc
