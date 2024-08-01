from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

get_db = database.get_db


def loggedUser():
    if logged1.logged_user == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")



@router.post("/create-group", response_model=schemas.ShowCreatedGroup)
def group_creation(*, request: schemas.Group, db: Session = Depends(get_db)):
    loggedUser()
    
    used_name = db.query(models.Groups).filter(models.Groups.name == request.name).first()
    if used_name:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="This group name is already in use")
     
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


@router.put("/change-admin")
def change_admin(password: int, new_admin: str, db: Session = Depends(get_db)):
    loggedUser()

    return {"Data": "The admin of the group {group_name} has been successfully changed to {new_admin}"}


@router.delete("/delete-group")
def delete_group(password: str, group_name: str,  db: Session = Depends(get_db)):
    loggedUser()

    admin = db.query(models.Member).filter(models.Member.admin_of_group == group_name).first()

    if not admin or admin.name != logged1.logged_user_name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not the admin of the group")
    
    if admin.password != password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong admin credential")
    
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