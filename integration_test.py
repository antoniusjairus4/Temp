import json
from risk_scoring import calculate_learner_score

def run_integration_tests():
    print("--- RiskView360 PWNDORA Scoring Integration Test ---\n")

    fake_records = [
        # 1. High Performer (Red Team focus)
        {
            "employee_id": "EMP-9001",
            "name": "Alex Mercer",
            "persona": "Offensive Specialist",
            "active_streak_days": 45, # Over max
            "overall_completion_rate": 0.95,
            "labs_completed": [
                {"lab_path": "SQLi Mastery", "category": "Web Exploitation", "passed": True},
                {"lab_path": "Burp Suite Basics", "category": "Web Exploitation", "passed": True},
                {"lab_path": "Phishing 101", "category": "Social Engineering", "passed": True},
                {"lab_path": "Docker Escapes", "category": "Container Analysis", "passed": True}
            ]
        },
        
        # 2. Struggling Beginner (Mixed results)
        {
            "employee_id": "EMP-2044",
            "name": "Sam Carter",
            "persona": "Junior Analyst",
            "active_streak_days": 3,
            "overall_completion_rate": 0.40,
            "labs_completed": [
                {"lab_path": "Basic PCAP", "category": "Network Forensics", "passed": True},
                {"lab_path": "Malware Sandbox", "category": "Malware Analysis", "passed": False},
                {"lab_path": "Web Logs", "category": "SOC / Log Analysis", "passed": False}
            ]
        },

        # 3. Solid Blue Teamer
        {
            "employee_id": "EMP-5502",
            "name": "Dhanya Nair",
            "persona": "Defensive Engineer",
            "active_streak_days": 15,
            "overall_completion_rate": 0.75,
            "labs_completed": [
                {"lab_path": "File Carving", "category": "Digital Forensics", "passed": True},
                {"lab_path": "Memory Dumps", "category": "Digital Forensics", "passed": True},
                {"lab_path": "Splunk Alerts", "category": "SOC / Log Analysis", "passed": True},
                {"lab_path": "Hunting Persistence", "category": "Incident Response", "passed": True}
            ]
        },

        # 4. Malformed/Missing Data (Robustness check)
        {
            "employee_id": "EMP-BROKEN",
            "active_streak_days": "not_an_int",
            "overall_completion_rate": None,
            "labs_completed": [
                {"category": "NonExistent Category", "passed": True}, # Unmapped
                "I am just a string, not a dict",
                {"category": "Social Engineering", "passed": True} # valid one inside a broken array
            ]
        }
    ]

    for idx, record in enumerate(fake_records, 1):
        print(f"=== Record {idx}: {record.get('name', record.get('employee_id'))} ===")
        print("Input:")
        print(json.dumps(record, indent=2))
        
        # Process through our scoring engine
        result = calculate_learner_score(record)
        
        print("\nOutput (Scoring Engine Result):")
        print(json.dumps(result, indent=2))
        print("="*60 + "\n")

if __name__ == "__main__":
    run_integration_tests()
