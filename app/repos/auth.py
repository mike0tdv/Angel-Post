from fastapi import HTTPException, status
from repos import logged1


def loggedUser():
    if logged1.logged_user == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Log in to see this info")