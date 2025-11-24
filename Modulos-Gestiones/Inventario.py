class Insumo:
    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio}"


class Bebida(Insumo):
    def __init__(self, nombre, cantidad, precio, tipo_bebida, tamanio):
        super().__init__(nombre, cantidad, precio)
        self.tipo_bebida = tipo_bebida
        self.tamanio = tamanio

    def __str__(self):
        return (f"{self.nombre} | Cantidad: {self.cantidad} | Precio: {self.precio} | "
                f"Tipo: {self.tipo_bebida} | Tamaño: {self.tamanio}")


class Producto:
    def __init__(self, nombre, cantidad, precio, ingredientes=None):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.ingredientes = ingredientes if ingredientes else []

    def actualizar_cantidad(self, nueva_cantidad):
        self.cantidad = nueva_cantidad

    def __str__(self):
        return f"{self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio}"


class Inventario:
    def __init__(self):
        self.productos = {}
        self.insumos = {}
        self.bebidas = {}

    def registrar_insumo(self, nombre, cantidad, precio):
        if nombre in self.insumos:
            print("Este insumo ya existe.")
            return

        self.insumos[nombre] = Insumo(nombre, cantidad, precio)
        print(f"Insumo '{nombre}' registrado correctamente.")

    def registrar_bebida(self, nombre, cantidad, precio):
        if nombre in self.bebidas:
            print("Esta bebida ya existe.")
            return

        tipo = input("Tipo de bebida: ")
        tamanio = input("Tamaño (350ml/600ml/etc): ")

        self.bebidas[nombre] = Bebida(nombre, cantidad, precio, tipo, tamanio)
        print(f"Bebida '{nombre}' registrada correctamente.")

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

    def registrar_producto(self, nombre, cantidad, precio, ingredientes):

        faltantes = []
        for ing in ingredientes:
            if ing not in self.insumos:
                faltantes.append(ing)

        if faltantes:
            print("\nNo se puede crear el producto.")
            print("Faltan estos insumos:")
            for f in faltantes:
                print(f"- {f}")
            return

        if nombre in self.productos:
            print("Este producto ya existe.")
            return

        self.productos[nombre] = Producto(nombre, cantidad, precio, ingredientes)
        print(f"Producto '{nombre}' registrado correctamente.")

    def actualizar_producto(self, nombre, nueva_cantidad):
        if nombre not in self.productos:
            print("El producto no existe.")
            return

        self.productos[nombre].actualizar_cantidad(nueva_cantidad)
        print(f"Cantidad actualizada para '{nombre}'.")

    def mostrar_inventario(self):
        if not self.productos:
            print("Inventario vacío.")
            return
        
        print("\n--- Inventario Actual ---")
        for producto in self.productos.values():
            print(producto)

    def detalles_producto(self, nombre):
        if nombre not in self.productos:
            print("Ese producto no existe.")
            return
        
        producto = self.productos[nombre]
        print(f"\n--- Detalles de {producto.nombre} ---")
        print(f"Cantidad disponible: {producto.cantidad}")
        print(f"Precio: ${producto.precio}")
        print("Ingredientes:")
        for ing in producto.ingredientes:
            print(f" - {ing}")


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


def menu():
    inventario = Inventario()

    while True:
        print("""
========== MENÚ INVENTARIO ==========
1. Registrar producto
2. Actualizar cantidad de un producto
3. Mostrar inventario
4. Ver detalles de un producto
5. Registrar insumo
6. Registrar bebida (herencia)
7. Ver insumos
8. Ver bebidas
9. Salir
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            cantidad = pedir_entero("Cantidad inicial: ")
            precio = pedir_float("Precio del producto: ")

            print("Ingrese los ingredientes separados por coma:")
            ingredientes = [i.strip() for i in input("→ ").split(",")]

            inventario.registrar_producto(nombre, cantidad, precio, ingredientes)

        elif opcion == "2":
            nombre = input("Nombre del producto: ")
            nueva_cantidad = pedir_entero("Nueva cantidad: ")
            inventario.actualizar_producto(nombre, nueva_cantidad)

        elif opcion == "3":
            inventario.mostrar_inventario()

        elif opcion == "4":
            nombre = input("Nombre del producto: ")
            inventario.detalles_producto(nombre)

        elif opcion == "5":
            nombre = input("Nombre del insumo: ")
            cantidad = pedir_entero("Cantidad disponible: ")
            precio = pedir_entero("Precio del insumo: ")
            inventario.registrar_insumo(nombre, cantidad, precio)

        elif opcion == "6":
            nombre = input("Nombre de la bebida: ")
            cantidad = pedir_entero("Cantidad disponible: ")
            precio = pedir_entero("Precio de la bebida: ")
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


menu()



