from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "analyst"


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True


class LogEntryResponse(BaseModel):
    id: int
    timestamp: datetime
    ip_address: str
    status_code: int
    endpoint: str
    user_agent: Optional[str]

    class Config:
        from_attributes = True
