from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)
    messagesSent = Column(Integer)
    groupName = Column(String, ForeignKey("groups.name")) 
    admin_of_group = Column(String, ForeignKey("groups.admin_username"))
    password = Column(String)

    groupAdmin = relationship("Groups", back_populates="admin")
    memberMesgs = relationship("Messages", back_populates="user")

class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    member_limit = Column(Integer)
    code = Column(Integer)
    admin_username = Column(String)
    places_taken = Column(Integer)

    admin = relationship("Member", back_populates="groupAdmin")
    messages = relationship("Messages", back_populates="group")

class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    groupName = Column(String, ForeignKey("Groups.name"))
    memberName = Column(String, ForeignKey("Member.name"))
    receiverName = Column(String)
    text = Column(String)

    group = relationship("Groups", back_populates="messages")
    user = relationship("Member", back_populates="groupAdmin")
