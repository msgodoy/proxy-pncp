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
    q: str = Query("", description="Termo de busca/filtro"),
    pagina: int = Query(1, description="Numero da pagina")
):
    hoje = datetime.now()
    
    # Se nao informadas pelo cliente, define as datas obrigatorias exigidas pelo PNCP
    if not data_inicial:
        # Janela dos ultimos 10 dias
        data_inicial = (hoje - timedelta(days=10)).strftime("%Y%m%d")
    if not data_final:
        data_final = hoje.strftime("%Y%m%d")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Cache-Control": "no-cache"
    }

    # Tentativa 1: Endpoint de Propostas Abertas
    url_proposta = (
        f"https://pncp.gov.br/api/consulta/v1/contratacoes/proposta"
        f"?dataInicial={data_inicial}"
        f"&dataFinal={data_final}"
        f"&codigoModalidadeContratacao=6"
        f"&pagina={pagina}"
        f"&tamanhoPagina=25"
    )
    if q and q.strip():
        url_proposta += f"&q={requests.utils.quote(q.strip())}"

    try:
        time.sleep(1.0)
        resp = requests.get(url_proposta, headers=headers, timeout=20)
        
        # Se o endpoint /proposta aceitar e retornar 200, entrega o JSON
        if resp.status_code == 200 and "application/json" in resp.headers.get("Content-Type", ""):
            return resp.json()

        # Tentativa 2 (Fallback): Se /proposta retornar 400 ou falhar, consulta /publicacao
        url_pub = (
            f"https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
            f"?dataInicial={data_inicial}"
            f"&dataFinal={data_final}"
            f"&codigoModalidadeContratacao=6"
            f"&pagina={pagina}"
            f"&tamanhoPagina=25"
        )
        if q and q.strip():
            url_pub += f"&q={requests.utils.quote(q.strip())}"

        resp_pub = requests.get(url_pub, headers=headers, timeout=20)
        if resp_pub.status_code == 200 and "application/json" in resp_pub.headers.get("Content-Type", ""):
            return resp_pub.json()

        return {"error": True, "message": f"PNCP retornou Status {resp.status_code}"}

    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
