from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
import schemas, models, database
from sqlalchemy.orm import Session
from repos import logged1

get_db = database.get_db


def about(db: Session):
    data = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    return data


def delete(db: Session, password: str):
    member = db.query(models.Member).filter(models.Member.name == logged1.logged_user_name).first()
    group = db.query(models.Groups).filter(models.Groups.name == member.groupName).first()

    if password != member.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password credentials")
    if group != None:
        if group.admin_username == logged1.logged_user_name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are an admin of a group. Change the admin first")
        group.places_taken -= 1


    db.delete(member)
    db.commit()
    db.flush()    
    return {"Data": "Account deleted successfully"}