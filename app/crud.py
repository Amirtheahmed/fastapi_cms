from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app import models, schema, utils


def get_articles(db: Session, skip: int = 0, limit: int = 100, search: str = ""):
    return (
        db.query(models.Article)
        .filter(models.Article.title.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_article(db: Session, article: schema.ArticleCreate):
    db_article = models.Article(**article.dict())

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_latest_article(db: Session):
    return db.query(models.Article).order_by(desc(models.Article.created_at)).first()


def update_article(
    db: Session, article: models.Article, article_data: schema.ArticleUpdate
):
    update_data = article_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)

    return article


def delete_article(db: Session, article_id: int):
    article_query = db.query(models.Article).filter(models.Article.id == article_id)

    article_query.delete()
    db.commit()

    return True


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.UserCreate):
    hashed_password = utils.hash_string(user.password)
    user.password = hashed_password
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")

    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")

    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found!")

    return user


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schema.CategoryCreate):
    db_category = models.Category(**category.dict())

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    category = (
        db.query(models.Category).filter(models.Category.id == category_id).first()
    )

    if not category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Category not found!"
        )

    return category


def update_category(
    db: Session, category_id: int, category_data: schema.CategoryUpdate
):
    category_query = db.query(models.Article).filter(models.Category.id == category_id)
    db_category = category_query.first()

    if not db_category:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Article not found"
        )

    update_data = category_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)

    return db_category


def delete_category(db: Session, category_id: int):
    category_query = db.query(models.Category).filter(models.Category.id == category_id)

    if not category_query.first():
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Category not found"
        )

    category_query.delete()
    db.commit()

    return True
