from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class MetodoPagamento(str, Enum):
    dinheiro = 'dinheiro'
    pix = 'pix'
    cartao_debito = 'cartão débito'
    cartao_credito = 'cartão crédito'


class TipoProduto(str, Enum):
    bebida = 'bebida'
    lanche = 'lanche'
    entrada = 'entrada'
    sobremesa = 'sobremesa'


class TipoEntrega(str, Enum):
    local = 'local'
    levar = 'levar'
    delivery = 'delivery'
    drive_thru = 'drive-thru'


class StatusComanda(str, Enum):
    em_processamento = 'em processamento'
    pronta = 'pronta'
    entrgue = 'entregue'
    cancelada = 'cancelada'


class StatusPagamento(str, Enum):
    pendente = 'pendente'
    pago = 'pago'
    recusado = 'recusado'
    estornado = 'estornado'


class PostCliente(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None
    endereco_num_residencia: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_complemento: str
    documento: str
    password: str


class GetCliente(BaseModel):
    id: int
    nome: str
    email: EmailStr
    telefone: str | None
    endereco_num_residencia: str
    endereco_rua: str
    endereco_bairro: str
    endereco_cidade: str
    endereco_complemento: str
    documento: str


class ListCliente(BaseModel):
    clientes: List[GetCliente]


class PostProduto(BaseModel):
    nome: str
    descricao: str
    imagem_link: str
    preco: float
    tipo: TipoProduto


class GetProduto(BaseModel):
    id: int
    nome: str
    descricao: str
    imagem_link: str
    preco: float
    tipo: TipoProduto


class PostCombo(BaseModel):
    nome: str
    imagem_link: str
    preco: float
    produtos: List[int]


class GetCombo(BaseModel):
    id: int
    nome: str
    imagem_link: str
    preco: float
    produtos: List[GetProduto]

    class Config:
        from_attributes = True


class ProdutoListResponse(BaseModel):
    produtos: List[GetProduto]


class CreateProdutoItem(BaseModel):
    id_produto: Optional[int] = None
    id_combo: Optional[int] = None
    quantidade: int
    observacao: Optional[str] = ''

    @field_validator('quantidade')
    @classmethod
    def validar_qtd(cls, v):
        if v < 1:
            raise ValueError('Quantidade deve ser maior que 0')
        return v


class CreateComanda(BaseModel):
    id_cliente: Optional[int] = None
    tipo_entrega: TipoEntrega
    metodo_pagamento: MetodoPagamento
    valor_a_pagar: float
    troco: Optional[float] = 0.0
    status_comanda: Optional[StatusComanda] = StatusComanda.em_processamento
    status_pagamento: StatusPagamento = StatusPagamento.pendente
    itens: List[CreateProdutoItem]


class ComandaOut(BaseModel):
    id: int
    preco_total: float
    id_cliente: Optional[int] = Field(alias='id_client')
    tipo_entrega: str
    metodo_pagamento: str
    valor_a_pagar: float
    troco: float
    status_comanda: StatusComanda
    status_pagamento: StatusPagamento
    data_registro: datetime

    class Config:
        from_attributes = True
