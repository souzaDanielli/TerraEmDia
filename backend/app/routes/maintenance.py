from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Maintenance, Machine, User
from app.schemas import MaintenanceCreate, MaintenanceOut
from app.auth import get_current_user

router = APIRouter(tags=["Manutenção"])


@router.post("", response_model=MaintenanceOut, status_code=status.HTTP_201_CREATED)
def create_maintenance(
    data: MaintenanceCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    machine = db.query(Machine).filter(Machine.id == data.machine_id, Machine.user_id == user.id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina não encontrada")

    maintenance = Maintenance(
        machine_id=data.machine_id,
        descricao=data.descricao,
        horimetro_no_momento=data.horimetro_no_momento,
        custo=data.custo,
        observacao=data.observacao,
    )
    db.add(maintenance)

    # Atualizar horímetro da máquina e recalcular próxima manutenção
    machine.horimetro_atual = data.horimetro_no_momento
    machine.proxima_manutencao = data.horimetro_no_momento + machine.intervalo_manutencao

    db.commit()
    db.refresh(maintenance)
    return maintenance


@router.get("/{machine_id}", response_model=List[MaintenanceOut])
def list_maintenance(
    machine_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    machine = db.query(Machine).filter(Machine.id == machine_id, Machine.user_id == user.id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina não encontrada")

    return (
        db.query(Maintenance)
        .filter(Maintenance.machine_id == machine_id)
        .order_by(Maintenance.data.desc())
        .all()
    )
