class Insumo:
    def __init__(self, id_insumo, nombre, cantidad, precio):
        self.id_insumo = id_insumo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.id_insumo} | {self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio}"


class Bebida(Insumo):
    def __init__(self, id_bebida, nombre, cantidad, precio, tipo_bebida, tamanio):
        super().__init__(id_bebida, nombre, cantidad, precio)
        self.tipo_bebida = tipo_bebida
        self.tamanio = tamanio

    def __str__(self):
        return (f"{self.id_insumo} | {self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio} | "
                f"Tipo: {self.tipo_bebida} | Tamaño: {self.tamanio}")


class Producto:
    def __init__(self, id_producto, nombre, precio, ingredientes_ids=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = ingredientes_ids if ingredientes_ids else {}
    

    def __str__(self):
        return f"{self.id_producto} | {self.nombre}  | Precio: ${self.precio}"


class Inventario:
    def __init__(self):
        
        self.productos = {}
        self.id_producto_actual = 1
        
        self.insumos = {}
        self.id_insumo_actual = 1
        
        self.bebidas = {}
        self.id_bebida_actual = 1

    # registrar un insumo normal
    def registrar_insumo(self, nombre, cantidad, precio):
        nombre_normaliza = nombre.strip().lower()
        for insumo in self.insumos.values():
            if insumo.nombre.strip().lower() == nombre_normaliza:
                print(f"¡ERROR!: Ya existe un insumo registrado con el nombre: {nombre}.")
                return None

        nuevo_id = self.id_insumo_actual
        nuevo_insumo = Insumo(nuevo_id, nombre, cantidad, precio)
        self.insumos[nuevo_id] = nuevo_insumo
        self.id_insumo_actual += 1

        print(f"Insumo '{nombre}' registrado con ID: {nuevo_id}.")
        return nuevo_insumo

   
    def registrar_bebida(self, nombre, cantidad, precio):
        nombre_normalizad = nombre.strip().lower()
        for bebida in self.bebidas.values():
            if bebida.nombre.strip().lower() == nombre_normalizad:
                print(f"¡ERROR!: Ya existe una bebida registrada con el nombre: {nombre}.")
                return None

        tipo = input("Tipo de bebida: ").strip()
        tamanio = input("Tamaño (350ml/600ml/etc): ").strip()

        nuevo_id = self.id_bebida_actual
        nueva_bebida = Bebida(nuevo_id, nombre, cantidad, precio, tipo, tamanio)
        self.bebidas[nuevo_id] = nueva_bebida
        self.id_bebida_actual += 1

        print(f"Bebida '{nombre}' registrada con ID: {nuevo_id}.")
        return nueva_bebida

    def mostrar_insumos(self):
        if not self.insumos:
            print("No hay insumos registrados.")
            return

        print("\n--- Insumos Disponibles ---")
        for insumo in self.insumos.values():
            print(insumo)

    def mostrar_bebidas(self):
        if not self.bebidas:
            print("No hay bebidas registradas.")
            return

        print("\n--- Bebidas Disponibles ---")
        for bebida in self.bebidas.values():
            print(bebida)

    # registrar producto con lista de IDs de insumos
    def registrar_producto(self, nombre, precio):
        ingredientes = {}
        nombre_normalizado = nombre.strip().lower()
        for producto in self.productos.values():
            if producto.nombre.strip().lower() == nombre_normalizado:
                print(f"¡ERROR!: Ya existe un producto registrado con el nombre: {nombre}.")
                return None
        

        print("\n--- Lista de Insumos Disponibles ---")
        for ins in self.insumos.values():
            print(ins)

        print("\nAgrega ingredientes al producto (por ID).")
        print("Si no quieres agregar más, escribe 0.\n")

        while True:
            try:
                ing_id = int(input("ID insumo: "))
                if ing_id == 0:
                    break
                if ing_id not in self.insumos:
                    print(" Ese insumo no existe.")
                    continue
                cantidad_usada = int(input("Cantidad  del insumo que usa este producto: "))
                ingredientes[ing_id] = cantidad_usada
            except ValueError:
                print("Ingrese un número válido.")
                continue

        nuevo = Producto(self.id_producto_actual, nombre, precio, ingredientes)
        self.productos[self.id_producto_actual] = nuevo

        print(f"\n✔ Producto '{nombre}' registrado con ID: {self.id_producto_actual}")
        self.id_producto_actual += 1

    def actualizar_precio_producto(self, nombre_o_id, nuevo_precio):
      # Buscar producto por nombre o por ID
        prod = self._buscar_producto_por_nombre_o_id(nombre_o_id)

        if not prod:
          print("El producto no existe.")
          return None

        prod.precio = nuevo_precio
        print(f"Precio actualizado para '{prod.nombre}' (ID {prod.id_producto}) → Nuevo precio: ${nuevo_precio}")
    
        return prod

    def mostrar_productos_y_detalles(self):
    
       if not self.productos:
          print("No hay productos registrados.")
          return

       print("\n--- Productos Registrados ---")
       for p in self.productos.values():
           print(p)   # asume que Producto.__str__ está bien definido

       entrada = input("\nIngrese NOMBRE o ID del producto para ver detalles (0 para cancelar): ").strip()
       if entrada == "" or entrada == "0":
          print("Operación cancelada.")
          return

       prod = self._buscar_producto_por_nombre_o_id(entrada)
       if not prod:
          print("Producto no encontrado.")
          return

       self.detalles_producto(prod.id_producto)

    def detalles_producto(self, id_producto):
    
       if id_producto not in self.productos:
          print("Ese producto no existe.")
          return

       p = self.productos[id_producto]

       print(f"\n--- Detalles de {p.nombre} ---")
       print(f"ID: {p.id_producto}")
       print(f"Precio: ${p.precio}")

       print("\nIngredientes:")
       if not p.ingredientes:
          print(" - Este producto no tiene ingredientes.")
          return

       for ing_id, cant in p.ingredientes.items():
    
           ins = self.insumos.get(ing_id, None)
           if ins:
              print(f" - {ins.nombre} (ID {ing_id}) -> Usa {cant} | Stock: {ins.cantidad}")
           else:
               print(f" - (INSUMO NO ENCONTRADO) (ID {ing_id}) -> Usa {cant}")
                

    # helper para buscar por nombre (string) o por id (si el usuario ingresa un número)
    def _buscar_producto_por_nombre_o_id(self, nombre_o_id):
        # si es un entero -> buscar por id
        try:
            pid = int(nombre_o_id)
            return self.productos.get(pid)
        except Exception:
            # buscar por nombre (case-insensitive)
            target = str(nombre_o_id).strip().lower()
            for p in self.productos.values():
                if p.nombre.strip().lower() == target:
                    return p
        return None
    

    def actualizar_cantidad_bebida(self):
        print("\n--- Actualizar Cantidad de Bebida ---")

        if not self.bebidas:
            print("No hay bebidas registradas.")
            return

        try:
            beb_id = int(input("ID de la bebida: "))
        except ValueError:
            print("ID inválido.")
            return

        if beb_id not in self.bebidas:
            print("Esa bebida no existe.")
            return

        beb = self.bebidas[beb_id]
        print(f"Bebida: {beb.nombre} | Cantidad actual: {beb.cantidad}")

        try:
            nueva_cantidad = int(input("Nueva cantidad: "))
        except ValueError:
            print("Cantidad inválida.")
            return

        beb.cantidad = nueva_cantidad
        print("✔ Cantidad actualizada correctamente.")



    def actualizar_cantidad_insumo(self):
        print("\n--- Actualizar Cantidad de Insumo ---")

        if not self.insumos:
            print("No hay insumos registrados.")
            return

        try:
            ins_id = int(input("ID del insumo: "))
        except ValueError:
            print("ID inválido.")
            return

        if ins_id not in self.insumos:
            print("Ese insumo no existe.")
            return

        ins = self.insumos[ins_id]
        print(f"Insumo: {ins.nombre} | Cantidad actual: {ins.cantidad}")

        try:
            nueva_cantidad = int(input("Nueva cantidad: "))
        except ValueError:
            print("Cantidad inválida.")
            return

        ins.cantidad = nueva_cantidad
        print("✔ Cantidad actualizada correctamente.")


def pedir_entero(texto):
    while True:
        try:
            numero = int(input(texto))
            if numero <=0:
                print("Error: Ingrese un número entero positivo.")
                continue
            return numero
        except ValueError:
            print("Error: Ingrese un número entero válido.")


def pedir_float(texto):
    while True:
        try:
            numero = float(input(texto))
            if numero <=0:
                print("Error: Ingrese un número positivo.")
                continue
            return numero
        except ValueError:
            print("Error: Ingrese un número decimal válido.")

# instancia global
inventario = Inventario()


def menu_inventario(inventario):
    while True:
        print("""
========== MENÚ INVENTARIO ==========
1. Registrar producto
2. Actualizar precio de un producto
3. Mostrar productos y ver detalles
4. Actualizar cantidad insumo
5. Actualizar cantidad bebida
6. Registrar Insumo
7. Registrar Bebida
8. Ver Insumos         
9. Ver bebidas
10. Salir
""")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            precio = pedir_float("Precio del producto: ")

            inventario.registrar_producto(nombre, precio)

        elif opcion == "2":
             identificador = input("Nombre o ID del producto a actualizar: ").strip()
             nuevo_precio = float(input("Nuevo precio: "))
             inventario.actualizar_precio_producto(identificador, nuevo_precio)

        elif opcion == "3":   
             inventario.mostrar_productos_y_detalles()

        elif opcion == "4":
             inventario.actualizar_cantidad_insumo()

        elif opcion == "5":
             inventario.actualizar_cantidad_bebida()

        elif opcion == "6":
            nombre = input("Nombre del insumo: ").strip()
            cantidad = pedir_entero("Cantidad disponible: ")
            precio = pedir_float("Precio del insumo: ")
            inventario.registrar_insumo(nombre, cantidad, precio)

            

        elif opcion == "7":
            nombre = input("Nombre de la bebida: ").strip()
            cantidad = pedir_entero("Cantidad disponible: ")
            precio = pedir_float("Precio de la bebida: ")
            inventario.registrar_bebida(nombre, cantidad, precio)
            

        elif opcion == "8":
             inventario.mostrar_insumos()

        elif opcion == "9":
             inventario.mostrar_bebidas()  
            
        elif opcion == "10":
             print("Saliendo del sistema...")
             break
        else:
            print("Opción no válida. Intente otra vez.")

menu_inventario(inventario)



