from datetime import datetime, timedelta
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
    data_inicial: str = Query(None, description="Data inicial YYYYMMDD"),
    data_final: str = Query(None, description="Data final YYYYMMDD"),
    pagina: int = Query(1, description="Numero da pagina")
):
    hoje = datetime.now()
    
    # Se nao informadas, define a janela padrao exigida pelo PNCP (ultimos 5 dias)
    if not data_inicial:
        data_inicial = (hoje - timedelta(days=5)).strftime("%Y%m%d")
    if not data_final:
        data_final = hoje.strftime("%Y%m%d")

    # URL 100% compativel com o Manual da API do PNCP (Modalidade 6 = Pregao Eletronico)
    url = (
        f"https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
        f"?dataInicial={data_inicial}"
        f"&dataFinal={data_final}"
        f"&codigoModalidadeContratacao=6"
        f"&pagina={pagina}"
        f"&tamanhoPagina=50"
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Cache-Control": "no-cache"
    }

    try:
        time.sleep(0.8) # Pausa de seguranca contra Rate Limit
        resp = requests.get(url, headers=headers, timeout=20)
        
        if resp.status_code == 429:
            return {"error": True, "message": "Rate Limit PNCP (429): Muitas requisicoes."}
            
        if "application/json" not in resp.headers.get("Content-Type", ""):
            return {"error": True, "message": f"Resposta nao-JSON do PNCP (Status {resp.status_code})"}

        resp.raise_for_status()
        return resp.json()

    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
