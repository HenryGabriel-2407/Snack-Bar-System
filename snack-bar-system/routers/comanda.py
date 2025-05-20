from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from snack_bar_system.database import get_session
from snack_bar_system.models import Comanda, Combo, Pedido_Item, Produto
from snack_bar_system.schemas import (
    ComandaOut,
    CreateComanda,
)

router = APIRouter(prefix='/comandas', tags=['comanda'])


# --- Pedido Item e Comanda ---
@router.post('/', response_model=ComandaOut, status_code=HTTPStatus.CREATED)
def criar_comanda(comanda: CreateComanda, session: Session = Depends(get_session)):
    for item in comanda.itens:
        if not item.id_produto and not item.id_combo:
            raise HTTPException(status_code=422, detail='Cada item deve conter pelo menos id_produto ou id_combo')

    nova_comanda = Comanda(
        id_client=comanda.id_cliente,
        tipo_entrega=comanda.tipo_entrega,
        metodo_pagamento=comanda.metodo_pagamento,
        valor_a_pagar=comanda.valor_a_pagar,
        troco=comanda.troco,
        status_comanda=comanda.status_comanda.value,
        status_pagamento=comanda.status_pagamento.value,
        preco_total=0.0,  # será atualizado depois
        pedido_item=[],
    )
    session.add(nova_comanda)
    session.flush()  # necessário para nova_comanda.id ser gerado

    total = 0.0
    for item in comanda.itens:
        # Cria o item do pedido
        pedido = Pedido_Item(
            id_comanda=nova_comanda.id,
            id_produto=item.id_produto,
            id_combo=item.id_combo,
            quantidade=item.quantidade,
            observacao=item.observacao,
        )

        # Busca preço do produto ou combo
        if item.id_produto:
            produto = session.get(Produto, item.id_produto)
            if not produto:
                raise HTTPException(status_code=404, detail=f'Produto ID {item.id_produto} não encontrado')
            total += produto.preco * item.quantidade

        elif item.id_combo:
            combo = session.get(Combo, item.id_combo)
            if not combo:
                raise HTTPException(status_code=404, detail=f'Combo ID {item.id_combo} não encontrado')
            total += combo.preco * item.quantidade

        session.add(pedido)

    # Atualiza o preço total
    nova_comanda.preco_total = total
    session.commit()
    session.refresh(nova_comanda)
    return nova_comanda


@router.get('/', response_model=List[ComandaOut])
def listar_comandas(session: Session = Depends(get_session)):
    comandas = session.scalars(select(Comanda)).all()
    return comandas
