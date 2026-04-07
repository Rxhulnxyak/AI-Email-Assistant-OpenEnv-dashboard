from typing import List, Optional, Dict, Union, Any
from pydantic import BaseModel, Field

class EmailHeader(BaseModel):
    id: str
    sender: str
    subject: str
    folder: str
    timestamp: str
    is_read: bool = False

class EmailDetail(BaseModel):
    id: str
    sender: str
    recipient: str
    subject: str
    body: str
    timestamp: str
    folder: str
    thread_id: str
    attachments: List[str] = []

class ToolOutput(BaseModel):
    tool_name: str
    output: str
    status: str = "success"

class EmailObservation(BaseModel):
    emails: List[EmailHeader] = []
    current_email: Optional[EmailDetail] = None
    tool_output: Optional[ToolOutput] = None
    folders: List[str] = ["Inbox", "Sent", "Drafts", "Spam", "Archive", "Urgent"]
    message: str = ""
    reward: float = 0.0
    done: bool = False

# Actions
class ListEmailsAction(BaseModel):
    folder: str = "Inbox"

class ReadEmailAction(BaseModel):
    email_id: str

class SearchEmailsAction(BaseModel):
    query: str

class CallToolAction(BaseModel):
    tool_name: str
    args: Dict[str, str]

class DraftReplyAction(BaseModel):
    email_id: str
    content: str

class SendReplyAction(BaseModel):
    email_id: str

class MoveEmailAction(BaseModel):
    email_id: str
    target_folder: str

class CalendarAction(BaseModel):
    method: str # "CheckCalendar" or "ScheduleEvent"
    args: Dict[str, str]

class ReadAttachmentAction(BaseModel):
    email_id: str
    filename: str

class ResetRequest(BaseModel):
    task_id: str = "beginner"
    options: Optional[Dict[str, Any]] = None

class Action(BaseModel):
    action_type: str
    action_data: Union[
        ListEmailsAction, 
        ReadEmailAction, 
        SearchEmailsAction, 
        CallToolAction, 
        DraftReplyAction, 
        SendReplyAction,
        MoveEmailAction,
        CalendarAction,
        ReadAttachmentAction
    ]

class Reward(BaseModel):
    value: float
    description: str
    penalty_reason: Optional[str] = None
