# TBP MVP — Tolerance Band Profiling

TBP is a simple, transparent tool that estimates how close a person or system is to overload.

It compares:
- **Capacity** — how much strain can be handled right now
- **Load** — how much strain is being applied

The result is a clear status:
- **GREEN / STABLE**
- **YELLOW / AT RISK**
- **RED / UNSTABLE**

This repository contains **TBP MVP v0.1** — a minimal, working core intended for testing, collaboration, and funding discussions.

---

## What this is

- A deterministic (non–AI black box) model
- Fully explainable and adjustable
- Designed to grow into time-based and adaptive systems

## What this is not

- Not medical advice
- Not a diagnostic tool
- Not a finished product

All values and weights are provisional by design.

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
