import uvicorn

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from loguru import logger


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
logger.add("logfile.log", level="DEBUG")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="post_list.html", context={"posts": []})


@app.get("/meta", response_class=HTMLResponse)
async def get_meta(request: Request):
    return templates.TemplateResponse(request=request, name="meta.html", context={
        "categories": [],
        "tags": []
    })


@app.get("/categories/new", response_class=HTMLResponse)
async def new_category(request: Request):
    return templates.TemplateResponse(request=request, name="category_form.html", context={"category": None})


@app.get("/categories/{category_id}/edit", response_class=HTMLResponse)
async def edit_category(request: Request, category_id: int):
    return templates.TemplateResponse(request=request, name="category_form.html", context={"category": {"id": category_id, "name": "Sample"}})


@app.get("/tags/new", response_class=HTMLResponse)
async def new_tag(request: Request):
    return templates.TemplateResponse(request=request, name="tag_form.html", context={})


@app.post("/tags/{tag_id}/delete", response_class=HTMLResponse)
async def delete_tag(request: Request, tag_id: int):
    # логика удаления
    return templates.TemplateResponse(request=request, name="meta.html", context={"categories": [], "tags": []})


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
    return templates.TemplateResponse(request=request, name="post_view.html", context={
        "post": {
            "id": post_id,
            "title": "Sample Post",
            "content": "This is a sample post.",
            "category": {"name": "Tech"},
            "tags": [{"name": "Python"}, {"name": "FastAPI"}]
        }
    })


@app.get("/category/{category_id}", response_class=HTMLResponse)
async def posts_by_category(request: Request, category_id: int):
    return templates.TemplateResponse(request=request, name="post_list.html", context={"posts": []})


@app.get("/tag/{tag_id}", response_class=HTMLResponse)
async def posts_by_tag(request: Request, tag_id: int):
    return templates.TemplateResponse(request=request, name="post_list.html", context={"posts": []})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
