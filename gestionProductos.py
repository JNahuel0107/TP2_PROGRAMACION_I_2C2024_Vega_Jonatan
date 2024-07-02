##--------------------------------------IMPORTS UTILOZADOS
import re 
import os
import csv
import utiles
from producto import Prod


##------------------------------------GESTION DE PRODUCTOS ALTA/BAJA/MODIFICACION---------------------
def agregarProducto(filecsv:str,invCodigo:list,invStock:list) -> bool:
    """
    agrega un nuevo produto a las lista de stock y productos

    Parameters:
    filecsv(str): ruta del archivo csv
    invCodigo(list) = lista de codigos de los articulos
    invStock(list) = lista de stock de cada articulo

    return:
    Bool
    
    """
    ##validamos el formato del codigo
    codigo=input("ingrese el codigo del produto")
    ##valido el formato del producto y si existe en la base de datos
    if existeProducto(filecsv,validarCodigo(codigo)):
        detalle = validarDetalle(input("ingrese la descripcion del producto"))
        usd_compra = validarPrecio(input("ingrese el valor del precio de compra"))
        usd_venta = validarPrecio(input("ingrese el valor del precio de venta"))
        peso = validarPrecio(input("ingrese el peso del producto"))
        
        objProducto = Prod(codigo,detalle,usd_compra,usd_venta,peso)

        agregarCsv(filecsv,objProducto)
        invCodigo.append(codigo)
        invStock.append(0)
        utiles.log(f"Alta de producto Codigio = {codigo}")
        return True
    else:
       return False


def eliminarProducto(filecsv:str,invCodigo:list,invStock:list) -> bool:
    """
    Elimina un producto, siempre y cuando el mimos no tenga stock

    Parameters:
    filecsv(str): ruta del archivo csv
    invCodigo(list) = lista de codigos de los articulos
    invStock(list) = lista de stock de cada articulo

    return:
    Bool
    
    """
    listaProducto=consultarCsv(filecsv)

    contador=0
    for producto in listaProducto:
        print(f"{contador} - [CODIGO] {producto.codigo } [DETALLE] {producto.detalle}")
        contador = contador + 1 
    
    seleccion = int(input("Seleccione el numero del producto al dar de baja"))
    codigo=listaProducto[seleccion].codigo

    idindex=invCodigo.index(codigo)
    if len(invStock) > idindex:
        if invStock[idindex] !=0:
            utiles.log(f"[ERROR] Item con stock, no es posible dar de baja")
            return False
        else:
             invStock.pop(idindex)
            
    listaProducto.pop(seleccion)

    modificarCsv(filecsv,listaProducto)
    #Elimino el producto en cuestion de los vectore
    invCodigo.pop(idindex)
    

    return True

def modificarPrecioCompra(filecsv:str,codigo:str):
    """
    modifica el precio de compra de un codigo de articulo

    Parameters:
    filecsv(str): ruta del archivo csv
    codigo(str): el codigo del articulo

    return:
    Bool
    
    """
    nuevoPrecio=input("ingrese el nuevo precio de compra")
    lisProductos=consultarCsv(filecsv)
    hayCambios=False
    for producto in lisProductos:
        if producto.codigo == codigo:
            producto.usdCompra=nuevoPrecio
            hayCambios=True
    
    if hayCambios:
         modificarCsv(filecsv,lisProductos)
    
    return True

def modificarPrecioVenta(filecsv:str,codigo:str):
    """
    modifica el precio de venta de un codigo de articulo

    Parameters:
    filecsv(str): ruta del archivo csv
    codigo(str): el codigo del articulo

    return:
    Bool
    
    """
    nuevoPrecio=input("ingrese el nuevo precio de venta")
    lisProductos=consultarCsv(filecsv)
    hayCambios=False
    for producto in lisProductos:
        if producto.codigo == codigo:
            producto.usdVenta=nuevoPrecio
            hayCambios=True
    
    if hayCambios:
        modificarCsv(filecsv,lisProductos)
    
    return True

