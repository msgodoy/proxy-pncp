import os
import time
from fastapi import FastAPI, Query
import requests

app = FastAPI(title="PNCP Proxy Ofertech")

@app.get("/")
def home():
    return {"status": "Proxy PNCP Ofertech esta online!"}

@app.get("/pncp/licitacoes")
def get_licitacoes(
    data_inicial: str = Query(..., description="Data inicial YYYYMMDD"),
    data_final: str = Query(..., description="Data final YYYYMMDD"),
    pagina: int = Query(1, description="Numero da pagina")
):
    url = (
        f"https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
        f"?dataInicial={data_inicial}"
        f"&dataFinal={data_final}"
        f"&codigoModalidadeContratacao=6"
        f"&pagina={pagina}"
        f"&tamanhoPagina=15"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Cache-Control": "no-cache"
    }
    
    try:
        # Pausa de 1.5s no servidor para evitar tomar HTTP 429 do PNCP
        time.sleep(1.5)
        
        response = requests.get(url, headers=headers, timeout=12)
        
        if response.status_code == 429:
            return {"error": True, "message": "PNCP Rate Limit (429): Muitas requisicoes simultaneas. Aguarde alguns instantes."}
            
        if "application/json" not in response.headers.get("Content-Type", ""):
            return {"error": True, "message": f"PNCP retornou HTML ou bloqueio (Status {response.status_code})"}

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
