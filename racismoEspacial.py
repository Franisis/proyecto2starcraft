import sys
from collections import defaultdict
class Celula:
    def __init__(self, id, x, y, tipo, peptidos_compartidos):
        self.id = id
        self.x = x
        self.y = y
        self.tipo = tipo
        self.peptidos_compartidos = peptidos_compartidos

    def __repr__(self):
        return f"Celula(id={self.id}, x={self.x}, y={self.y}, tipo={self.tipo}, peptidos={self.peptidos_compartidos})"

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
def construir_lista_adyacencia(caso):
    # Diccionario para almacenar los péptidos y las células que los contienen
    peptido_to_celulas = defaultdict(list)
    
    # Rellenar el diccionario con cada péptido y las células que lo contienen
    for celula in caso['celulas']:
        for peptido in celula.peptidos_compartidos:
            peptido_to_celulas[peptido].append(celula.id)
    
    # Diccionario para la lista de adyacencia
    adyacencia = defaultdict(set)
    
    # Construir la lista de adyacencia
    for celulas_compartiendo in peptido_to_celulas.values():
        # Crear pares de células que comparten al menos un péptido
        for i in range(len(celulas_compartiendo)):
            for j in range(i + 1, len(celulas_compartiendo)):
                c1, c2 = celulas_compartiendo[i], celulas_compartiendo[j]
                adyacencia[c1].add(c2)
                adyacencia[c2].add(c1)
    
    return adyacencia


# Llamar a la función para leer la entrada y mostrar el resultado

casos = leer_entrada()
casosAdyacencia = []
"""
for i, caso in enumerate(casos):
    print(f"Caso {i + 1}:")
    print(f"  Número de células: {caso['num_celulas']}")
    print(f"  Distancia máxima: {caso['distancia_maxima']}")
    print(f"  Células:")
    for celula in caso["celulas"]:
        print(f"    {celula}")
"""
def construir_red_de_flujo(caso, adyacencia):
    # Crear el diccionario de la red de flujo como un grafo dirigido
    red_flujo = defaultdict(list)
    
    # Nodos especiales para la fuente (entrada) y el sumidero (salida)
    fuente = 'fuente'
    sumidero = 'sumidero'
    
    # Iterar sobre las células en el caso
    for celula in caso['celulas']:
        if celula.tipo == 1:
            # Conectar la fuente a todas las células de tipo 1
            red_flujo[fuente].append(celula.id)
        
        elif celula.tipo == 3:
            # Conectar las células de tipo 3 al sumidero
            red_flujo[celula.id].append(sumidero)
        
        # Conectar las células entre sí usando la lista de adyacencia
        for adyacente in adyacencia[celula.id]:
            # Evitar conexiones no deseadas
            if celula.tipo == 1 and caso['celulas'][adyacente-1].tipo != 2:
                continue  # Células de tipo 1 solo se conectan con células de tipo 2
            if caso['celulas'][adyacente-1].tipo == 3 and celula.tipo != 2:
                continue  # Células de tipo 3 solo pueden conectarse desde células de tipo 2
            # Agregar el enlace en la red de flujo
            red_flujo[celula.id].append(adyacente)
    
    return red_flujo

for i, celulas in enumerate(casos):
    print('cambio caso')
    adyacencia = construir_lista_adyacencia(celulas)
    casosAdyacencia.append(adyacencia)
    for celula, adyacentes in adyacencia.items():
        print(f"Célula {celula} -> {sorted(adyacentes)}")
        

for caso in casos:
    print('nuevo caso')
    print(caso['distancia_maxima'])
    for celula in caso['celulas']:
        if celula.tipo==1:
            print(celula.id, 'celula iniciadora')
        if celula.tipo ==2:
            print(celula.id, 'celula calculadora')
        if celula.tipo ==3:
            print(celula.id, 'celula de respuesta')

redes_de_flujo=[]     
for i in range(len(casosAdyacencia)):
    caso=casos[i]
    adyacencia=casosAdyacencia[i]
    redes_de_flujo.append(construir_red_de_flujo(caso, adyacencia))


for red in redes_de_flujo:
    print(red)