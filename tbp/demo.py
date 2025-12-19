import json
from tbp.model import calculate_tbp


CASES = {
    "stable": {
        "sleep_hours": 8,
        "stress_level": 3,
        "physical_pain": 1,
        "work_hours": 40,
        "social_support": 7,
        "environment_stability": 8,
        "emotional_load": 2,
        "cognitive_load": 3,
        "financial_stress": 2,
        "recovery_quality": 7
    },
    "at_risk": {
        "sleep_hours": 6,
        "stress_level": 7,
        "physical_pain": 4,
        "work_hours": 55,
        "social_support": 3,
        "environment_stability": 4,
        "emotional_load": 6,
        "cognitive_load": 7,
        "financial_stress": 8,
        "recovery_quality": 4
    },
    "unstable": {
        "sleep_hours": 3,
        "stress_level": 9,
        "physical_pain": 8,
        "work_hours": 80,
        "social_support": 1,
        "environment_stability": 2,
        "emotional_load": 9,
        "cognitive_load": 8,
        "financial_stress": 9,
        "recovery_quality": 2
    }
}


def main():
    for name, case in CASES.items():
        result = calculate_tbp(case)
        print("\n" + "=" * 60)
        print(f"CASE: {name.upper()}")
        print("=" * 60)
        print(result.summary)
        print(json.dumps(result.__dict__, indent=2))


if __name__ == "__main__":
    main()
