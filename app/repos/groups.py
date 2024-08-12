from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1, auth

get_db = database.get_db


def get_group(db: Session, limit: int):
    data = db.query(models.Groups).limit(limit).all()
    return data


def send_message(group_name: str, receiver: str, message: str, db: Session):
    group = db.query(models.Groups).filter(models.Groups.name == group_name).first()
    message_receiver = db.query(models.Member).filter(models.Member.name == receiver).first()
    sender = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No group with the given name has been found")
    if not message_receiver or message_receiver.groupName != group_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No member with the given name has been found")
    
    new_message = models.Messages(groupName = group_name, memberName = sender.name, receiverName = receiver, text = message)   
    sender.messagesSent += 1
    db.add(new_message)
    db.flush()
    db.commit()
    db.refresh(new_message)

    return {"Data": "Message sent successfully"}


def show_all(db: Session, group_name: str):
    data = db.query(models.Member).filter(models.Member.groupName == group_name).all()
    return data


def join_new( db: Session, group_name: str, group_code: int):
    # creating instances of the user and his old group(if he had one)
    user = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    old_group_name = user.groupName
    old_group = db.query(models.Groups).filter(models.Groups.name == old_group_name).first()
    data = db.query(models.Groups).filter(models.Groups.name == group_name).first()

    if old_group_name == group_name:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You are already a member of this group!")

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No group with the given name has been found")

    if data.places_taken == data.member_limit:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="The group is already full")
    
    if group_code != data.code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid group code")
    
    if old_group:
        old_group.places_taken -= 1

    user.groupName = group_name
    data.places_taken += 1
    db.flush()
    db.commit()
    return {"Data": f"You joined '{group_name}' successfully"}


def leave(group_name: str, db: Session):
    member = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    if member.groupName != group_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You are not a member of this group: {group_name}")

    group = db.query(models.Groups).filter(models.Groups.name == group_name).first() 
    member.groupName = None
    group.places_taken -= 1
    db.flush()
    db.commit()
    return {"Data": f"You left '{group_name}' successfully"}
