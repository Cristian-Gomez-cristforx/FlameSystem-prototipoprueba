# Clase Pedido
class Pedido:
    def __init__(self, id_pedido, cliente, total, tipo_entrega):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.items = []  # LISTA VACÍA
        self.total = total
        self.tipo_entrega = tipo_entrega
        self.estado = "Pendiente"
        self.pago_confirmado = False

    def confirmar_pago(self):
        self.pago_confirmado = True
        self.estado = "Pagado"

    def cancelar(self):
        self.estado = "Cancelado"

    def __str__(self):
        return (
            f"ID Pedido: {self.id_pedido}, Cliente: {self.cliente}, "
            f"Estado: {self.estado}, Pago confirmado: {self.pago_confirmado}, "
            f"Tipo entrega: {self.tipo_entrega}, Total: ${self.total}"
        )


# ----------------------------------------------------------------------
# Clase GestorPedidos
# ----------------------------------------------------------------------

class GestorPedidos:
    def __init__(self):
        self.pedidos = {}   
        self.id_actual = 1

    # Registrar pedido
    def registrar_pedido(self, cliente, total, tipo_entrega):
        pedido = Pedido(self.id_actual, cliente, total, tipo_entrega)
        self.pedidos[self.id_actual] = pedido
        self.id_actual += 1
        return pedido

    # Cancelar pedido
    def cancelar_pedido(self, id_pedido):
        pedido = self.pedidos.get(id_pedido)
        if pedido:
            pedido.cancelar()
            return pedido
        return None

    # Confirmar pago
    def confirmar_pago(self, id_pedido):
        pedido = self.pedidos.get(id_pedido)
        if pedido:
            pedido.confirmar_pago()
            return pedido
        return None

    # Listar pedidos
    def listar_pedidos(self):
        return self.pedidos.values()

    # Buscar pedido
    def buscar_pedido(self, id_pedido):
        return self.pedidos.get(id_pedido, None)


# ----------------------------------------------------------------------
# Consola                              
# ----------------------------------------------------------------------

def menu():
    gestor = GestorPedidos()

    while True:
        print("\n--- Menú de Pedidos ---")
        print("1. Registrar pedido")
        print("2. Cancelar pedido")
        print("3. Confirmar pago")
        print("4. Listar pedidos")
        print("5. Buscar pedido por ID")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cliente = input("Nombre del cliente: ")
            total = float(input("Total del pedido: $ "))

            # Tipo de entrega
            print("\nTipo de entrega:")
            print("1. Mesa")
            print("2. A domicilio")
            print("3. Recogida")
            tipo = input("Seleccione una opción: ")

            if tipo == "1":
                tipo_entrega = "Mesa"
            elif tipo == "2":
                tipo_entrega = "Domicilio"
            elif tipo == "3":
                tipo_entrega = "Recogida"
            else:
                print("Opción inválida. Se asignará: Mesa")
                tipo_entrega = "Mesa"

            pedido = gestor.registrar_pedido(cliente, total, tipo_entrega)
            print(f"\nPedido registrado con ID: {pedido.id_pedido}")

        elif opcion == "2":
            id_pedido = int(input("ID del pedido a cancelar: "))
            pedido = gestor.cancelar_pedido(id_pedido)
            if pedido:
                print("Pedido cancelado.")
            else:
                print("Pedido no encontrado.")

        elif opcion == "3":
            id_pedido = int(input("ID del pedido a confirmar pago: "))
            pedido = gestor.confirmar_pago(id_pedido)
            if pedido:
                print("Pago confirmado.")
            else:
                print("Pedido no encontrado.")

        elif opcion == "4":
            print("\n--- Lista de Pedidos ---")
            for pedido in gestor.listar_pedidos():
                print(pedido)

        elif opcion == "5":
            id_pedido = int(input("ID del pedido: "))
            pedido = gestor.buscar_pedido(id_pedido)
            if pedido:
                print(pedido)
            else:
                print("Pedido no encontrado.")

        elif opcion == "6":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")

menu()
