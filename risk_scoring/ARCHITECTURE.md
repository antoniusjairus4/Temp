# RiskView360 PWNDORA Scoring Engine Architecture

This document describes the pure Python logic module used for processing learner records and calculating global scores, ATT&CK coverage, and NIST readiness.

## How to Import This Module

The backend developer (Dhanya) can wire this into the FastAPI endpoint easily. The package has zero external dependencies and handles all math internally.

### Usage

```python
from risk_scoring import calculate_learner_score

# Assuming `learner_json` is the parsed dictionary from the request/database
result = calculate_learner_score(learner_json)
```

### Return Shape

The function is guaranteed to return a dictionary in the following shape, even if the input is malformed or missing fields (it will default safely to 0s instead of crashing):

```json
{
  "employee_id": "EMP001",
  "global_score": 62,
  "covered_techniques_count": 3,
  "covered_techniques": [
    "T1566.001",
    "T1566",
    "T1566.002"
  ],
  "tactic_coverage_percent": {
    "Reconnaissance": 0.0,
    "Initial Access": 60.0,
    "Execution": 0.0,
    "Persistence": 0.0,
    "Privilege Escalation": 0.0,
    "Defense Evasion": 0.0,
    "Credential Access": 0.0,
    "Discovery": 0.0,
    "Lateral Movement": 0.0,
    "Collection": 0.0,
    "Command and Control": 0.0,
    "Exfiltration": 0.0,
    "Impact": 0.0
  },
  "nist_readiness_percent": {
    "Identify": 0.0,
    "Protect": 20.0,
    "Detect": 0.0,
    "Respond": 0.0,
    "Recover": 0.0
  }
}
```

## Module Structure

- `__init__.py`: Exposes the main function `calculate_learner_score`.
- `mappings.py`: Contains constants, mapping dictionaries for ATT&CK techniques, NIST functions, and lab categories.
- `scorer.py`: The core business logic engine that processes the JSON input and calculates all metrics.

## Scoring Formulas

The scoring engine calculates a `global_score` on a scale of 0 to 100. It is composed of two main components:

### 1. Performance Score (Weight: 90%)
This score represents the learner's overall completion rate across all labs.
```
Performance Score = overall_completion_rate * BASE_SCORE_MAX * COMPLETION_RATE_WEIGHT
```
- `overall_completion_rate`: Provided in the JSON (0.0 to 1.0)
- `BASE_SCORE_MAX`: 100
- `COMPLETION_RATE_WEIGHT`: 0.9

### 2. Streak Bonus (Weight: 10%)
This score rewards consistency based on the learner's active daily streak.
```
Streak Bonus = (active_streak_days / MAX_STREAK_DAYS) * BASE_SCORE_MAX * STREAK_BONUS_WEIGHT
```
- `active_streak_days`: Provided in the JSON (Capped at `MAX_STREAK_DAYS`)
- `MAX_STREAK_DAYS`: 30
- `STREAK_BONUS_WEIGHT`: 0.1

### Total Global Score
```
Total Global Score = Round(Performance Score + Streak Bonus)
```
The maximum achievable score is capped at 100.

## Mapping Logic

The backend provides an array of `labs_completed`. Each lab has a `category` (e.g., "Social Engineering").
The scoring engine maps these categories to specific ATT&CK techniques.

1. **Category to Technique**: When a lab is marked as `passed: true`, the engine looks up the `category` in `CATEGORY_TO_TECHNIQUES`. All corresponding ATT&CK techniques are added to a `covered_techniques` set. 
   - **Note on Defensive Categories:** For defensive disciplines like Incident Response, Digital Forensics, and SOC/Log Analysis, the categories are mapped to the *offensive techniques those disciplines are designed to detect or investigate*, rather than representing offensive execution capabilities.
2. **Failed Labs**: If a lab has `passed: false`, it contributes **0** to the technique coverage.
3. **Technique to Tactic & NIST**: Every technique in `covered_techniques` is looked up in `TECHNIQUE_METADATA` to determine its parent Tactic (e.g., "Initial Access") and NIST Function (e.g., "Protect").

## Coverage Calculations

- **Per-Tactic Coverage %**: Calculated by dividing the number of covered techniques in a Tactic by the total number of defined techniques for that Tactic in our metadata dictionary. 
- **Per-NIST Readiness %**: Calculated by dividing the number of covered techniques mapped to a NIST function by the total number of defined techniques for that NIST function.

**Important Note on Coverage Base:** The coverage percentages are calculated relative to our curated ~32-technique subset explicitly mapped in `mappings.py`, *not* the entire MITRE ATT&CK framework. This ensures that 100% coverage means 100% of the techniques supported by PWNDORA's platform, providing a realistic metric for the learner.

## Adding New Labs/Categories

To add new lab categories or map new techniques, update the dictionaries in `mappings.py`. No changes are required in `scorer.py` as the logic is completely data-driven.
