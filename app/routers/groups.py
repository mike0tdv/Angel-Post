from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)

get_db = database.get_db


def loggedUser(logged: bool):
    if logged != logged1.logged_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")




@router.get("/", response_model=List[schemas.ShowGroup])
def show_groups(db: Session = Depends(get_db), limit: int = 10):
    data = db.query(models.Groups).limit(limit).all()
    return data


@router.post("/{group_name}/sent-message")
def sent_message(logged: bool, group_name: str, receiver: str, message: str, db: Session = Depends(get_db)):
    loggedUser(logged)

    group = db.query(models.Groups).filter(models.Groups.name == group_name).first()
    message_receiver = db.query(models.Member).filter(models.Member.name == receiver).first()
    sender = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No group with the given name has been found")
    if message_receiver.groupName != group_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No member with the given name has been found")
    
    new_message = models.Messages(groupName = group_name, memberName = sender.name, receiverName = receiver, text = message)   
    sender.messagesSent += 1
    db.add(new_message)
    db.flush()
    db.commit()
    db.refresh(new_message)

    return {"Data": "Message sent successfully"}


@router.get("/{group_name}/show-members", response_model=List[schemas.ShowMember])
def show_members(*, db: Session = Depends(get_db), group_name: str, logged: bool):
    loggedUser(logged)
    
    data = db.query(models.Member).filter(models.Member.groupName == group_name).all()
    return data


@router.post("/group/join-{group_name}")
def join_group(*, db: Session = Depends(get_db), group_name: str, logged: bool, group_code: int):
    loggedUser(logged)

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


@router.put("/{group_name}/leave")
def leave_group(group_name: str, logged: bool, db: Session = Depends(get_db)):
    loggedUser(logged)

    member = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    if member.groupName != group_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"You are not a member of this group: {group_name}")

    group = db.query(models.Groups).filter(models.Groups.name == group_name).first() 
    member.groupName = None
    group.places_taken -= 1
    db.flush()
    db.commit()
    return {"Data": f"You left '{group_name}' successfully"}


@router.post("/create", response_model=schemas.ShowCreatedGroup)
def group_creation(*, request: schemas.Group, db: Session = Depends(get_db), logged: bool):
    loggedUser(logged)
    
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


@router.delete("/delete")
def delete_group(logged: bool, password: str, group_name: str,  db: Session = Depends(get_db)):
    loggedUser(logged)

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