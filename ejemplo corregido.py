import rule_engine
# Crear base de datos de clientes
clientes = [
    {
        "nombre": "Mayabi",
        "edad": 22,
        "salud": "saludable",
        "historial_familiar": "false",
        "estilo_vida": "activo",
        "ocupacion": "oficina",
        "historial_seguro": "bueno"
    },
    {
        "nombre": "Carlos",
        "edad": 45,
        "salud": "diabetes",
        "historial_familiar": "true",
        "estilo_vida": "fumador",
        "ocupacion": "minero",
        "historial_seguro": "reclamos_frecuentes"
    },
    {
        "nombre": "Ana",
        "edad": 51,
        "salud": "hipertension",
        "historial_familiar": "true",
        "estilo_vida": "alcoholico",
        "ocupacion": "piloto",
        "historial_seguro": "bueno"
    },
    {
        "nombre": "Carlos",
        "edad": 30,
        "salud": "diabetes",
        "historial_familiar": "true",
        "estilo_vida": "fumador",
        "ocupacion": "piloto",
        "historial_seguro": "malo"
    },
    {
        "nombre": "Jaime",
        "edad": 38,
        "salud": "obesidad",
        "historial_familiar": "false",
        "estilo_vida": "deportista",
        "ocupacion": "oficina",
        "historial_seguro": "bueno"
    }
        
]
 

# Reglas de riesgo corregidas
reglas_riesgo = {
    "bajo": rule_engine.Rule(
        "(edad < 30) and "
        "(salud == 'saludable') and "
        "(historial_familiar == 'false') and "
        "(estilo_vida == 'activo') and "
        "(ocupacion == 'oficina') and "
        "(historial_seguro == 'bueno')"
    ),
    "alto": rule_engine.Rule(
        "(edad > 51 and salud in ['diabetes', 'hipertension']) or "
        "(historial_familiar == 'true') or "
        "(estilo_vida in ['fumador', 'alcoholico']) or "
        "(ocupacion in ['piloto', 'bombero'])"
    ),
    "moderado": rule_engine.Rule(
        "(edad >= 40 and edad <= 50) or "
        "(salud in ['diabetes', 'hipertension']) or "
        "(historial_familiar == 'true') or "
        "(estilo_vida in ['fumador', 'alcoholico'])"
    ),
    "promedio": rule_engine.Rule(
        "(edad >= 15 and edad <= 39) and "
        "(salud in ['saludable', 'obesidad', 'ansiedad']) and "
        "(historial_familiar in ['true', 'false']) and "
        "(estilo_vida in ['deportista', 'activo']) and "
        "(ocupacion in ['piloto', 'bombero', 'oficina'])"
    )
}
 
# Evaluar riesgo para cada cliente
for cliente in clientes:
    if reglas_riesgo["bajo"].matches(cliente):
        nivel_riesgo = "Bajo Riesgo"
    elif reglas_riesgo["alto"].matches(cliente):
        nivel_riesgo = "Alto Riesgo"
    elif reglas_riesgo["moderado"].matches(cliente):
        nivel_riesgo = "Moderado Riesgo"
    elif reglas_riesgo["promedio"].matches(cliente):
        nivel_riesgo = "Promedio Riesgo"
    else:
        nivel_riesgo = "Desconocido"
    
    print(f"Cliente: {cliente['nombre']}, Nivel de Riesgo: {nivel_riesgo}")