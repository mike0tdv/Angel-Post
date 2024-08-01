from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1

router = APIRouter(
    prefix="/members",
    tags=["Member"]
)

get_db = database.get_db

def loggedUser():
    if logged1.logged_user == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")


@router.get("/about", response_model=schemas.About)
def about_member(db: Session = Depends(get_db)):
    loggedUser()

    data = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    return data


@router.get("/messages-sent")
def show_messagesSent(limit: int = 10):
    loggedUser()      
    return {"Data":f"Last {limit} Messages Sent"}


@router.delete("/{member_name}/delete-account")
def delete_account(password: str, db: Session = Depends(get_db)):
    loggedUser()

    member = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    group = db.query(models.Groups).filter(models.Groups.name == member.groupName).first()

    if password != member.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password credentials")
    # if group.admin_username == member.name:


    # group.places_taken -= 1


    db.delete(member)
    db.commit()
    db.flush()    
    return {"Data": "Account deleted successfully"}