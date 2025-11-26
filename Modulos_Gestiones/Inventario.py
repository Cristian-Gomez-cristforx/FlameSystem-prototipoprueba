class Insumo:
    def __init__(self, id_insumo, nombre, cantidad, precio):
        self.id_insumo = id_insumo
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.id_insumo} | {self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio}"


class Bebida(Insumo):
    def __init__(self, id_insumo, nombre, cantidad, precio, tipo_bebida, tamanio):
        super().__init__(id_insumo, nombre, cantidad, precio)
        self.tipo_bebida = tipo_bebida
        self.tamanio = tamanio

    def __str__(self):
        return (f"{self.id_insumo} | {self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio} | "
                f"Tipo: {self.tipo_bebida} | Tamaño: {self.tamanio}")


class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio, ingredientes_ids=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        # ingredientes_ids es una lista de IDs de insumos (enteros)
        self.ingredientes = ingredientes_ids if ingredientes_ids else []

    def actualizar_cantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def __str__(self):
        return f"{self.id_producto} | {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio}"


class Inventario:
    def __init__(self):
        # productos: id_producto -> Producto
        self.productos = {}
        self.id_producto_actual = 1
        # insumos: id_insumo -> Insumo o Bebida
        self.insumos = {}
        self.id_insumo_actual = 1
        # bebidas: id_insumo -> Bebida (apunta a los mismos objetos que insumos)
        self.bebidas = {}

    # registrar un insumo normal
    def registrar_insumo(self, nombre, cantidad, precio):
        nombre_normalizado = nombre.strip().lower()
        for insumo in self.insumos.values():
            if insumo.nombre.strip().lower() == nombre_normalizado:
                print(f"¡ERROR!: Ya existe un insumo registrado con el nombre: {nombre}.")
                return None

        nuevo_id = self.id_insumo_actual
        nuevo_insumo = Insumo(nuevo_id, nombre, cantidad, precio)
        self.insumos[nuevo_id] = nuevo_insumo
        self.id_insumo_actual += 1

        print(f"Insumo '{nombre}' registrado con ID: {nuevo_id}.")
        return nuevo_insumo

    # registrar bebida: se crea como Bebida y se guarda en insumos y bebidas
    def registrar_bebida(self, nombre, cantidad, precio):
        nombre_normalizado = nombre.strip().lower()
        for insumo in self.insumos.values():
            if insumo.nombre.strip().lower() == nombre_normalizado:
                print(f"¡ERROR!: Ya existe un insumo/bebida registrado con el nombre: {nombre}.")
                return None

        tipo = input("Tipo de bebida: ").strip()
        tamanio = input("Tamaño (350ml/600ml/etc): ").strip()

        nuevo_id = self.id_insumo_actual
        nueva_bebida = Bebida(nuevo_id, nombre, cantidad, precio, tipo, tamanio)
        self.insumos[nuevo_id] = nueva_bebida
        self.bebidas[nuevo_id] = nueva_bebida
        self.id_insumo_actual += 1

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
    def registrar_producto(self, nombre, cantidad, precio, ingredientes_ids):
        # Validar que exista cada ID
        faltantes = [ing for ing in ingredientes_ids if ing not in self.insumos]
        if faltantes:
            print("\nNo se puede crear el producto.")
            print("Faltan estos insumos (IDs):")
            for f in faltantes:
                print(f"- {f}")
            return None

        # validar que no exista producto con mismo nombre
        nombre_normalizado = nombre.strip().lower()
        for p in self.productos.values():
            if p.nombre.strip().lower() == nombre_normalizado:
                print("¡ERROR!: Este producto ya existe.")
                return None

        nuevo_id = self.id_producto_actual
        nuevo_producto = Producto(nuevo_id, nombre, cantidad, precio, ingredientes_ids.copy())
        self.productos[nuevo_id] = nuevo_producto
        self.id_producto_actual += 1

        print(f"Producto '{nombre}' registrado correctamente con ID: {nuevo_id}.")
        return nuevo_producto

    def actualizar_producto(self, nombre_o_id, nueva_cantidad):
        prod = self._buscar_producto_por_nombre_o_id(nombre_o_id)
        if not prod:
            print("El producto no existe.")
            return None
        prod.actualizar_cantidad(nueva_cantidad)
        print(f"Cantidad actualizada para '{prod.nombre}' (ID {prod.id_producto}).")
        return prod

    def mostrar_inventario(self):
        if not self.productos:
            print("Inventario vacío.")
            return
        print("\n--- Inventario Actual ---")
        for producto in self.productos.values():
            print(producto)

    def detalles_producto(self, nombre_o_id):
        prod = self._buscar_producto_por_nombre_o_id(nombre_o_id)
        if not prod:
            print("Ese producto no existe.")
            return

        print(f"\n--- Detalles de {prod.nombre} (ID {prod.id_producto}) ---")
        print(f"Cantidad disponible: {prod.cantidad}")
        print(f"Precio: ${prod.precio}")
        print("Ingredientes (ID - Nombre - Stock):")
        if not prod.ingredientes:
            print(" - (Sin ingredientes registrados)")
            return
        for ing_id in prod.ingredientes:
            ins = self.insumos.get(ing_id)
            if ins:
                print(f" - {ing_id} | {ins.nombre} | Cantidad disponible: {ins.cantidad}")
            else:
                print(f" - {ing_id} | (INSUMO NO ENCONTRADO)")

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


