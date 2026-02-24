from app.database import SessionLocal
from app.models import User, Machine, Maintenance, Supply, Movement, MovementType
from app.auth import get_password_hash

def seed_admin():
    db = SessionLocal()
    admin_email = "admin@terraemdia.com"
    admin_password = "admin123"
    admin_name = "Administrador"

    # Check if admin already exists
    existing = db.query(User).filter(User.email == admin_email).first()
    if not existing:
        admin = User(
            email=admin_email,
            hashed_password=get_password_hash(admin_password),
            name=admin_name,
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")
    db.close()

def seed_all():
    db = SessionLocal()

    # Usuários
    users_data = [
        {"email": "joao@terraemdia.com", "password": "joao123", "name": "João Silva"},
        {"email": "maria@terraemdia.com", "password": "maria123", "name": "Maria Oliveira"},
        {"email": "33@gmail.com", "password": "123456", "name": "Pedro Souza"},
    ]
    users = []
    for u in users_data:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            user = User(
                email=u["email"],
                hashed_password=get_password_hash(u["password"]),
                name=u["name"],
                is_active=True,
                is_admin=False
            )
            db.add(user)
            db.commit()
            users.append(user)
        else:
            users.append(existing)

    # Máquinas
    machines_data = [
        {"nome": "Trator Massey", "tipo": "trator", "horimetro_atual": 1200, "intervalo_manutencao": 250, "proxima_manutencao": 1250, "user": users[0]},
        {"nome": "Colheitadeira John Deere", "tipo": "colheitadeira", "horimetro_atual": 800, "intervalo_manutencao": 200, "proxima_manutencao": 900, "user": users[1]},
        {"nome": "Plantadeira Stara", "tipo": "plantadeira", "horimetro_atual": 300, "intervalo_manutencao": 150, "proxima_manutencao": 350, "user": users[2]},
    ]
    machines = []
    for m in machines_data:
        machine = Machine(
            nome=m["nome"],
            tipo=m["tipo"],
            horimetro_atual=m["horimetro_atual"],
            intervalo_manutencao=m["intervalo_manutencao"],
            proxima_manutencao=m["proxima_manutencao"],
            owner=m["user"]
        )
        db.add(machine)
        db.commit()
        machines.append(machine)

    # Manutenções
    maintenances_data = [
        {"machine": machines[0], "descricao": "Troca de óleo", "horimetro_no_momento": 1200, "custo": 350.0, "observacao": "Óleo sintético"},
        {"machine": machines[1], "descricao": "Revisão geral", "horimetro_no_momento": 800, "custo": 1200.0, "observacao": "Inclui filtros"},
        {"machine": machines[2], "descricao": "Troca de disco", "horimetro_no_momento": 300, "custo": 500.0, "observacao": "Disco novo"},
    ]
    for mt in maintenances_data:
        maintenance = Maintenance(
            machine=mt["machine"],
            descricao=mt["descricao"],
            horimetro_no_momento=mt["horimetro_no_momento"],
            custo=mt["custo"],
            observacao=mt["observacao"]
        )
        db.add(maintenance)
    db.commit()

    # Suprimentos
    supplies_data = [
        {"nome": "Diesel", "unidade": "L", "quantidade_atual": 500, "quantidade_minima": 100, "user": users[0]},
        {"nome": "Adubo NPK", "unidade": "kg", "quantidade_atual": 2000, "quantidade_minima": 500, "user": users[1]},
        {"nome": "Sementes de soja", "unidade": "saco", "quantidade_atual": 50, "quantidade_minima": 10, "user": users[2]},
    ]
    supplies = []
    for s in supplies_data:
        supply = Supply(
            nome=s["nome"],
            unidade=s["unidade"],
            quantidade_atual=s["quantidade_atual"],
            quantidade_minima=s["quantidade_minima"],
            owner=s["user"]
        )
        db.add(supply)
        db.commit()
        supplies.append(supply)

    # Movimentos de estoque
    movements_data = [
        {"supply": supplies[0], "tipo": MovementType.entrada, "quantidade": 200, "observacao": "Compra de diesel"},
        {"supply": supplies[0], "tipo": MovementType.saida, "quantidade": 50, "observacao": "Uso em trator"},
        {"supply": supplies[1], "tipo": MovementType.entrada, "quantidade": 1000, "observacao": "Compra de adubo"},
        {"supply": supplies[1], "tipo": MovementType.saida, "quantidade": 300, "observacao": "Aplicação na lavoura"},
        {"supply": supplies[2], "tipo": MovementType.entrada, "quantidade": 20, "observacao": "Compra de sementes"},
        {"supply": supplies[2], "tipo": MovementType.saida, "quantidade": 5, "observacao": "Plantio"},
    ]
    for mv in movements_data:
        movement = Movement(
            supply=mv["supply"],
            tipo=mv["tipo"],
            quantidade=mv["quantidade"],
            observacao=mv["observacao"]
        )
        db.add(movement)
    db.commit()

    print("Seed completo inserido.")
    db.close()

if __name__ == "__main__":
    seed_admin()
    seed_all()
