from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Tuple

@dataclass(frozen=True)
class TBPResult:
    capacity: float
    load: float
    stability_ratio: float
    status: str
    band: str
    contributors: Dict[str, float]

DEFAULT_WEIGHTS = {
    "stress_level": 1.2,
    "physical_pain": 1.3,
    "work_hours": 1.0 / 10.0,
    "environment_instability": 1.0,
}

DEFAULT_BANDS = [
    ("GREEN", 0.60, "STABLE"),
    ("YELLOW", 0.85, "AT_RISK"),
    ("RED", float("inf"), "UNSTABLE"),
]

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def validate_inputs(inputs: Dict[str, Any]) -> Dict[str, float]:
    required = [
        "sleep_hours",
        "stress_level",
        "physical_pain",
        "work_hours",
        "social_support",
        "environment_stability",
    ]
    missing = [k for k in required if k not in inputs]
    if missing:
        raise ValueError(f"Missing required inputs: {missing}")

    return {
        "sleep_hours": clamp(float(inputs["sleep_hours"]), 0, 12),
        "stress_level": clamp(float(inputs["stress_level"]), 0, 10),
        "physical_pain": clamp(float(inputs["physical_pain"]), 0, 10),
        "work_hours": clamp(float(inputs["work_hours"]), 0, 100),
        "social_support": clamp(float(inputs["social_support"]), 0, 10),
        "environment_stability": clamp(float(inputs["environment_stability"]), 0, 10),
    }

def compute_capacity(sleep_hours: float, social_support: float) -> float:
    sleep_deficit = max(0.0, 8.0 - sleep_hours)
    capacity = 100.0 - (sleep_deficit * 2.0) + (social_support * 1.5)
    return max(10.0, capacity)

def compute_load(
    stress_level: float,
    physical_pain: float,
    work_hours: float,
    environment_stability: float,
) -> Tuple[float, Dict[str, float]]:

    environment_instability = 10.0 - environment_stability

    contributors = {
        "stress_level": stress_level * DEFAULT_WEIGHTS["stress_level"],
        "physical_pain": physical_pain * DEFAULT_WEIGHTS["physical_pain"],
        "work_hours": work_hours * DEFAULT_WEIGHTS["work_hours"],
        "environment_instability": environment_instability * DEFAULT_WEIGHTS["environment_instability"],
    }
    return sum(contributors.values()), contributors

def classify(stability_ratio: float) -> Tuple[str, str]:
    for band, upper, status in DEFAULT_BANDS:
        if stability_ratio < upper:
            return band, status
    return "RED", "UNSTABLE"

def calculate_tbp(inputs: Dict[str, Any]) -> TBPResult:
    v = validate_inputs(inputs)

    capacity = compute_capacity(
        sleep_hours=v["sleep_hours"],
        social_support=v["social_support"],
    )

    load, contributors = compute_load(
        stress_level=v["stress_level"],
        physical_pain=v["physical_pain"],
        work_hours=v["work_hours"],
        environment_stability=v["environment_stability"],
    )

    stability_ratio = load / capacity
    band, status = classify(stability_ratio)

    return TBPResult(
        capacity=round(capacity, 2),
        load=round(load, 2),
        stability_ratio=round(stability_ratio, 4),
        band=band,
        status=status,
        contributors={k: round(v, 2) for k, v in contributors.items()},
  )
