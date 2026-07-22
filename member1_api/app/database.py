import json
import os

# Path pointing to the root data directory where Dhanya created datasets
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))

class Database:
    def __init__(self):
        self.employees = []
        self.labs = []
        self.load_seed_data()

    def load_seed_data(self):
        try:
            # Load Employees
            emp_path = os.path.join(DATA_DIR, "employees_seed.json")
            if os.path.exists(emp_path):
                with open(emp_path, "r") as f:
                    self.employees = json.load(f)

            # Load Master Labs
            lab_path = os.path.join(DATA_DIR, "labs_master_list.json")
            if os.path.exists(lab_path):
                with open(lab_path, "r") as f:
                    self.labs = json.load(f)

        except Exception as e:
            print(f"Error loading seed data: {e}")

db = Database()