from fastapi import FastAPI, HTTPException
from server.models import Action, ResetRequest
from server.env import AIEmailEnv
import uvicorn
import os
import gradio as gr
from typing import Optional, Any
from server.dashboard import build_ui

app = FastAPI(title="AI Email Assistant OpenEnv")
env = AIEmailEnv()

@app.get("/api")
def read_root():
    return {"message": "AI Email Assistant OpenEnv API is running. Tag: openenv"}

@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    try:
        task_id = request.task_id if request else "beginner"
        obs = env.reset(task_id)
        # Return plain dict for maximum compatibility
        return {"observation": obs.model_dump(), "info": {}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/step")
def step(action: Action):
    try:
        obs, reward, done, info = env.step(action)
        return {
            "observation": obs.model_dump(),
            "reward": reward,
            "done": done,
            "info": info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/state")
def state():
    return env.state().model_dump()

# Mount Gradio Dashboard
app = gr.mount_gradio_app(app, build_ui(), path="/dashboard")

@app.get("/")
def redirect_to_dashboard():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
