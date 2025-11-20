from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from ..schemas.common import Response
from ..db.session import get_db
from ..schemas.user import UserCreate, UserRead
from ..schemas.auth import Token
from ..services.user_service import UserService
from ..services.auth_service import AuthService
from ..core.security import SECRET_KEY, ALGORITHM
from ..models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Response[UserRead])
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    user = UserService.create_user(db, user_in)
    return Response(
        success=True,
        message="Signup successful",
        data=user
    )

@router.post("/login", response_model=Response[Token])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    access_token = AuthService.create_login_token(
        db, form_data.username, form_data.password
    )
    return Response(
        success=True,
        message="Login successful",
        data=Token(access_token=access_token)
    )


class TokenBody(BaseModel):
    access_token: str

@router.post("/me", response_model=Response[UserRead])
def read_current_user_json(
    token_body: TokenBody,
    db: Session = Depends(get_db),
):
    token = token_body.access_token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(
        success=True,
        message="Current user info",
        data=user
    )
