from collections import deque

UNIDADE = "metros"

# cada linha do arquivo vira duas entradas porque se anda nos dois sentidos
def carregar_grafo(caminho):
    grafo = {}
    with open(caminho, encoding="utf-8") as arq:
        for linha in arq:
            # ignora linhas em branco
            if not linha.strip():
                continue
            a, b, peso = linha.split()
            peso = int(peso)
            grafo.setdefault(a, []).append((b, peso))  # ida
            grafo.setdefault(b, []).append((a, peso))  # volta
    return grafo


# cada aresta aparece duas vezes na lista, por isso divide por 2
def contar_arestas(grafo):
    return sum(len(vizinhos) for vizinhos in grafo.values()) // 2


# BFS simples a partir do LABTEC: devolve as portas que NÃO foram alcançadas
# se a lista vier vazia, o grafo está conectado; se vier algo, falta aresta no arquivo
def portas_nao_alcancadas(grafo, origem="LABTEC"):
    alcancadas = {origem}
    fila = deque([origem])
    while fila:
        atual = fila.popleft()
        for vizinho, _ in grafo[atual]:
            if vizinho not in alcancadas:
                alcancadas.add(vizinho)
                fila.append(vizinho)
    return sorted(set(grafo) - alcancadas)


# rodando "python grafo.py" faz a conferência do passo 3 do enunciado
if __name__ == "__main__":
    g = carregar_grafo("arestas.txt")
    print(f"Portas: {len(g)}")
    print(f"Arestas: {contar_arestas(g)}")
    faltando = portas_nao_alcancadas(g)
    if faltando:
        print("Portas não alcançadas a partir do LABTEC:", faltando)
    else:
        print("OK: a BFS a partir do LABTEC alcança todas as portas.")
