from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
import os
from dotenv import load_dotenv
import requests
from fastapi.responses import JSONResponse

# Inicializa FastAPI
app = FastAPI()

# Carrega variáveis do .env
load_dotenv()

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # troque por domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para obter conexão com banco de dados
def get_connection():
    try:
        driver = os.getenv("DB_DRIVER", "").strip()
        server = os.getenv("DB_SERVER")
        database = os.getenv("DB_NAME")
        username = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            "TrustServerCertificate=yes;"
        )
        return pyodbc.connect(conn_str, autocommit=True)
    except Exception as e:
        print(f"[ERRO] Conexão falhou: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco: {str(e)}")

# Endpoint de adiantamentos
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
        colunas = [col[0] for col in cursor.description]
        resultado = [dict(zip(colunas, row)) for row in rows]

        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "API rodando com sucesso"}

@app.get("/ip")
def get_external_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        ip_data = response.json()
        return {"ip_externo": ip_data.get("ip", "IP não encontrado")}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"ip_externo": f"Erro ao obter IP externo: {str(e)}"}
        )

@app.get("/test-db")
def testar_conexao():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 AS resultado")
        resultado = cursor.fetchone()
        return {"conexao": "sucesso", "resultado": resultado[0]}
    except Exception as e:
        return {"conexao": "falha", "erro": str(e)}
