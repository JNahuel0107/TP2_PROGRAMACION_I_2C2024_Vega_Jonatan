class deposito:
    iddep=0
    def __init__(self,capacidad) -> None:
        self.id=deposito.iddep
        deposito.iddep=deposito.iddep+1
        self.capacidad=capacidad
        self.stock=[]
    def __len__(self):
        cantidadUsada=0
        for stk in self.stock:
            cantidadUsada=cantidadUsada + stk['cantidad']
        disponible=self.capacidad-cantidadUsada
        return int(disponible)
    
    def agregarProducto(self,codigo,cantidad)->int:
        if len(self) >= cantidad:
            for prod in self.stock:
                if prod['item']==codigo:
                    prod['cantidad'] = prod['cantidad'] + cantidad
                    return 0
            self.stock.append({'item':codigo,'cantidad':cantidad})
            return 0
        else:
           
            cantidadFaltante = cantidad - len(self)
            cantidadAgregar=cantidad-cantidadFaltante
            if cantidadAgregar>0:
                for prod in self.stock:
                    if prod['item']==codigo:
                        prod['cantidad'] = prod['cantidad'] + cantidadAgregar
                        return cantidadFaltante
                self.stock.append({'item':codigo,'cantidad':cantidadAgregar})
            return cantidadFaltante

            
            
    def descontarProducto(self,codigo,candescontar):
        cantSinDescontar=candescontar
        for prod in self.stock:
            if prod['item'] == codigo:
                prod['cantidad'] = prod['cantidad'] - candescontar

                if prod['cantidad']<= 0 :
                    cantSinDescontar = prod['cantidad'] * (-1)
                    prod['cantidad'] = 0
                    self.stock.remove(prod)
        return cantSinDescontar

    def objToJson(self):
        Data = {'CodigoDeposito' : self.id,
                'CapacidadMaxima':self.capacidad,
                'Stock':self.stock}
        return Data
    
    def eliminaritem(self,codigo):
         for prod in self.stock:
            if prod['item'] == codigo:
                self.stock.pop(prod)

    
    def listarDepostios(self):
        id=self.id
        capMaxi=self.capacidad
        capocupada=0
        for stk in self.stock:
            capocupada=capocupada + stk['cantidad']

        capDisponible = capMaxi-capocupada

        return print(f"ID: {id}  -  {capocupada} / {capMaxi} - Disponible {capDisponible}")
    
    def buscarProducto(self,codigo):
        for stk in self.stock:
            if stk['item'] == codigo:  
                print(f"Depisto {self.id} : {stk['cantidad']}")
    def DepositosporPeso(self,codigo,peso)->dict:
        for stk in self.stock:
            if stk['item'] == codigo:  
                data = {'Depisto': self.id ,
                        'Peso Total' : (peso*stk['cantidad'])}
                
                return data