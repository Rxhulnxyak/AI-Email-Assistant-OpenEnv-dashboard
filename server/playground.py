import json
from server.env import AIEmailEnv
from server.models import (
    Action, ListEmailsAction, ReadEmailAction, MoveEmailAction, 
    CallToolAction, DraftReplyAction, SendReplyAction, CalendarAction
)

def main():
    print("Welcome to the AI Email Assistant OpenEnv Playground!")
    env = AIEmailEnv()
    
    print("\nAvailable Tasks:")
    print("1. beginner (Triage)")
    print("2. intermediate (Security FAQ)")
    print("3. advanced (Retention)")
    print("4. crisis (Expert: Crisis Management)")
    print("5. scheduler (Expert: Meeting Scheduler)")
    
    task_id = input("\nSelect Task ID: ")
    obs = env.reset(task_id)
    
    while not obs.done:
        print(f"\n--- Current Task: {env.current_task['name']} ---")
        print(f"Goal: {env.current_task['objective']}")
        print(f"Status Message: {obs.message}")
        print(f"Emails in Inbox: {[e.subject for e in env.system.list_emails('Inbox')]}")
        
        if obs.current_email:
            print(f"\n[READING EMAIL] From: {obs.current_email.sender}")
            print(f"Subject: {obs.current_email.subject}")
            print(f"Body: {obs.current_email.body}")
            
        if obs.tool_output:
            print(f"\n[TOOL OUTPUT] {obs.tool_output.tool_name}: {obs.tool_output.output}")

        print("\nActions:")
        print("1. List [folder]")
        print("2. Read [email_id]")
        print("3. Move [email_id] [folder]")
        print("4. Tool [name] [query/email]")
        print("5. Calendar [Check/Schedule]")
        print("6. Draft [email_id] [content]")
        print("7. Send [email_id]")
        print("8. Exit")
        
        choice = input("\nYour action (e.g. '2 abc12345'): ").split(' ', 2)
        cmd = choice[0]
        
        try:
            if cmd == '1':
                action = Action(action_type="ListEmails", action_data=ListEmailsAction(folder=choice[1]))
            elif cmd == '2':
                action = Action(action_type="ReadEmail", action_data=ReadEmailAction(email_id=choice[1]))
            elif cmd == '3':
                action = Action(action_type="MoveEmail", action_data=MoveEmailAction(email_id=choice[1], target_folder=choice[2]))
            elif cmd == '4':
                tool_name = choice[1]
                arg_key = "query" if "kb" in tool_name else "email"
                action = Action(action_type="CallTool", action_data=CallToolAction(tool_name=tool_name, args={arg_key: choice[2]}))
            elif cmd == '5':
                if choice[1].lower() == "check":
                    action = Action(action_type="CalendarAction", action_data=CalendarAction(method="CheckCalendar", args={}))
                else:
                    title = input("Title: ")
                    start = input("Start (YYYY-MM-DD HH:MM): ")
                    action = Action(action_type="CalendarAction", action_data=CalendarAction(method="ScheduleEvent", args={"title": title, "start": start}))
            elif cmd == '6':
                action = Action(action_type="DraftReply", action_data=DraftReplyAction(email_id=choice[1], content=choice[2]))
            elif cmd == '7':
                action = Action(action_type="SendReply", action_data=SendReplyAction(email_id=choice[1]))
            elif cmd == '8':
                break
            else:
                print("Invalid command.")
                continue

            obs, reward, done, info = env.step(action)
            print(f"\n>>> REWARD: {reward}")
            
        except IndexError:
            print("Missing arguments for command.")
        except Exception as e:
            print(f"Error: {e}")

    print("\n--- Interaction Finished ---")
    print(f"Final Score: {env._calculate_reward() * 100}%")

if __name__ == "__main__":
    main()
