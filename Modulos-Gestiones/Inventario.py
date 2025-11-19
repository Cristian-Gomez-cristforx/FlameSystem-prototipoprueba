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

    def registrar_producto(self, nombre, cantidad, precio, ingredientes):
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


def menu():
    inventario = Inventario()

    while True:
        print("""
========== MENÚ INVENTARIO ==========
1. Registrar producto
2. Actualizar cantidad de un producto
3. Mostrar inventario
4. Ver detalles de un producto
5. Salir
""")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            cantidad = int(input("Cantidad inicial: "))
            precio = float(input("Precio del producto: "))

            print("Ingrese los ingredientes (separados por coma):")
            ingredientes = input("→ ").split(",")
            ingredientes = [i.strip() for i in ingredientes]

            inventario.registrar_producto(nombre, cantidad, precio, ingredientes)

        elif opcion == "2":
            nombre = input("Nombre del producto a actualizar: ")
            nueva_cantidad = int(input("Nueva cantidad: "))
            inventario.actualizar_producto(nombre, nueva_cantidad)

        elif opcion == "3":
            inventario.mostrar_inventario()

        elif opcion == "4":
            nombre = input("Nombre del producto para ver detalles: ")
            inventario.detalles_producto(nombre)

        elif opcion == "5":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no valida.")



menu()