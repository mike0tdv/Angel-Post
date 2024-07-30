from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
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
    
    # admin_of_group = relationship("Groups", back_populates="adminID")



class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    member_limit = Column(Integer)
    code = Column(Integer)
    admin_username = Column(String) # relationship with the Member base
    places_taken = Column(Integer)

    # adminID = relationship("Member", back_populates="admin_of_group")


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    groupID = Column(Integer)
    memberID = Column(Integer)
    text = Column(String)

