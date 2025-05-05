from fastapi import Form
from pydantic import BaseModel, Field


class PostDTO(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    category_id: int | None
    tag_ids: list[int] | None

    @classmethod
    def as_form(cls, title: str = Form(...), content: str = Form(...), category_id: int = Form(...), tag_ids: list[int] | None = Form(...)):
        return cls(title=title, content=content, category_id=category_id, tag_ids=tag_ids)



