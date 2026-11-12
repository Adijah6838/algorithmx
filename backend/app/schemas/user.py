from pydantic import BaseModel, EmailStr
from typing import Optional

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: Optional[RoleResponse] = None
    
    class Config:
        from_attributes = True
