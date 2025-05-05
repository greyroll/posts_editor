import uvicorn

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse

from loguru import logger

from classes.db_manager import DBManager
from orm_models.category import Category
from orm_models.post import Post
from orm_models.tag import Tag
from pydantic_model import PostDTO

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logger.add("logfile.log", level="DEBUG")
db = DBManager()


# [x]
# region Home

@app.get("/", response_class=HTMLResponse)
async def home():
    return RedirectResponse(url="/posts", status_code=302)

# endregion

# [x]
# region Meta

@app.get("/meta", response_class=HTMLResponse)
async def get_meta(request: Request, message: str | None = None, message_type: str = "info"):
    categories = db.get_all_cats()
    tags = db.get_all_tags()
    return templates.TemplateResponse(request=request, name="meta.html", context={
        "message": message,
        "message_type": message_type,
        "categories": categories,
        "tags": tags
    })

# endregion

#  [x]
# region Categories

@app.get("/categories/new", response_class=HTMLResponse)
async def new_category_get(request: Request):
    return templates.TemplateResponse(request=request, name="category_form.html", context={"category": None})

@app.post("/categories/new")
async def new_category_post(name: str = Form(...)):
    db.create_cat(name)
    return RedirectResponse(url="/meta?message=Category+added&message_type=success", status_code=302)

@app.get("/categories/{category_id}/edit", response_class=HTMLResponse)
async def edit_category_get(request: Request, category_id: int):
    category: Category | None = db.get_cat_by_id(category_id)
    return templates.TemplateResponse(request=request, name="category_form.html", context={"category": category})

@app.post("/categories/{category_id}/edit")
async def edit_category_post(category_id: int, name: str = Form(...)):
    db.update_cat(cat_id=category_id, new_name=name)
    return RedirectResponse(url="/meta?message=Category+updated&message_type=success", status_code=302)

# endregion

# [x]
# region Tags

@app.get("/tags/new", response_class=HTMLResponse)
async def new_tag_get(request: Request):
    return templates.TemplateResponse(request=request, name="tag_form.html", context={})

@app.post("/tags/new", response_class=HTMLResponse)
async def new_tag_post(name: str = Form(...)):
    db.create_tag(name)
    return RedirectResponse(url="/meta?message=Tag+added&message_type=success", status_code=302)

@app.post("/tags/{tag_id}/delete", response_class=HTMLResponse)
async def delete_tag(tag_id: int):
    db.delete_tag(tag_id)
    return RedirectResponse(url="/meta?message=Tag+deleted&message_type=success", status_code=302)

# endregion

# region Posts

@app.get("/posts", response_class=HTMLResponse)
async def get_post_list(request: Request, message: str | None = None, message_type: str = "info"):
    posts = db.get_all_posts()
    return templates.TemplateResponse(request=request, name="post_list.html", context={
        "message": message,
        "message_type": message_type,
        "posts": posts
    })


@app.get("/posts/new", response_class=HTMLResponse)
async def new_post_get(request: Request):
    categories: list[Category] = db.get_all_cats()
    tags: list[Tag] = db.get_all_tags()
    return templates.TemplateResponse(request=request, name="post_form.html", context={
        "post": None,
        "categories": categories,
        "tags": tags,
    })

@app.post("/posts/new")
async def new_post_post(post_dto: PostDTO = Depends(PostDTO.as_form)):
    db.create_post(
        title=post_dto.title,
        content=post_dto.content,
        category_id=post_dto.category_id,
        tag_ids=post_dto.tag_ids
    )
    return RedirectResponse(url="/posts?message=Post+added&message_type=success", status_code=302)

@app.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_get(request: Request, post_id: int):
    post = db.get_post_by_id(post_id)
    categories: list[Category] = db.get_all_cats()
    tags: list[Tag] = db.get_all_tags()
    return templates.TemplateResponse(request=request, name="post_form.html", context={
        "post": post,
        "categories": categories,
        "tags": tags,
    })

@app.post("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_post(post_id: int, post_dto: PostDTO = Depends(PostDTO.as_form)):
    db.update_post(
        post_id=post_id,
        title=post_dto.title,
        content=post_dto.content,
        category_id=post_dto.category_id,
        tag_ids=post_dto.tag_ids
    )
    return RedirectResponse(url="/posts?message=Post+edited&message_type=success", status_code=302)

@app.get("/posts/{post_id}", response_class=HTMLResponse)
async def view_post(request: Request, post_id: int):
    post: Post = db.get_post_by_id(post_id)
    return templates.TemplateResponse(request=request, name="post_view.html", context={"post": post})

# endregion

# region Filters (By Category / Tag)

@app.get("/category/{category_id}", response_class=HTMLResponse)
async def posts_by_category(request: Request, category_id: int):
    return templates.TemplateResponse(request=request, name="post_list.html", context={"posts": []})

@app.get("/tag/{tag_id}", response_class=HTMLResponse)
async def posts_by_tag(request: Request, tag_id: int):
    return templates.TemplateResponse(request=request, name="post_list.html", context={"posts": []})

# endregion

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
