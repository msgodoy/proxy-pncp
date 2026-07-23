import os
from fastapi import FastAPI, Query
import requests

app = FastAPI(title="PNCP Proxy Ofertech")

@app.get("/")
def home():
    return {"status": "Proxy PNCP Ofertech esta online!"}

@app.get("/pncp/licitacoes")
def get_licitacoes(
    q: str = Query("", description="Termo de busca"),
    data_inicial: str = Query(..., description="Data inicial YYYYMMDD"),
    data_final: str = Query(..., description="Data final YYYYMMDD"),
    pagina: int = Query(1, description="Numero da pagina")
):
    # Endpoint otimizado de pesquisa do PNCP
    url = (
        f"https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
        f"?dataInicial={data_inicial}"
        f"&dataFinal={data_final}"
        f"&codigoModalidadeContratacao=6"
        f"&pagina={pagina}"
        f"&tamanhoPagina=50"
    )
    
    # Se houver termo, inclui na busca
    if q and q.strip():
        url += f"&q={q.strip()}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "pt-BR,pt;q=0.9"
    }
    
    try:
        # Timeout direto de 20s sem loops longos de re-tentativa
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
