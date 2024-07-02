import utiles
import gestionProductos
from deposito import deposito
from Gestion import gestion
import os

def cargarProductos(csv):
    listProductos = gestionProductos.consultarCsv(csv)
    for prod in listProductos:
        invProducto.append(prod.codigo)

def cargarinvStok(codigo:str)->int:
    cantidadStok=0
    for dep in invDepositos:
        for item in dep.stock:
            if item['item']==codigo:
                cantidadStok=+cantidadStok+item['cantidad']
    return cantidadStok

print("Gestion de productos\n")

db="productos.csv"
invProducto=[]
invStock=[]
invDepositos = gestion.getdeposito()
cargarProductos(db)

for prod in invProducto:
    invStock.append(cargarinvStok(prod))
    

opciones_menu = ("Seleccione una opción:\n"
                 "1-Alta de producto\n"
                 "2-Baja de producto\n"
                 "3-Modificar producto\n"
                 "4-Listar Productos\n"
                 "5-Importar Productos\n"
                 "6-Vender Producto\n"
                 "7-Listar Estado Depositos\n"
                 "8-BuscarProducto por menos stock\n"
                 "9-Filtrar Producto por precio media\n"
                 "10-Ordenar depositos por peso\n"
                 "0-Salir\n")




while True:
    opcion = utiles.get_int(opciones_menu, "Opción inválida", 0, 10, 3)
    
    if opcion is None:
        print("No se ingresó una opción válida después de varios intentos. Saliendo...")
        break
    
    match opcion:
        case 0:
            print("Saliendo del programa.")
            break
        case 1:
            # Llamamos a la funcion para ingresar el nuevo producto
            gestionProductos.agregarProducto(db, invProducto, invStock)
        case 2:
            # Llamar a la función para baja de producto
            gestionProductos.eliminarProducto(db, invProducto, invStock)
        case 3:
            codigo = input("Ingrese el código de producto a modificar: ")
            gestionProductos.modificarPrecioCompra(db, codigo)
            gestionProductos.modificarPrecioVenta(db, codigo)
        case 4:
            gestionProductos.mostrarProductos(db, invProducto, invStock)
        case 5:
            gestion.importar(db, invProducto, invStock, invDepositos)
        case 6:
            gestion.vender(db, invProducto, invStock, invDepositos)
        case 7:
            print(f"[ID de depósito] - [CAPACIDAD ocupada/máxima] - [DISPONIBLE]")
            for dep in invDepositos:
                deposito.listarDepostios(dep)
        case 8:
            index = utiles.buscarMenor(invStock)
            print(f"[PRODUCTO {invProducto[index]}]")
            print(f"TOTAL STOCK: {invStock[index]}")
            # Buscamos en depósito
            for dep in invDepositos:
                deposito.buscarProducto(dep, invProducto[index])
        case 9:
            precios = []
            listProductos = gestionProductos.consultarCsv(db) 
            for prod in listProductos:
                precios.append(prod.usdCompra)
            
            media = utiles.buscarPrecioMedia(precios)
            for prod in listProductos:
                if media > prod.usdCompra:
                    print(f"Producto: {prod.codigo}")
        case 10:
            listProductos = gestionProductos.consultarCsv(db) 
            diccionarioProductos=[]
            peso_tot=0
            for produ in listProductos:
                if produ.codigo in invProducto:
                    peso = produ.peso
                    for dep in invDepositos:
                        data=deposito.DepositosporPeso(dep, produ.codigo,peso)
                        if data != None:
                            diccionarioProductos.append(data)
                            
            
            diccionarioAgrupado =[]
            for item in diccionarioProductos:
                dep=item['Depisto']
                peso=item['Peso Total']

            for dep in invDepositos:
                depo=dep.id
                pesoTotal=0
                for item in diccionarioProductos:
                    if depo ==item['Depisto']:
                        pesoTotal += item['Peso Total']
                
                diccionarioAgrupado.append({'Deposito' : depo,
                                            'Peso Total':pesoTotal})
                
                
            utiles.ordenarDiccionario(diccionarioAgrupado)
            
            for dicc in diccionarioAgrupado:
                print(f"Deposito : {dicc['Deposito']} - Peso Total :{dicc['Peso Total']}")
                             
                

              

        case _:
            print("Opción no reconocida.")


    input("precione una recla apra continur")

    os.system('cls')