import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import mariadb

from jugador import jugador


def descarregaWeb():
    url = 'https://www.transfermarkt.es/fc-barcelona/kader/verein/131'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    req = urllib.request.Request(url, None, headers)
    with urllib.request.urlopen(req) as response:
        resposta = response.read().decode("utf-8")
    fitxer = open("jugadors.html", "wt")
    fitxer = open("jugadors.html", "wt", encoding="utf-8")
    fitxer.write(resposta)
    fitxer.close()


def llegirFitxer():
    fitxer = open("jugadors.html", "rt", encoding="utf-8")
    html = fitxer.read()
    fitxer.close()

    inici = html.find('<table class="items">')
    final = html.find('<div class="keys"')
    taula = html[inici:final]

    taula = taula.replace('class=rn_nummer', 'class="rn_nummer"')
    taula = taula.replace('&nbsp;', '')

    fitxer = open("taula.xml", "wt", encoding="utf-8")
    fitxer.write(taula)
    fitxer.close()


def carregarXML():
    tree = ET.parse("taula.xml")
    root = tree.getroot()
    llistajugadors = []
    # Numeros:
    for tr in root.iter('tbody'):
        for td in tr.iter('td'):
            for div in td.iter('div'):
                j1 = jugador()
                j1.numero = div.text
                llistajugadors.append(j1)
    # Noms:
    comptador = 0
    for tbody in root.iter('tbody'):
        for a in tbody.iter('a'):
            if a.text is not None:
                llistajugadors[comptador].nombre = a.text
                llistajugadors[comptador].nombre = llistajugadors[comptador].nombre.strip()
                comptador += 1

    # Posició:
    comptador = 0
    for tbody in root.iter('tbody'):
        for table in tbody.iter('table'):
            for td in table.iter('td'):
                if td.text is not None:
                    valor = td.text
                    valor = valor.strip()
                    if len(valor) > 0:
                        llistajugadors[comptador].posicion = td.text
                        llistajugadors[comptador].posicion = llistajugadors[comptador].posicion.strip()
                        comptador += 1
    # Nacimiento

    comptador = 0
    for tbody in root.iter('tbody'):
        tsd = 0
        for tr in tbody.iter('tr'):
            for td in tr.iter('td'):
                j = td.get("class")
                if j == "zentriert":
                    tsd += 1
                    if td.text is not None:
                        valor = td.text
                        valor = valor.strip()
                        if len(valor) > 0 and tsd % 7 == 1:
                            # llistajugadors[comptador].nacimiento = td.text
                            # llistajugadors[comptador].nacimiento = llistajugadors[comptador].nacimiento.strip()
                            # llistajugadors[comptador].nacimiento = llistajugadors[comptador].nacimiento.split(" ", 0)
                            fecha = td.text.strip().split(" ")[0].replace("/", "-")
                            fecha = fecha.split("-")[2] + "-" + fecha.split("-")[1] + "-" + fecha.split("-")[0]
                            llistajugadors[comptador].nacimiento = fecha
                            comptador += 1

    # Altura
    comptador = 0
    for tbody in root.iter('tbody'):
        tsd = 0
        for tr in tbody.iter('tr'):
            for td in tr.iter('td'):
                j = td.get("class")
                if j == "zentriert":
                    tsd += 1
                    if td.text is not None:
                        valor = td.text
                        valor = valor.strip()
                        if len(valor) > 0 and tsd % 7 == 3:
                            # llistajugadors[comptador].altura = td.text
                            altura = td.text.strip().split(" ")[0].replace("m", "")
                            altura2 = altura.split(" ")[0].replace(",", ".")
                            altura3 = altura2.split(" ")[0].replace("-", "0")
                            # llistajugadors[comptador].altura = llistajugadors[comptador].altura.strip()
                            llistajugadors[comptador].altura =altura3
                            comptador += 1
    # valorMercado
    comptador = 0
    for tbody in root.iter('tbody'):
        tsd = 0
        for tr in tbody.iter('tr'):
            for td in tr.iter('td'):
                j = td.get("class")
                if j == "rechts hauptlink":
                    tsd += 1
                    if td.text is not None:
                        valor = td.text
                        valor = valor.strip()
                        if len(valor) > 0:
                            valorado = td.text.strip().split(" ")[0].replace("mil", "")
                            valorado2 = valorado.split(" ")[0].replace("€", "")
                            llistajugadors[comptador].valorMercado = valorado2
                            comptador += 1

    for j in llistajugadors:
        print(j.numero)
        print(j.nombre)
        print(j.posicion)
        print(j.nacimiento)
        print(j.altura)
        print(j.valorMercado)
        print("")
        insertJugadors = f"""INSERT INTO jugadores 
                (nombre,  posicion, nacimiento, numero, altura, valorMercado, idEquipo)
                VALUES
                ('{j.nombre}','{j.posicion}','{j.nacimiento}','{j.numero}','{j.altura}','{j.valorMercado}','{2}');
                """
        executarSQL(insertJugadors)
        print('Jugador añadido\n')


def executarSQL(sql):
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
    cur.execute(sql)
    conn.commit()
    conn.close()


#descarregaWeb()
llegirFitxer()
carregarXML()
