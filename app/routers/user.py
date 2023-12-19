from http import HTTPStatus
from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import crud, schema
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=HTTPStatus.OK, response_model=List[schema.User])
async def get_users(db: Session = Depends(get_db)) -> List[schema.User]:
    users = crud.get_users(db)

    return users


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schema.User)
async def create_user(
    payload: schema.UserCreate, db: Session = Depends(get_db)
) -> schema.User:
    user = crud.create_user(db, payload)

    return user


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=schema.User)
async def get_user(user_id: int, db: Session = Depends(get_db)) -> schema.User:
    user = crud.get_user(db, user_id)

    return user
