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

"""Small dependency-free probability utilities for the CCDT prototype."""

from __future__ import annotations

from math import exp, log
from typing import Hashable, Mapping


def normalize(weights: Mapping[Hashable, float]) -> dict[Hashable, float]:
    if any(value < 0 for value in weights.values()):
        raise ValueError("Probabilities/weights must be non-negative")
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("At least one weight must be positive")
    return {key: value / total for key, value in weights.items()}


def sigmoid(value: float) -> float:
    if value >= 0:
        z = exp(-value)
        return 1.0 / (1.0 + z)
    z = exp(value)
    return z / (1.0 + z)


def bayesian_filter_step(
    prior: Mapping[Hashable, float],
    transition: Mapping[Hashable, Mapping[Hashable, float]],
    likelihood: Mapping[Hashable, float],
) -> dict[Hashable, float]:
    """One discrete Bayesian-filter update."""
    prior_n = normalize(prior)
    states = set(likelihood)
    predicted: dict[Hashable, float] = {state: 0.0 for state in states}

    for prev_state, prev_prob in prior_n.items():
        row = transition.get(prev_state)
        if row is None:
            raise KeyError(f"Missing transition row for {prev_state!r}")
        row_n = normalize(row)
        for state in states:
            predicted[state] += prev_prob * row_n.get(state, 0.0)

    posterior_weights = {
        state: predicted[state] * likelihood[state] for state in states
    }
    return normalize(posterior_weights)


def expected_value(
    probabilities: Mapping[Hashable, float],
    values: Mapping[Hashable, float],
) -> float:
    probs = normalize(probabilities)
    missing = set(probs) - set(values)
    if missing:
        raise KeyError(f"Missing values for states: {sorted(map(str, missing))}")
    return sum(probs[state] * values[state] for state in probs)


def mutual_information(
    joint: Mapping[tuple[Hashable, Hashable], float],
    *,
    log_base: float = 2.0,
) -> float:
    """Mutual information I(X;Y) from a discrete joint distribution."""
    joint_n = normalize(joint)
    px: dict[Hashable, float] = {}
    py: dict[Hashable, float] = {}
    for (x, y), p in joint_n.items():
        px[x] = px.get(x, 0.0) + p
        py[y] = py.get(y, 0.0) + p

    denom = log(log_base)
    info = 0.0
    for (x, y), pxy in joint_n.items():
        if pxy == 0:
            continue
        info += pxy * (log(pxy / (px[x] * py[y])) / denom)
    return info
