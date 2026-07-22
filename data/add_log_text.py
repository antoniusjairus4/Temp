import json
with open("data/employees_seed.json") as f:
    employees = json.load(f)
for emp in employees:
    first_name = emp["name"].split()[0]
    for lab in emp["labs_completed"]:
        lab_name = lab["lab_path"]
        score = lab["score"]
        attempts = lab["attempts"]
        passed = lab["passed"]
        failed_topics = lab.get("failed_topics", [])
        attempt_word = "Attempt" if attempts == 1 else "Attempts"
        if passed:
            entry = f"{first_name} completed '{lab_name}' — Score: {score}%, {attempt_word}: {attempts}"
        else:
            entry = f"{first_name} attempted '{lab_name}' — Score: {score}%, {attempt_word}: {attempts}, did not pass"
        if failed_topics:
            if len(failed_topics) == 1:
                entry += f", flagged weak on {failed_topics[0]}"
            else:
                topics_str = ", ".join(failed_topics[:-1]) + f" and {failed_topics[-1]}"
                entry += f", flagged weak on {topics_str}"
        lab["log_entry"] = entry
with open("data/employees_seed.json", "w") as f:
    json.dump(employees, f, indent=2)
print("Done. Added 'log_entry' field to every lab in every employee record.")
print("\n--- Sample entries ---")
count = 0
for emp in employees:
    for lab in emp["labs_completed"]:
        print(lab["log_entry"])
        count += 1
        if count >= 8:
            break
    if count >= 8:
        break