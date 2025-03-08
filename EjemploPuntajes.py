import rule_engine

# Base de datos de clientes
clientes = [
    {"nombre": "Mayabi", "edad": 22, "salud": "saludable", "historial_familiar": "false", "estilo_vida": "activo", "ocupacion": "oficina", "historial_seguro": "bueno"},
    {"nombre": "Carlos", "edad": 45, "salud": "diabetes", "historial_familiar": "true", "estilo_vida": "fumador", "ocupacion": "minero", "historial_seguro": "reclamos_frecuentes"},
    {"nombre": "Ana", "edad": 51, "salud": "hipertension", "historial_familiar": "true", "estilo_vida": "alcoholico", "ocupacion": "piloto", "historial_seguro": "bueno"},
    {"nombre": "Carlos", "edad": 30, "salud": "diabetes", "historial_familiar": "true", "estilo_vida": "fumador", "ocupacion": "piloto", "historial_seguro": "malo"},
    {"nombre": "Jaime", "edad": 42, "salud": "obesidad", "historial_familiar": "true", "estilo_vida": "activo", "ocupacion": "oficina", "historial_seguro": "malo"}
]

# Reglas de puntuación 
reglas = [
    {"condicion": "edad >= 30 and edad < 40", "puntaje": 2},
    {"condicion": "edad >= 40 and edad < 50", "puntaje": 4},
    {"condicion": "edad >= 50 and edad < 60", "puntaje": 6},
    {"condicion": "edad >= 60", "puntaje": 8},
    {"condicion": "salud == 'obesidad'", "puntaje": 3},
    {"condicion": "salud == 'ansiedad'", "puntaje": 2},
    {"condicion": "salud == 'diabetes'", "puntaje": 5},
    {"condicion": "salud == 'hipertension'", "puntaje": 5},
    {"condicion": "historial_familiar == 'true'", "puntaje": 3},
    {"condicion": "estilo_vida == 'fumador'", "puntaje": 4},
    {"condicion": "estilo_vida == 'alcoholico'", "puntaje": 4},
    {"condicion": "ocupacion == 'piloto'", "puntaje": 5},
    {"condicion": "ocupacion == 'bombero'", "puntaje": 5},
    {"condicion": "ocupacion == 'minero'", "puntaje": 3},
    {"condicion": "historial_seguro == 'malo'", "puntaje": 3},
    {"condicion": "historial_seguro == 'reclamos_frecuentes'", "puntaje": 5}
]

# Clasificación del nivel de riesgo según puntaje
def clasificar_riesgo(puntaje):
    if puntaje <= 5:
        return "Bajo Riesgo"
    elif 6 <= puntaje <= 10:
        return "Promedio Riesgo"
    elif 11 <= puntaje <= 15:
        return "Moderado Riesgo"
    else:
        return "Alto Riesgo"

# Evaluación de reglas 
def calcular_puntaje(cliente):
    puntaje_total = 0
    for regla in reglas:
        engine = rule_engine.Rule(regla["condicion"])
        if engine.matches(cliente):
            puntaje_total += regla["puntaje"]
    return puntaje_total

# Evaluar y mostrar resultados
for cliente in clientes:
    puntaje = calcular_puntaje(cliente)
    nivel_riesgo = clasificar_riesgo(puntaje)
    print(f"Cliente: {cliente['nombre']}, Puntaje: {puntaje}, Nivel de Riesgo: {nivel_riesgo}")
