from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Supply, User
from app.schemas import SupplyCreate, SupplyUpdate, SupplyOut
from app.auth import get_current_user

router = APIRouter(tags=["Estoque"])


@router.get("", response_model=List[SupplyOut])
def list_supplies(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Supply).filter(Supply.user_id == user.id).all()


@router.post("", response_model=SupplyOut, status_code=status.HTTP_201_CREATED)
def create_supply(data: SupplyCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    supply = Supply(
        user_id=user.id,
        nome=data.nome,
        unidade=data.unidade,
        quantidade_atual=data.quantidade_atual,
        quantidade_minima=data.quantidade_minima,
    )
    db.add(supply)
    db.commit()
    db.refresh(supply)
    return supply


@router.put("/{supply_id}", response_model=SupplyOut)
def update_supply(
    supply_id: int,
    data: SupplyUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    supply = db.query(Supply).filter(Supply.id == supply_id, Supply.user_id == user.id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Insumo não encontrado")

    if data.nome is not None:
        supply.nome = data.nome
    if data.unidade is not None:
        supply.unidade = data.unidade
    if data.quantidade_minima is not None:
        supply.quantidade_minima = data.quantidade_minima

    db.commit()
    db.refresh(supply)
    return supply
