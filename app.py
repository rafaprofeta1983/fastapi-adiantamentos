from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Dados do .env
DB_SERVER = os.getenv("DB_SERVER")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DRIVER = os.getenv("DB_DRIVER")

def get_connection():
    try:
        conn_str = f"""
            DRIVER={{{os.getenv("DB_DRIVER")}}};
            SERVER={os.getenv("DB_SERVER")};
            DATABASE={os.getenv("DB_NAME")};
            UID={os.getenv("DB_USER")};
            PWD={os.getenv("DB_PASSWORD")};
            TrustServerCertificate=yes;
        """
        conn = pyodbc.connect(conn_str, autocommit=True)
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco: {str(e)}")

# Inicializa o FastAPI
app = FastAPI()

# Permite chamadas externas (como do OutSystems)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, troque "*" por domínio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/adiantamentos")
def listar_adiantamentos():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                ADTOITEM.Id,
                AdiantamentoTitulo_Id,
                Data,
                Valor,
                Historico,
                EMP.RazaoSocial AS Empresa,
                ADTOITEM.Numero,
                ADTOITEM.RazaoSocial,
                ADTOITEM.Codigo,
                SaldoADescontar
            FROM vw_90_TableItemAdiantamentoTitulo AS ADTOITEM
            LEFT JOIN vw_90_TableAdiantamentoTitulo AS ADTO
            ON ADTOITEM.AdiantamentoTitulo_Id = ADTO.Id
            LEFT JOIN empresa_financeiro AS EMP
            ON ADTOITEM.Empresa_Id = EMP.Id
            WHERE 
            Origem = 'Titulo'
            AND YEAR(ADTOITEM.Data) > 2021
            AND SaldoADescontar > 0.10

            
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        colunas = [column[0] for column in cursor.description]
        resultado = [dict(zip(colunas, row)) for row in rows]

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))