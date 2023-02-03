import sys

import mariadb
from flask import Flask, request
from jinja2 import Environment, FileSystemLoader

from config import consultaSQL

app = Flask(__name__)


@app.route('/')
def mostrar_equips():
    arraylokmedonalagana= []
    enviroment = Environment(loader=FileSystemLoader("Template/"))
    template = enviroment.get_template("plantillaLlistatEquips.html")
    try:
        conn = mariadb.connect(
            user="pythonMaster",
            password="Admin1234",
            host="localhost",
            port=3306,
            database="proves"
        )
    except mariadb.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        sys.exit(1)

    cur = conn.cursor()
    cur.execute("SELECT * FROM equipos;")
    resultat = cur.fetchall()
    conn.commit()
    conn.close()

    for resultats in resultat:
        arraylokmedonalagana.append(
            {'id': resultats[0], 'nombre': resultats[1]}
        )
    info = {"equip": arraylokmedonalagana}
    contingut = template.render(info)
    return f'{contingut}'

@app.route('/', methods=['GET', 'POST'])
def capturar_boto():
    jugadorEquip= []

    if request.method == 'POST':
        enviroment = Environment(loader=FileSystemLoader("Template/"))
        template = enviroment.get_template("plantillaEquip.html")
        infoEquip=request.form.get('mostrarEquip')
        try:
            conn = mariadb.connect(
                user="pythonMaster",
                password="Admin1234",
                host="localhost",
                port=3306,
                database="proves"
            )
        except mariadb.Error as e:
            print(f"Error conectando a la base de datos: {e}")
            sys.exit(1)

        cur = conn.cursor()
        cur.execute(f"""SELECT * FROM jugadores, equipos where jugadores.idEquipo = equipos.idEquipo and jugadores.idEquipo={infoEquip};""")
        resultat = cur.fetchall()
        conn.commit()
        conn.close()

        for resultats in resultat:
            jugadorEquip.append(
                {'id': resultats[0], 'nombre': resultats[1], 'posicion': resultats[2], 'nacimiento': resultats[3],'numero':resultats[4], 'altura': resultats[5], 'valorMercado': resultats[6], 'idEquipo': resultats[7], 'nombreEquipo': resultats[9]}
            )
        info = {"equip": jugadorEquip}

        contingut = template.render(info)
        return f'{contingut}'

