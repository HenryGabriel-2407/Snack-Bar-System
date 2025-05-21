from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from snack_bar_system.database import get_session
from snack_bar_system.models import Cliente
from snack_bar_system.schemas import GetCliente, ListCliente, PostCliente, UpdateCliente
from snack_bar_system.security import get_password_to_hash

router = APIRouter(prefix='/cliente', tags=['cliente'])


# ------ CLIENTE -------
@router.post('/', response_model=GetCliente)
def post_cliente(cliente: PostCliente, session: Session = Depends(get_session)):
    banco = session.scalar(select(Cliente).where(Cliente.email == cliente.email))
    if banco:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Email já existe')
    cliente_novo = Cliente(
        nome=cliente.nome,
        email=cliente.email,
        endereco_num_residencia=cliente.endereco_num_residencia,
        endereco_rua=cliente.endereco_rua,
        endereco_bairro=cliente.endereco_bairro,
        endereco_cidade=cliente.endereco_cidade,
        endereco_complemento=cliente.endereco_complemento,
        senha_hash=get_password_to_hash(cliente.password),
    )
    cliente_novo.telefone = cliente.telefone
    cliente_novo.documento = cliente.documento

    session.add(cliente_novo)
    session.commit()
    session.refresh(cliente_novo)
    return cliente_novo


@router.get('/', response_model=ListCliente)
def get_list_cliente(session: Session = Depends(get_session)):
    clientes = session.scalars(select(Cliente)).all()
    return {'clientes': clientes}

@router.get('/{cliente_id}', response_model=GetCliente)
def get_cliente(cliente_id: int, session: Session=Depends(get_session)):
    cliente = session.scalar(select(Cliente).where(Cliente.id == cliente_id))
    if not cliente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cliente não existe / encontrado")
    return cliente

@router.delete('/{cliente_id}')
def delete_cliente(cliente_id: int, session: Session=Depends(get_session)):
    cliente = session.scalar(select(Cliente).where(Cliente.id == cliente_id))
    if not cliente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cliente não existe / encontrado")
    session.delete(cliente)
    session.commit()
    return "Cliente excluído com sucesso!"

@router.put('/{cliente_id}', response_model=GetCliente)
def update_cliente(cliente_id: int, dados: UpdateCliente, session: Session=Depends(get_session)):
    cliente = session.scalar(select(Cliente).where(Cliente.id == cliente_id))
    if not cliente:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cliente não existe / encontrado")
    cliente.nome = dados.nome
    cliente.email = dados.email
    cliente.telefone = dados.telefone
    cliente.endereco_num_residencia = dados.endereco_num_residencia
    cliente.endereco_rua = dados.endereco_rua
    cliente.endereco_bairro = dados.endereco_bairro
    cliente.endereco_cidade = dados.endereco_cidade
    cliente.endereco_complemento = dados.endereco_complemento
    cliente.documento = dados.documento
    cliente.password = get_password_to_hash(dados.password)
    session.add(cliente)
    session.commit()
    return cliente