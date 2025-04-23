from datetime import datetime

from sqlmodel import Field, SQLModel, Relationship

from orm_models.category import Category
from orm_models.tag import Tag
from orm_models.post_tag import PostTag


class Post(SQLModel, table=True):
    __tablename__ = "post"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    category_id: int | None = Field(default=None, foreign_key="category.id")
    category: Category | None = Relationship(back_populates="posts")

    tags: list[Tag] = Relationship(back_populates="posts", link_model=PostTag)


