from datetime import datetime
import json
import re 
def get_int(mensaje:str,mensa_error:str,minimo:int,maximo:int,reintentos:int) -> int|None:
    intentos = 0
    while intentos < reintentos:
        valor = input(mensaje)
        if valor.isdigit():
            valor = int(valor)
            if minimo <= valor <= maximo:
                return valor
        print(mensa_error)
        intentos = intentos + 1
    return None


def buscarMenor(lista:list)->int:
    codigo=min(lista)
    return lista.index(codigo)

def buscarPrecioMedia(lista:list)->float:
    total = sum(lista)
    media = total/len(lista)
    return float(media)

def ordenar(lista,tipo):
    if tipo == "MAYOR":
        ordenarListaNumerosMayor(lista)
    elif tipo =="MENOR":
        ordenarListaNumerosMenor(lista)

        

#RECIBO UNA LISTA DE NUMEROS Y LO ORDENO DE MENOR A MAYOR
def ordenarListaNumerosMenor(lista):
    for i in range(len(lista)):
        valorMinimo = i
        for j in range(i+1, len(lista)):
            if lista[j] < lista[valorMinimo]:
                valorMinimo = j

        valorAuxiliar = lista[i]
        lista[i] = lista[valorMinimo]
        lista[valorMinimo] = valorAuxiliar

#RECIBO UNA LISTA DE NUMEROS Y LO ORDENO DE MENOR A MAYOR
def ordenarListaNumerosMayor(lista):
    for i in range(len(lista)):
        valorMaximo = i
        for j in range(i+1, len(lista)):
            if lista[j] > lista[valorMaximo]:
                valorMaximo = j

        valorAuxiliar = lista[i]
        lista[i] = lista[valorMaximo]
        lista[valorMaximo] = valorAuxiliar


def ordenarDiccionario(diccionario:dict):
    """
    Ordena una lista de manera acendente

    Parameters:
    lista(list) : una lista de objetos
    atributo:str : la propiedad del objeto de la clase que va a comprara
    
    """
    for i in range(len(diccionario)):
        valorMaximo = i
        for j in range(i+1, len(diccionario)):
            if diccionario[j]['Peso Total'] < diccionario[valorMaximo]['Peso Total']:
                valorMaximo = j
        valorAuxiliar = diccionario[i]
        diccionario[i] = diccionario[valorMaximo]
        diccionario[valorMaximo] = valorAuxiliar


def isFloat(mensaje:str):
    while True:
        valor=input(mensaje)
        if valor.replace(".","").isdigit():
            valor=float(valor)
            if valor > 0:
                return valor
            else:
                mensaje="El valor ingresado debe ser mayor a 0"
        else:
            mensaje="El valor ingresado debe ser numerico ej : 20.10"

def log(mensaje:str):
        fechaHora=datetime.now()
        horaFormateada=fechaHora.strftime("%d/%m/%Y %H:%M")
        print(f"{horaFormateada} {mensaje}")

#--------------------------------Validaciones-----------------------------------
def validarCuit(cuit):
    while(True):
        if re.match(r'^\d{2}-\d{8}-\d{1}',cuit):
            return cuit
        else:
            print("El cuit debe ser con el formato valido NN-NNNNNNNN-N siendo N un valor Numerico")
            ##SI SE INGRESO MAL, VUELVEO A PREGUNTAR, HASTA INGRESAR CORRECTAMENTE EL VALOR 
            cuit=input("ingrese el Cuit")

def validarSeleccion(seleccion,minimo,maximo):
    while(True):
        if seleccion.isdigit():
            seleccion=int(seleccion)
            if seleccion >= 0 and seleccion >= minimo and seleccion <= maximo :
                return seleccion
            else:
                print(f"el valor debe estar entre {minimo} y {maximo}")
                seleccion=input("ingrese el valor nuevamente")
        else:
            print("el valor ingresado, debe ser numerico ej : 50")
            seleccion=input("ingrese el valor nuevamente")


#-------------------------------JSON

def ActualizarEstadoDep(path,data:list):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)
    
def imprimirEstadosDep(path)->list:
    lstDepositos=[]
    with open(path, 'r') as file:
        archivo = json.load(file)
    
        return archivo
#------------------------------TXT

def escribirTxt(textos:list):
    pathArchivo = "ventas.txt"
    for texto in textos:
        with open(pathArchivo, 'a') as archivo:
            archivo.write(str(texto)+"\n")