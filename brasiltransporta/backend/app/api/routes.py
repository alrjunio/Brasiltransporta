from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/ping")
def ping():
    return {"ping": "pong"}
