from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "clave_memoria"

def crear_tablero():

    simbolos = ["🍎","🍌","🍇","🍉","🍓","🍒"]
    cartas = simbolos * 2
    random.shuffle(cartas)

    tablero = [
        cartas[0:4],
        cartas[4:8],
        cartas[8:12]
    ]

    return tablero


@app.route("/", methods=["GET","POST"])
def juego():

    if "tablero" not in session:
        session["tablero"] = crear_tablero()
        session["descubiertas"] = []
        session["seleccion"] = []
        session["intentos"] = 0

    tablero = session["tablero"]
    descubiertas = session["descubiertas"]
    seleccion = session["seleccion"]
    intentos = session["intentos"]

    if request.method == "POST":

        fila = int(request.form["fila"])
        col = int(request.form["col"])

        if (fila,col) not in seleccion and (fila,col) not in descubiertas:
            seleccion.append((fila,col))

        if len(seleccion) == 2:

            f1,c1 = seleccion[0]
            f2,c2 = seleccion[1]

            if tablero[f1][c1] == tablero[f2][c2]:
                descubiertas.append((f1,c1))
                descubiertas.append((f2,c2))

            seleccion = []
            intentos += 1

    session["descubiertas"] = descubiertas
    session["seleccion"] = seleccion
    session["intentos"] = intentos

    ganado = len(descubiertas) == 12

    return render_template(
        "index.html",
        tablero=tablero,
        descubiertas=descubiertas,
        seleccion=seleccion,
        intentos=intentos,
        ganado=ganado
    )


@app.route("/reiniciar")
def reiniciar():
    session.clear()
    return "Juego reiniciado <a href='/'>Volver al juego</a>"


if __name__ == "__main__":
    app.run(debug=True)