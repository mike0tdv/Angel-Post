from pydantic import BaseModel
from typing import Optional

class Members(BaseModel):
    name: str
    age: int
    city: str
    password: str

class ShowMember(BaseModel):
    name: str
    messagesSent: Optional[int] = None

    class Config:
        orm_mode = True


class About(BaseModel):
    name: str
    age: int
    city: str
    groupName: Optional[str] = None
    messagesSent: Optional[int] = None
    admin_of_group: Optional[str] = None
    

class Group(BaseModel):
    name: str
    member_limit: int
    code: int

class ShowGroup(BaseModel):
    name: str
    member_limit: int
    places_taken: int
    admin_username: str
    
    class Config:
        orm_mode = True


class ShowCreatedGroup(ShowGroup):
    code: int


class Login(BaseModel):
    username: str
    password: str

