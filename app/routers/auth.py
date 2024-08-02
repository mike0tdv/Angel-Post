from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import schemas, database, models
from sqlalchemy.orm import Session
from repos import logged1, auth

router = APIRouter(
    tags=["Authentication"]
    )

get_db = database.get_db

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(schemas.Login), db: Session = Depends(get_db)):
    return auth.loginMain(db, request)


@router.post("/sign-in", response_model=schemas.Members)
def create_members(request: schemas.Members, db: Session = Depends(get_db)):
    return auth.signIn(db, request)
