from pydantic import BaseModel


class Members(BaseModel):
    name: str
    age: int
    city: str
    messagesSent: int # Must add calculation of the messages sent
    groupCode: int
    password: str

    class Config:
        orm_mode = True


class Group(BaseModel):
    name: str
    member_limit: int
    code: int

class ShowGroup(BaseModel):
    name: str
    member_limit: int
    
    class Config:
        orm_mode = True
