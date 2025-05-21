from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic models for request and response validation/serialization

class UserBase(BaseModel):
    firstname: str
    password: str
    lastname: str
    email: str
    login: str

class UserInDB(UserBase):
    user_id: int

    class Config:
        from_attributes = True # This was formerly orm_mode = True in older Pydantic versions

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    firstname: Optional[str] = None
    password: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    login: Optional[str] = None

class DataBase(BaseModel):
    category_id: int
    description: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime
    content: str
    format: str
    name: str

class DataCreate(DataBase):
    pass

class DataUpdate(BaseModel):
    category_id: Optional[int] = None
    description: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    content: Optional[str] = None
    format: Optional[str] = None
    name: Optional[str] = None

class DataInDB(DataBase):
    data_id: int

    class Config:
        from_attributes = True