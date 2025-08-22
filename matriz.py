import ast

class Matriz:
    def __init__(self, archivo):
        # Valores iniciales
        self.valores = [] # Matriz del laberinto
        self.leer_archivo(archivo)

    # lee el archivo y construye la matriz
    def leer_archivo(self, archivo):
        with open(archivo, "r") as f:
            for linea in f:
                if not linea.startswith("["):
                    continue
                # Convertir la línea en lista de enteros
                fila = ast.literal_eval(linea.strip())
                self.valores.append(fila)

    # Retorna la cantidad de filas y columnas
    def dimensiones(self):
        filas = len(self.valores)
        columnas = len(self.valores[0]) if filas > 0 else 0
        return filas, columnas