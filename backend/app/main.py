from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import auth, machines, maintenance, supplies, movements

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Terra em Dia",
    description="Sistema de controle de manutenção de máquinas agrícolas e estoque de insumos",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(machines.router, prefix="/api/machines", tags=["Machines"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["Maintenance"])
app.include_router(supplies.router, prefix="/api/supplies", tags=["Supplies"])
app.include_router(movements.router, prefix="/api/movements", tags=["Movements"])

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.get("/api/")
def api_healthcheck():
    return {"status": "ok"}
