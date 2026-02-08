from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}



@app.on_event("startup")
async def on_startup():
    print("Auth service started")