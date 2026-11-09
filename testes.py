import os
import tempfile

from buscas import ALGORITMOS, bfs, dfs, dijkstra, gulosa, pares_divergentes
from grafo import carregar_grafo, contar_arestas, portas_nao_alcancadas

EXEMPLO = """LABTEC LAB201 12
LAB201 LAB202 10
LAB202 LAB203 9
LABTEC PATIO 8
PATIO LAB203 40
"""


# grafo de exemplo do enunciado: os resultados têm que bater com a tabela do PDF
def testar_exemplo():
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as arq:
        arq.write(EXEMPLO)
    g = carregar_grafo(arq.name)
    os.remove(arq.name)

    assert g["LABTEC"] == [("LAB201", 12), ("PATIO", 8)]
    assert bfs(g, "LABTEC", "LAB203") == (["LABTEC", "PATIO", "LAB203"], 48, 4)
    assert gulosa(g, "LABTEC", "LAB203")[:2] == (["LABTEC", "PATIO", "LAB203"], 48)
    assert dfs(g, "LABTEC", "LAB203")[1] in (31, 48)
    assert dijkstra(g, "LABTEC", "LAB203") == (["LABTEC", "LAB201", "LAB202", "LAB203"], 31, 5)
    print("Grafo de exemplo do enunciado: OK")


# grafo do prédio: conectado e todas as buscas acham caminho entre qualquer par
def testar_predio():
    g = carregar_grafo("arestas.txt")
    print(f"Prédio: {len(g)} portas, {contar_arestas(g)} arestas")
    assert portas_nao_alcancadas(g) == [], "falta aresta no arquivo"
    for a in g:
        for b in g:
            otimo = dijkstra(g, a, b)[1]
            for nome, funcao in ALGORITMOS.items():
                caminho, custo, _ = funcao(g, a, b)
                assert caminho[0] == a and caminho[-1] == b, (nome, a, b)
                # nenhum algoritmo pode achar caminho mais barato que o Dijkstra
                assert custo >= otimo, (nome, a, b)
    print("Prédio: todas as buscas funcionam entre todos os pares: OK")

    print("\nPares em que BFS e Dijkstra discordam (maior diferença primeiro):")
    for dif, a, b, cam_bfs, c_bfs, cam_dij, c_dij in pares_divergentes(g)[:5]:
        print(f"\n{a} -> {b} (diferença {dif} m)")
        print(f"  BFS      {len(cam_bfs)} portas, {c_bfs} m: {' -> '.join(cam_bfs)}")
        print(f"  Dijkstra {len(cam_dij)} portas, {c_dij} m: {' -> '.join(cam_dij)}")


if __name__ == "__main__":
    testar_exemplo()
    testar_predio()