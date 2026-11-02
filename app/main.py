from fastapi import FastAPI

from app.routes import activities

app = FastAPI(title="Activity Tracker")

app.include_router(activities.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
