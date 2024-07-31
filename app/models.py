from sqlalchemy import Column, Integer, String
from database import Base



class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)
    messagesSent = Column(Integer) # Must add calculation of the messages sent
    groupName = Column(String)
    admin_of_group = Column(String)
    password = Column(String)



class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    member_limit = Column(Integer)
    code = Column(Integer)
    admin_username = Column(String)
    places_taken = Column(Integer)


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    groupID = Column(Integer)
    memberID = Column(Integer)
    text = Column(String)

