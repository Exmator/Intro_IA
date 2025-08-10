class Grafo:

    def __init__(self, lista_adyacencia):
        self.lista_adyacencia = lista_adyacencia

    def obtener_vecinos(self, v):
        return self.lista_adyacencia[v]

    # funcion heuristica
    def h(self, n):
        #inserte su codigo aqui
        return H[n] # puede retornar una lista con el calculo de la heuristica para cada estado

    def primero_profundidad(self, nodo_inicio, nodo_final):
       #inserte si codigo aqui
        return None
        
    def primero_anchura(self, nodo_inicio, nodo_final):
       #inserte si codigo aqui
        return None
    
    def a_estrella(self, nodo_inicio, nodo_final):
       #inserte si codigo aqui
        return None
    