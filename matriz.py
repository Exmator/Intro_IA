import ast

class Matriz:
    def __init__(self, archivo):
        self.valores = []
        self.leer_archivo(archivo)

    def leer_archivo(self, archivo):
        with open(archivo, "r") as f:
            for linea in f:
                # Convertir la línea en lista de enteros
                fila = ast.literal_eval(linea.strip())
                self.valores.append(fila)

    def mostrar(self):
        for fila in self.valores:
            print(fila)

    def dimensiones(self):
        filas = len(self.valores)
        columnas = len(self.valores[0]) if filas > 0 else 0
        return filas, columnas