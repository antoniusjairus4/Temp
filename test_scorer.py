import json
from risk_scoring import calculate_learner_score

def test_happy_path():
    sample_data = {
        "employee_id": "EMP001",
        "active_streak_days": 12,
        "overall_completion_rate": 0.65,
        "labs_completed": [
            {
                "category": "Social Engineering",
                "passed": True
            },
            {
                "category": "Web Exploitation",
                "passed": False
            }
        ]
    }
    result = calculate_learner_score(sample_data)
    # Streak: 12/30 * 10 = 4.0
    # Perf: 0.65 * 90 = 58.5
    # Total: 62.5 -> round to 62
    assert result["global_score"] == 62
    assert result["covered_techniques_count"] == 3  # From Social Engineering

def test_zero_labs():
    sample_data = {
        "employee_id": "EMP002",
        "active_streak_days": 0,
        "overall_completion_rate": 0.0,
        "labs_completed": []
    }
    result = calculate_learner_score(sample_data)
    assert result["global_score"] == 0
    assert result["covered_techniques_count"] == 0

def test_all_failed_labs():
    sample_data = {
        "employee_id": "EMP003",
        "active_streak_days": 5,
        "overall_completion_rate": 0.20, # some completion but no passes
        "labs_completed": [
            {
                "category": "Web Exploitation",
                "passed": False
            }
        ]
    }
    result = calculate_learner_score(sample_data)
    # Streak: 5/30 * 10 = 1.66
    # Perf: 0.20 * 90 = 18
    # Total: 19.66 -> round to 20
    assert result["global_score"] == 20
    assert result["covered_techniques_count"] == 0

def test_exceed_max_streak():
    sample_data = {
        "employee_id": "EMP004",
        "active_streak_days": 500, # well above 30
        "overall_completion_rate": 1.0,
        "labs_completed": [
            {
                "category": "Web Exploitation",
                "passed": True
            }
        ]
    }
    result = calculate_learner_score(sample_data)
    # Max streak caps at 30, so 10 points
    # Max perf 1.0 = 90 points
    # Total: 100
    assert result["global_score"] == 100
    assert result["covered_techniques_count"] == 3

def test_unmapped_category():
    sample_data = {
        "employee_id": "EMP005",
        "active_streak_days": 0,
        "overall_completion_rate": 0.5,
        "labs_completed": [
            {
                "category": "NonExistentHack",
                "passed": True
            }
        ]
    }
    result = calculate_learner_score(sample_data)
    # Should not crash.
    assert result["covered_techniques_count"] == 0
    assert result["global_score"] == 45 # 0.5 * 90

def test_malformed_input():
    sample_data = {
        "employee_id": "EMP006",
        "active_streak_days": "not_a_number",
        "overall_completion_rate": None,
        "labs_completed": "just_a_string"
    }
    result = calculate_learner_score(sample_data)
    assert result["global_score"] == 0
    assert result["covered_techniques_count"] == 0
    
def test_completely_invalid_type():
    result = calculate_learner_score("I am not a dictionary")
    assert result["global_score"] == 0
    assert result["employee_id"] == "UNKNOWN"

if __name__ == "__main__":
    test_happy_path()
    test_zero_labs()
    test_all_failed_labs()
    test_exceed_max_streak()
    test_unmapped_category()
    test_malformed_input()
    test_completely_invalid_type()
    print("All tests passed successfully.")
