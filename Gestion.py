from gestionProductos import consultarCsv
import json
import utiles
import utiles
from deposito import deposito
from datetime import datetime


class gestion:
    def __init__(self) -> None:
        pass

    def importar(filecsv,invCodigo:list,invStock:list,depositos:list):
        """
        importamos un producto a nuestra base de datos de depositos, asignando
        un deposito si tiene stock, sino crea un deposito nuevo

        Parameters:
        filecsv(str): ruta del archivo csv
        codigo(str): el codigo del articulo

        return:
        Bool
        
        """
        listProductos=consultarCsv(filecsv)
        #listamos los productos de la base de datos CSV
        contador=1
        for producto in listProductos:
            print(f"{contador} - [CODIGO] {producto.codigo } [DETALLE] {producto.detalle}")
            contador = contador + 1 
        #Elegimos un producto y junto con la cantidad a importar
        seleccion=utiles.validarSeleccion(input("Seleccione una opcion : "),0,contador)
        
        cantidad= utiles.validarSeleccion(input("ingrese la cantidad a importar"),0,90000)

        codigo=listProductos[seleccion-1].codigo
        existeProd=False
        for codProd in invCodigo:
            if codProd == codigo:
                idindex=invCodigo.index(codigo)
                invStock[idindex] = invStock[idindex] + cantidad
                existeProd=True
        
        if not existeProd:
            invCodigo.append(codigo)
            invStock.append(cantidad)

        agregeItem = False
      
        faltaAgregar=cantidad
        if(depositos!=[]):
            #Valido si tengo el articulo en mi deposito
            for dep in depositos:
                    agregeItem = True
                    faltaAgregar=deposito.agregarProducto(dep,codigo,faltaAgregar)
                  
            if 0<faltaAgregar:
 
                newDep=deposito(utiles.validarSeleccion(input("Inserte la capacidad maxima de almacenamiento"),faltaAgregar,90000))
                deposito.agregarProducto(newDep,codigo,faltaAgregar)
                depositos.append(newDep)
               
        else:
          
            utiles.log("no existen depositos creados,se creara uno nuevo")
            newDep=deposito(utiles.validarSeleccion(input("Inserte la capacidad maxima de almacenamiento"),cantidad,90000))
            depositos.append(newDep)
            deposito.agregarProducto(newDep,codigo,cantidad)
           # if  0>faltaAgregar:
                ##creo un deposito y solicito la capcidad maxixma del mismo
                    ##validar que no sea menor que lo faltante
                    #Agrego el nuevo deposito lo que me quedo pendiente
         #           newDep=deposito(utiles.validarSeleccion(input("Inserte la capacidad maxima de almacenamiento"),1,90000))
          #          deposito.agregarProducto(newDep,codigo,faltaAgregar)
          #          depositos.append(newDep)

        gestion.actDepositos(depositos)
        
        
        
                
    def actDepositos(depositos:list):
        """
        actualiza el estado de los depositos en nuestra base de datos (JSON)

        Parameters:
        depositos(list)lista de depositos 
    
        """
        diccionario=[]
        for dep in depositos:
            diccionario.append(deposito.objToJson(dep))
        utiles.ActualizarEstadoDep("deposito.json",diccionario)

    def log(mensaje:str):
        utiles.log(mensaje)

    def vender(listcsv,invCodigos:list,invStock:list,depositos:list):

        lstproductos = consultarCsv(listcsv)
        
        print("[CODIGO] [DETALLE] [CANTIDAD EN INVENTARIO]")
        contador=-1
        for producto in lstproductos:
            contador = contador+1
            codigoindex=invCodigos.index(producto.codigo)
            if invStock[codigoindex] > 0:
                 cantidad = invStock[codigoindex]
                 print(f"{contador}  {producto.codigo}   {producto.detalle}  {cantidad}")
                 
        
        #solicito datos de CUIT:
        cuit=utiles.validarCuit(input("ingrese el numero de CUIT(NN-NNNNNNNN-N)"))

        codProd=utiles.validarSeleccion(input("Seleccione la opcino a comprar"),0,contador)
        
        codigo=lstproductos[int(codProd)].codigo
        cantMax=invStock[codigoindex] 
        canVenta=utiles.validarSeleccion(input("ingrese la cantidad a comprar"),1,cantMax)
        cantaDescontar=canVenta
        validar=True
        #verficio la capacidad disponible y si la tengo prosigo descontando del inventario de stock
      

        if invStock[codigoindex] < int(canVenta):
            canVenta=utiles.validarSeleccion(input("ingrese la cantidad a comprar"),1,cantMax)
        else:
            invStock[codigoindex]  = invStock[codigoindex] -int(canVenta)

        #busco el producto en mis depositos y descuento la cantidad
        for dep in depositos:
            
            cantaDescontar=deposito.descontarProducto(dep,codigo,cantaDescontar)
            
        cotizacion = utiles.isFloat("ingrese la cotizacion del dia")
        gestion.limpiarDepositos(depositos)
        gestion.actDepositos(depositos)
        gestion.generar_ticket(cotizacion,lstproductos[int(codProd)],canVenta,cuit)
            


    def limpiarDepositos(depositos:list):
        i=0
        while i<len(depositos):
            if depositos[i].stock ==[]:
                del depositos[i]
            else:
                i +=1
               
     
    def generar_ticket(cotizacion:float,obProducto,cantidad:int,cuit:str):
        
        precioVenta = cotizacion * obProducto.usdVenta
        fechaHora=datetime.now()
        horaFormateada=fechaHora.strftime("%d/%m/%Y %H:%M")

        DataTikect=[horaFormateada,cuit,obProducto.detalle,cantidad,obProducto.usdVenta,precioVenta,cotizacion]
        utiles.escribirTxt(DataTikect)
        #imprimo por pantalla el ticket
        print("-------------------------------------")
        print(f"[VENTA] {fechaHora}\n"
        f"CUIT Comprador : {cuit}\n"
        f"Detalle producto : {obProducto.detalle}\n"
        f"Cantidad Ventidad:{cantidad}\n"
        f"importe USD: {obProducto.usdVenta}\n"
        f"importe ARS : {precioVenta}\n"
        f"Cotizacion del dia: {cotizacion}")
        print("-------------------------------------")




##FUNCIONES PARA LA PREACARGA DE DEPOSITOS

    def getdeposito()->list:
        lstDepositos=[]
        for stk in  utiles.imprimirEstadosDep("deposito.json"):
            newdep = deposito(stk['CapacidadMaxima'])
            for item in stk['Stock']:
                deposito.agregarProducto(newdep,item['item'],item['cantidad'])
            lstDepositos.append(newdep)
        return lstDepositos
    