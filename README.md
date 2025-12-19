# TBP MVP

TBP (Tolerance Band Profiling) is a simple tool that estimates how close a person or system is to overload.

It compares two things:
- Capacity: how much strain can be handled right now
- Load: how much strain is being applied

The output is a clear status:
- GREEN / STABLE
- YELLOW / AT RISK
- RED / UNSTABLE

This repository contains a working MVP (v0.1).

---

WHAT THIS IS
- A small, deterministic model
- Transparent and explainable
- Built to be extended

WHAT THIS IS NOT
- Medical advice
- A diagnostic system
- A finished product

All numbers and weights are provisional.

---

INPUTS (MVP)
- sleep_hours (0–12)
- stress_level (0–10)
- physical_pain (0–10)
- work_hours (0–100 per week)
- social_support (0–10)
- environment_stability (0–10, where 10 is stable)

---

HOW TO RUN

Requirements:
- Python 3.10 or higher

From the project root, run:

python -m tbp.cli --case input.json

This prints a JSON result with capacity, load, and status.

---

COLLABORATION / FUNDING

This project is seeking collaborators and early-stage funding
to expand and validate the system.
