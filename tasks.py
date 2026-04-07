from typing import Dict, Any, Callable
from mock_system import MockSystem

def beginner_grader(system: MockSystem) -> float:
    total_emails = len(system.emails)
    if total_emails == 0: return 0.0
    
    correct = 0
    for email in system.emails.values():
        if "@example.com" in email.sender and email.folder == "Internal":
            correct += 1
        elif "@example.com" not in email.sender and email.folder == "External":
            correct += 1
            
    return round(correct / total_emails, 2)

def intermediate_grader(system: MockSystem) -> float:
    score = 0.0
    for email_id, draft in system.drafts.items():
        if "sso" in draft.lower() and "https://sso.internal" in draft.lower():
            score = 1.0
            break
        elif "sso" in draft.lower():
            score = 0.5
    return score

def advanced_grader(system: MockSystem) -> float:
    score = 0.0
    for email_id, draft in system.drafts.items():
        content = draft.lower()
        if "1 month free" in content and "loyalty" in content:
            score = 1.0
            break
        elif "1 month free" in content:
            score = 0.6
        elif "discount" in content:
            score = 0.3
    return score

    return score

def crisis_grader(system: MockSystem) -> float:
    # Requires checking CRM + KB + Drafting correct response
    score = 0.0
    for email_id, draft in system.drafts.items():
        content = draft.lower()
        if "incident" in content and "investigating" in content and "24 hours" in content:
            score = 1.0
        elif "investigating" in content:
            score = 0.5
    return score

def scheduler_grader(system: MockSystem) -> float:
    # Requires finding overlap (11:00-12:00 or 15:00-16:00)
    score = 0.0
    for event in system.events:
        if "Sync" in event["title"] and event["start"] == "2026-04-07 11:00":
            score = 1.0
    return score

TASKS = {
    "beginner": {
        "name": "Corporate Triage",
        "objective": "Categorize all emails into 'Internal' or 'External' folders based on sender domain (@example.com).",
        "difficulty": "Easy",
        "initial_emails": [
            {"sender": "boss@example.com", "recipient": "me@example.com", "subject": "Quarterly Report", "body": "Please review by EOD."},
            {"sender": "spam@gmail.com", "recipient": "me@example.com", "subject": "Win a Prize!", "body": "Click here to claim."},
            {"sender": "hr@example.com", "recipient": "me@example.com", "subject": "Open Enrollment", "body": "Benefit window is closing."},
            {"sender": "jane.smith@partner.com", "recipient": "me@example.com", "subject": "Project Proposal", "body": "Attached is the proposal."}
        ],
        "grader": beginner_grader,
        "metadata": {"type": "classification"}
    },
    "intermediate": {
        "name": "Security Policy FAQ",
        "objective": "A user is asking how to reset their password. Look up the policy and draft an accurate response.",
        "difficulty": "Medium",
        "initial_emails": [
            {"sender": "user123@example.com", "recipient": "support@example.com", "subject": "Password Reset", "body": "Hi, I forgot my password. How do I reset it?"}
        ],
        "grader": intermediate_grader,
        "metadata": {"type": "synthesis"}
    },
    "advanced": {
        "name": "Strategic Retention",
        "objective": "A high-value customer wants to cancel. Negotiate a retention offer using CRM data and company policy.",
        "difficulty": "Hard",
        "initial_emails": [
            {"sender": "angry.customer@gmail.com", "recipient": "retention@example.com", "subject": "I am canceling my subscription", "body": "Your service is too expensive and I don't feel valued."}
        ],
        "grader": advanced_grader,
        "metadata": {"type": "negotiation"}
    },
    "crisis": {
        "name": "Expert: Crisis Management",
        "objective": "A customer reports a potential data breach. Use CRM and KB to verify policy and draft a holding statement.",
        "difficulty": "Expert",
        "initial_emails": [
            {"sender": "hacker.detective@gmail.com", "recipient": "security@example.com", "subject": "URGENT: Data Leak Found", "body": "I found your customer list on a dark web forum. Please confirm."}
        ],
        "grader": crisis_grader,
        "metadata": {"type": "critical"}
    },
    "scheduler": {
        "name": "Expert: The Meeting Scheduler",
        "objective": "Coordinate a meeting between two partners. Check the calendar and find the first available common slot.",
        "difficulty": "Expert",
        "initial_emails": [
            {"sender": "jane.smith@partner.com", "recipient": "me@example.com", "subject": "Meeting?", "body": "Are you free at 11am today?"},
            {"sender": "bob.jones@partner.com", "recipient": "me@example.com", "subject": "Re: Meeting", "body": "11am works for me too!"}
        ],
        "grader": scheduler_grader,
        "metadata": {"type": "coordination"}
    }
}
