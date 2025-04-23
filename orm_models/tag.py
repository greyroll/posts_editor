from sqlmodel import Field, SQLModel, Relationship

from orm_models.post_tag import PostTag


class Tag(SQLModel, table=True):
	__tablename__ = "tag"

	id: int | None = Field(default=None, primary_key=True)
	name: str = Field(index=True, unique=True)

	posts: list["Post"] = Relationship(back_populates="tags", link_model=PostTag)

