from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):

        from .user_service import UserService

        # email 로 사용자 조회
        user = UserService.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_login_token(db: Session, email: str, password: str) -> str:
        user = AuthService.authenticate_user(db, email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        # 토큰 payload 에 user_id, username, email 모두 포함
        data = {
            "user_id": str(user.id),
            "username": user.username,
            "email": user.email,
        }

        return create_access_token(
            data=data,
            expires_delta=access_token_expires,
        )
