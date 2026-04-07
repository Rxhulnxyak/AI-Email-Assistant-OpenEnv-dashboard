from fastapi import FastAPI, HTTPException
from server.models import Action, ResetRequest
from server.env import AIEmailEnv
import uvicorn
import os
import gradio as gr
from server.dashboard import build_ui

app = FastAPI(title="AI Email Assistant OpenEnv")
env = AIEmailEnv()

@app.get("/api")
def read_root():
    return {"message": "AI Email Assistant OpenEnv API is running. Tag: openenv"}

@app.post("/reset")
def reset(request: ResetRequest):
    try:
        task_id = request.task_id
        obs = env.reset(task_id)
        return {"observation": obs, "info": {}}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state()

# Mount Gradio Dashboard to Root
app = gr.mount_gradio_app(app, build_ui(), path="/")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
