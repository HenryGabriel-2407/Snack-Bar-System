from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Produto:
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(nullable=False)
    imagem_link: Mapped[str] = mapped_column(nullable=False)
    preco: Mapped[float] = mapped_column(nullable=False)
    tipo: Mapped[str]
    combos: Mapped[list["Combo"]] = relationship(
        secondary="combo_produto",
        back_populates="produtos",
        init=False
    )


@table_registry.mapped_as_dataclass
class Combo:
    __tablename__ = "combo"
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    imagem_link: Mapped[str] = mapped_column(nullable=False)
    preco: Mapped[float] = mapped_column(nullable=False)
    produtos: Mapped[list["Produto"]] = relationship(
        secondary="combo_produto",
        back_populates="combos"
    )

@table_registry.mapped_as_dataclass
class Combo_Produto:
    __tablename__ = "combo_produto"

    combo_id: Mapped[int] = mapped_column(ForeignKey("combo.id"), nullable=False, primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produto.id"), nullable=False, primary_key=True)

@table_registry.mapped_as_dataclass
class Pedido_Item:
    __tablename__ = "pedido_item"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    id_comanda: Mapped[int] = mapped_column(ForeignKey("comanda.id"), nullable=False)
    id_produto: Mapped[int] = mapped_column(ForeignKey("produto.id"), nullable=True)
    id_combo: Mapped[int] = mapped_column(ForeignKey("combo.id"), nullable=True)
    quantidade: Mapped[int] = mapped_column(nullable=False)
    observacao: Mapped[str] = mapped_column(nullable=True)


@table_registry.mapped_as_dataclass
class Comanda:
    __tablename__ = "comanda"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    preco_total: Mapped[float]
    id_client: Mapped[Optional[int]] = mapped_column(ForeignKey("cliente.id"), nullable=True)
    status_comanda: Mapped[str]
    data_registro: Mapped[datetime] = mapped_column(init=False, server_default=func.now())
    tipo_entrega: Mapped[str]
    metodo_pagamento: Mapped[str]
    valor_a_pagar: Mapped[float]
    status_pagamento: Mapped[str]
    pedido_item: Mapped[list["Pedido_Item"]] = relationship(backref="comanda")
    troco: Mapped[float] = mapped_column(default=0.0)


@table_registry.mapped_as_dataclass
class Cliente:
    __tablename__ = "cliente"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    telefone: Mapped[str] = mapped_column(init=False)
    endereco_num_residencia: Mapped[str] = mapped_column(nullable=False)
    endereco_rua: Mapped[str] = mapped_column(nullable=False)
    endereco_bairro: Mapped[str] = mapped_column(nullable=False)
    endereco_cidade: Mapped[str] = mapped_column(nullable=False)
    endereco_complemento: Mapped[str] = mapped_column(nullable=False)
    documento: Mapped[str]  = mapped_column(init=False) # CPF ou CNPJ
    senha_hash: Mapped[str] = mapped_column(nullable=False)