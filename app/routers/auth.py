from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import schemas, database, models
from sqlalchemy.orm import Session
# from hashing import Hash
from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas import Logged

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

get_db = database.get_db

logged_user = schemas.Logged.logged_user
logged_user_name = schemas.Logged.logged_user_name

# def loggedUser(logged: bool):
#     if logged != logged_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")

@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends(schemas.Login), db: Session = Depends(get_db)):
    global logged_user, logged_user_name
    
    #checking if the user has entered the right credentials and if has an account in the first place
    user = db.query(models.Member).filter(models.Member.name==request.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")
    
    if not user.password == request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password credentials")

    logged_user = True
    logged_user_name = request.username
    return {"Data": f"Welcome back {request.username}"}