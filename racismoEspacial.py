from math import sqrt
from collections import defaultdict, deque

import sys

class Celula:
    def __init__(self, id, x, y, tipo, peptidos):
        self.id = id
        self.x = x
        self.y = y
        self.tipo = tipo
        self.peptidos = peptidos

    def __repr__(self):
        return f"Celula(id={self.id}, x={self.x}, y={self.y}, tipo={self.tipo}, peptidos={self.peptidos})"


def contar_coincidencias(cadena1, cadena2):
    # Convertir las cadenas en listas de palabras
    lista1 = cadena1
    lista2 = cadena2
    
    # Contar cuántas palabras de la lista1 están en la lista2
    coincidencias = sum(1 for palabra in lista1 if palabra in lista2)
    
    return coincidencias




def leer_entrada():
    # Leer el número de casos
    num_casos = int(sys.stdin.readline().strip())
    casos = []

    for _ in range(num_casos):
        # Leer el número de células y la distancia máxima
        num_celulas, distancia_maxima = map(int, sys.stdin.readline().strip().split())
        
        # Lista para almacenar las células de este caso
        celulas = []
        
        for _ in range(num_celulas):
            # Leer la información de cada célula
            linea = sys.stdin.readline().strip().split()
            id_celula = int(linea[0])
            x = int(linea[1])
            y = int(linea[2])
            tipo = int(linea[3])
            peptidos_compartidos = linea[4:]
            
            # Crear la instancia de Celula y agregarla a la lista de células
            celula = Celula(id_celula, x, y, tipo, peptidos_compartidos)
            celulas.append(celula)
        
        # Agregar el caso a la lista de casos
        casos.append({
            "num_celulas": num_celulas,
            "distancia_maxima": distancia_maxima,
            "celulas": celulas
        })
    
    return casos




def distancia(celula1, celula2):
    return sqrt((celula1.x - celula2.x)**2 + (celula1.y - celula2.y)**2)


def construir_red(caso, distancia_maxima):
    
    red_flujo = defaultdict(dict)  # Nodo apunta a un dict con sus vecinos y sus pesos

    # Conectar fuente con las células tipo 1
    for celula in caso['celulas']:
        if celula.tipo == 1:
            red_flujo['fuente'][celula.id] = 1  # Peso arbitrario para las conexiones desde 'fuente'

    # Conectar células tipo 3 con el sumidero
    for celula in caso['celulas']:
        if celula.tipo == 3:
            red_flujo[celula.id]['sumidero'] = 1  # Peso arbitrario para las conexiones al 'sumidero'

    # Conectar células entre sí según las reglas
    for celula1 in caso['celulas']:
        for celula2 in caso['celulas']:
            if celula1.id != celula2.id:
                # Si están dentro de la distancia máxima
                if distancia(celula1, celula2) <= distancia_maxima:
                    # Si tienen coincidencias en péptidos
                    coincidencias = contar_coincidencias(celula1.peptidos, celula2.peptidos)
                    if coincidencias > 0:
                        # Reglas de conexión con pesos según coincidencias
                        if celula1.tipo == 1 and celula2.tipo == 2:
                            red_flujo[celula1.id][celula2.id] = coincidencias
                        elif celula1.tipo == 2 and (celula2.tipo == 2 or celula2.tipo == 3):
                            red_flujo[celula1.id][celula2.id] = coincidencias

    return red_flujo



def bfs(capacity, flow, source, sink, parent):
    """Realiza una búsqueda en anchura para encontrar un camino aumentante."""
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        current = queue.popleft()
        for neighbor, cap in capacity[current].items():
            if neighbor not in visited and cap - flow[current][neighbor] > 0:
                parent[neighbor] = current
                visited.add(neighbor)
                if neighbor == sink:
                    return True
                queue.append(neighbor)
    return False

def edmonds_karp(network, source, sink):
    """Calcula el flujo máximo utilizando Edmonds-Karp."""
    # Inicializamos capacidades y flujos
    capacity = defaultdict(lambda: defaultdict(int))
    for u, neighbors in network.items():
        for v, cap in neighbors.items():
            capacity[u][v] = cap

    flow = defaultdict(lambda: defaultdict(int))
    parent = {}

    max_flow = 0

    while bfs(capacity, flow, source, sink, parent):
        # Encuentra el flujo máximo a través del camino aumentante
        path_flow = float('Inf')
        s = sink

        while s != source:
            path_flow = min(path_flow, capacity[parent[s]][s] - flow[parent[s]][s])
            s = parent[s]

        # Actualiza los flujos en las aristas del camino
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow




casos = leer_entrada()
for caso in casos:
    distanciaMaxima = caso['distancia_maxima']
    red=construir_red(caso, caso['distancia_maxima'])  #red de flujo original  
    flujoMaximo=edmonds_karp(red, 'fuente', 'sumidero')
    flujoMinimo= sys.maxsize
    mexico= None
    new=None
    for celula in list(caso['celulas']):
        
        if celula.tipo==2:
            
            casoCopy = caso.copy()
            casoCopy['celulas'].pop(casoCopy['celulas'].index(celula)) #borra la celula del caso para construir una nueva red de flujo sin esa celula
            
            blockedNet = construir_red(caso, distanciaMaxima)
            maxflow = edmonds_karp(blockedNet, 'fuente', 'sumidero')
            
            
            if maxflow<= flujoMinimo and maxflow<flujoMaximo and maxflow>0:
                new = celula.id
                flujoMinimo = maxflow
                mexico = flujoMaximo
                print(new,flujoMinimo,flujoMaximo)
                
            

    
