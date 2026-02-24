from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# ── Auth ─────────────────────────────────────────────────
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Máquinas ─────────────────────────────────────────────
class MachineCreate(BaseModel):
    nome: str
    tipo: str
    horimetro_atual: float = 0
    intervalo_manutencao: float


class MachineUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    horimetro_atual: Optional[float] = None
    intervalo_manutencao: Optional[float] = None


class MachineOut(BaseModel):
    id: int
    nome: str
    tipo: str
    horimetro_atual: float
    intervalo_manutencao: float
    proxima_manutencao: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Manutenção ───────────────────────────────────────────
class MaintenanceCreate(BaseModel):
    machine_id: int
    descricao: str
    horimetro_no_momento: float
    custo: float = 0
    observacao: str = ""


class MaintenanceOut(BaseModel):
    id: int
    machine_id: int
    descricao: str
    horimetro_no_momento: float
    data: datetime
    custo: float
    observacao: str

    class Config:
        from_attributes = True


# ── Estoque ──────────────────────────────────────────────
class SupplyCreate(BaseModel):
    nome: str
    unidade: str
    quantidade_atual: float = 0
    quantidade_minima: float = 0


class SupplyUpdate(BaseModel):
    nome: Optional[str] = None
    unidade: Optional[str] = None
    quantidade_minima: Optional[float] = None


class SupplyOut(BaseModel):
    id: int
    nome: str
    unidade: str
    quantidade_atual: float
    quantidade_minima: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Movimentação ─────────────────────────────────────────
class MovementCreate(BaseModel):
    supply_id: int
    tipo: str  # "entrada" | "saida"
    quantidade: float
    observacao: str = ""


class MovementOut(BaseModel):
    id: int
    supply_id: int
    tipo: str
    quantidade: float
    data: datetime
    observacao: str

    class Config:
        from_attributes = True
