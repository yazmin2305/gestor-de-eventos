import functools
import operator
from datetime import datetime
from optparse import Values
import sqlite3

def conectar():
    con = sqlite3.connect("mydatabase")
    cur = con.cursor()
    return con, cur    

#Creacion de la tabla en la base de datos Sqlite
try:
    con, cur = conectar()
    cur.execute(""" CREATE TABLE EVENTO(
            codigo integer primary key NOT NULL,
            nombre text NOT NULL,
            entrada_sell integer NOT NULL,
            fecha_evento text NOT NULL
            )""")
    print("Se creo la tabla evento ")
except(sqlite3.OperationalError):
    print("La tabla evento ya existe")  
con.close()

#Declaración de funciones
def ingresar_datos():
    con, cur = conectar()
    codigo = int(input("Ingrese el codigo del evento: "))
    nombre = input("Ingrese el nombre del evento: ")
    entradas = int(input("Ingrese la cantidad de entradas por vender: "))
    fecha = input("Ingrese la fecha de realización del evento: ")                
    sentenceInsert = "insert into evento(codigo, nombre, entrada_sell, fecha_evento) Values (?,?,?,?)", (codigo, nombre, entradas, fecha)
    cur.execute("insert into evento(codigo, nombre, entrada_sell, fecha_evento) Values (?,?,?,?)", (codigo, nombre, entradas, fecha))
    cur.close()
    con.commit()
    con.close()

def imprimir_datos(datos):
    fila = datos.fetchone()
    if fila != None:
        print(fila)
    else:
        print("No existe ningun evento asociado \n")

def imprimir_total_datos():
    con, cur = conectar()
    totalDatos = cur.execute('SELECT codigo, nombre, entrada_sell, fecha_evento FROM EVENTO')
    for fila in totalDatos:
        print(fila)
    print("")
    cur.close()
    con.close()
    
def buscar_evento(opcion):
    con, cur = conectar()
    if(opcion == 1):
        nombreEvent = input("Ingrese el nombre del evento: ")
        datos = cur.execute("SELECT codigo, nombre, entrada_sell, fecha_evento FROM EVENTO WHERE nombre = ?", (nombreEvent,))
        imprimir_datos(datos)            

    if(opcion == 2):
        codigoEvent = int(input("Ingrese el código del evento: "))
        datos = cur.execute("SELECT codigo, nombre, entrada_sell, fecha_evento FROM EVENTO WHERE codigo = ?", (codigoEvent,))
        imprimir_datos(datos)
    cur.close()
    con.close()

def comprar_entradas(numEntradas, codigoEntrada):
    con, cur = conectar()
    fecha = cur.execute("SELECT fecha_evento FROM EVENTO WHERE codigo = ?", (codigoEntrada,))
    fila = fecha.fetchone()
    if fila != None:
        fechaEvent = '-'.join(fila)
        fechaEvento = datetime.strptime(fechaEvent, "%d-%m-%Y")
        fechaNow = datetime.now().strftime("%d-%m-%Y")
        #res = fechaEvent - fechaNow
        print("fecha actual: ", fechaNow)
        print("fecha vieja: ", fechaEvento)
        Entradas = cur.execute("SELECT entrada_sell FROM EVENTO WHERE codigo = ?", (codigoEntrada,))
        numEntTotal = functools.reduce(lambda sub, ele:sub*10+ele, Entradas.fetchone())
            
        if numEntTotal == 0:
            print("Las entradas para este evento estan agotadas \n")
        elif numEntTotal - numEntradas < 0:
            print(f"Excedió el numero de entradas disponible. La cantidad de entradas disponibles en el momento son: {numEntTotal} \n")
        else:
            numEntTotal = numEntTotal - numEntradas
            cur.execute("UPDATE EVENTO SET entrada_sell = ? WHERE codigo = ?",(numEntTotal, codigoEntrada,))
            print("Las entradas han sido compradas exitosamente \n")
    else:
        print("No existe ningun evento con dicho código \n") 
    cur.close()
    con.commit()
    con.close()
       
#Menu
print("****MENU DE OPCIONES****")        
opcion = '0'
while not(opcion == '5'):
    print("1. Agregar los datos de un evento ")
    print("2. Buscar un evento por codigo o nombre ")
    print("3. Mostrar todos los eventos ")
    print("4. Comprar entrada ")
    print("5. Salir: ")
    
    opcion=input('Digite la opcion: ')
    
    if (opcion =='1'):
       ingresar_datos()
    
    if (opcion =='2'):
        print("Digite 1 si desea buscar el evento por su nombre ")
        print("Digite 2 si desea buscar el evento por su codigo ")
        opcion = int(input("Seleccione una opcion: "))
        buscar_evento(opcion)
        
    if (opcion =='3'):        
        imprimir_total_datos()
    
    if (opcion =='4'):
        codigoEntrada = int(input("Ingrese el codigo del evento al cual quiere asistir: "))
        numEntradas = int(input("Ingrese el numero de entradas a comprar: "))        
        #fechaEvent = '-'.join(fecha.fetchone())
        #fechaNow = datetime.now().strftime("%d-%m-%Y")
        #print(fechaEvent)
        comprar_entradas(numEntradas, codigoEntrada)
            
    if (opcion =='5'):
        print(' **** Saliendo ****')
        break


