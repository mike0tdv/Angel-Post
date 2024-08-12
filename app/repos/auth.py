from fastapi import HTTPException, status
from repos import logged1
import database, models, schemas
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

get_db = database.get_db

def loggedUser():
    if logged1.logged_user == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")
    

def loginMain(db: Session, request: OAuth2PasswordRequestForm):
     
    user = db.query(models.Member).filter(models.Member.name==request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")
    
    if not user.password == request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password credentials")

    logged1.logged_user = True
    logged1.logged_user_name = request.username
    return {"Data": f"Welcome back {request.username}"}


def signIn(db: Session, request: schemas.Members):
    
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


def signOut():
    logged1.logged_user = False
    logged1.logged_user_name = None
    return {"Data": "Successfully logged out!"}