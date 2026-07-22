#!/usr/bin/env python3
"""
Standalone validator for RiskView360 <-> PWNDORA seed data.
Run with no dependencies beyond the Python 3 standard library:

    python3 validate_seed.py

Checks employees_seed.json against:
  1. Schema 1 (field presence, types, value ranges)
  2. labs_master_list.json (lab_path + category must exist and match)

Exits with code 0 if all checks pass, 1 if any employee fails.
Intended to run BEFORE the FastAPI backend is wired up, so data
integrity issues are caught independently of main.py.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
EMPLOYEES_FILE = HERE / "employees_seed.json"
LABS_FILE = HERE / "labs_master_list.json"

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED_EMP_FIELDS = {
    "employee_id": str,
    "name": str,
    "persona": str,
    "active_streak_days": int,
    "labs_completed": list,
    "overall_completion_rate": float,
}

REQUIRED_LAB_FIELDS = {
    "lab_path": str,
    "category": str,
    "score": int,
    "passed": bool,
    "attempts": int,
    "completion_date": str,
    "failed_topics": list,
}


def load_json(path):
    if not path.exists():
        print(f"ERROR: {path} not found")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def main():
    employees = load_json(EMPLOYEES_FILE)
    labs_master = load_json(LABS_FILE)

    valid_lab_paths = {l["lab_path"]: l["category"] for l in labs_master}
    valid_categories = {l["category"] for l in labs_master}

    errors = []
    warnings = []

    if not isinstance(employees, list):
        errors.append("Top-level employees_seed.json must be a JSON array")
        employees = []

    seen_ids = set()

    for idx, emp in enumerate(employees):
        prefix = f"[employee #{idx} / id={emp.get('employee_id', '?')}]"

        # --- top-level field presence + types ---
        for field, ftype in REQUIRED_EMP_FIELDS.items():
            if field not in emp:
                errors.append(f"{prefix} missing required field '{field}'")
                continue
            val = emp[field]
            if ftype is float and isinstance(val, int):
                val = float(val)  # allow ints where float expected
            if not isinstance(val, ftype):
                errors.append(
                    f"{prefix} field '{field}' expected {ftype.__name__}, "
                    f"got {type(emp[field]).__name__}"
                )

        # --- employee_id uniqueness ---
        emp_id = emp.get("employee_id")
        if emp_id in seen_ids:
            errors.append(f"{prefix} duplicate employee_id")
        seen_ids.add(emp_id)

        # --- overall_completion_rate range ---
        rate = emp.get("overall_completion_rate")
        if isinstance(rate, (int, float)) and not (0 <= rate <= 1):
            errors.append(f"{prefix} overall_completion_rate {rate} out of range [0,1]")

        # --- active_streak_days sanity ---
        streak = emp.get("active_streak_days")
        if isinstance(streak, int) and streak < 0:
            errors.append(f"{prefix} active_streak_days cannot be negative")

        # --- labs_completed ---
        labs = emp.get("labs_completed", [])
        if not isinstance(labs, list):
            continue
        if len(labs) == 0:
            warnings.append(f"{prefix} has zero labs_completed")

        for lidx, lab in enumerate(labs):
            lprefix = f"{prefix} lab #{lidx}"
            for field, ftype in REQUIRED_LAB_FIELDS.items():
                if field not in lab:
                    errors.append(f"{lprefix} missing required field '{field}'")
                    continue
                if not isinstance(lab[field], ftype):
                    errors.append(
                        f"{lprefix} field '{field}' expected {ftype.__name__}, "
                        f"got {type(lab[field]).__name__}"
                    )

            lab_path = lab.get("lab_path")
            category = lab.get("category")

            # lab_path must exist in master list
            if lab_path not in valid_lab_paths:
                errors.append(
                    f"{lprefix} lab_path '{lab_path}' not found in labs_master_list.json "
                    f"(does NOT match Noorul's mapping table)"
                )
            elif category != valid_lab_paths[lab_path]:
                errors.append(
                    f"{lprefix} category '{category}' does not match master list category "
                    f"'{valid_lab_paths[lab_path]}' for lab_path '{lab_path}'"
                )

            if category not in valid_categories:
                errors.append(f"{lprefix} category '{category}' is not a recognized category")

            score = lab.get("score")
            if isinstance(score, int) and not (0 <= score <= 100):
                errors.append(f"{lprefix} score {score} out of range [0,100]")

            attempts = lab.get("attempts")
            if isinstance(attempts, int) and attempts < 1:
                errors.append(f"{lprefix} attempts must be >= 1")

            date_str = lab.get("completion_date")
            if isinstance(date_str, str) and not DATE_RE.match(date_str):
                errors.append(f"{lprefix} completion_date '{date_str}' not in YYYY-MM-DD format")

            passed = lab.get("passed")
            if isinstance(passed, bool) and isinstance(score, int):
                if passed and score < 50:
                    warnings.append(
                        f"{lprefix} passed=True but score={score} looks unusually low"
                    )
                if not passed and score > 85:
                    warnings.append(
                        f"{lprefix} passed=False but score={score} looks unusually high"
                    )

    # --- report ---
    print(f"Checked {len(employees)} employee(s) against {len(labs_master)} master labs.\n")

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
        print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        print("\nFAILED: fix the errors above before pushing.")
        sys.exit(1)
    else:
        print("PASSED: all employees conform to Schema 1 and reference valid lab_path values.")
        sys.exit(0)


if __name__ == "__main__":
    main()
