import pygame
import sys
import time
from matriz import Matriz
from grafo import Grafo

# Direccion archivo laberinto
archivo_laberinto = "matriz1.txt"

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)

# Tamaño de celda
TAM_CELDA = 5
DELAY = 0.01  # Delay para la animación

# Laberinto
matriz = Matriz(archivo_laberinto)
grafo = Grafo(matriz)

# ----------------------------
# Función para dibujar el laberinto
# ----------------------------
def dibujar_laberinto(screen, matriz):
    for i, fila in enumerate(matriz.valores):
        for j, valor in enumerate(fila):
            x, y = j * TAM_CELDA, i * TAM_CELDA
            if valor == 1:
                color = NEGRO
            elif valor == 2:
                color = VERDE
            elif valor == 3:
                color = ROJO
            else:
                color = BLANCO
            pygame.draw.rect(screen, color, (x, y, TAM_CELDA, TAM_CELDA))
            pygame.draw.rect(screen, (200, 200, 200), (x, y, TAM_CELDA, TAM_CELDA), 1)

# ----------------------------
# Función para animar un camino
# ----------------------------
def animar_camino(screen, camino, color, delay=DELAY):
    for (i, j) in camino:
        x, y = j * TAM_CELDA, i * TAM_CELDA
        if (i, j) == grafo.coordenadaInicial or (i, j) == grafo.coordenadaFinal:
            continue
        pygame.draw.rect(screen, color, (x, y, TAM_CELDA, TAM_CELDA))
        pygame.draw.rect(screen, (200, 200, 200), (x, y, TAM_CELDA, TAM_CELDA), 1)
        pygame.display.flip()
        time.sleep(delay)

# ----------------------------
# Definir los caminos encontrados
# ----------------------------
camino_dfs = grafo.camino_por_profundidad
camino_bfs = grafo.camino_por_anchura
camino_astar = grafo.camino_por_a_estrella

# ----------------------------
# Main con pygame
# ----------------------------
def main():
    pygame.init()
    filas, columnas = matriz.dimensiones()
    screen = pygame.display.set_mode((columnas * TAM_CELDA, filas * TAM_CELDA))
    pygame.display.set_caption("Animación Laberinto - DFS, BFS, A*")

    dibujar_laberinto(screen, matriz)
    pygame.display.flip()

    # Imprimir la lista de nodos recorridos para cada algoritmo
    print("DFS:")
    print(camino_dfs)
    print("BFS:")
    print(camino_bfs)
    print("A*:")
    print(camino_astar)

    # Espera 1 segundo antes de empezar
    time.sleep(1)

    # Animar cada camino
    animar_camino(screen, camino_dfs, AZUL)      # DFS = azul
    animar_camino(screen, camino_bfs, NARANJA)   # BFS = naranja
    animar_camino(screen, camino_astar, MORADO)  # A* = morado

    # Esperar hasta que se cierre la ventana
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
