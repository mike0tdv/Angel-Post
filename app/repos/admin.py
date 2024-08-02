from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1, auth

get_db = database.get_db


def create(db: Session, request: schemas.Group):

    admin = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    used_name = db.query(models.Groups).filter(models.Groups.name == request.name).first()
    
    if used_name:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="This group name is already in use")
    if admin.admin_of_group != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are already an admin of a group. Change the admin first")


    new_group = models.Groups(name=request.name, member_limit=request.member_limit, code=request.code, admin_username=logged1.logged_user_name, places_taken = 1)
    
    user = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    old_group = db.query(models.Groups).filter(models.Groups.name == user.groupName).first() 
    if old_group:
        old_group.places_taken -= 1

    admin = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    admin.admin_of_group = request.name
    admin.groupName = request.name

    db.add(new_group)
    db.flush()
    db.commit()
    db.refresh(new_group)
    return new_group



def admin_change(db: Session, password: str, new_admin: str, group_name: str):

    group = db.query(models.Groups).filter(models.Groups.name == group_name).first()
    member = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    admin_new = db.query(models.Member).filter(models.Member.name == new_admin).first()
    
    
    if member.password != password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong admin credential")
    if group.admin_username != member.name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the admin of this group")
    if not admin_new:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No member with the given name has been found")
    if admin_new.groupName != group.name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{new_admin} is not a member of this group")
    if admin_new.admin_of_group != None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user is already an admin of another group")
    
    member.admin_of_group = None
    admin_new.admin_of_group = group_name
    group.admin_username = new_admin
    db.flush()
    db.commit()
    return {"Data": f"The admin of the group {group_name} has been successfully changed to {new_admin}"}


def delete(db: Session, password: str, group_name: str):
    
    admin = db.query(models.Member).filter(models.Member.admin_of_group == group_name).first()

    if admin.password != password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong admin credential")
    
    if not admin or admin.name != logged1.logged_user_name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the admin of the group")
    
    group = db.query(models.Groups).filter(models.Groups.name == admin.admin_of_group).first()

    members = db.query(models.Member).all()
    
    for member in members:
        if member.groupName == group.name:
             member.groupName = None
        if member.admin_of_group == group.name:
            member.admin_of_group = None

    db.delete(group)
    db.flush()
    db.commit()
    return {"Group has been successfully deleted"}