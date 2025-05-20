from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from snack_bar_system.database import get_session
from snack_bar_system.models import Produto
from snack_bar_system.schemas import GetProduto, PostProduto, ProdutoListResponse

router = APIRouter(prefix='/produto', tags=['produto'])


# ----- PRODUTO -----
@router.post('/produto', response_model=GetProduto)
def post_produto(produto: PostProduto, session: Session = Depends(get_session)):
    novo_produto = Produto(**produto.dict())
    session.add(novo_produto)
    session.commit()
    session.refresh(novo_produto)
    return novo_produto


@router.get('/produto', response_model=ProdutoListResponse)
def get_produto(session: Session = Depends(get_session)):
    produtos = session.scalars(select(Produto)).all()
    return {'produtos': produtos}
