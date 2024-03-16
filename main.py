from uvicorn import Server, Config
from fastapi import FastAPI, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
import os

from routers import yolo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(yolo.router)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    server = Server(Config(app, host="0.0.0.0", port=port, lifespan="on"))

    # Run object detection in background
    capture_task = BackgroundTasks()
    capture_task.add_task(yolo.capture_frames)

    server.run(background_tasks=[capture_task])
