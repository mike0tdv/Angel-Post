from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List, Dict
import schemas, models, database
from sqlalchemy.orm import Session
from routers import member, groups, auth
from repos import logged1
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# create an instance of FastAPI()
app = FastAPI()

# creating the connection to the db and the instance
models.Base.metadata.create_all(database.engine)

get_db = database.get_db

 
app.include_router(auth.router)
app.include_router(member.router)
app.include_router(groups.router)