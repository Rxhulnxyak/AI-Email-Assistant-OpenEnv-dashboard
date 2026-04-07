from env import AIEmailEnv
from models import Action, ListEmailsAction, MoveEmailAction, ReadEmailAction
import json

def run_demo():
    print("🚀 Starting AI Email Assistant OpenEnv Demo (Local Mode)...")
    env = AIEmailEnv()
    
    # 1. Reset Environment for Beginner Task
    print("\n--- [Step 1] Resetting for: Corporate Triage ---")
    observation = env.reset("beginner")
    print(f"Goal: {observation.message}")
    print(f"Initial Inbox: {[e.subject for e in observation.emails]}")

    # 2. Process Emails (Categorization Logic)
    print("\n--- [Step 2] Processing Emails ---")
    for email in observation.emails:
        print(f"\nProcessing: '{email.subject}' from {email.sender}")
        
        # Action: Read the email
        read_action = Action(action_type="ReadEmail", action_data=ReadEmailAction(email_id=email.id))
        env.step(read_action)
        
        # Logic: Categorize by domain
        target = "Internal" if "@example.com" in email.sender else "External"
        print(f"  ↳ Decision: Move to '{target}' folder")
        
        # Action: Move Email
        move_action = Action(action_type="MoveEmail", action_data=MoveEmailAction(email_id=email.id, target_folder=target))
        obs, reward, done, info = env.step(move_action)
        
        print(f"  ↳ Current Total Reward: {reward}")

    # 3. Final Results
    print("\n--- [Step 3] Final State ---")
    final_state = env.state()
    print(f"Task Completed: {final_state['current_task']}")
    print(f"Final Score: {reward * 100}%")

    if reward >= 1.0:
        print("\n✅ SUCCESS: All emails correctly categorized!")
    else:
        print("\n❌ FAILED: Some emails are in the wrong folder.")

if __name__ == "__main__":
    run_demo()