def mostrarProductos(filecsv:str,invCodig:list,invStock:list):
    listProducto = consultarCsv(filecsv)
    
    print("[CODIGO] [DETALLE] [USDCOMPRA] [USDVENTA] [CANTIDAD EN INVENTARIO]")
    for producto in listProducto:
        codigo = producto.codigo
        cantidad = 0
        if codigo in invCodig:
            idindex=invCodig.index(codigo)
            cantidad=invStock[idindex]
        print(f"{producto.codigo}   {producto.detalle}   {producto.usdCompra}   {producto.usdVenta}   {cantidad}")

    


    





##------------------------------------VALIDACIONES  PRODUCTOS-----------------------------------------
def existeProducto(filecsv:str,codigo):
    listaProductos=consultarCsv(filecsv)
    
    for producto in listaProductos:
        if producto.codigo == codigo:
            utiles.log(f"[Error] el codigo: {codigo} existe en la base de datos")
            return False
    return True

def validarCodigo(codigo:str):
    while(True):
        if re.match(r'^\d{4}-[A-Z]{2}$',codigo):
            return codigo
        else:
            print("El codigo debe tener el formato NNNN-AA, donde N es un valor numerico y A un alfabetico")
            
            codigo=input("ingrese el codigo del producto")

def validarDetalle(detalle:str):
    while(True):
        if 1 <= len(detalle):
            if 25 >= len(detalle):
                return detalle
            else:
                print("el detalle debe tener menos de 26 caracteres")
                detalle=input("ingrese el detalle del producto")
        else:
            print("el detalle no puede estar vacio")
            detalle=input("ingrese el detalle del producto")

##uso esta funcion para validar el precio y los pesos
def validarPrecio(precio):
    while(True):
        if precio.replace('.','',1).isdigit():
            precio=float(precio)
            if precio > 0:
                return precio
            else:
                print("el valor no debe ser inferior a 0")
                precio=input("ingrese un valor")
        else:
            print("el valor ingresado, debe ser numerico")
            precio=input("ingrese un valor")
##------------------------------------FIN VALIDACIONES  DE PRODUCTOS------------------------------------


##------------------------------------MANIPULACION DE CSV-------------------------------------------------

def consultarCsv(filecsv:str):
    lstProductos=[]
    with open(filecsv,'r',newline='') as dbfile:
                csvarch=csv.reader(dbfile)
                next(csvarch,None)
                for row in csvarch:
                    codigo,detalle,usd_compra,usd_venta,peso = row
                    usd_compra=float(usd_compra)
                    usd_venta=float(usd_venta)
                    peso=float(peso)
                    lstProductos.append(Prod(codigo,detalle,usd_compra,usd_venta,peso))
                return lstProductos

def modificarCsv(filecsv:str,listaProductos:list):
    with open(filecsv,'w',newline='') as dbfile:
                csvarch=csv.writer(dbfile)
                csvarch.writerow(["codigo","detalle","usd_compra","usd_venta","peso"])
                ##recorro cada producto y lo voy agregando 
                for producto in listaProductos:
                    csvarch.writerow([producto.codigo,producto.detalle,producto.usdCompra,producto.usdVenta,producto.peso])
                return True

def agregarCsv(filecsv:str,objProducto):
    if os.path.exists(filecsv):
        with open(filecsv,'a',newline='') as dbfile:
                    csvarch = csv.writer(dbfile)
                    csvarch.writerow([objProducto.codigo,objProducto.detalle,objProducto.usdCompra,objProducto.usdVenta,objProducto.peso])
                    return True
    else:
        crearCsv(filecsv)
        agregarCsv(filecsv,objProducto)

##Creo el csv con el encabezado 
def crearCsv(filecsv:str):
    with open(filecsv, 'w', newline='') as dbfile:
            csvarch = csv.writer(dbfile)
            csvarch.writerow(["codigo","detalle","usd_compra","usd_venta","peso"])


##-------------------------FIN MANIPULACION DE CSV-------------------------------------------------


