from flask import Flask, render_template, request

app = Flask(__name__)

# Factores de riesgo con puntajes
factores_riesgo = {
    "edad": {(0, 29): 0, (30, 39): 2, (40, 49): 4, (50, 59): 6, (60, 100): 8},
    "salud": {"saludable": 0, "obesidad": 3, "ansiedad": 2, "diabetes": 5, "hipertension": 5},
    "historial_familiar": {"true": 3, "false": 0},
    "estilo_vida": {"activo": 0, "deportista": 0, "fumador": 4, "alcoholico": 4},
    "ocupacion": {"oficina": 0, "piloto": 5, "bombero": 5, "minero": 3},
    "historial_seguro": {"bueno": 0, "malo": 5, "reclamos_frecuentes": 3}
}

# Función para clasificar el riesgo con edad > 60 como "Alto Riesgo"
def clasificar_riesgo(puntaje, edad):
    if edad > 60:
        return "Alto Riesgo"
    elif puntaje <= 5:
        return "Bajo Riesgo"
    elif 6 <= puntaje <= 15:
        return "Moderado Riesgo"
    else:
        return "Alto Riesgo"

# Función para calcular el puntaje
def calcular_puntaje(cliente):
    puntaje = 0
    for rango, puntos in factores_riesgo["edad"].items():
        if rango[0] <= cliente["edad"] <= rango[1]:
            puntaje += puntos
            break
    puntaje += factores_riesgo["salud"].get(cliente["salud"], 0)
    puntaje += factores_riesgo["historial_familiar"].get(cliente["historial_familiar"], 0)
    puntaje += factores_riesgo["estilo_vida"].get(cliente["estilo_vida"], 0)
    puntaje += factores_riesgo["ocupacion"].get(cliente["ocupacion"], 0)
    puntaje += factores_riesgo["historial_seguro"].get(cliente["historial_seguro"], 0)
    return puntaje

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = int(request.form['edad'])
        salud = request.form['salud']
        historial_familiar = request.form['historial_familiar']
        estilo_vida = request.form['estilo_vida']
        ocupacion = request.form['ocupacion']
        historial_seguro = request.form['historial_seguro']
        
        nuevo_cliente = {
            "nombre": nombre,
            "edad": edad,
            "salud": salud,
            "historial_familiar": historial_familiar,
            "estilo_vida": estilo_vida,
            "ocupacion": ocupacion,
            "historial_seguro": historial_seguro
        }
        
        puntaje = calcular_puntaje(nuevo_cliente)
        nivel_riesgo = clasificar_riesgo(puntaje, edad)
        
        resultados.append({"nombre": nombre, "puntaje": puntaje, "nivel_riesgo": nivel_riesgo})
    
    return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
