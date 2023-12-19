from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schema, crud, utils, models, oauth2
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", status_code=HTTPStatus.OK)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # get user
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Invalid Credentials"
        )

    if not utils.verify_hash(user_credentials.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "access_type": "bearer"}
