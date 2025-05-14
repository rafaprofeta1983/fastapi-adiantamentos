from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import os
from dotenv import load_dotenv

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# Banco de dados
def get_connection():
    try:
        conn_str = f"""
            DRIVER={{{os.getenv("DB_DRIVER")}}};
            SERVER={os.getenv("DB_SERVER")};
            DATABASE={os.getenv("DB_NAME")};
            UID={os.getenv("DB_USER")};
            PWD={os.getenv("DB_PASSWORD")}};
            TrustServerCertificate=yes;
        """
        return pyodbc.connect(conn_str, autocommit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco: {str(e)}")

# Rota
@app.get("/adiantamentos")
def listar_adiantamentos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 10 * FROM sua_tabela")
        colunas = [col[0] for col in cursor.description]
        return [dict(zip(colunas, row)) for row in cursor.fetchall()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
