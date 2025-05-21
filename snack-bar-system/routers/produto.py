from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from http import HTTPStatus

from snack_bar_system.database import get_session
from snack_bar_system.models import Produto
from snack_bar_system.schemas import GetProduto, PostProduto, ProdutoListResponse, UpdateProduto

router = APIRouter(prefix='/produto', tags=['produto'])


# ----- PRODUTO -----
@router.post('/', response_model=GetProduto)
def post_produto(produto: PostProduto, session: Session = Depends(get_session)):
    novo_produto = Produto(**produto.dict())
    session.add(novo_produto)
    session.commit()
    session.refresh(novo_produto)
    return novo_produto


@router.get('/', response_model=ProdutoListResponse)
def get_produtos(session: Session = Depends(get_session)):
    produtos = session.scalars(select(Produto)).all()
    return {'produtos': produtos}


@router.get('/{produto_id}', response_model=GetProduto)
def get_produto(produto_id: int, session: Session = Depends(get_session)):
    produto = session.scalar(select(Produto).where(Produto.id == produto_id))
    if not produto:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado")
    return produto

@router.delete('/{produto_id}')
def delete_produto(produto_id: int, session: Session = Depends(get_session)):
    produto = session.scalar(select(Produto).where(Produto.id == produto_id))
    if not produto:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado")
    # Verificar se tem combo associado ao produto
    session.delete(produto)
    session.commit()
    return 'Produto deletado com sucesso!'


@router.put('/{produto_id}', response_model=GetProduto)
def update_produto(produto_id: int, dados: UpdateProduto, session: Session = Depends(get_session)):
    produto = session.scalar(select(Produto).where(Produto.id == produto_id))
    if not produto:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado")
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)
    session.add(produto)
    session.commit()
    return produto