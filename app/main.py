from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def index():
    return {"status": "ok"}