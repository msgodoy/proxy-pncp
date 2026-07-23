import os
from fastapi import FastAPI, Query
import requests

app = FastAPI(title="PNCP Proxy para Google Apps Script")

@app.get("/")
def home():
    return {"status": "Proxy PNCP esta online!"}

@app.get("/pncp/licitacoes")
def get_licitacoes(
    q: str = Query("notebook", description="Termo de busca"),
    data_inicial: str = Query(..., description="Data inicial YYYYMMDD"),
    data_final: str = Query(..., description="Data final YYYYMMDD"),
    pagina: int = Query(1, description="Numero da pagina")
):
    url = f"https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao?dataInicial={data_inicial}&dataFinal={data_final}&codigoModalidadeContratacao=6&q={q}&pagina={pagina}&tamanhoPagina=50"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
