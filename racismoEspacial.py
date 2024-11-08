import sys

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

# Llamar a la función para leer la entrada y mostrar el resultado
casos = leer_entrada()
for i, caso in enumerate(casos):
    print(f"Caso {i + 1}:")
    print(f"  Número de células: {caso['num_celulas']}")
    print(f"  Distancia máxima: {caso['distancia_maxima']}")
    print(f"  Células:")
    for celula in caso["celulas"]:
        print(f"    {celula}")
