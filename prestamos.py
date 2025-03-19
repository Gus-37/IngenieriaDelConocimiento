from flask import Flask, request, render_template

app = Flask(__name__)

def evaluar_prestamo(cliente):
    historial_crediticio = cliente["historial_crediticio"]
    ingresos = cliente["ingresos"]
    cuota = cliente["cuota"]
    dti = cliente["dti"]
    tipo_empleo = cliente["tipo_empleo"]
    garantias = cliente["garantias"]
    historial_prestamos = cliente["historial_prestamos"]

    if garantias == "alta":
        if historial_crediticio > 600 or historial_crediticio == 0:  # Sin historial también es aceptado
            return "Aprobado"
        elif dti < 50 and ingresos / cuota >= 1.5:
            return "Aprobación Condicional"
        else:
            return "Rechazado"
    
  
    if garantias == "baja":
        if historial_crediticio > 750 and ingresos / cuota >= 3 and dti < 30:
            return "Aprobado"
        elif historial_crediticio >= 600 and ingresos / cuota >= 2 and dti < 40 and tipo_empleo == "fijo":
            return "Aprobación Condicional"
        else:
            return "Rechazado"
    
    return "Rechazado"  # Si no cumple ninguna condición, se rechaza

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluar', methods=['POST'])
def evaluar():
    datos = request.form
    nombre = datos["nombre"]

    historial_crediticio = 0 if datos["historial_crediticio"] == "no_aplica" else int(datos["historial_crediticio"])
    historial_prestamos = "no_aplica" if datos["historial_crediticio"] == "no_aplica" else datos["historial_prestamos"]

    cliente = {
        "nombre": nombre,
        "historial_crediticio": historial_crediticio,
        "ingresos": int(datos["ingresos"]),
        "cuota": int(datos["cuota"]),
        "dti": int(datos["dti"]),
        "tipo_empleo": datos["tipo_empleo"],
        "garantias": datos["garantias"],
        "historial_prestamos": historial_prestamos
    }

    resultado = evaluar_prestamo(cliente)
    
    return render_template('index.html', resultado=resultado, nombre=nombre)

if __name__ == "__main__":
    app.run(debug=True)
