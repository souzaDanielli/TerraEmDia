from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Machine, User
from app.schemas import MachineCreate, MachineUpdate, MachineOut
from app.auth import get_current_user

router = APIRouter(tags=["Máquinas"])


@router.get("", response_model=List[MachineOut])
def list_machines(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Machine).filter(Machine.user_id == user.id).all()


@router.post("", response_model=MachineOut, status_code=status.HTTP_201_CREATED)
def create_machine(data: MachineCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    machine = Machine(
        user_id=user.id,
        nome=data.nome,
        tipo=data.tipo,
        horimetro_atual=data.horimetro_atual,
        intervalo_manutencao=data.intervalo_manutencao,
        proxima_manutencao=data.horimetro_atual + data.intervalo_manutencao,
    )
    db.add(machine)
    db.commit()
    db.refresh(machine)
    return machine


@router.put("/{machine_id}", response_model=MachineOut)
def update_machine(
    machine_id: int,
    data: MachineUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    machine = db.query(Machine).filter(Machine.id == machine_id, Machine.user_id == user.id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina não encontrada")

    if data.nome is not None:
        machine.nome = data.nome
    if data.tipo is not None:
        machine.tipo = data.tipo
    if data.intervalo_manutencao is not None:
        machine.intervalo_manutencao = data.intervalo_manutencao
    if data.horimetro_atual is not None:
        machine.horimetro_atual = data.horimetro_atual
        # Recalcular próxima manutenção quando horímetro é atualizado
        machine.proxima_manutencao = machine.horimetro_atual + machine.intervalo_manutencao

    db.commit()
    db.refresh(machine)
    return machine


@router.delete("/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    machine = db.query(Machine).filter(Machine.id == machine_id, Machine.user_id == user.id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina não encontrada")
    db.delete(machine)
    db.commit()
