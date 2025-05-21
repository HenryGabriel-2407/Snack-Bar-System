from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routers import cliente, comanda, combo, produto

app = FastAPI()

app.include_router(cliente.router)
app.include_router(produto.router)
app.include_router(combo.router)
app.include_router(comanda.router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.get("/produto", response_class=HTMLResponse)
def page_produtos(request: Request):
    return templates.TemplateResponse("produtos.html", {"request": request})