def pedir_entero(texto):
    while True:
        try:
            return int(input(texto))
        except ValueError:
            print("Error: ingrese un número entero válido.")


def pedir_float(texto):
    while True:
        try:
            return float(input(texto))
        except ValueError:
            print("Error: ingrese un número válido.")


# instancia global
inventario = Inventario()


def menu_inventario(inventario):
    while True:
        print("""
========== MENÚ INVENTARIO ==========
1. Registrar producto
2. Actualizar cantidad de un producto
3. Mostrar inventario
4. Ver detalles de un producto
5. Registrar insumo
6. Registrar bebida
7. Ver insumos
8. Ver bebidas
9. Salir
""")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nombre = input("Nombre del producto: ").strip()
            cantidad = pedir_entero("Cantidad inicial: ")
            precio = pedir_float("Precio del producto: ")

            if not inventario.insumos:
                print("ERROR: No hay insumos registrados. Regístrelos primero.")
                continue

            # Mostrar insumos con ID para que el usuario elija
            print("\n--- Insumos disponibles ---")
            for insumo_id, insumo in inventario.insumos.items():
                print(f"{insumo_id} - {insumo.nombre} (Cantidad: {insumo.cantidad})")

            ingredientes_ids = []
            while True:
                ing_id = pedir_entero("Agrega ID de insumo (o '0' para terminar): ")
                if ing_id == 0:
                    break
                if ing_id not in inventario.insumos:
                    print("ID inválido, intenta de nuevo.")
                    continue
                # evitar duplicados en la lista de ingredientes del producto
                if ing_id in ingredientes_ids:
                    print("Ese insumo ya fue agregado al producto.")
                    continue
                ingredientes_ids.append(ing_id)

            inventario.registrar_producto(nombre, cantidad, precio, ingredientes_ids)

        elif opcion == "2":
            identificador = input("Nombre o ID del producto a actualizar: ").strip()
            nueva_cantidad = pedir_entero("Nueva cantidad: ")
            inventario.actualizar_producto(identificador, nueva_cantidad)

        elif opcion == "3":
            inventario.mostrar_inventario()

        elif opcion == "4":
            identificador = input("Nombre o ID del producto: ").strip()
            inventario.detalles_producto(identificador)

        elif opcion == "5":
            nombre = input("Nombre del insumo: ").strip()
            cantidad = pedir_entero("Cantidad disponible: ")
            precio = pedir_float("Precio del insumo: ")
            inventario.registrar_insumo(nombre, cantidad, precio)

        elif opcion == "6":
            nombre = input("Nombre de la bebida: ").strip()
            cantidad = pedir_entero("Cantidad disponible: ")
            precio = pedir_float("Precio de la bebida: ")
            inventario.registrar_bebida(nombre, cantidad, precio)

        elif opcion == "7":
            inventario.mostrar_insumos()

        elif opcion == "8":
            inventario.mostrar_bebidas()

        elif opcion == "9":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Intente otra vez.")





