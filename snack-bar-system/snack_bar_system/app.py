from fastapi import FastAPI, Depends, HTTPException
from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy import select
from snack_bar_system.schemas import PostCombo, PostProduto, GetProduto, GetCombo, ProdutoListResponse, GetCliente, PostCliente, ListCliente, CreateProdutoItem, CreateComanda, ComandaOut
from snack_bar_system.database import get_session
from snack_bar_system.models import Produto, Combo, Combo_Produto, Cliente, Comanda, Pedido_Item
from typing import List
from snack_bar_system.security import get_password_to_hash

app = FastAPI()

# ----- PRODUTO -----
@app.post("/produto", response_model=GetProduto)
def post_produto(produto: PostProduto, session: Session=Depends(get_session)):
    novo_produto = Produto(**produto.dict())
    try:
        session.add(novo_produto)
        session.commit()
        session.refresh(novo_produto)
        return novo_produto
    except:
        return "Deu ruim kkkkkkkkkkkk"

@app.get("/produto", response_model=ProdutoListResponse)
def get_produto(session: Session=Depends(get_session)):
    produtos = session.scalars(select(Produto)).all()
    return {'produtos': produtos}


# ------ COMBO ------
@app.post("/combos", response_model=GetCombo)
def criar_combo(combo: PostCombo, session: Session = Depends(get_session)):
    produtos = session.query(Produto).filter(Produto.id.in_(combo.produtos)).all()
    if not produtos or len(produtos) != len(combo.produtos):
        raise HTTPException(status_code=400, detail="Um ou mais produtos não encontrados")
    novo_combo = Combo(
        nome=combo.nome,
        imagem_link=combo.imagem_link,
        preco=combo.preco,
        produtos=produtos
    )
    session.add(novo_combo)
    session.commit()
    session.refresh(novo_combo)
    return novo_combo

@app.get("/combos", response_model=List[GetCombo])
def get_combo(session: Session = Depends(get_session)):
    return session.scalars(select(Combo)).all()


# ------ CLIENTE -------
@app.post("/cliente", response_model=GetCliente)
def post_cliente(cliente: PostCliente, session: Session = Depends(get_session)):
    banco = session.scalar(select(Cliente).where(Cliente.email == cliente.email))
    if banco:
        raise HTTPException(status_code= HTTPStatus.BAD_REQUEST, detail="Email já existe")
    cliente_novo = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        endereco_num_residencia=cliente.endereco_num_residencia,
        endereco_rua=cliente.endereco_rua,
        endereco_bairro=cliente.endereco_bairro,
        endereco_cidade=cliente.endereco_cidade,
        endereco_complemento=cliente.endereco_complemento,
        senha_hash=get_password_to_hash(cliente.password)
    )
    cliente_novo.telefone = cliente.telefone
    cliente_novo.documento = cliente.documento

    session.add(cliente_novo)
    session.commit()
    session.refresh(cliente_novo)
    return cliente_novo

@app.get("/cliente", response_model=ListCliente)
def get_list_cliente(session: Session=Depends(get_session)):
    clientes = session.scalars(select(Cliente)).all()
    return {'clientes': clientes}

# --- Pedido Item e Comanda ---
@app.post("/comandas", response_model=ComandaOut, status_code=HTTPStatus.CREATED)
def criar_comanda(comanda: CreateComanda, session: Session = Depends(get_session)):
    for item in comanda.itens:
        if not item.id_produto and not item.id_combo:
            raise HTTPException(
                status_code=422,
                detail="Cada item deve conter pelo menos id_produto ou id_combo"
            )

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
                raise HTTPException(status_code=404, detail=f"Produto ID {item.id_produto} não encontrado")
            total += produto.preco * item.quantidade

        elif item.id_combo:
            combo = session.get(Combo, item.id_combo)
            if not combo:
                raise HTTPException(status_code=404, detail=f"Combo ID {item.id_combo} não encontrado")
            total += combo.preco * item.quantidade

        session.add(pedido)

    # Atualiza o preço total
    nova_comanda.preco_total = total
    session.commit()
    session.refresh(nova_comanda)
    return nova_comanda

@app.get("/comandas", response_model=List[ComandaOut])
def listar_comandas(session: Session = Depends(get_session)):
    comandas = session.scalars(select(Comanda)).all()
    return comandas