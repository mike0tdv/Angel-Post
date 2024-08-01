from fastapi import FastAPI
import models, database
from routers import member, groups, auth, admin

# create an instance of FastAPI()
app = FastAPI()

# creating the connection to the db and the instance
models.Base.metadata.create_all(database.engine)

get_db = database.get_db


app.include_router(auth.router)
app.include_router(member.router)
app.include_router(admin.router)
app.include_router(groups.router)
