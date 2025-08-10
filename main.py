from collections import deque
import heapq

# ==============================
# Funciones de utilidad
# ==============================

def leer_matriz():
    """
    Lee una matriz NxM desde la entrada del usuario.
    Cada fila se ingresa como números separados por espacios.
    Ejemplo de fila: 0 1 0 3
    """
    N = int(input("Ingrese el número de filas (N): "))
    M = int(input("Ingrese el número de columnas (M): "))
    laberinto = []
    print("Ingrese el laberinto fila por fila (0=espacio, 1=pared, 2=inicio, 3=meta):")
    for _ in range(N):
        fila = list(map(int, input().split()))
        if len(fila) != M:
            raise ValueError(f"La fila debe tener exactamente {M} elementos.")
        laberinto.append(fila)
    return laberinto


def encontrar_posiciones(laberinto):
    """Encuentra las coordenadas de inicio (2) y meta (3) en la matriz."""
    inicio = meta = None
    for i, fila in enumerate(laberinto):
        for j, valor in enumerate(fila):
            if valor == 2:
                inicio = (i, j)
            elif valor == 3:
                meta = (i, j)
    return inicio, meta


def matriz_a_grafo(laberinto):
    """
    Convierte la matriz del laberinto a una lista de adyacencia.
    Cada nodo es una tupla (fila, columna).
    """
    N = len(laberinto)
    M = len(laberinto[0])
    grafo = {}
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha

    for i in range(N):
        for j in range(M):
            if laberinto[i][j] != 1:  # No es pared
                grafo[(i, j)] = []
                for dx, dy in movimientos:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < N and 0 <= nj < M and laberinto[ni][nj] != 1:
                        grafo[(i, j)].append(((ni, nj), 1))  # peso = 1
    return grafo


def distancia_manhattan(a, b):
    """Calcula la distancia de Manhattan entre dos coordenadas (x1, y1) y (x2, y2)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ==============================
# Algoritmos de búsqueda
# ==============================

def bfs(grafo, inicio, meta):
    """Búsqueda en anchura (BFS)."""
    cola = deque([(inicio, [inicio])])
    visitados = set()

    while cola:
        nodo, camino = cola.popleft()
        if nodo == meta:
            return camino
        if nodo in visitados:
            continue
        visitados.add(nodo)
        for vecino, _ in grafo.get(nodo, []):
            if vecino not in visitados:
                cola.append((vecino, camino + [vecino]))
    return None


def dfs(grafo, inicio, meta):
    """Búsqueda en profundidad (DFS)."""
    pila = [(inicio, [inicio])]
    visitados = set()

    while pila:
        nodo, camino = pila.pop()
        if nodo == meta:
            return camino
        if nodo in visitados:
            continue
        visitados.add(nodo)
        for vecino, _ in grafo.get(nodo, []):
            if vecino not in visitados:
                pila.append((vecino, camino + [vecino]))
    return None


def a_estrella(grafo, inicio, meta):
    """Algoritmo A*."""
    open_set = []
    heapq.heappush(open_set, (0, inicio, [inicio]))  # (f_score, nodo, camino)
    g_score = {inicio: 0}

    while open_set:
        _, nodo, camino = heapq.heappop(open_set)

        if nodo == meta:
            return camino

        for vecino, costo in grafo.get(nodo, []):
            tentativo_g = g_score[nodo] + costo
            if tentativo_g < g_score.get(vecino, float('inf')):
                g_score[vecino] = tentativo_g
                f_score = tentativo_g + distancia_manhattan(vecino, meta)
                heapq.heappush(open_set, (f_score, vecino, camino + [vecino]))
    return None

# ==============================
# Programa principal
# ==============================

def main():
    laberinto = leer_matriz()
    inicio, meta = encontrar_posiciones(laberinto)

    if not inicio or not meta:
        print("Error: No se encontró inicio (2) o meta (3) en el laberinto.")
        return

    grafo = matriz_a_grafo(laberinto)

    print("\nRuta BFS:", bfs(grafo, inicio, meta))
    print("Ruta DFS:", dfs(grafo, inicio, meta))
    print("Ruta A* :", a_estrella(grafo, inicio, meta))


if _name_ == "_main_":
    main()
