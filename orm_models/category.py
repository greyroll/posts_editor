from sqlmodel import Field, SQLModel, Relationship


class Category(SQLModel, table=True):
    __tablename__ = "category"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    posts: list["Post"] = Relationship(back_populates="category")
