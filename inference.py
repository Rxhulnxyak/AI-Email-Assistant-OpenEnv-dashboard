import os
import json
import requests
import argparse

# Standalone Inference Script for Scaler Portal Compliance
# Includes mandatory [START], [STEP], and [END] log markers.

def run_beginner(env_url):
    print("[START]")
    # Reset Environment
    payload = {"task_id": "beginner"}
    print(f"Triggering reset on {env_url}/reset...")
    response = requests.post(f"{env_url}/reset", json=payload)
    
    if response.status_code != 200:
        print(f"Reset failed with status {response.status_code}: {response.text}")
        print("[END]")
        return 0.0

    result = response.json()
    observation = result.get("observation", result)
    print(f"Goal: {observation.get('message', 'No message')}")
    
    emails = observation.get('emails', [])
    last_reward = 0.0
    
    # Simple logic: Categorize first 2 emails
    for email in emails[:2]:
        email_id = email.get('id')
        # Action: Read
        requests.post(f"{env_url}/step", json={"action_type": "ReadEmail", "action_data": {"email_id": email_id}})
        print("[STEP]")
        
        # Action: Move
        target = "Internal" if "@example.com" in email.get('sender', '') else "External"
        step_payload = {"action_type": "MoveEmail", "action_data": {"email_id": email_id, "target_folder": target}}
        step_resp = requests.post(f"{env_url}/step", json=step_payload).json()
        print("[STEP]")
        last_reward = step_resp.get('reward', 0.0)
        
    print(f"Final Reward: {last_reward}")
    print("[END]")
    return last_reward

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", type=str, default="beginner")
    parser.add_argument("--env_url", type=str, default="http://localhost:8000")
    args = parser.parse_args()

    url = args.env_url
    if not url.startswith("http"):
        url = f"http://{url}"
        
    try:
        run_beginner(url)
    except Exception as e:
        print(f"Inference error: {e}")
        print("[END]")
