from http import HTTPStatus
from typing import List, Annotated, Optional

from fastapi import HTTPException, Depends, APIRouter, Query
from sqlalchemy.orm import Session

from app import crud, schema, models, oauth2
from app.database import get_db

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/", status_code=HTTPStatus.OK, response_model=List[schema.Article])
async def get_articles(
    limit: Annotated[int, Query(ge=1)],
    page: Annotated[int, Query(ge=1)],
    search: Annotated[str, Query()] = "",
    db: Session = Depends(get_db),
) -> List[schema.Article]:
    """
    Get all articles

    :return:
    """
    offset = 0 if page == 1 else (limit * page - 1)
    try:
        articles = crud.get_articles(db=db, skip=offset, limit=limit, search=search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return articles


@router.post("/", status_code=HTTPStatus.CREATED, response_model=schema.Article)
async def create_article(
    payload: schema.ArticleCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schema.Article:
    """
    Create a article

    :param current_user:
    :param db:
    :param payload:
    :return:
    """
    payload.author_id = current_user.id
    new_article = crud.create_article(db, payload)
    if not new_article:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error occurred, Please try again",
        )

    return new_article


@router.get("/latest", status_code=HTTPStatus.OK, response_model=schema.Article)
async def get_latest_article(db: Session = Depends(get_db)) -> schema.Article:
    """
    Get the latest article

    :return:
    """
    article = crud.get_latest_article(db)

    return article


@router.post("/{article_id}", status_code=HTTPStatus.OK, response_model=schema.Article)
async def update_article(
    article_id: int,
    payload: schema.ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
) -> schema.Article:
    """
    Update a article

    :param db:
    :param article_id: str
    :param payload: schemas.ArticleUpdate
    :return:
    """

    article_query = db.query(models.Article).filter(models.Article.id == article_id)
    db_article = article_query.first()

    if not db_article:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Article not found"
        )

    if current_user.id != db_article.author_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="You are not authorized to modify this resource!",
        )

    article = crud.update_article(db, db_article, payload)

    return article


@router.get("/{article_id}", status_code=HTTPStatus.OK, response_model=schema.Article)
async def get_article(article_id: int, db: Session = Depends(get_db)) -> schema.Article:
    """
    Get a article

    :param db:
    :param article_id:
    :return:
    """
    article = crud.get_article(db, article_id)

    if not article:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Article not found"
        )

    return article


@router.delete("/{article_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    """
    Delete a article

    :param db:
    :param article_id:
    :return:
    """

    article = db.query(models.Article).filter(models.Article.id == article_id).first()

    if not article:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Article not found"
        )

    if current_user.id != article.author_id:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="You are not authorized to modify this resource!",
        )

    crud.delete_article(db, article_id)
