from app.database import SessionLocal, engine, Base 
from app.models import User, Machine, Maintenance, Supply, Movement, MovementType
from app.auth import hash_password 
from datetime import datetime, timedelta

def init_db():
    print("Limpar e criar tabelas...")
    Base.metadata.drop_all(bind=engine) # Opcional: limpa tudo antes de popular
    Base.metadata.create_all(bind=engine)

def seed_all():
    db = SessionLocal()
    try:
        print("Iniciando população do banco de dados...")

        # 1. USUÁRIOS
        users_data = [
            {"email": "admin@gmail.com", "password": "admin123", "name": "Admin Terra"},
            {"email": "joao@gmail.com", "password": "joao123", "name": "João do Trator"},
            {"email": "fazenda@gmail.com", "password": "123", "name": "Gerente Fazenda"},
        ]
        
        db_users = []
        for u in users_data:
            user = User(email=u["email"], hashed_password=hash_password(u["password"]), name=u["name"])
            db.add(user)
            db.flush() # Para gerar o ID
            db_users.append(user)

        # 2. MÁQUINAS (Distribuídas entre os usuários)
        # Definir admin para facilitar referência
        admin = db_users[0]
        machines_data = [
            # Máquinas do Usuário 0 (Admin)
            {"nome": "Trator MF 4290", "tipo": "Trator", "h_atual": 1500, "int": 250, "prox": 1550, "owner": admin}, # OK
            {"nome": "Colheitadeira S700", "tipo": "Colheitadeira", "h_atual": 2480, "int": 500, "prox": 2500, "owner": admin}, # Próximo (Faltam 20h)
            {"nome": "Trator Case IH Magnum 340", "tipo": "Trator", "h_atual": 1200, "int": 250, "prox": 1250, "owner": admin}, # Próximo
            {"nome": "Colheitadeira NH CR 9.90", "tipo": "Colheitadeira", "h_atual": 850, "int": 500, "prox": 1350, "owner": admin}, # OK
            {"nome": "Pulverizador John Deere 4730", "tipo": "Pulverizador", "h_atual": 2100, "int": 300, "prox": 2100, "owner": admin}, # Atenção (Venceu)
            {"nome": "Trator Massey Ferguson 7722", "tipo": "Trator", "h_atual": 450, "int": 250, "prox": 500, "owner": admin}, # Próximo
            {"nome": "Semeadora Momentum Stara", "tipo": "Plantadeira", "h_atual": 320, "int": 150, "prox": 450, "owner": admin}, # OK
            {"nome": "Escavadeira CAT 320", "tipo": "Escavadeira", "h_atual": 5600, "int": 1000, "prox": 6000, "owner": admin}, # OK
            {"nome": "Caminhão VW Constellation", "tipo": "Caminhão", "h_atual": 15200, "int": 5000, "prox": 15000, "owner": admin}, # Atenção (Venceu)
            {"nome": "Trator Valtra T250", "tipo": "Trator", "h_atual": 890, "int": 250, "prox": 1000, "owner": admin}, # OK
            
            # Máquinas do Usuário 1 (João)
            {"nome": "Trator JD 6125J", "tipo": "Trator", "h_atual": 1100, "int": 250, "prox": 1100, "owner": db_users[1]}, # Atenção (Venceu)
            {"nome": "Pulverizador Patriot", "tipo": "Pulverizador", "h_atual": 600, "int": 300, "prox": 900, "owner": db_users[1]}, # OK
            
            # Máquinas do Usuário 2 (Gerente)
            {"nome": "Plantadeira Stara", "tipo": "Plantadeira", "h_atual": 450, "int": 100, "prox": 455, "owner": db_users[2]}, # Próximo
            {"nome": "Caminhão Transp.", "tipo": "Caminhão", "h_atual": 12000, "int": 5000, "prox": 17000, "owner": db_users[2]},
        ]

        db_machines = []
        for m in machines_data:
            machine = Machine(
                nome=m["nome"], tipo=m["tipo"], horimetro_atual=m["h_atual"],
                intervalo_manutencao=m["int"], proxima_manutencao=m["prox"],
                user_id=m["owner"].id
            )
            db.add(machine)
            db.flush()
            db_machines.append(machine)

        # 3. MANUTENÇÕES (Histórico)
        maintenances_history = [
            {"m_id": db_machines[0].id, "desc": "Troca de Óleo e Filtros", "h": 1250, "custo": 850.0},
            {"m_id": db_machines[1].id, "desc": "Revisão Barra de Corte", "h": 2000, "custo": 4500.0},
            {"m_id": db_machines[2].id, "desc": "Reparo Hidráulico", "h": 850, "custo": 1200.0},
        
            # Histórico da Máquina 0 (Trator Case)
            {"m_id": db_machines[0].id, "desc": "Troca de Óleo 500h", "h": 500, "custo": 1200.0, "dias": 180},
            {"m_id": db_machines[0].id, "desc": "Revisão Geral 750h", "h": 750, "custo": 2500.0, "dias": 120},
            {"m_id": db_machines[0].id, "desc": "Troca de Filtros 1000h", "h": 1000, "custo": 800.0, "dias": 45},
            
            # Histórico da Máquina 1 (Colheitadeira NH)
            {"m_id": db_machines[1].id, "desc": "Preparação Safra", "h": 400, "custo": 5200.0, "dias": 210},
            {"m_id": db_machines[1].id, "desc": "Troca de navalhas", "h": 600, "custo": 1500.0, "dias": 90},
            {"m_id": db_machines[1].id, "desc": "Lubrificação completa", "h": 800, "custo": 300.0, "dias": 15},
            
            # Histórico da Máquina 2 (Pulverizador JD)
            {"m_id": db_machines[2].id, "desc": "Limpeza de bicos", "h": 1500, "custo": 450.0, "dias": 300},
            {"m_id": db_machines[2].id, "desc": "Revisão bomba de pressão", "h": 1800, "custo": 3100.0, "dias": 150},
            {"m_id": db_machines[2].id, "desc": "Troca de mangueiras", "h": 2000, "custo": 1200.0, "dias": 60},
            
            # Histórico da Máquina 6 (Caminhão VW)
            {"m_id": db_machines[6].id, "desc": "Troca de Pneus Dianteiros", "h": 10000, "custo": 4800.0, "dias": 200},
            {"m_id": db_machines[6].id, "desc": "Manutenção de Freios", "h": 14000, "custo": 2200.0, "dias": 30},
        ]

        for mh in maintenances_history:
            dias = mh.get("dias", 0)
            maint = Maintenance(
                machine_id=mh["m_id"],
                descricao=mh["desc"],
                horimetro_no_momento=mh["h"],
                custo=mh["custo"],
                # Gera uma data retroativa baseada no campo 'dias', se existir
                data=datetime.now() - timedelta(days=dias),
                observacao="Manutenção preventiva realizada conforme manual."
            )
            db.add(maint)

        # 4. INSUMOS (ESTOQUE)
        supplies_data = [
            {"nome": "Óleo Diesel S10", "und": "L", "atual": 5000, "min": 1000, "user": db_users[0]},
            {"nome": "Óleo Lubrificante 15W40", "und": "L", "atual": 20, "min": 50, "user": db_users[0]}, # Estoque Baixo
            {"nome": "Filtro de Ar Primário", "und": "Unid", "atual": 5, "min": 2, "user": db_users[1]},
            {"nome": "Adubo NPK 04-14-08", "und": "Saco 50kg", "atual": 100, "min": 20, "user": db_users[2]},
            {"nome": "Semente Milho Híbrido", "und": "Saco", "atual": 15, "min": 50, "user": db_users[2]}, # Estoque Baixo
            {"nome": "Diesel S10", "und": "L", "atual": 10000, "min": 2000, "user": admin},
            {"nome": "Óleo 15W40", "und": "L", "atual": 40, "min": 100, "user": admin}, # Estoque Baixo
            {"nome": "Graxa Azul Lithium", "und": "kg", "atual": 15, "min": 10, "user": admin},
            {"nome": "Filtro de Óleo PSL562", "und": "Unid", "atual": 12, "min": 5, "user": admin},
            {"nome": "Aditivo Radiador", "und": "L", "atual": 5, "min": 20, "user": admin}, # Estoque Baixo
            {"nome": "Pneu Traseiro 18.4-34", "und": "Unid", "atual": 2, "min": 2, "user": admin},
            {"nome": "Bico de Pulverização", "und": "Unid", "atual": 50, "min": 20, "user": admin},
            {"nome": "Herbicida Glifosato", "und": "L", "atual": 200, "min": 50, "user": admin},
            {"nome": "Fertilizante NPK", "und": "Saco", "atual": 500, "min": 100, "user": admin},
            {"nome": "Parafuso Sextavado M12", "und": "Unid", "atual": 100, "min": 20, "user": admin},
        ]

        db_supplies = []
        for s in supplies_data:
            supply = Supply(
                nome=s["nome"], unidade=s["und"], 
                quantidade_atual=s["atual"], quantidade_minima=s["min"],
                user_id=s["user"].id
            )
            db.add(supply)
            db.flush()
            db_supplies.append(supply)

        # 5. MOVIMENTAÇÕES DE ESTOQUE
        # 5. MOVIMENTAÇÕES DE ESTOQUE AMPLIADAS (Foco no Admin)
        movements_history = [
            # Fluxo de Diesel (Muitas entradas e saídas)
            {"s_id": db_supplies[0].id, "tipo": MovementType.entrada, "qtd": 5000, "obs": "Compra Mensal - Posto Central", "dias": 20},
            {"s_id": db_supplies[0].id, "tipo": MovementType.saida, "qtd": 450, "obs": "Abastecimento Trator Case", "dias": 15},
            {"s_id": db_supplies[0].id, "tipo": MovementType.saida, "qtd": 600, "obs": "Abastecimento Colheitadeira", "dias": 10},
            {"s_id": db_supplies[0].id, "tipo": MovementType.saida, "qtd": 300, "obs": "Abastecimento Pulverizador", "dias": 2},
            
            # Fluxo de Óleo Lubrificante (Simulando consumo em manutenção)
            {"s_id": db_supplies[1].id, "tipo": MovementType.entrada, "qtd": 100, "obs": "Compra Tambor 100L", "dias": 30},
            {"s_id": db_supplies[1].id, "tipo": MovementType.saida, "qtd": 25, "obs": "Troca de óleo Trator Case", "dias": 12},
            {"s_id": db_supplies[1].id, "tipo": MovementType.saida, "qtd": 35, "obs": "Troca de óleo Colheitadeira", "dias": 5},
            
            # Fluxo de Fertilizantes e Herbicidas
            {"s_id": db_supplies[8].id, "tipo": MovementType.entrada, "qtd": 1000, "obs": "Carga Cooperativa", "dias": 25},
            {"s_id": db_supplies[8].id, "tipo": MovementType.saida, "qtd": 500, "obs": "Plantio Talhão Norte", "dias": 5},
            {"s_id": db_supplies[7].id, "tipo": MovementType.entrada, "qtd": 500, "obs": "Compra Glifosato", "dias": 15},
            {"s_id": db_supplies[7].id, "tipo": MovementType.saida, "qtd": 300, "obs": "Aplicação Pré-emergente", "dias": 3},
            
            # Reposição de Peças
            {"s_id": db_supplies[3].id, "tipo": MovementType.entrada, "qtd": 10, "obs": "Compra Lote Filtros", "dias": 40},
            {"s_id": db_supplies[3].id, "tipo": MovementType.saida, "qtd": 2, "obs": "Revisão Trator Case", "dias": 10},
        ]

        for mv in movements_history:
            dias = mv.get("dias", 0)
            mov = Movement(
                supply_id=mv["s_id"],
                tipo=mv["tipo"],
                quantidade=mv["qtd"],
                observacao=mv["obs"],
                data=datetime.now() - timedelta(days=dias)
            )
            db.add(mov)

        db.commit()
        print("Banco de dados populado com sucesso! 🚀")

    except Exception as e:
        print(f"Erro ao popular banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_all()