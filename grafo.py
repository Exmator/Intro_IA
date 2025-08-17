from matriz import Matriz

class Grafo:
    def __init__(self, matriz: Matriz):
        # Definicion de atributos iniciales
        self.matriz = matriz.valores
        self.coordenadaInicial = None
        self.coordenadaFinal = None
        self.grafo = {}
        self.lista_heuristica = {}
        self.camino_por_profundidad = []
        self.camino_por_anchura = []
        self.camino_por_a_estrella = []

        # Se construye el grafo y se calcula la heurística a la coordenada final
        self.construir_grafo()
        self.funcion_heuristica(self.coordenadaFinal)

        # Determinar los caminos de cada algoritmo
        self.primero_profundidad()
        self.primero_anchura()
        self.a_estrella()

    # Funcion que encuentra las coordenadas inicial (2) y final (3)
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

        # Se crea el grafo realizando una búsqueda en anchura desde el punto inicial 
        # hasta recorrer todo lo posible del laberinto
        while lista_coordenadas_no_visitadas:
            coordenada_actual = lista_coordenadas_no_visitadas.pop(0)
            lista_coordenadas_visitadas.append(coordenada_actual)

            # Expandir en las cuatro direcciones (Arriba, Abajo, Izquierda, Derecha)
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nueva_coordenada = (coordenada_actual[0] + dx, coordenada_actual[1] + dy)
                
                # Si no es una coordenada valida (Esta fuera del mapa o es un muro) no guardar
                if not self.es_coordenada_valida(nueva_coordenada):
                    continue

                # Inicializar si no existe la coordenada en el grafo
                if coordenada_actual not in self.grafo:
                    self.grafo[coordenada_actual] = []

                # Guardar la coordenada
                self.grafo[coordenada_actual].append(nueva_coordenada)

                # Si la nueva coordenada no ha sido visitada, agregarla a la lista
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

    # Calcula la heurística para cada nodo del grafo con respecto a la coordenada objetivo n
    def funcion_heuristica(self, n):
        for nodo in self.grafo:
            self.lista_heuristica[nodo] = self.distancia_manhattan(nodo, n)
    
    def primero_profundidad(self):
        inicio = self.coordenadaInicial
        fin = self.coordenadaFinal
        camino_profundidad = []
        stack = [inicio]   # Pila para el DFS
        visitados = set()

        while stack:
            nodo = stack.pop()   # sacar el último (LIFO)

            # Si es un nodo ya visitado, ignorarlo
            if nodo in visitados:
                continue

            # Agregar a la lista de camino visitado
            camino_profundidad.append(nodo)
            visitados.add(nodo)

            # Si encontramos el final
            if nodo == fin:
                self.camino_por_profundidad = camino_profundidad
                break

            # Agregar vecinos no visitados a la pila
            for vecino in self.obtener_vecinos(nodo):
                if vecino not in visitados:
                    stack.append(vecino)

        
    def primero_anchura(self):
        inicio = self.coordenadaInicial
        fin = self.coordenadaFinal
        camino_anchura = []
        queue = [inicio]   # Cola para el BFS
        visitados = set()

        while queue:
            nodo = queue.pop(0)  # sacar el primero (FIFO)

            # Si es un nodo ya visitado, ignorarlo
            if nodo in visitados:
                continue

            # Agregar a la lista de camino visitado
            camino_anchura.append(nodo)
            visitados.add(nodo)

            # Si encontramos el final
            if nodo == fin:
                self.camino_por_anchura = camino_anchura
                break

            # Agregar vecinos no visitados a la cola
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
            # Ordenar la lista de abiertos para obtener el nodo con menor coste y sacarlo
            abiertos.sort(key=lambda x: x[0])
            _, nodo = abiertos.pop(0)

            # Si es un nodo ya visitado, ignorarlo
            if nodo in visitados:
                continue

            # Agregar a la lista de camino visitado
            camino_a_estrella.append(nodo)
            visitados.add(nodo)

            # Si encontramos el final
            if nodo == fin:
                self.camino_por_a_estrella = camino_a_estrella
                break

            # Se recorre cada vecino del nodo
            for vecino in self.obtener_vecinos(nodo):
                # Si el vecino ya fue visitado, ignorarlo
                if vecino in visitados:
                    continue

                # Calcular nuevos costos minimos para los vecinos
                nuevo_g = g_cost[nodo] + 1  # costo de moverse (todos los movimientos valen 1)
                if vecino not in g_cost or nuevo_g < g_cost[vecino]:
                    g_cost[vecino] = nuevo_g
                    f_cost[vecino] = nuevo_g + self.lista_heuristica[vecino]
                    abiertos.append((f_cost[vecino], vecino))