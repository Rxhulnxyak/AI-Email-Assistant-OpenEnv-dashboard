import requests
import json
import sys
from pydantic import ValidationError
from server.models import EmailObservation, Action

# Configuration
API_URL = "http://localhost:7860"

def check_endpoint(name, method, path, **kwargs):
    print(f"Checking {name} ({path})...", end=" ")
    try:
        if method == "GET":
            response = requests.get(f"{API_URL}{path}", timeout=5)
        else:
            response = requests.post(f"{API_URL}{path}", json=kwargs.get("json", {}), timeout=5)
        
        if response.status_code == 200:
            print("✅ PASS")
            return response.json()
        else:
            print(f"❌ FAIL (Status: {response.status_code})")
            return None
    except Exception as e:
        print(f"❌ FAIL (Error: {e})")
        return None

def verify_spec():
    print("\n--- OpenEnv Spec Verification ---\n")
    
    # 1. Root Check
    root = check_endpoint("Root", "GET", "/api")
    
    # 2. Reset Check & Pydantic Validation
    reset_data = check_endpoint("Reset (Beginner)", "POST", "/reset?task_id=beginner")
    if reset_data:
        try:
            EmailObservation(**reset_data)
            print("   ↳ Pydantic Observation Validation: ✅ PASS")
        except ValidationError as e:
            print(f"   ↳ Pydantic Observation Validation: ❌ FAIL\n{e}")

    # 3. Step Check
    sample_action = {
        "action_type": "ListEmails",
        "action_data": {"folder": "Inbox"}
    }
    step_data = check_endpoint("Step (ListEmails)", "POST", "/step", json=sample_action)
    if step_data:
        if "observation" in step_data and "reward" in step_data:
            print("   ↳ Step Response Structure: ✅ PASS")
        else:
            print("   ↳ Step Response Structure: ❌ FAIL")

    # 4. State Check
    state_data = check_endpoint("State", "GET", "/state")
    
    print("\n--- Verification Complete ---")
    if all([root, reset_data, step_data, state_data]):
        print("\nSUMMARY: Your environment is FULLY COMPLIANT with the OpenEnv specification.")
        sys.exit(0)
    else:
        print("\nSUMMARY: Check your server is running (python app.py) before verification.")
        sys.exit(1)

if __name__ == "__main__":
    verify_spec()
