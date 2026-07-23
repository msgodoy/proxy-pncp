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
    q: str = Query("", description="Termo de busca/filtro (ex: notebook, computador)"),
    pagina: int = Query(1, description="Numero da pagina")
):
    """
    Busca no endpoint oficial de PROPOSTAS ABERTAS do PNCP (/v1/contratacoes/proposta).
    Garante que 100% dos pregões retornados estejam ativos e com prazos vigentes para disputa.
    """
    url = (
        f"https://pncp.gov.br/api/consulta/v1/contratacoes/proposta"
        f"?codigoModalidadeContratacao=6"
        f"&pagina={pagina}"
        f"&tamanhoPagina=25"
    )
    
    if q and q.strip():
        url += f"&q={requests.utils.quote(q.strip())}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "pt-BR,pt;q=0.9",
        "Cache-Control": "no-cache"
    }
    
    try:
        time.sleep(1.0) # Pausa de seguranca para evitar Rate Limit
        response = requests.get(url, headers=headers, timeout=25)
        
        if response.status_code == 429:
            return {"error": True, "message": "PNCP Rate Limit (429): Muitas requisicoes simultaneas. Aguarde alguns instantes."}
            
        if "application/json" not in response.headers.get("Content-Type", ""):
            return {"error": True, "message": f"PNCP retornou resposta nao-JSON ou bloqueio (Status {response.status_code})"}

        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": True, "message": "Timeout no PNCP: A API do governo demorou mais de 25s para responder."}
    except requests.exceptions.RequestException as e:
        return {"error": True, "message": str(e)}
