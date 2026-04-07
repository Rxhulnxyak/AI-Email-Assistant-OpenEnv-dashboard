import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from env import AIEmailEnv
from models import Action, ListEmailsAction, MoveEmailAction, ReadEmailAction

def test_reset_env():
    env = AIEmailEnv()
    obs = env.reset("beginner")
    assert len(obs.emails) > 0
    assert "Corporate Triage" in obs.message

def test_move_email_logic():
    env = AIEmailEnv()
    env.reset("beginner")
    emails = env.system.list_emails("Inbox")
    email_id = emails[0].id
    
    # Move to Internal
    move_action = Action(action_type="MoveEmail", action_data=MoveEmailAction(email_id=email_id, target_folder="Internal"))
    obs, reward, done, info = env.step(move_action)
    
    email = env.system.read_email(email_id)
    assert email.folder == "Internal"
    assert reward > 0

def test_intermediate_task_policy():
    env = AIEmailEnv()
    env.reset("intermediate")
    
    # Search KB
    from models import CallToolAction
    action = Action(action_type="CallTool", action_data=CallToolAction(tool_name="search_kb", args={"query": "security"}))
    obs, reward, done, info = env.step(action)
    assert "Security Policy" in obs.tool_output.output
    
    # Draft Response
    from models import DraftReplyAction
    emails = env.system.list_emails("Inbox")
    draft_action = Action(action_type="DraftReply", action_data=DraftReplyAction(email_id=emails[0].id, content="Please use SSO: https://sso.internal"))
    obs, reward, done, info = env.step(draft_action)
    assert reward == 1.0
    assert done == True

def test_invalid_task():
    env = AIEmailEnv()
    with pytest.raises(ValueError):
        env.reset("invalid_task_id")
