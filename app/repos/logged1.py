from fastapi import APIRouter
import main

router = APIRouter()

logged_user: bool = False
logged_user_name: str = None