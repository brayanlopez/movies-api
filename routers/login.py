from fastapi import APIRouter
from fastapi.responses import JSONResponse

from schemas.User import User

from utils.jwt_manager import create_token

login_router = APIRouter()

@login_router.post("/login", tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token_bytes = create_token(user.model_dump())
        return JSONResponse(content=token_bytes, status_code=200)