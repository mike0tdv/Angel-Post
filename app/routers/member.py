from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1

router = APIRouter(
    prefix="/members",
    tags=["Member"]
)

get_db = database.get_db

@router.post("/sign-in", response_model=schemas.Members)
def create_members(request: schemas.Members, db: Session = Depends(get_db)):

    data = db.query(models.Member).filter(models.Member.name == request.name).first()
    if data:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="This username is already in use")
    new_member = models.Member(name=request.name, age=request.age, city=request.city, password=request.password, messagesSent = 0)
    db.add(new_member)
    db.flush()
    db.commit()
    db.refresh(new_member)
    logged1.logged_user = True
    logged1.logged_user_name = request.name
    return new_member

@router.get("/about", response_model=schemas.About)
def about_member(*, db: Session = Depends(get_db), login_confirmation: bool):
    if login_confirmation != logged1.logged_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")

    data = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    return data


@router.get("/messages-sent")
def show_messagesSent(login_confirmation: bool, limit: int = 10):
    if login_confirmation != logged1.logged_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")      
    return {"Data":f"Last {limit} Messages Sent"}