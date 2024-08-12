from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1, auth, groups

router = APIRouter(
    prefix="/group",
    tags=["Group"]
)

get_db = database.get_db


@router.get("/", response_model=List[schemas.ShowGroup])
def show_groups(db: Session = Depends(get_db), limit: int = 10):
    return groups.get_group(db, limit)


@router.post("/{group_name}/send-message")
def sent_message(group_name: str, receiver: str, message: str, db: Session = Depends(get_db)):
    auth.loggedUser()
    return groups.send_message(group_name, receiver, message, db)


@router.get("/{group_name}/show-members", response_model=List[schemas.ShowMember])
def show_members(*, db: Session = Depends(get_db), group_name: str):
    auth.loggedUser()
    return groups.show_all(db, group_name)


@router.post("/group/join-{group_name}")
def join_group(*, db: Session = Depends(get_db), group_name: str, group_code: int):
    auth.loggedUser()
    return groups.join_new(db, group_name, group_code)


@router.put("/{group_name}/leave")
def leave_group(group_name: str, db: Session = Depends(get_db)):
    auth.loggedUser()
    return groups.leave(group_name, db)
