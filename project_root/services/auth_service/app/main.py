from fastapi import FastAPI

from app.api.routers.auth_routers import router as auth_router
from app.api.routers.user_routers import router as user_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def on_startup():
    print("Auth service started")
