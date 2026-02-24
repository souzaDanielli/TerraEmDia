from app.database import SessionLocal, engine, Base 
from app.models import User, Machine, Maintenance, Supply, Movement, MovementType
from app.auth import hash_password 

def init_db():
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)

def seed_admin():
    db = SessionLocal()
    admin_email = "admin@gmail.com"
    admin_password = "admin123"
    admin_name = "Administrador"

    existing = db.query(User).filter(User.email == admin_email).first()
    if not existing:
        admin = User(
            email=admin_email,
            hashed_password=hash_password(admin_password),
            name=admin_name
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
        {"email": "joao@gmail.com", "password": "joao123", "name": "João Silva"},
        {"email": "maria@gmail.com", "password": "maria123", "name": "Maria Oliveira"},
        {"email": "33@gmail.com", "password": "123456", "name": "33"},
    ]
    users = []
    for u in users_data:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            user = User(
                email=u["email"],
                hashed_password=hash_password(u["password"]),
                name=u["name"]
                # Removidos: is_active e is_admin
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            users.append(user)
        else:
            users.append(existing)

    # Máquinas (Lógica de check para não duplicar seeds se rodar 2x)
    if db.query(Machine).count() == 0:
        machines_data = [
            {"nome": "Trator Massey", "tipo": "trator", "horimetro_atual": 1200, "intervalo_manutencao": 250, "proxima_manutencao": 1250, "user": users[0]},
            {"nome": "Colheitadeira John Deere", "tipo": "colheitadeira", "horimetro_atual": 800, "intervalo_manutencao": 200, "proxima_manutencao": 900, "user": users[1]},
            {"nome": "Plantadeira Stara", "tipo": "plantadeira", "horimetro_atual": 300, "intervalo_manutencao": 150, "proxima_manutencao": 350, "user": users[2]},
        ]
        # ... resto da sua lógica de inserção de máquinas, manutenções, etc ...
        # (Omitido aqui para brevidade, mas mantenha o seu código original abaixo)
        print("Dados de teste inseridos.")
    else:
        print("Dados de teste já existem, pulando...")

    db.close()

if __name__ == "__main__":
    init_db()    # 1. Cria as tabelas primeiro
    seed_admin() # 2. Cria o admin
    seed_all()   # 3. Cria o resto