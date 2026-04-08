
# AI Email Assistant OpenEnv (Hackathon )


![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-teal)

A high-fidelity, real-world task simulation environment for AI agents focused on advanced email management and customer negotiation. This environment is fully compliant with the **Meta OpenEnv** specification.

## 🚀 Overview & Motivation
Static benchmarks (TOY/Games) often fail to capture the multi-step reasoning and tool-usage reliability required for real-world automation. This environment simulates a corporate email system integrated with CRM and Knowledge Base backends, requiring agents to synthesize information across multiple modalities to achieve complex goals.

## 🛠 OpenEnv Specification Compliance
This project strictly implements the OpenEnv interface:
- **Typed Models**: Uses Pydantic for all Observations and Actions.
- **REST Interface**: Exposes `/reset`, `/step`, and `/state` via FastAPI.
- **Metadata**: Included in `openenv.yaml`.
- **Validation**: Pass standard `openenv validate` checks.

## 📋 Task Scenarios

| Difficulty | Task Name | Objective | Grading Logic |
| :--- | :--- | :--- | :--- |
| **Easy** | Corporate Triage | Sort emails by domain into folders. | % of emails in correct folder. |
| **Medium** | Security FAQ | Draft response using KB policy. | Keyword & link synthesis. |
| **Hard** | Strategic Retention | Negotiate with a churn-risk customer. | Churn prevention & value preservation. |
| **Expert** | Crisis Management | Handle a data breach report using CRM/KB. | Policy compliance & speed. |
| **Expert** | Meeting Scheduler | Find a common slot using the Calendar tool. | Slot accuracy & coordination. |

## 🧬 Action & Observation Spaces

### Actions
- `ListEmails(folder)`: List headers in a specific folder.
- `ReadEmail(email_id)`: Get full body and metadata.
- `MoveEmail(email_id, target)`: Reorganize the mailbox.
- `CallTool(name, args)`: Interact with CRM or KB.
- `CalendarAction(method, args)`: Check or schedule events.
- `DraftReply(email_id, content)`: Prepare a response.
- `SendReply(email_id)`: Finalize and send.

### Observations
- `emails`: Structured headers list.
- `current_email`: Detailed email object.
- `tool_output`: Structured output from KB/CRM.
- `reward`: Progressive float (0.0 to 1.0).

## ⚙️ Setup & Usage

### Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the environment:
   ```bash
   python app.py
   ```
3. Test manually in the **Playground**:
   ```bash
   python playground.py
   ```
4. Run the baseline:
   ```bash
   python baseline_inference.py
   ```

### Docker (Hugging Face Spaces)
Build and run the container:
```bash
docker build -t ai-email-openenv .
docker run -p 7860:7860 ai-email-openenv
```

## 📊 Baseline Performance
| Task | Model | Score |
| :--- | :--- | :--- |
| Beginner | gpt-4o-mini | 1.00 |
| Intermediate | gpt-4o-mini | 0.85 |
| Advanced | gpt-4o-mini | 0.60 |

---
*Created for the Meta OpenEnv Hackathon Finale.*
