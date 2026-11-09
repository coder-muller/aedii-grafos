# Rotas do Prédio com Grafos

Trabalho de Algoritmos e Estruturas de Dados II, Unisenac Campus Pelotas (Prof. Pablo De Chiaro).

## Integrantes

- Guilherme Coelho Müller
- Arthur Ortiz Fonseca

## Unidade do peso

Metros. O peso de cada aresta é a distância entre duas portas vizinhas, não a distância acumulada desde o LabTec.
A distância de um caminho inteiro é calculada pelos algoritmos somando os pesos das arestas.

### Origem das medidas

Não fiz a medição no prédio: as portas, as arestas e os pesos (`arestas.txt` e `desenho-grafo.png`) foram
pegos do trabalho do colega Derek Cavalcanti
([derekzinnn/atividade-grafos-aedii](https://github.com/derekzinnn/atividade-grafos-aedii)), que estimou as
distâncias em linha reta a partir da escala da planta. O código (`grafo.py`, `buscas.py`, `api.py`, `testes.py`)
foi feito por mim.

## Arquivos

| Arquivo | O que tem |
|---|---|
| `desenho-grafo.png` | Desenho do grafo sobre a planta, com portas, arestas, pesos e o LabTec como ponto zero |
| `arestas.txt` | Uma aresta por linha (`PORTA PORTA PESO`), cada aresta uma única vez |
| `grafo.py` | `carregar_grafo` monta a lista de adjacência nos dois sentidos |
| `buscas.py` | `bfs`, `dfs`, `gulosa` e `dijkstra`, todas devolvendo `(caminho, custo, visitados)` |
| `api.py` | API em FastAPI |
| `testes.py` | Testes do exemplo do enunciado e do grafo do prédio |

O grafo tem 47 portas e 64 arestas. Portas de sala usam o nome da sala. Portas de corredor usam o número da planta.

## Como cada algoritmo funciona

- **BFS**: usa uma fila e explora por camadas. Acha o caminho com **menos portas**, mas ignora o peso.
- **DFS**: usa uma pilha e vai o mais fundo possível pelo primeiro vizinho. O caminho depende da ordem das
  linhas no `arestas.txt` e não tem garantia nenhuma de ser curto.
- **Gulosa**: em cada porta escolhe o vizinho com a **aresta mais curta** que ainda não visitou. Decide só pelo
  passo atual, então pode entrar num caminho ruim. Se cair num beco sem saída, recua uma porta e tenta o próximo
  vizinho mais perto.
- **Dijkstra**: usa uma fila de prioridade (`heapq`) e sempre finaliza a porta com a menor distância acumulada.
  Garante o caminho de **menor custo total**.

Todas usam um conjunto de visitados, porque o prédio tem ciclos e sem isso a busca andaria em círculo.

## Par de portas em que BFS e Dijkstra discordam

**LABTEC até BIBLIOTECA1** (`/comparar?origem=LABTEC&destino=BIBLIOTECA1`):

| Algoritmo | Portas | Custo | Caminho |
|---|---|---|---|
| BFS | 10 | 128 m | LABTEC → PORTA06 → CANTINA2 → IGREJA1 → IGREJA2 → BIBLIOTECA2 → PORTA29 → PORTA28 → PORTA27 → BIBLIOTECA1 |
| Dijkstra | 12 | 110 m | LABTEC → LAB201 → LAB202 → LAB203 → BANHEIROFEM → BANHEIROMASC → PORTA14 → PORTA19 → COORDENADOR → PORTA23 → SALAPROFESSORES → BIBLIOTECA1 |

**Por quê:** a BFS conta portas, não metros. Indo pela direita (Cantina, Igreja e Biblioteca) são 9 arestas,
contra 11 pelo corredor da esquerda, então a BFS chega primeiro ao destino por esse lado e para. Só que esse
caminho tem arestas longas: PORTA27 a BIBLIOTECA1 tem 27 m, LABTEC a PORTA06 tem 21 m e IGREJA2 a BIBLIOTECA2
tem 18 m. O Dijkstra soma os pesos e escolhe o corredor da esquerda, que tem **duas portas a mais**, mas arestas
curtas (de 5 a 19 m), e chega com **18 m a menos**. Ou seja, menos portas não quer dizer menos distância, e só o
Dijkstra garante o menor custo.

Para listar outros pares em que os dois discordam, rode `python testes.py`.
