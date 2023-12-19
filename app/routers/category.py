from http import HTTPStatus
from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app import crud, schema
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", status_code=HTTPStatus.OK, response_model=List[schema.Category])
async def get_categories(db: Session = Depends(get_db)) -> List[schema.Category]:
    categories = crud.get_categories(db)

    return categories


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schema.Category)
async def create_category(
    payload: schema.CategoryCreate, db: Session = Depends(get_db)
) -> schema.Category:
    category = crud.create_category(db, payload)

    return category


@router.get("/{category_id}", status_code=HTTPStatus.OK, response_model=schema.Category)
async def get_category(
    category_id: int, db: Session = Depends(get_db)
) -> schema.Category:
    category = crud.get_category(db, category_id)

    return category


@router.delete("/{category_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category

    :param db:
    :param category_id:
    :return:
    """

    crud.delete_category(db, category_id)


@router.post(
    "/{category_id}", status_code=HTTPStatus.OK, response_model=schema.Category
)
async def update_category(
    category_id: int, payload: schema.CategoryUpdate, db: Session = Depends(get_db)
) -> schema.Category:
    """
    Update a category

    :param db:
    :param category_id: str
    :param payload: schemas.CategoryUpdate
    :return:
    """

    category = crud.update_category(db, category_id, payload)

    return category
