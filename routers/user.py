from fastapi import HTTPException, APIRouter, status
from sqlalchemy import select

from schema.request import UserSignUPRequest
from database.db_connection import SessionFactory
from models import User
router = APIRouter(tags=["User"])

# 회원가입
@router.post(
    path="/users/signup",
    status_code=status.HTTP_201_CREATED,
)
def signup_user_handler(body: UserSignUPRequest):
    # 이메일 중복 검사
    with SessionFactory() as session:
        stmt = select(User).where(User.email == body.email)
        existing_user = session.scalar(stmt)
        if existing_user:
            # 중복 이메일인 경우 오류 응답 반환
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일입니다."
            )