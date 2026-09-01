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

from ccdt import InteractionType, build_reference_system


def test_reference_system_has_six_study_twins():
    system = build_reference_system()
    assert list(system.twins) == ["PL", "PR", "CF", "MM", "LG", "AS"]
    assert system.twins["PL"].metadata["total_modules"] == 200


def test_reference_system_contains_all_four_interaction_types():
    system = build_reference_system()
    assert {item.interaction_type for item in system.interactions} == {
        InteractionType.PT_PT,
        InteractionType.DT_DT,
        InteractionType.PT_DT,
        InteractionType.DT_PT,
    }


def test_state_tuple_can_be_updated_and_logged():
    system = build_reference_system()
    state = system.update_state(
        "MM",
        physical={"module_12_status": "delayed"},
        sensors={"machine_status": "down"},
        actions={"queue_action": "resequence"},
        rewards={"time": -2.0},
        events={"machine_breakdown": True},
    )
    assert state.physical["module_12_status"] == "delayed"
    event = system.log_event("MM", "machine_breakdown", downtime_days=2)
    assert event.twin_id == "MM"
    assert event.payload["downtime_days"] == 2
