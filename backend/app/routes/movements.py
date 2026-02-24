from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Movement, Supply, User, MovementType
from app.schemas import MovementCreate, MovementOut
from app.auth import get_current_user

router = APIRouter(tags=["Movimentação"])


@router.post("", response_model=MovementOut, status_code=status.HTTP_201_CREATED)
def create_movement(
    data: MovementCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    supply = db.query(Supply).filter(Supply.id == data.supply_id, Supply.user_id == user.id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Insumo não encontrado")

    if data.tipo not in ("entrada", "saida"):
        raise HTTPException(status_code=400, detail="Tipo deve ser 'entrada' ou 'saida'")

    movement = Movement(
        supply_id=data.supply_id,
        tipo=MovementType(data.tipo),
        quantidade=data.quantidade,
        observacao=data.observacao,
    )
    db.add(movement)

    # Atualizar quantidade do insumo
    if data.tipo == "entrada":
        supply.quantidade_atual += data.quantidade
    else:
        if supply.quantidade_atual < data.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente em estoque")
        supply.quantidade_atual -= data.quantidade

    db.commit()
    db.refresh(movement)
    return movement


@router.get("/{supply_id}", response_model=List[MovementOut])
def list_movements(
    supply_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    supply = db.query(Supply).filter(Supply.id == supply_id, Supply.user_id == user.id).first()
    if not supply:
        raise HTTPException(status_code=404, detail="Insumo não encontrado")

    return (
        db.query(Movement)
        .filter(Movement.supply_id == supply_id)
        .order_by(Movement.data.desc())
        .all()
    )
