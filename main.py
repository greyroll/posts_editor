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

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logger.add("logfile.log", level="DEBUG")
db = DBManager()

# region Home

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    posts = db.get_all_posts()
    return templates.TemplateResponse(request=request, name="post_list.html", context={"posts": posts})

# endregion

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

# region Categories

@app.get("/categories/new", response_class=HTMLResponse)
async def new_category_get(request: Request):
    return templates.TemplateResponse(request=request, name="category_form.html", context={"category": None})

@app.post("/categories/new")
async def new_category_post(name: str = Form(...)):
    db.create_cat(name)
    return RedirectResponse(url="/meta?message=Category+added&message_type=success", status_code=302)

@app.get("/categories/{category_id}/edit", response_class=HTMLResponse)
async def edit_category(request: Request, category_id: int):
    category: Category | None = db.get_cat_by_id(category_id)
    return templates.TemplateResponse(request=request, name="category_form.html", context={"category": category})

@app.post("/categories/{category_id}/edit")
async def edit_category(request: Request, category_id: int, name: str = Form(...)):
    db.update_cat(cat_id=category_id, new_name=name)
    return RedirectResponse(url="/meta?message=Category+updated&message_type=success", status_code=302)

# endregion

# region Tags

@app.get("/tags/new", response_class=HTMLResponse)
async def new_tag(request: Request):
    return templates.TemplateResponse(request=request, name="tag_form.html", context={})

@app.post("/tags/{tag_id}/delete", response_class=HTMLResponse)
async def delete_tag(request: Request, tag_id: int):
    return templates.TemplateResponse(request=request, name="meta.html", context={"categories": [], "tags": []})

# endregion

# region Posts

@app.get("/posts/new", response_class=HTMLResponse)
async def new_post(request: Request):
    return templates.TemplateResponse(request=request, name="post_form.html", context={
        "post": None,
        "categories": [],
        "tags": [],
        "post_tag_ids": []
    })

@app.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post(request: Request, post_id: int):
    return templates.TemplateResponse(request=request, name="post_form.html", context={
        "post": {"id": post_id, "title": "Sample", "content": "Text", "category_id": 1},
        "categories": [],
        "tags": [],
        "post_tag_ids": [1, 2]
    })

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
