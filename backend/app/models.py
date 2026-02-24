from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


# ── Usuário ──────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    machines = relationship("Machine", back_populates="owner", cascade="all, delete-orphan")
    supplies = relationship("Supply", back_populates="owner", cascade="all, delete-orphan")


# ── Máquinas ─────────────────────────────────────────────
class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # trator, colheitadeira, etc.
    horimetro_atual = Column(Float, default=0)
    intervalo_manutencao = Column(Float, nullable=False)  # ex: 250h
    proxima_manutencao = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="machines")
    maintenances = relationship("Maintenance", back_populates="machine", cascade="all, delete-orphan")

    @property
    def status(self) -> str:
        if self.horimetro_atual >= self.proxima_manutencao:
            return "Atenção"
        diff = self.proxima_manutencao - self.horimetro_atual
        if diff <= self.intervalo_manutencao * 0.1:
            return "Próximo"
        return "OK"


class Maintenance(Base):
    __tablename__ = "maintenances"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    descricao = Column(String, nullable=False)
    horimetro_no_momento = Column(Float, nullable=False)
    data = Column(DateTime(timezone=True), server_default=func.now())
    custo = Column(Float, default=0)
    observacao = Column(String, default="")

    machine = relationship("Machine", back_populates="maintenances")


# ── Estoque ──────────────────────────────────────────────
class Supply(Base):
    __tablename__ = "supplies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nome = Column(String, nullable=False)
    unidade = Column(String, nullable=False)  # kg, L, saco
    quantidade_atual = Column(Float, default=0)
    quantidade_minima = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="supplies")
    movements = relationship("Movement", back_populates="supply", cascade="all, delete-orphan")

    @property
    def status(self) -> str:
        if self.quantidade_atual <= self.quantidade_minima:
            return "Estoque Baixo"
        return "OK"


class MovementType(str, enum.Enum):
    entrada = "entrada"
    saida = "saida"


class Movement(Base):
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    supply_id = Column(Integer, ForeignKey("supplies.id"), nullable=False)
    tipo = Column(SAEnum(MovementType), nullable=False)
    quantidade = Column(Float, nullable=False)
    data = Column(DateTime(timezone=True), server_default=func.now())
    observacao = Column(String, default="")

    supply = relationship("Supply", back_populates="movements")
