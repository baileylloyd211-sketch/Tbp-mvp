from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Tuple, List


@dataclass(frozen=True)
class TBPResult:
    capacity: float
    load: float
    stability_ratio: float
    status: str
    band: str
    contributors: Dict[str, float]
    top_drivers: List[str]
    summary: str


DEFAULT_WEIGHTS = {
    # Original MVP stressors
    "stress_level": 1.2,              # 0-10
    "physical_pain": 1.3,             # 0-10
    "work_hours": 1.0 / 10.0,         # hours/week -> scaled
    "environment_instability": 1.0,   # derived from environment_stability (0-10)

    # Added inclusive stressors (optional inputs)
    "emotional_load": 1.1,            # 0-10
    "cognitive_load": 1.0,            # 0-10
    "financial_stress": 1.0,          # 0-10
}

DEFAULT_BANDS = [
    ("GREEN", 0.60, "STABLE"),
    ("YELLOW", 0.85, "AT_RISK"),
    ("RED", float("inf"), "UNSTABLE"),
]


def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _get_optional(inputs: Dict[str, Any], key: str, default: float) -> float:
    if key not in inputs or inputs[key] is None:
        return default
    try:
        return float(inputs[key])
    except (TypeError, ValueError):
        return default


def validate_inputs(inputs: Dict[str, Any]) -> Dict[str, float]:
    """
    Required (MVP):
      sleep_hours: 0-12
      stress_level: 0-10
      physical_pain: 0-10
      work_hours: 0-100 (clamped)
      social_support: 0-10
      environment_stability: 0-10 (10 = stable)

    Optional (expanded MVP-safe):
      emotional_load: 0-10
      cognitive_load: 0-10
      financial_stress: 0-10
      recovery_quality: 0-10 (affects capacity; default=5)
    """
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

    sleep_hours = clamp(float(inputs["sleep_hours"]), 0, 12)
    stress_level = clamp(float(inputs["stress_level"]), 0, 10)
    physical_pain = clamp(float(inputs["physical_pain"]), 0, 10)
    work_hours = clamp(float(inputs["work_hours"]), 0, 100)
    social_support = clamp(float(inputs["social_support"]), 0, 10)
    environment_stability = clamp(float(inputs["environment_stability"]), 0, 10)

    # Optional fields (safe defaults)
    emotional_load = clamp(_get_optional(inputs, "emotional_load", 0.0), 0, 10)
    cognitive_load = clamp(_get_optional(inputs, "cognitive_load", 0.0), 0, 10)
    financial_stress = clamp(_get_optional(inputs, "financial_stress", 0.0), 0, 10)
    recovery_quality = clamp(_get_optional(inputs, "recovery_quality", 5.0), 0, 10)

    return {
        "sleep_hours": sleep_hours,
        "stress_level": stress_level,
        "physical_pain": physical_pain,
        "work_hours": work_hours,
        "social_support": social_support,
        "environment_stability": environment_stability,
        "emotional_load": emotional_load,
        "cognitive_load": cognitive_load,
        "financial_stress": financial_stress,
        "recovery_quality": recovery_quality,
    }


def compute_capacity(
    sleep_hours: float,
    social_support: float,
    recovery_quality: float,
    base_capacity: float = 100.0,
) -> float:
    """
    Capacity model (still simple, now more human-realistic):

    - Sleep deficit penalty: below 8 hours reduces capacity
    - Social support buffer: increases capacity
    - Recovery quality modifier: raises/lowers capacity slightly (0-10)

    recovery_quality default is 5, so old inputs behave similarly.
    """
    sleep_deficit = max(0.0, 8.0 - sleep_hours)

    capacity = base_capacity
    capacity -= sleep_deficit * 2.0
    capacity += social_support * 1.5

    # Recovery quality: -7.5 .. +7.5 capacity shift (centered at 5)
    capacity += (recovery_quality - 5.0) * 1.5

    return max(10.0, capacity)


def compute_load(v: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
    """
    Load = sum(stressor * weight)
    environment_instability derived as (10 - environment_stability)
    """
    environment_instability = 10.0 - v["environment_stability"]

    contributors = {
        "stress_level": v["stress_level"] * DEFAULT_WEIGHTS["stress_level"],
        "physical_pain": v["physical_pain"] * DEFAULT_WEIGHTS["physical_pain"],
        "work_hours": v["work_hours"] * DEFAULT_WEIGHTS["work_hours"],
        "environment_instability": environment_instability * DEFAULT_WEIGHTS["environment_instability"],

        # New optional contributors (0 if not provided)
        "emotional_load": v["emotional_load"] * DEFAULT_WEIGHTS["emotional_load"],
        "cognitive_load": v["cognitive_load"] * DEFAULT_WEIGHTS["cognitive_load"],
        "financial_stress": v["financial_stress"] * DEFAULT_WEIGHTS["financial_stress"],
    }

    total_load = sum(contributors.values())
    return total_load, contributors


def classify(stability_ratio: float) -> Tuple[str, str]:
    for band, upper, status in DEFAULT_BANDS:
        if stability_ratio < upper:
            return band, status
    return "RED", "UNSTABLE"


def _top_driver_labels(contributors: Dict[str, float], n: int = 3) -> List[str]:
    # Only show positive contributors
    items = [(k, v) for k, v in contributors.items() if v > 0]
    items.sort(key=lambda kv: kv[1], reverse=True)
    return [k for k, _ in items[:n]]


def _make_summary(status: str, band: str, stability_ratio: float, top_drivers: List[str]) -> str:
    ratio_pct = round(stability_ratio * 100.0, 1)
    if not top_drivers:
        drivers_text = "no strong single driver"
    else:
        drivers_text = ", ".join(top_drivers)

    if status == "STABLE":
        return f"{band} / {status}: load is {ratio_pct}% of capacity, driven mainly by {drivers_text}."
    if status == "AT_RISK":
        return f"{band} / {status}: load is {ratio_pct}% of capacity. Main drivers: {drivers_text}. Consider reducing load or improving recovery."
    return f"{band} / {status}: load is {ratio_pct}% of capacity. Main drivers: {drivers_text}. Priority is immediate load reduction and recovery."


def calculate_tbp(inputs: Dict[str, Any]) -> TBPResult:
    v = validate_inputs(inputs)

    capacity = compute_capacity(
        sleep_hours=v["sleep_hours"],
        social_support=v["social_support"],
        recovery_quality=v["recovery_quality"],
        base_capacity=100.0,
    )

    load, contributors = compute_load(v)

    stability_ratio = load / capacity
    band, status = classify(stability_ratio)

    top_drivers = _top_driver_labels(contributors, n=3)
    summary = _make_summary(status, band, stability_ratio, top_drivers)

    return TBPResult(
        capacity=round(capacity, 2),
        load=round(load, 2),
        stability_ratio=round(stability_ratio, 4),
        status=status,
        band=band,
        contributors={k: round(val, 2) for k, val in contributors.items()},
        top_drivers=top_drivers,
        summary=summary,
    )
