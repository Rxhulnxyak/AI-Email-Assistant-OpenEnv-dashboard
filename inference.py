import os
import json
import requests
from typing import List, Dict
from models import Action, ListEmailsAction, ReadEmailAction, CallToolAction, DraftReplyAction, SendReplyAction

# Configuration
API_URL = "http://localhost:7860"
HF_TOKEN = os.getenv("HF_TOKEN", "your_token_here")
MODEL = "gpt-4o-mini" # Or any HF model

class Agent:
    def __init__(self, task_id="beginner"):
        self.task_id = task_id
        self.observation = self._reset()
        self.steps = 0

    def _reset(self):
        response = requests.post(f"{API_URL}/reset?task_id={self.task_id}")
        return response.json()

    def _step(self, action_type, action_data):
        payload = {
            "action_type": action_type,
            "action_data": action_data
        }
        response = requests.post(f"{API_URL}/step", json=payload)
        return response.json()

    def run(self):
        print(f"--- Running Task: {self.task_id} ---")
        print(f"Goal: {self.observation['message']}")
        
        # Simple Logic for Beginner Task: Categorization
        # In a real baseline, this would be an LLM call.
        # Here we simulate the LLM's multi-step decision process.
        
        emails = self.observation['emails']
        for email in emails:
            print(f"Processing Email: {email['subject']} from {email['sender']}")
            
            # Action: Read Email
            print(f"Action: Reading email {email['id']}")
            result = self._step("ReadEmail", {"email_id": email['id']})
            
            # Action: Move based on domain
            sender = email['sender']
            target = "Internal" if "@example.com" in sender else "External"
            print(f"Action: Moving to folder {target}")
            
            # OpenEnv move action (Simulated via a move tool if needed, 
            # currently we'll just implement the move logic in the system)
            # For this hackathon, we'll assume the agent calls a move action.
            # (Adding MoveEmail to models if not there)
            self._step("CallTool", {"tool_name": "move_email", "args": {"email_id": email['id'], "target": target}})

        # Final State
        state = requests.get(f"{API_URL}/state").json()
        print(f"\nFinal Reward: {result['reward']}")
        print(f"Score: {result['reward'] * 100}%")

if __name__ == "__main__":
    # Start the server in a separate process or assume it is running
    print("Pre-requisite: Ensure 'python app.py' is running.")
    agent = Agent("beginner")
    agent.run()
