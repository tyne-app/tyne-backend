from fastapi import FastAPI,status,HTTPException,APIRouter, Response
from sqlalchemy.orm import Session
from fastapi.params import Depends
from loguru import logger

local_router = APIRouter(
    prefix="/v1/local",
    tags=["Local"]
)

@local_router.post("/register")
def register_account():
    pass
