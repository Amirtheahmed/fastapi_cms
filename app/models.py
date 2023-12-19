from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, index=True, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    published = Column(Boolean, nullable=False, default=True)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        default=None,
    )
    number_of_words = Column(Integer, nullable=False, default=0)
    minutes_to_read = Column(Integer, nullable=False, default=0)
    image = Column(String, nullable=True)
    slug = Column(String, nullable=True)
    keywords = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scheduled_at = Column(TIMESTAMP(timezone=True), nullable=True)
    source_url = Column(String, nullable=True)
    fetch_timestamp = Column(TIMESTAMP(timezone=True), nullable=True)
    view_count = Column(Integer, nullable=False, default=0)
    shortened_link = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

    author = relationship("User", back_populates="articles")
    category = relationship("Category", back_populates="articles")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    articles = relationship("Article", back_populates="category")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, server_default=expression.true())
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=expression.text("now()")
    )

    articles = relationship("Article", back_populates="author")
