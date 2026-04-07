import gradio as gr
from env import AIEmailEnv
from models import Action, ListEmailsAction, ReadEmailAction, MoveEmailAction, CallToolAction, DraftReplyAction, SendReplyAction, CalendarAction, ReadAttachmentAction
import json
import pandas as pd

class Dashboard:
    def __init__(self):
        self.env = AIEmailEnv()
        self.current_obs = self.env.reset("beginner")

    def reset_env(self, task_id):
        self.current_obs = self.env.reset(task_id)
        return self._get_mailbox_df(), f"Task: {task_id} Reset. Goal: {self.env.current_task['objective']}", 0.0, ""

    def _get_mailbox_df(self):
        emails = self.env.system.list_emails("Inbox")
        if not emails:
            return pd.DataFrame(columns=["ID", "Sender", "Subject", "Folder"])
        return pd.DataFrame([{"ID": e.id, "Sender": e.sender, "Subject": e.subject, "Folder": e.folder} for e in emails])

    def perform_step(self, action_type, arg1, arg2):
        try:
            if action_type == "ReadEmail":
                action = Action(action_type="ReadEmail", action_data=ReadEmailAction(email_id=arg1))
            elif action_type == "MoveEmail":
                action = Action(action_type="MoveEmail", action_data=MoveEmailAction(email_id=arg1, target_folder=arg2))
            elif action_type == "SearchKB":
                action = Action(action_type="CallTool", action_data=CallToolAction(tool_name="search_kb", args={"query": arg1}))
            elif action_type == "CheckCalendar":
                 action = Action(action_type="CalendarAction", action_data=CalendarAction(method="CheckCalendar", args={}))
            # Add more as needed for the demo
            else:
                return self._get_mailbox_df(), "Action not supported in UI demo yet.", 0.0, ""

            obs, reward, done, info = self.env.step(action)
            self.current_obs = obs
            
            msg = obs.message
            if obs.current_email:
                msg = f"Reading: {obs.current_email.subject}\n\n{obs.current_email.body}"
            if obs.tool_output:
                msg = f"Tool: {obs.tool_output.tool_name}\n\n{obs.tool_output.output}"
                
            return self._get_mailbox_df(), msg, reward, "Done!" if done else "In Progress"
        except Exception as e:
            return self._get_mailbox_df(), f"Error: {e}", 0.0, "Error"

def build_ui():
    dash = Dashboard()
    
    with gr.Blocks(title="AI Email Assistant OpenEnv dashboard") as demo:
        gr.Markdown("# 📧 AI Email Assistant OpenEnv dashboard")
        gr.Markdown("Visualizing the agent environment for the Meta OpenEnv Hackathon Finale.")
        
        with gr.Row():
            task_select = gr.Dropdown(choices=["beginner", "intermediate", "advanced", "crisis", "scheduler"], label="Select Task", value="beginner")
            reset_btn = gr.Button("Reset Environment")
            
        with gr.Row():
            with gr.Column(scale=2):
                mailbox = gr.DataFrame(dash._get_mailbox_df(), label="Current Inbox")
            with gr.Column(scale=1):
                reward_display = gr.Number(label="Current Reward", value=0.0)
                status_display = gr.Textbox(label="Status", value="Ready")

        with gr.Row():
            log_display = gr.Textbox(label="Environment Output / Email Content", lines=10)

        with gr.Row():
            action_type = gr.Dropdown(choices=["ReadEmail", "MoveEmail", "SearchKB", "CheckCalendar"], label="Action")
            arg1 = gr.Textbox(label="Arg 1 (ID / Query)")
            arg2 = gr.Textbox(label="Arg 2 (Folder / Optional)")
            step_btn = gr.Button("Step Environment")

        reset_btn.click(dash.reset_env, inputs=[task_select], outputs=[mailbox, log_display, reward_display, status_display])
        step_btn.click(dash.perform_step, inputs=[action_type, arg1, arg2], outputs=[mailbox, log_display, reward_display, status_display])

    return demo

if __name__ == "__main__":
    ui = build_ui()
    ui.launch(server_name="0.0.0.0", server_port=7861)
