{\rtf1\ansi\ansicpg1252\cocoartf2870
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
from fastapi import FastAPI, Query\
import requests\
\
app = FastAPI(title="PNCP Proxy para Google Apps Script")\
\
@app.get("/")\
def home():\
    return \{"status": "Proxy PNCP est\'e1 online!"\}\
\
@app.get("/pncp/licitacoes")\
def get_licitacoes(\
    q: str = Query("notebook", description="Termo de busca"),\
    data_inicial: str = Query(..., description="Data inicial no formato YYYYMMDD"),\
    data_final: str = Query(..., description="Data final no formato YYYYMMDD"),\
    pagina: int = Query(1, description="N\'famero da p\'e1gina")\
):\
    """\
    Realiza a requisi\'e7\'e3o ao PNCP a partir de um IP de servidor de aplica\'e7\'e3o,\
    evitando os bloqueios de IP enfrentados pelo Google Apps Script.\
    """\
    url = (\
        f"https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"\
        f"?dataInicial=\{data_inicial\}"\
        f"&dataFinal=\{data_final\}"\
        f"&codigoModalidadeContratacao=6"\
        f"&q=\{q\}"\
        f"&pagina=\{pagina\}"\
        f"&tamanhoPagina=50"\
    )\
    \
    headers = \{\
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",\
        "Accept": "application/json, text/plain, */*"\
    \}\
    \
    try:\
        response = requests.get(url, headers=headers, timeout=15)\
        response.raise_for_status()\
        return response.json()\
    except requests.exceptions.RequestException as e:\
        return \{"error": True, "message": str(e)\}\
}