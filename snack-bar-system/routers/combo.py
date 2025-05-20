from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from snack_bar_system.database import get_session
from snack_bar_system.models import Combo, Produto
from snack_bar_system.schemas import (
    GetCombo,
    PostCombo,
)

router = APIRouter(prefix='/combos', tags=['combo'])


# ------ COMBO ------
@router.post('/combos', response_model=GetCombo)
def criar_combo(combo: PostCombo, session: Session = Depends(get_session)):
    produtos = session.query(Produto).filter(Produto.id.in_(combo.produtos)).all()
    if not produtos or len(produtos) != len(combo.produtos):
        raise HTTPException(status_code=400, detail='Um ou mais produtos não encontrados')
    novo_combo = Combo(nome=combo.nome, imagem_link=combo.imagem_link, preco=combo.preco, produtos=produtos)
    session.add(novo_combo)
    session.commit()
    session.refresh(novo_combo)
    return novo_combo


@router.get('/combos', response_model=List[GetCombo])
def get_combo(session: Session = Depends(get_session)):
    return session.scalars(select(Combo)).all()
