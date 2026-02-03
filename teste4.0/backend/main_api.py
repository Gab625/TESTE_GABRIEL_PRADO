from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import get_db

app = FastAPI(title="API ANS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/operadoras")
def get_operadoras(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit

    total_registros = db.execute(text("SELECT count(*) FROM operadoras")).scalar()
    
    sql = text("""
        SELECT cnpj, razao_social, cidade, uf 
        FROM operadoras
        ORDER BY razao_social
        LIMIT :limit OFFSET :offset
    """)
    result = db.execute(sql, {"limit": limit, "offset": offset})
    dados = [dict(row._mapping) for row in result]
    
    return {
        "metadata": {
            "total": total_registros,
            "page": page,
            "limit": limit,
            "total_pages": (total_registros + limit - 1) // limit
        },
        "data": dados
    }

@app.get("/api/operadoras/{cnpj}")
def get_operadora(cnpj: str, db: Session = Depends(get_db)):
    sql = text("SELECT * FROM operadoras " \
    "WHERE cnpj = :cnpj")
    result = db.execute(sql, {"cnpj": cnpj}).fetchone()
    
    if result:
        return dict(result._mapping)
    return {"error": "Operadora not found"}

@app.get("/api/operadoras/{cnpj}/despesas")
def get_despesas_operadora(cnpj: str, db: Session = Depends(get_db)):
    sql = text("""
        SELECT cnpj, valordespesas 
        FROM despesas 
        WHERE cnpj = :cnpj
    """)
    result = db.execute(sql, {"cnpj": cnpj})
    
    return [dict(row._mapping) for row in result]

@app.get("/api/estatisticas")
def get_estatisticas(db: Session = Depends(get_db)):
    sql = text("""SELECT cnpj, razao_social,total_despesas, media_trimestral FROM despesas_agregadas ORDER BY media_trimestral DESC LIMIT 5""")
    result = db.execute(sql)

    return [dict(row._mapping) for row in result]