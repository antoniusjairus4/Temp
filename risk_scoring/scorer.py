import logging
from typing import Dict, List, Any
from .mappings import (
    BASE_SCORE_MAX, MAX_STREAK_DAYS, STREAK_BONUS_WEIGHT, COMPLETION_RATE_WEIGHT,
    TACTICS, NIST_FUNCTIONS, TECHNIQUE_METADATA, CATEGORY_TO_TECHNIQUES
)

logger = logging.getLogger(__name__)

def calculate_learner_score(learner_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate the global score, ATT&CK coverage, and NIST readiness for a learner.
    
    Args:
        learner_data: A dictionary representing the learner JSON record.
        
    Returns:
        A dictionary containing the calculated scores and metrics.
    """
    if not isinstance(learner_data, dict):
        logger.error("calculate_learner_score received non-dict learner_data. Defaulting to empty metrics.")
        return _empty_result()

    employee_id = learner_data.get("employee_id", "UNKNOWN")

    # Safely parse streak days
    try:
        raw_streak = learner_data.get("active_streak_days", 0)
        active_streak_days = float(raw_streak) if raw_streak is not None else 0.0
    except (ValueError, TypeError):
        logger.warning(f"Invalid active_streak_days for {employee_id}, defaulting to 0.")
        active_streak_days = 0.0
        
    active_streak_days = min(max(active_streak_days, 0.0), float(MAX_STREAK_DAYS))

    # Safely parse completion rate
    try:
        raw_rate = learner_data.get("overall_completion_rate", 0.0)
        overall_completion_rate = float(raw_rate) if raw_rate is not None else 0.0
    except (ValueError, TypeError):
        logger.warning(f"Invalid overall_completion_rate for {employee_id}, defaulting to 0.")
        overall_completion_rate = 0.0
        
    overall_completion_rate = min(max(overall_completion_rate, 0.0), 1.0)
    
    # Safely parse labs
    labs_completed = learner_data.get("labs_completed", [])
    if not isinstance(labs_completed, list):
        logger.warning(f"Invalid labs_completed format for {employee_id}, expected list. Defaulting to empty.")
        labs_completed = []
    
    # Tracking sets for covered techniques
    covered_techniques = set()
    
    for lab in labs_completed:
        if not isinstance(lab, dict):
            continue
            
        # Only count passed labs for coverage
        if lab.get("passed") is True:
            category = lab.get("category", "")
            
            # Gracefully handle unmapped or missing categories
            if category in CATEGORY_TO_TECHNIQUES:
                for tech in CATEGORY_TO_TECHNIQUES[category]:
                    covered_techniques.add(tech)
            else:
                logger.debug(f"Category '{category}' not found in mappings, skipping coverage calculation.")
                    
    # Calculate per-tactic coverage
    tactic_coverage = {tactic: 0 for tactic in TACTICS}
    tactic_totals = {tactic: 0 for tactic in TACTICS}
    
    for tech, meta in TECHNIQUE_METADATA.items():
        tactic_totals[meta["tactic"]] += 1
        if tech in covered_techniques:
            tactic_coverage[meta["tactic"]] += 1
            
    tactic_percentages = {}
    for tactic in TACTICS:
        if tactic_totals[tactic] > 0:
            tactic_percentages[tactic] = round((tactic_coverage[tactic] / tactic_totals[tactic]) * 100, 2)
        else:
            tactic_percentages[tactic] = 0.0
            
    # Calculate per-NIST-function readiness
    nist_coverage = {nist: 0 for nist in NIST_FUNCTIONS}
    nist_totals = {nist: 0 for nist in NIST_FUNCTIONS}
    
    for tech, meta in TECHNIQUE_METADATA.items():
        nist_totals[meta["nist"]] += 1
        if tech in covered_techniques:
            nist_coverage[meta["nist"]] += 1
            
    nist_percentages = {}
    for nist in NIST_FUNCTIONS:
        if nist_totals[nist] > 0:
            nist_percentages[nist] = round((nist_coverage[nist] / nist_totals[nist]) * 100, 2)
        else:
            nist_percentages[nist] = 0.0
            
    # Global score calculation
    # 1. Base performance from overall completion rate
    performance_score = overall_completion_rate * BASE_SCORE_MAX * COMPLETION_RATE_WEIGHT
    
    # 2. Streak bonus
    streak_bonus = (active_streak_days / MAX_STREAK_DAYS) * BASE_SCORE_MAX * STREAK_BONUS_WEIGHT
    
    # 3. Total global score
    global_score = round(performance_score + streak_bonus)
    
    # Ensure it stays exactly within boundaries [0, BASE_SCORE_MAX]
    global_score = max(0, min(global_score, BASE_SCORE_MAX))

    return {
        "employee_id": employee_id,
        "global_score": global_score,
        "covered_techniques_count": len(covered_techniques),
        "covered_techniques": list(covered_techniques),
        "tactic_coverage_percent": tactic_percentages,
        "nist_readiness_percent": nist_percentages
    }

def _empty_result() -> Dict[str, Any]:
    """Helper to return an empty structured result if input is completely malformed."""
    return {
        "employee_id": "UNKNOWN",
        "global_score": 0,
        "covered_techniques_count": 0,
        "covered_techniques": [],
        "tactic_coverage_percent": {tactic: 0.0 for tactic in TACTICS},
        "nist_readiness_percent": {nist: 0.0 for nist in NIST_FUNCTIONS}
    }
