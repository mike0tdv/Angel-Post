from pydantic import BaseModel
from typing import Optional


# class Logged():
#     logged_user: bool = False
#     logged_user_name: str = None


class Members(BaseModel):
    name: str
    age: int
    city: str
    password: str
    # messagesSent: int # Must add calculation of the messages sent
    # groupCode: Optional[int] = None
    # admin_of_group: Optional[str] = None

class ShowMember(BaseModel):
    name: str
    messagesSent: Optional[int] = None # Must add calculation of the messages sent
    # admin_of_group: str

    class Config:
        orm_mode = True


class About(BaseModel):
    name: str
    age: int
    city: str
    groupName: str
    messagesSent: Optional[int] = None # Must add calculation of the messages sent
    admin_of_group: Optional[str] = None
    

class Group(BaseModel):
    name: str
    member_limit: int
    code: int

class ShowGroup(BaseModel):
    name: str
    member_limit: int
    admin_username: str
    
    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str