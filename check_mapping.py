import re
from risk_scoring.mappings import CATEGORY_TO_TECHNIQUES

def run_checks():
    dhanyas_categories = [
        "Web Exploitation",
        "Malware Analysis",
        "Digital Forensics",
        "Network Forensics",
        "Incident Response",
        "SOC / Log Analysis",
        "Social Engineering",
        "Reconnaissance / OSINT",
        "Steganography",
        "Container Analysis",
        "Cryptography / Encoding",
        "Networking Fundamentals",
        "Systems Fundamentals (Linux/Windows)",
        "Web Infrastructure / Apache",
        "Pentesting Methodology / Adversary Mindset"
    ]

    print("--- 1. Category and Technique Count ---")
    all_techniques = set()
    for cat, techs in CATEGORY_TO_TECHNIQUES.items():
        print(f"[{len(techs)} techniques] {cat}")
        all_techniques.update(techs)

    print("\n--- 2. Total Unique Technique Count ---")
    total_unique = len(all_techniques)
    print(f"Total Unique Techniques Mapped: {total_unique}")
    if total_unique >= 30:
        print("[PASS] 30+ techniques mapped.")
    else:
        print("[FAIL] Less than 30 techniques mapped.")

    print("\n--- 3. ATT&CK Format Validation ---")
    invalid_techs = []
    # Match T1234 or T1234.001
    pattern = re.compile(r"^T\d{4}(\.\d{3})?$")
    for tech in all_techniques:
        if not pattern.match(tech):
            invalid_techs.append(tech)
    
    if not invalid_techs:
        print("[PASS] All technique IDs follow valid MITRE ATT&CK formatting (TXXXX or TXXXX.YYY).")
    else:
        print(f"[FAIL] Invalid formats found: {invalid_techs}")

    print("\n--- 4. Missing Categories Check ---")
    mapped_categories = set(CATEGORY_TO_TECHNIQUES.keys())
    missing = [c for c in dhanyas_categories if c not in mapped_categories]
    if not missing:
        print("[PASS] All 15 of Dhanya's real categories are perfectly mapped (exact spelling/casing).")
    else:
        print(f"[FAIL] Missing categories: {missing}")
        
    print("\n--- Additional Check: Empty Values / Duplicates ---")
    empty_cats = [c for c, t in CATEGORY_TO_TECHNIQUES.items() if not t]
    if not empty_cats:
        print("[PASS] No category has an empty list of techniques.")
    else:
        print(f"[FAIL] Categories with empty technique lists: {empty_cats}")
        
if __name__ == "__main__":
    run_checks()
