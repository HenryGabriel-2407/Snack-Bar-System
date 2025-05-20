from fastapi import FastAPI

from routers import cliente, comanda, combo, produto

app = FastAPI()

app.include_router(cliente.router)
app.include_router(produto.router)
app.include_router(combo.router)
app.include_router(comanda.router)
