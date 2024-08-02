from fastapi import HTTPException, status, Depends, APIRouter
from typing import List
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1, auth, admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

get_db = database.get_db


@router.post("/create-group", response_model=schemas.ShowCreatedGroup)
def group_creation(*, request: schemas.Group, db: Session = Depends(get_db)):
    auth.loggedUser()
    return admin.create(db, request)


@router.put("/change-admin")
def change_admin(password: str, new_admin: str, group_name: str, db: Session = Depends(get_db)):
    auth.loggedUser()
    return admin.admin_change(db, password, new_admin, group_name)


@router.delete("/delete-group")
def delete_group(password: str, group_name: str,  db: Session = Depends(get_db)):
    auth.loggedUser()
    return admin.delete(db, password, group_name)