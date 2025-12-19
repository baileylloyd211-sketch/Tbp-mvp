# TBP MVP (Tolerance Band Profiling)

TBP is a transparent, deterministic model that estimates how close a person or system is to overload.

It takes a small set of inputs (sleep, stress, pain, workload, support, environment) and returns:
- **Capacity** (how much strain can be sustained right now)
- **Load** (how much strain is being applied)
- **Stability Ratio** = load / capacity
- **Band + Status**: GREEN / STABLE, YELLOW / AT_RISK, RED / UNSTABLE

This repository contains **MVP v0.1** — a minimal core that runs, produces outputs, and can be expanded.

---

## What this is (and isn’t)

**This is:**
- A prototype for modeling stability and overload
- Fully explainable (no black-box AI)
- Designed for iteration, testing, and extension

**This is not:**
- Medical advice
- A diagnostic or clinical tool
- A finished product

All parameters and weights are provisional by design.

---

## Inputs (MVP)

All inputs are normalized to a 0–10 scale unless noted.

- `sleep_hours` (0–12)
- `stress_level` (0–10)
- `physical_pain` (0–10)
- `work_hours` (0–100, hours per week)
- `social_support` (0–10)
- `environment_stability` (0–10, where 10 = stable)

---

## Example Output

```json
{
  "capacity": 94.0,
  "load": 71.3,
  "stability_ratio": 0.7585,
  "band": "YELLOW",
  "status": "AT_RISK",
  "contributors": {
    "stress_level": 8.4,
    "physical_pain": 5.2,
    "work_hours": 5.5,
    "environment_instability": 6.0
  }
}
## How to Run (Local)

Requirements:
- Python 3.10+

Clone the repo and run:

```bash
python -m tbp.cli --case input.json
