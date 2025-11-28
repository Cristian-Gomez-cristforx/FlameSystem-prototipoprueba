from datetime import datetime


class Pedido:
    def __init__(self, id_pedido, cliente, total, tipo_entrega):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.items = []  
        self.total = total
        self.tipo_entrega = tipo_entrega
        self.estado = "Pendiente"
        self.pago_confirmado = False
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def cancelar(self):
        self.estado = "Cancelado"
        self.pago_confirmado = False

    def confirmar_pago(self):
        self.pago_confirmado = True

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def __str__(self):
        return (f"ID Pedido: {self.id_pedido} | Cliente: {self.cliente} | Total: ${self.total} | "
                f"Tipo: {self.tipo_entrega} | Estado: {self.estado} | Pago: {self.pago_confirmado} | Fecha: {self.fecha}")


# ======================================================
#               CLASE GESTOR DE PEDIDOS
# ======================================================

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

    # Listar todos los pedidos
    def listar_pedidos(self):
        return self.pedidos.values()

    # Buscar por ID
    def buscar_pedido(self, id_pedido):
        return self.pedidos.get(id_pedido)

    # Pedidos pendientes para cocina
    def pedidos_para_cocinero(self):
        return [p for p in self.pedidos.values() if p.estado == "Pendiente"]

    # Actualizar estado del pedido
    def actualizar_estado_pedido(self, id_pedido, nuevo_estado):
        pedido = self.pedidos.get(id_pedido)
        if pedido:
            pedido.actualizar_estado(nuevo_estado)
            return pedido
        return None


# ======================================================
#                 MENÚ EN CONSOLA
# ======================================================
gestor=GestorPedidos()
if __name__ == "__main__":
    
    def mostrar_menu(self):
        
        print("\n=== SISTEMA DE PEDIDOS - Flameburg.co ===")
        print("1. Registrar pedido")
        print("2. Cancelar pedido")
        print("3. Confirmar pago")
        print("4. Listar pedidos")
        print("5. Buscar pedido por ID")
        print("6. Visualizar pedidos pendientes (Cocinero)")
        print("7. Actualizar estado de un pedido")
        print("8. Salir")
        while True:
            opcion=input("Seleccione una opción: ")



            # ---------------------------
            # Registrar pedido
            # ---------------------------
            if opcion == "1":
                cliente = input("Nombre del cliente: ")
                total = int(input("Total del pedido: "))

                print("Tipo de entrega:")
                print("1. Mesa")
                print("2. Domicilio")
                print("3. Recoger")

                tipo_op = input("Seleccione tipo: ")

                tipos = {
                    "1": "Mesa",
                    "2": "Domicilio",
                    "3": "Recoger"
                }

                tipo_entrega = tipos.get(tipo_op, "Mesa")

                pedido = gestor.registrar_pedido(cliente, total, tipo_entrega)
                print("Pedido registrado:", pedido)

            # ---------------------------
            # Cancelar pedido
            # ---------------------------
            elif opcion == "2":
                try:
                    id_pedido = int(input("ID del pedido a cancelar: "))
                except ValueError:
                    print("ID inválido.")
                    continue

                resultado = gestor.cancelar_pedido(id_pedido)
                print("Resultado:", resultado if resultado else "Pedido no encontrado")

            # ---------------------------
            # Confirmar pago
            # ---------------------------
            elif opcion == "3":
                try:
                    id_pedido = int(input("ID del pedido a confirmar pago: "))
                except ValueError:
                    print("ID inválido.")
                    continue

                resultado = gestor.confirmar_pago(id_pedido)
                print("Resultado:", resultado if resultado else "Pedido no encontrado")

            # ---------------------------
            # Listar pedidos
            # ---------------------------
            elif opcion == "4":
                print("\n--- Lista de pedidos ---")
                for p in gestor.listar_pedidos():
                    print(p)

            # ---------------------------
            # Buscar por ID
            # ---------------------------
            elif opcion == "5":
                try:
                    id_pedido = int(input("Ingrese el ID: "))
                except ValueError:
                    print("ID inválido.")
                    continue

                pedido = gestor.buscar_pedido(id_pedido)
                print(pedido if pedido else "Pedido no encontrado")

            # ---------------------------
            # Pedidos para cocinero
            # ---------------------------
            elif opcion == "6":
                print("\n--- Pedidos Pendientes ---")
                pedidos = gestor.pedidos_para_cocinero()

                if not pedidos:
                    print("No hay pedidos pendientes.")
                else:
                    for p in pedidos:
                        print(p)

            # ---------------------------
            # Actualizar estado
            # ---------------------------
            elif opcion == "7":
                try:
                    id_pedido = int(input("ID del pedido: "))
                except ValueError:
                    print("ID inválido.")
                    continue

                print("Nuevo estado:")
                print("1. En preparación")
                print("2. Listo para entregar")
                print("3. Entregado")

                est = input("Seleccione: ")

                estados = {
                    "1": "En preparación",
                    "2": "Listo para entregar",
                    "3": "Entregado"
                }

                nuevo_estado = estados.get(est)
                if not nuevo_estado:
                    print("Estado no válido.")
                    continue

                pedido = gestor.actualizar_estado_pedido(id_pedido, nuevo_estado)
                print(pedido if pedido else "Pedido no encontrado")

            # ---------------------------
            # Salir
            # ---------------------------
            elif opcion == "8":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida.")




