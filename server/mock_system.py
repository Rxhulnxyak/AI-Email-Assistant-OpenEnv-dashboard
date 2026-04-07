import uuid
from datetime import datetime
from typing import List, Dict, Optional
from models import EmailDetail, EmailHeader, ToolOutput

class MockSystem:
    def __init__(self):
        self.emails: Dict[str, EmailDetail] = {}
        self.crm: Dict[str, Dict] = {}
        self.kb: Dict[str, str] = {}
        self.drafts: Dict[str, str] = {}
        self.events: List[Dict] = []
        self.attachments: Dict[str, str] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        # Sample Calendar Data
        self.events.append({"title": "Team Sync", "start": "2026-04-07 10:00", "end": "2026-04-07 11:00"})
        self.events.append({"title": "Customer Call", "start": "2026-04-07 14:00", "end": "2026-04-07 15:00"})
        
        # Sample CRM Data
        self.crm["john.doe@example.com"] = {
            "name": "John Doe",
            "status": "VIP",
            "churn_risk": "Low",
            "value": 5000.0,
            "last_interaction": "2026-03-20"
        }
        self.crm["jane.smith@partner.com"] = {
            "name": "Jane Smith",
            "status": "Strategic Partner",
            "value": 15000.0,
            "last_interaction": "2026-04-01"
        }
        self.crm["angry.customer@gmail.com"] = {
            "name": "Angry Customer",
            "status": "Standard",
            "churn_risk": "High",
            "value": 200.0,
            "last_interaction": "2026-04-06"
        }

        # Sample KB Data
        self.kb["Discount Policy"] = (
            "Our standard discount for retention is 20% for 6 months. "
            "For VIP customers, we can offer up to 40% or 1 month free. "
            "All discounts must be applied only if the customer mentions 'Cancellation' or 'Too Expensive'."
        )
        self.kb["Security Policy"] = (
            "Never share API keys or credentials over email. "
            "Internal requests for password resets must be redirected to the internal portal (https://sso.internal)."
        )

        # Sample Attachments
        self.attachments["invoice_2026.pdf"] = "INVOICE #9982: Total $540.23. Due: 2026-04-15."
        self.attachments["incident_report.docx"] = "REPORT: Potential security anomaly detected at 04:00 UTC."

    def add_email(self, sender: str, recipient: str, subject: str, body: str, folder: str = "Inbox", attachments: List[str] = None):
        id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        email = EmailDetail(
            id=id,
            sender=sender,
            recipient=recipient,
            subject=subject,
            body=body,
            timestamp=timestamp,
            folder=folder,
            thread_id=id,
            attachments=attachments or []
        )
        self.emails[id] = email
        return id

    def list_emails(self, folder: str) -> List[EmailHeader]:
        headers = []
        for email in self.emails.values():
            if email.folder == folder:
                headers.append(EmailHeader(
                    id=email.id,
                    sender=email.sender,
                    subject=email.subject,
                    folder=email.folder,
                    timestamp=email.timestamp,
                    is_read=False
                ))
        return headers

    def read_email(self, email_id: str) -> Optional[EmailDetail]:
        return self.emails.get(email_id)

    def move_email(self, email_id: str, target_folder: str):
        if email_id in self.emails:
            self.emails[email_id].folder = target_folder
            return True
        return False

    def search_kb(self, query: str) -> List[str]:
        results = []
        for key, value in self.kb.items():
            if query.lower() in key.lower() or query.lower() in value.lower():
                results.append(f"{key}: {value}")
        return results

    def check_crm(self, email_addr: str) -> Optional[Dict]:
        return self.crm.get(email_addr)

    def search_emails(self, query: str) -> List[EmailHeader]:
        headers = []
        for email in self.emails.values():
            if query.lower() in email.subject.lower() or query.lower() in email.body.lower():
                headers.append(EmailHeader(
                    id=email.id,
                    sender=email.sender,
                    subject=email.subject,
                    folder=email.folder,
                    timestamp=email.timestamp
                ))
        return headers

    def list_events(self) -> List[Dict]:
        return self.events

    def add_event(self, title: str, start: str, end: str):
        self.events.append({"title": title, "start": start, "end": end})
        return True

    def read_attachment(self, email_id: str, filename: str) -> Optional[str]:
        email = self.emails.get(email_id)
        if email and filename in email.attachments:
            return self.attachments.get(filename, "Content unavailable.")
        return None
