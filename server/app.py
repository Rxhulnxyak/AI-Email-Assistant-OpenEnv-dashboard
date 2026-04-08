import os
import uvicorn
import gradio as gr
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from openenv.core.env_server import create_fastapi_app

from server.models import Action, EmailObservation
from server.env import AIEmailEnv
from server.dashboard import build_ui

# IMPORTANT FIX FOR HACKATHON PHASE 2:
# We must use `create_fastapi_app` from openenv-core! 
# If we try to write our own custom FastAPI routes, the Scaler Validator 
# cannot find the /info or /schema endpoints it needs to scrape the "3 tasks with graders"!

base_app = create_fastapi_app(
    env=AIEmailEnv(),
    action_cls=Action,
    observation_cls=EmailObservation
)

# Seamlessly mount the gorgeous Glassmorphism dashboard on top of the compliant API!
app = gr.mount_gradio_app(base_app, build_ui(), path="/dashboard")

@app.get("/")
def redirect_to_dashboard():
    return RedirectResponse(url="/dashboard")

def main():
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
