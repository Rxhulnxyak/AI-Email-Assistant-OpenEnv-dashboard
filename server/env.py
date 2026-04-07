import json
import os
import uuid
from typing import Tuple, Dict, Any, List
from server.models import Action, EmailObservation, Reward, ToolOutput, ListEmailsAction, ReadEmailAction, SearchEmailsAction, CallToolAction, DraftReplyAction, SendReplyAction
from server.mock_system import MockSystem

class OpenEnv:
    """Base class for OpenEnv interface"""
    def reset(self, task_id: str = None) -> EmailObservation:
        raise NotImplementedError

    def step(self, action: Action) -> Tuple[EmailObservation, float, bool, Dict]:
        raise NotImplementedError

    def state(self) -> Dict:
        raise NotImplementedError

class AIEmailEnv(OpenEnv):
    def __init__(self):
        self.system = MockSystem()
        self.current_task = None
        self.step_count = 0
        self.max_steps = 20
        self.reward_history = []
        self.metadata = {}
        self.session_id = str(uuid.uuid4())[:8]
        self._init_logs()

    def _init_logs(self):
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def reset(self, task_id: str = "beginner") -> EmailObservation:
        from server.tasks import TASKS
        self.system = MockSystem() # Clear previous state
        self.step_count = 0
        self.reward_history = []
        
        task = TASKS.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found.")
        
        self.current_task = task
        # Seed the mock system with task-specific emails
        for email_data in task["initial_emails"]:
            self.system.add_email(**email_data)
        
        self.metadata = task.get("metadata", {})
        
        return EmailObservation(
            emails=self.system.list_emails("Inbox"),
            message=f"Environment reset. Task: {task['name']}. Goal: {task['objective']}"
        )

    def step(self, action: Action) -> Tuple[EmailObservation, float, bool, Dict]:
        self.step_count += 1
        
        # Dispatch action
        action_type = action.action_type
        data = action.action_data
        
        obs = EmailObservation()
        
        if action_type == "ListEmails":
            obs.emails = self.system.list_emails(data.folder)
        elif action_type == "ReadEmail":
            obs.current_email = self.system.read_email(data.email_id)
        elif action_type == "ReadAttachment":
            content = self.system.read_attachment(data.email_id, data.filename)
            obs.tool_output = ToolOutput(tool_name="Attachment", output=content or "File not found")
        elif action_type == "MoveEmail":
            success = self.system.move_email(data.email_id, data.target_folder)
            obs.message = f"Email moved to {data.target_folder}" if success else "Error: Email not found"
        elif action_type == "SearchEmails":
            obs.emails = self.system.search_emails(data.query)
        elif action_type == "CalendarAction":
            if data.method == "CheckCalendar":
                events = self.system.list_events()
                obs.tool_output = ToolOutput(tool_name="Calendar", output=json.dumps(events))
            elif data.method == "ScheduleEvent":
                success = self.system.add_event(
                    title=data.args.get("title", "Event"),
                    start=data.args.get("start", ""),
                    end=data.args.get("end", "")
                )
                obs.message = "Event scheduled." if success else "Error scheduling event"
        elif action_type == "CallTool":
            if data.tool_name == "search_kb":
                results = self.system.search_kb(data.args.get("query", ""))
                obs.tool_output = ToolOutput(tool_name="KB", output="\n".join(results))
            elif data.tool_name == "check_crm":
                info = self.system.check_crm(data.args.get("email", ""))
                obs.tool_output = ToolOutput(tool_name="CRM", output=json.dumps(info) if info else "No user found")
        elif action_type == "DraftReply":
            self.system.drafts[data.email_id] = data.content
            obs.message = "Draft saved."
        elif action_type == "SendReply":
            if data.email_id in self.system.drafts:
                # In a real system, we'd add to "Sent" folder
                obs.message = "Email sent successfully."
            else:
                obs.message = "Error: No draft found for this email."

        # Grading
        reward = self._calculate_reward()
        done = self._is_done() or self.step_count >= self.max_steps
        
        obs.reward = reward
        obs.done = done
        
        self._log_step(action, obs)
        
        return obs, reward, done, {"step": self.step_count}

    def _log_step(self, action: Action, obs: EmailObservation):
        log_file = f"logs/session_{self.session_id}.jsonl"
        entry = {
            "step": self.step_count,
            "action": action.dict(),
            "reward": obs.reward,
            "done": obs.done
        }
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _calculate_reward(self) -> float:
        if self.current_task and "grader" in self.current_task:
            return self.current_task["grader"](self.system)
        return 0.0

    def _is_done(self) -> bool:
        # Task is done if reward is 1.0 or criteria met
        if self._calculate_reward() >= 1.0:
            return True
        return False

    def state(self) -> Dict:
        return {
            "emails": [e.dict() for e in self.system.emails.values()],
            "drafts": self.system.drafts,
            "step": self.step_count,
            "current_task": self.current_task["name"] if self.current_task else None
        }
