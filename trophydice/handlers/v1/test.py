from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Message(BaseModel):
    message: str


@router.get("/ping", response_model=Message)
def do_ping():
    return {"message": "pong"}
