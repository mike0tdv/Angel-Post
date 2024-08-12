from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1, auth, member
from typing import List

router = APIRouter(
    prefix="/members",
    tags=["Member"]
)

get_db = database.get_db


@router.get("/about", response_model=schemas.About)
def about_member(db: Session = Depends(get_db)):
    auth.loggedUser()
    return member.about(db)
    

@router.get("/messages-sent", response_model=List[schemas.ShowMessage])
def show_messagesSent(db: Session = Depends(get_db)):
    auth.loggedUser()      
    return member.messages_show(db)


@router.delete("/delete-account")
def delete_account(password: str, db: Session = Depends(get_db)):
    auth.loggedUser()   
    return member.delete(db, password)