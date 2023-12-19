from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class ArticleBase(BaseModel):
    title: str
    content: Optional[str] = None
    published: bool = True


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class CategoryWithArticles(Category):
    articles: List[ArticleBase] = []


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str
    is_active: bool = True


class User(UserBase):
    id: int
    username: str
    is_active: bool = True
    created_at: datetime

    class Config:
        orm_mode = True


class UserWithArticles(User):
    articles: List[ArticleBase] = []


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ArticleCreate(ArticleBase):
    category_id: int
    author_id: int
    number_of_words: Optional[int] = 0
    minutes_to_read: Optional[int] = 0
    image: Optional[str] = None
    slug: Optional[str] = None
    keywords: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    source_url: Optional[str] = None
    fetch_timestamp: Optional[datetime] = None
    view_count: Optional[int] = 0
    shortened_link: Optional[str] = None


class ArticleUpdate(ArticleBase):
    category_id: Optional[int] = None
    author_id: Optional[int] = None
    number_of_words: Optional[int] = 0
    minutes_to_read: Optional[int] = 0
    image: Optional[str] = None
    slug: Optional[str] = None
    keywords: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    source_url: Optional[str] = None
    fetch_timestamp: Optional[datetime] = None
    view_count: Optional[int] = 0
    shortened_link: Optional[str] = None


class Article(ArticleBase):
    id: int
    category_id: int
    author_id: int
    number_of_words: Optional[int] = 0
    minutes_to_read: Optional[int] = 0
    image: Optional[str] = None
    slug: Optional[str] = None
    keywords: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    source_url: Optional[str] = None
    fetch_timestamp: Optional[datetime] = None
    view_count: Optional[int] = 0
    shortened_link: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author: User

    class Config:
        orm_mode = True


class ArticleWithAuthorCategory(Article):
    category: CategoryBase
    author: UserBase


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
