import mariadb
import sys

def crearTaules():
    crearEquip = """CREATE TABLE IF NOT EXISTS equipos
    ( idEquipo INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(40) NOT NULL,
    ciudad VARCHAR(40) NOT NULL,
    fundacion int NOT NULL,
    PRIMARY KEY (idEquipo),
    CONSTRAINT nombre_equipo UNIQUE (nombre)
    );
    """
    crearJugador="""CREATE TABLE IF NOT EXISTS jugadores
    ( idJugador INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(60) NOT NULL,
    posicion ENUM('Portero','Defensa central','Lateral izquierdo','Lateral derecho','Pivote','Mediocentro','Extremo izquierdo','Extremo derecho','Delantero centro') NOT NULL,
    nacimiento DATE NOT NULL,
    numero int NOT NULL,
    altura double NOT NULL,
    valorMercado int NOT NULL,
    idEquipo int NOT NULL,
    PRIMARY KEY (idJugador),
    CONSTRAINT fk_type
    FOREIGN KEY(idEquipo) 
        REFERENCES equipos(idEquipo));
    """
    executarSQL(crearEquip)
    executarSQL(crearJugador)
def menuProgram():
    while True:
        print("1.Insertar un equipo")
        print("2.Insertar un jugador")
        print("3.Listar todos los equipos")
        print("4.Listar todos los jugadores")
        print("5.Eliminar equipos")
        print("6.Eliminar jugadores")
        print("7.Sortir")
        opcio =int(input("Opció:"))
        if opcio == 1:
            insertarEquip()
        elif opcio == 2:
            insertarJugador()
        elif opcio == 3:
            llistarEquip()
        elif opcio == 4:
            llistarJugador()
        elif opcio == 5:
            eliminarEquipo()
        elif opcio == 6:
            eliminarJugador()
        elif opcio == 7:
            break


def insertarEquip():
    while True:
        print("Que nombre tiene el equipo?")
        nombreEquipo = input()
        print("De donde es el equipo?")
        ciudadEquipo = input()
        print("En que año se fundo?")
        fundacionEquipo = input()
        insertEquip = f"""INSERT INTO equipos 
        (nombre, ciudad, fundacion)
        VALUES
        ('{nombreEquipo}','{ciudadEquipo}',{fundacionEquipo});
        """
        executarSQL(insertEquip)
        print('Equipo añadido\n')
        print('Quieres crear otro? (Si/No)')
        repetir = input()
        if repetir.upper() == 'SI':
            continue
        else:
            menuProgram()

def insertarJugador():
    while True:
        global posicionJugador
        print('Que nombre tiene el jugador?')
        nombreJugador = input()
        print('En que posicion juega? \n1.Portero\n2.Defensa central\n3.Lateral izquierdo\n4.Lateral derecho\n5.Pivote\n'
              '6.Mediocentro\n7.Extremo izquierdo\n8.Extremo derecho\n9.Delantero centro')
        opcionpos = int(input())
        if opcionpos==1:
            posicionJugador = 'Portero'
        elif opcionpos==2:
            posicionJugador ='Defensa central'
        elif opcionpos==3:
            posicionJugador ='Lateral izquierdo'
        elif opcionpos==4:
            posicionJugador ='Lateral derecho'
        elif opcionpos==5:
            posicionJugador ='Pivote'
        elif opcionpos==6:
            posicionJugador ='Mediocentro'
        elif opcionpos==7:
            posicionJugador ='Extremo izquierdo'
        elif opcionpos==8:
            posicionJugador ='Extremo derecho'
        elif opcionpos==9:
            posicionJugador ='Delantero centro'
        print("Dia, mes y año del jugador YYYY/MM/DD")
        anojugador = input('Año:')
        mesjugador = input(anojugador+'/')
        diajugador = input(anojugador+'/'+mesjugador+'/')
        fechatotal = (anojugador+'-'+mesjugador+'-'+diajugador)
        print("Número del jugador?")
        numjugador=input()
        print('Altura del jugador?')
        alturajgd=input()
        print('Valor que tiene en el mercado?')
        valorjgd=input()
        print('ID del equipo que pertenece?')
        idEquipojgd=input()
        insertJugadors = f"""INSERT INTO jugadores 
        (nombre,  posicion, nacimiento, numero, altura, valorMercado, idEquipo)
        VALUES
        ('{nombreJugador}','{posicionJugador}','{fechatotal}','{numjugador}','{alturajgd}','{valorjgd}','{idEquipojgd}');
        """
        executarSQL(insertJugadors)
        print('Jugador añadido\n')
        print('Quieres crear otro? (Si/No)')
        repetir = input()
        if repetir.upper() == 'SI':
            continue
        else:
            menuProgram()

def llistarEquip():
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

    listarEquipo = f"""SELECT * FROM equipos;"""
    cur = conn.cursor()
    cur.execute(listarEquipo)
    resultado = cur.fetchall()
    conn.close()
    for i in resultado:
        print(i)
    print("")

def llistarJugador():
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

    listarJugador = f"""SELECT * FROM jugadores;"""
    cur = conn.cursor()
    cur.execute(listarJugador)
    resultado = cur.fetchall()
    conn.close()
    for i in resultado:
        print(i)
    print("")

def eliminarEquipo():
    print('Mientras el equipo contenga algun jugador dentro, el equipo no sera eliminado.')
    print('Pon la id del equipo que quieres eliminar:')
    opcionid=input()
    eliminarEquipos = f"""DELETE FROM equipos WHERE idEquipo ='{opcionid}' ;"""
    executarSQL(eliminarEquipos)

def eliminarJugador():
    print('Pon la id del jugador que quieres eliminar:')
    opcionid = input()
    eliminarJgd = f"""DELETE FROM jugadores WHERE idJugador='{opcionid}' ;"""
    executarSQL(eliminarJgd)




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

def consultaSQL():
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

    return conn
