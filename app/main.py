from fastapi import FastAPI, HTTPException, status, Depends
from typing import Optional, List
import schemas, models, database
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(database.engine)

get_db = database.get_db


@app.get("/members")
def ShowMembers():
    return {"Data":"All Members"}


@app.post("/members-create")
def create_members(request: schemas.Members, db: Session = Depends(get_db)):
    new_member = models.Member(name=request.name, age=request.age, city=request.city, groupCode=request.groupCode, password=request.password, messagesSent=request.messagesSent)
    db.add(new_member)
    db.flush()
    db.commit()
    db.refresh(new_member)
    return new_member


@app.get("/member/{id}/stats")
def MemberStats(id: int, db: Session = Depends(get_db)):
    data = db.query(models.Member).filter(models.Member.id == id).first()
    return {"Data": {
        "Name": data.name,
        "Messages Sent": data.messagesSent, # Must add calculation of the messages sent
        }}


@app.get("/member/{id}/login/messages-sent")
def ShowMessagesSent(id: int, login_confirmation: bool = False, limit: int = 10):
    if login_confirmation == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Missing login confirmation")      
    else: return {"Data":f"Last {limit} Messages Sent"}


@app.get("/group", response_model=List[schemas.ShowGroup])
def ShowGroups(db: Session = Depends(get_db), limit: int = 10):
    data = db.query(models.Groups).limit(limit).all()
    return data



@app.post("/group-create")
def GroupCreation(request: schemas.Group, db: Session = Depends(get_db)):
    new_group = models.Groups(name=request.name, member_limit=request.member_limit, code=request.code)
    db.add(new_group)
    db.flush()
    db.commit()
    db.refresh(new_group)
    return new_group