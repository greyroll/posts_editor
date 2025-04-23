from sqlmodel import Field, SQLModel


class PostTag(SQLModel, table=True):
	__tablename__ = "post_tag"

	post_id: int = Field(foreign_key="post.id", primary_key=True)
	tag_id: int = Field(foreign_key="tag.id", primary_key=True)



