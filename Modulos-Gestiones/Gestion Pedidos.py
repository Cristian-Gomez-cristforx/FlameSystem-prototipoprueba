from datetime import datetime

#  CLASE PEDIDO
class Pedido:
    def _init_(self, id_pedido, cliente, items, total):
        self.id = id_pedido
        self.cliente = cliente
        self.items = items
        self.total = total
        self.estado = "creado"
        self.pagado = False
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def cancelar(self):
        self.estado = "cancelado"
        self.pagado = False

    def confirmar_pago(self):
        self.pagado = True
        self.estado = "pagado"

    def _str_(self):
        return f"ID: {self.id} | Cliente: {self.cliente} | Total: {self.total} | Estado: {self.estado} | Pagado: {self.pagado} | Fecha: {self.fecha}"


#  CLASE GESTOR DE PEDIDOS
class GestorPedidos:
    def _init_(self):
        self.pedidos = []
        self.id_actual = 1

    def registrar_pedido(self, cliente, items, total):
        pedido = Pedido(self.id_actual, cliente, items, total)
        self.pedidos.append(pedido)
        self.id_actual += 1
        return pedido

    def cancelar_pedido(self, id_pedido):
        pedido = self.buscar_pedido(id_pedido)
        if pedido:
            pedido.cancelar()
            return pedido
        return None

    def confirmar_pago(self, id_pedido):
        pedido = self.buscar_pedido(id_pedido)
        if pedido:
            pedido.confirmar_pago()
            return pedido
        return None

    def listar_pedidos(self):
        return self.pedidos

    def buscar_pedido(self, id_pedido):
        for pedido in self.pedidos:
            if pedido.id == id_pedido:
                return pedido
        return None


#  MENÚ DE CONSOLA
class SistemaConsola:
    def _init_(self):
        self.gestor = GestorPedidos()

    def mostrar_menu(self):
        print("\n=== GESTIÓN DE PEDIDOS (Flameburg.co) ===")
        print("1. Registrar pedido")
        print("2. Cancelar pedido")
        print("3. Confirmar pago")
        print("4. Visualizar pedidos")
        print("5. Salir")
        return input("Seleccione una opción: ")

    def ejecutar(self):
        while True:
            opcion = self.mostrar_menu()

            # Registrar pedido
            if opcion == "1":
                cliente = input("Nombre del cliente: ")
                items = input("Items (separados por coma): ").split(",")
                total = int(input("Valor total del pedido: "))
                pedido = self.gestor.registrar_pedido(cliente, items, total)
                print("Pedido registrado:", pedido)

            # Cancelar pedido
            elif opcion == "2":
                id_pedido = int(input("ID del pedido a cancelar: "))
                resultado = self.gestor.cancelar_pedido(id_pedido)
                print("Resultado:", resultado if resultado else "Pedido no encontrado")

            # Confirmar pago
            elif opcion == "3":
                id_pedido = int(input("ID del pedido a confirmar pago: "))
                resultado = self.gestor.confirmar_pago(id_pedido)
                print("Resultado:", resultado if resultado else "Pedido no encontrado")

            # Listar pedidos
            elif opcion == "4":
                print("\n--- Lista de pedidos ---")
                for p in self.gestor.listar_pedidos():
                    print(p)

            # Salir
            elif opcion == "5":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida.")

SistemaConsola().ejecutar()
