# 🌱 Terra em Dia

Sistema simples para controle de manutenção de máquinas agrícolas e estoque de insumos.

## Tecnologias

- **Frontend:** React + Vite
- **Backend:** FastAPI (Python)
- **Banco:** PostgreSQL
- **Dev:** Docker Compose

## Como rodar (desenvolvimento)

### Pré-requisitos
- [Docker](https://www.docker.com/) e Docker Compose instalados

### Subir o projeto

```bash
docker compose up --build
```

Aguarde todos os containers iniciarem. O sistema estará disponível em:

| Serviço   | URL                        |
|-----------|----------------------------|
| Frontend  | http://localhost:5173       |
| Backend   | http://localhost:8000       |
| API Docs  | http://localhost:8000/docs  |
| Banco     | localhost:5432              |

### Parar o projeto

```bash
docker compose down
```

### Limpar tudo (inclusive banco)

```bash
docker compose down -v
```

## Funcionalidades

- ✅ Cadastro e login de usuário
- ✅ Cadastro de máquinas agrícolas
- ✅ Registro de manutenção com recálculo automático
- ✅ Alerta de máquinas que precisam de manutenção
- ✅ Cadastro de insumos
- ✅ Entrada e saída de estoque
- ✅ Alerta de estoque baixo
- ✅ Dashboard com visão geral dos alertas

## Estrutura

```
TerraEmDia/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py          # Entry point FastAPI
│       ├── config.py         # Settings
│       ├── database.py       # SQLAlchemy setup
│       ├── models.py         # Modelos do banco
│       ├── schemas.py        # Schemas Pydantic
│       ├── auth.py           # JWT + bcrypt
│       └── routes/
│           ├── auth.py       # POST /register, /login
│           ├── machines.py   # CRUD máquinas
│           ├── maintenance.py# Manutenção
│           ├── supplies.py   # CRUD insumos
│           └── movements.py  # Movimentações
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api.js
        ├── index.css
        ├── context/
        │   └── AuthContext.jsx
        └── pages/
            ├── LoginPage.jsx
            ├── RegisterPage.jsx
            ├── DashboardPage.jsx
            ├── MachinesPage.jsx
            └── SuppliesPage.jsx
```
