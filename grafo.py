from matriz import Matriz

archivo_laberinto = "matrizPrueba.txt"

class Grafo:
    def __init__(self, matriz: Matriz):
        self.matriz = matriz.valores
        self.coordenadaInicial = None
        self.coordenadaFinal = None
        self.grafo = {}
        self.lista_heuristica = {}
        self.construir_grafo()
        self.funcion_heuristica(self.coordenadaFinal)
        self.camino_por_profundidad = []
        self.camino_por_anchura = []
        self.camino_por_a_estrella = []

        self.primero_profundidad()
        self.primero_anchura()
        self.a_estrella()

    def encontrar_coordenadas_inicial_final(self):
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                if self.matriz[i][j] == 2:
                    self.coordenadaInicial = (i, j)
                elif self.matriz[i][j] == 3:
                    self.coordenadaFinal = (i, j)

    def construir_grafo(self):
        self.encontrar_coordenadas_inicial_final()
        lista_coordenadas_no_visitadas = [self.coordenadaInicial]
        lista_coordenadas_visitadas = []

        while lista_coordenadas_no_visitadas:
            coordenada_actual = lista_coordenadas_no_visitadas.pop(0)
            lista_coordenadas_visitadas.append(coordenada_actual)

            # Expandir en las cuatro direcciones
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nueva_coordenada = (coordenada_actual[0] + dx, coordenada_actual[1] + dy)
                
                if not self.es_coordenada_valida(nueva_coordenada):
                    continue

                # Inicializar si no existe
                if coordenada_actual not in self.grafo:
                    self.grafo[coordenada_actual] = []

                self.grafo[coordenada_actual].append(nueva_coordenada)

                if nueva_coordenada not in lista_coordenadas_visitadas and nueva_coordenada not in lista_coordenadas_no_visitadas:
                    lista_coordenadas_no_visitadas.append(nueva_coordenada)

    def es_coordenada_valida(self, coordenada):
        x, y = coordenada
        return (0 <= x < len(self.matriz) and
                0 <= y < len(self.matriz[0]) and
                self.matriz[x][y] != 1)  # 1 representa un obstáculo
    
    def obtener_vecinos(self, v):
        return self.grafo[v] if v in self.grafo else []
    
    def distancia_manhattan(self, a, b):
        """Calcula la distancia de Manhattan entre dos coordenadas (x1, y1) y (x2, y2)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def funcion_heuristica(self, n):
        for nodo in self.grafo:
            self.lista_heuristica[nodo] = self.distancia_manhattan(nodo, n)
    
    def primero_profundidad(self):
        inicio = self.coordenadaInicial
        fin = self.coordenadaFinal
        camino_profundidad = []
        stack = [inicio]   # (nodo_actual, camino_hasta_ahora)
        visitados = set()

        while stack:
            nodo = stack.pop()   # sacar el último (LIFO)
            
            if nodo in visitados:
                continue
            camino_profundidad.append(nodo)
            visitados.add(nodo)

            # Si encontramos el final
            if nodo == fin:
                self.camino_por_profundidad = camino_profundidad
                break

            # Agregar vecinos no visitados
            for vecino in self.obtener_vecinos(nodo):
                if vecino not in visitados:
                    stack.append(vecino)

        
    def primero_anchura(self):
        inicio = self.coordenadaInicial
        fin = self.coordenadaFinal
        camino_anchura = []
        queue = [inicio]   # (nodo_actual, camino)
        visitados = set()

        while queue:
            nodo = queue.pop(0)  # sacar el primero (FIFO)

            if nodo in visitados:
                continue
            camino_anchura.append(nodo)
            visitados.add(nodo)

            if nodo == fin:
                self.camino_por_anchura = camino_anchura
                break

            for vecino in self.obtener_vecinos(nodo):
                if vecino not in visitados:
                    queue.append(vecino)


    
    def a_estrella(self):
        inicio = self.coordenadaInicial
        fin = self.coordenadaFinal

        # Inicializamos costos
        camino_a_estrella = []
        g_cost = {inicio: 0}
        f_cost = {inicio: self.lista_heuristica[inicio]}
        abiertos = [(f_cost[inicio], inicio)]  # (f, nodo)
        visitados = set()

        while abiertos:
            # Ordenar por f_cost (el menor primero)
            abiertos.sort(key=lambda x: x[0])
            _, nodo = abiertos.pop(0)

            if nodo in visitados:
                continue
            camino_a_estrella.append(nodo)
            visitados.add(nodo)

            if nodo == fin:
                self.camino_por_a_estrella = camino_a_estrella
                break

            for vecino in self.obtener_vecinos(nodo):
                if vecino in visitados:
                    continue

                nuevo_g = g_cost[nodo] + 1  # costo de moverse (todos los movimientos valen 1)
                if vecino not in g_cost or nuevo_g < g_cost[vecino]:
                    g_cost[vecino] = nuevo_g
                    f_cost[vecino] = nuevo_g + self.lista_heuristica[vecino]
                    abiertos.append((f_cost[vecino], vecino))


    def mostrar(self):
        print("Coordenada Inicial:", self.coordenadaInicial)
        print("Coordenada Final:", self.coordenadaFinal)
        print("Grafo construido:")
        for nodo, vecinos in self.grafo.items():
            print(f"{nodo} -> {vecinos}")
        print("Heurística (distancia Manhattan al objetivo):")
        for nodo, heuristica in self.lista_heuristica.items():
            print(f"  {nodo}: {heuristica}")


# Ejemplo de uso
if __name__ == "__main__":
    matriz = Matriz(archivo_laberinto)
    grafo = Grafo(matriz)
    grafo.mostrar()

    print("\nCamino por DFS:", grafo.camino_por_profundidad)
    print("Camino por BFS:", grafo.camino_por_anchura)
    print("Camino por A*:", grafo.camino_por_a_estrella)
