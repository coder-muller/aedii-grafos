# buscas.py: BFS, DFS, gulosa e Dijkstra
# as quatro têm a mesma assinatura (grafo, origem, destino)
# e devolvem (caminho, custo, visitados); se não houver caminho, (None, None, visitados)
import heapq
from collections import deque


# monta o caminho voltando pelas anotações "de onde cheguei" até a origem
def montar_caminho(anterior, origem, destino):
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(anterior[caminho[-1]])
    caminho.reverse()
    return caminho


# o custo não está no grafo: é a soma dos pesos das arestas do caminho
def calcular_custo(grafo, caminho):
    custo = 0
    for a, b in zip(caminho, caminho[1:]):
        peso = dict(grafo[a])[b]
        custo += peso
    return custo


# BFS: usa FILA (FIFO), explora por camadas
# acha o caminho com MENOS PORTAS, mas ignora o peso das arestas
# "visitados" conta as portas tiradas da fila mais o destino, que encerra a busca ao ser descoberto
def bfs(grafo, origem, destino):
    if origem == destino:
        return [origem], 0, 1
    anterior = {}
    # conjunto de marcadas: sem ele a busca anda em círculo nos ciclos do prédio
    marcadas = {origem}
    fila = deque([origem])
    examinadas = 0
    while fila:
        atual = fila.popleft()
        examinadas += 1
        for vizinho, _ in grafo[atual]:
            if vizinho not in marcadas:
                marcadas.add(vizinho)
                anterior[vizinho] = atual
                # achou o destino: para aqui e monta o caminho
                if vizinho == destino:
                    caminho = montar_caminho(anterior, origem, destino)
                    return caminho, calcular_custo(grafo, caminho), examinadas + 1
                fila.append(vizinho)
    return None, None, examinadas


# DFS: usa PILHA (LIFO), vai fundo no primeiro vizinho antes de olhar os outros
# o caminho depende da ordem dos vizinhos (ordem das linhas no arestas.txt)
def dfs(grafo, origem, destino):
    anterior = {}
    visitados = set()
    pilha = [origem]
    while pilha:
        atual = pilha.pop()
        if atual in visitados:
            continue
        visitados.add(atual)
        if atual == destino:
            caminho = montar_caminho(anterior, origem, destino)
            return caminho, calcular_custo(grafo, caminho), len(visitados)
        # empilha ao contrário para o PRIMEIRO vizinho da lista ser o primeiro a sair
        for vizinho, _ in reversed(grafo[atual]):
            if vizinho not in visitados:
                anterior[vizinho] = atual
                pilha.append(vizinho)
    return None, None, len(visitados)


# gulosa: em cada porta, escolhe o vizinho com a aresta MAIS CURTA que ainda não foi visitado
# só olha o passo atual, não o caminho todo; por isso não garante o menor custo
# nunca repete uma porta; se cair num beco sem saída, recua uma porta e tenta o próximo mais perto
def gulosa(grafo, origem, destino):
    visitados = {origem}
    caminho = [origem]
    while caminho:
        atual = caminho[-1]
        if atual == destino:
            return caminho, calcular_custo(grafo, caminho), len(visitados)
        opcoes = [(peso, vizinho) for vizinho, peso in grafo[atual] if vizinho not in visitados]
        if opcoes:
            _, mais_perto = min(opcoes)
            visitados.add(mais_perto)
            caminho.append(mais_perto)
        else:
            # beco sem saída: remove a porta atual do caminho e volta para a anterior
            caminho.pop()
    return None, None, len(visitados)


# Dijkstra: acha o caminho de MENOR PESO TOTAL
# heapq é a fila de prioridade: heappop sempre devolve a porta com a menor distância
def dijkstra(grafo, origem, destino):
    # passo 1: todas as portas começam com distância infinita; a origem com 0
    distancia = {p: float("inf") for p in grafo}
    anterior = {}  # de onde cheguei
    distancia[origem] = 0
    fila = [(0, origem)]
    finalizadas = set()
    while fila:
        # passo 2: pega a porta ainda não finalizada com a menor distância
        d, atual = heapq.heappop(fila)
        if atual in finalizadas:
            continue  # entrada antiga na fila, essa porta já tem distância definitiva
        finalizadas.add(atual)
        # passo 4: ao finalizar o destino, monta o caminho voltando pelas anotações
        if atual == destino:
            caminho = montar_caminho(anterior, origem, destino)
            return caminho, distancia[destino], len(finalizadas)
        # passo 3: relaxamento, se passar por "atual" for mais curto, atualiza o vizinho
        for vizinho, peso in grafo[atual]:
            nova = d + peso
            if nova < distancia[vizinho]:
                distancia[vizinho] = nova
                anterior[vizinho] = atual
                heapq.heappush(fila, (nova, vizinho))
    return None, None, len(finalizadas)


# dicionário usado pela API para escolher o algoritmo pelo nome
ALGORITMOS = {
    "bfs": bfs,
    "dfs": dfs,
    "gulosa": gulosa,
    "dijkstra": dijkstra,
}


# procura pares de portas em que BFS e Dijkstra devolvem caminhos diferentes
# ordena pela diferença de custo (maior primeiro), para achar um bom exemplo para o README
def pares_divergentes(grafo):
    pares = []
    portas = sorted(grafo)
    for i, a in enumerate(portas):
        for b in portas[i + 1:]:
            cam_bfs, custo_bfs, _ = bfs(grafo, a, b)
            cam_dij, custo_dij, _ = dijkstra(grafo, a, b)
            if cam_bfs != cam_dij:
                pares.append((custo_bfs - custo_dij, a, b, cam_bfs, custo_bfs, cam_dij, custo_dij))
    pares.sort(reverse=True)
    return pares