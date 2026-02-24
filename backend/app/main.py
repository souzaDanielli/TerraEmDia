from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import auth, machines, maintenance, supplies, movements

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Terra em Dia",
    description="Sistema de controle de manutenção de máquinas agrícolas e estoque de insumos",
    version="1.0.0",
)

# CORS — permite o frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas
app.include_router(auth.router)
app.include_router(machines.router)
app.include_router(maintenance.router)
app.include_router(supplies.router)
app.include_router(movements.router)


@app.get("/")
def root():
    return {"message": "Terra em Dia API 🌱"}
