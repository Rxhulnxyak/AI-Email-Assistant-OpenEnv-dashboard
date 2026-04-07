import os
import json
import requests
import argparse
from typing import List, Dict
from models import Action, ListEmailsAction, ReadEmailAction, CallToolAction, DraftReplyAction, SendReplyAction

# Simple Logic for Beginner Task: Categorization
def run_beginner(env_url):
    # Reset Environment
    response = requests.post(f"{env_url}/reset?task_id=beginner")
    observation = response.json()
    print(f"Goal: {observation['message']}")
    
    emails = observation['emails']
    last_reward = 0.0
    for email in emails:
        # Action: Read Email
        payload = {"action_type": "ReadEmail", "action_data": {"email_id": email['id']}}
        requests.post(f"{env_url}/step", json=payload)
        
        # Action: Move based on domain
        target = "Internal" if "@example.com" in email['sender'] else "External"
        payload = {"action_type": "MoveEmail", "action_data": {"email_id": email['id'], "target_folder": target}}
        response = requests.post(f"{env_url}/step", json=payload).json()
        last_reward = response['reward']
        
    print(f"Final Reward: {last_reward}")
    return last_reward

def run_inference(task_id, env_url):
    print(f"--- Running Inference for Task: {task_id} on {env_url} ---")
    if task_id == "beginner":
        return run_beginner(env_url)
    else:
        # Minimal reset for other tasks as baseline
        response = requests.post(f"{env_url}/reset?task_id={task_id}")
        print(f"Reset response: {response.status_code}")
        return 0.0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", type=str, default="beginner")
    parser.add_argument("--env_url", type=str, default="http://localhost:7860")
    args = parser.parse_args()

    # If env_url is provided by portal without http, add it
    url = args.env_url
    if not url.startswith("http"):
        url = f"http://{url}"

    run_inference(args.task_id, url)
