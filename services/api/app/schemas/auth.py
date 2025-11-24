from typing import Optional
from pydantic import BaseModel, EmailStr



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenBody(BaseModel):
    access_token: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
