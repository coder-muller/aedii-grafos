# api.py: expõe o grafo e as buscas com FastAPI
# rodar com: uvicorn api:app --reload  e abrir http://127.0.0.1:8000/docs
from fastapi import FastAPI, HTTPException

from buscas import ALGORITMOS
from grafo import UNIDADE, carregar_grafo

app = FastAPI(title="Rotas do Prédio com Grafos")

# o grafo é carregado uma vez só, quando a API sobe
grafo = carregar_grafo("arestas.txt")


# porta inexistente devolve 404 com mensagem
def validar_porta(porta):
    if porta not in grafo:
        raise HTTPException(404, f"Porta não encontrada: {porta}")


# roda um algoritmo e formata a resposta no formato pedido no enunciado
def executar(nome, origem, destino):
    caminho, custo, visitados = ALGORITMOS[nome](grafo, origem, destino)
    return {
        "algoritmo": nome,
        "caminho": caminho,
        "custo": custo,
        "unidade": UNIDADE,
        "visitados": visitados,
    }


# GET /portas: todas as portas do prédio, em ordem alfabética
@app.get("/portas")
def portas():
    return sorted(grafo)


# GET /vizinhos/{porta}: vizinhos da porta e o peso de cada aresta
@app.get("/vizinhos/{porta}")
def vizinhos(porta: str):
    validar_porta(porta)
    return [{"porta": p, "peso": w} for p, w in grafo[porta]]


# GET /rota: caminho, custo e visitados de UM algoritmo
@app.get("/rota")
def rota(origem: str, destino: str, algoritmo: str = "dijkstra"):
    validar_porta(origem)
    validar_porta(destino)
    algoritmo = algoritmo.lower()
    if algoritmo not in ALGORITMOS:
        raise HTTPException(400, f"Algoritmo inválido. Use um destes: {', '.join(ALGORITMOS)}")
    return executar(algoritmo, origem, destino)


# GET /comparar: os quatro algoritmos lado a lado para o mesmo par de portas
@app.get("/comparar")
def comparar(origem: str, destino: str):
    validar_porta(origem)
    validar_porta(destino)
    return [executar(nome, origem, destino) for nome in ALGORITMOS]