from datetime import datetime

# ================= CLASE PEDIDO =================
class Pedido:
    def __init__(self, id_pedido, cliente, total, tipo_entrega):
        self.id = id_pedido
        self.cliente = cliente
        
        # LISTA VACÍA
        self.items = []  

        self.total = total
        self.tipo_entrega = tipo_entrega
        self.estado = "creado"
        self.pagado = False
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def cancelar(self):
        self.estado = "cancelado"
        self.pagado = False

    def confirmar_pago(self):
        self.pagado = True
        self.estado = "pagado"

    def __str__(self):
        return (
            f"ID: {self.id} | Cliente: {self.cliente} | Total: {self.total} | "
            f"Entrega: {self.tipo_entrega} | Estado: {self.estado} | "
            f"Pagado: {self.pagado} | Fecha: {self.fecha}"
        )


# ================= GESTOR DE PEDIDOS =================
class GestorPedidos:
    def __init__(self):
        self.pedidos = {} 
        self.id_actual = 1

    def registrar_pedido(self, cliente, total, tipo_entrega):
        pedido = Pedido(self.id_actual, cliente, total, tipo_entrega)

        # Guardar en diccionario
        self.pedidos[self.id_actual] = pedido
        self.id_actual += 1

        return pedido

    def cancelar_pedido(self, id_pedido):
        pedido = self.pedidos.get(id_pedido)
        if pedido:
            pedido.cancelar()
            return pedido
        return None

    def confirmar_pago(self, id_pedido):
        pedido = self.pedidos.get(id_pedido)
        if pedido:
            pedido.confirmar_pago()
            return pedido
        return None

    def listar_pedidos(self):
        return self.pedidos.values()

    def buscar_pedido(self, id_pedido):
        return self.pedidos.get(id_pedido, None)


# ================= SISTEMA POR CONSOLA =================
class SistemaConsola:
    def __init__(self):
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

            # Registrar nuevo pedido
            if opcion == "1":
                cliente = input("Nombre del cliente: ")
                total = int(input("Valor total del pedido: "))

                print("\nTipo de entrega:")
                print("1. Mesa")
                print("2. Domicilio")
                print("3. Recogida")
                tipo = input("Seleccione opción: ")

                if tipo == "1":
                    tipo_entrega = "mesa"
                elif tipo == "2":
                    tipo_entrega = "domicilio"
                elif tipo == "3":
                    tipo_entrega = "recogida"
                else:
                    print("Opción no válida, se asignará 'mesa'.")
                    tipo_entrega = "mesa"

                pedido = self.gestor.registrar_pedido(cliente, total, tipo_entrega)
                print("Pedido registrado:", pedido)

            elif opcion == "2":
                id_pedido = int(input("ID del pedido a cancelar: "))
                resultado = self.gestor.cancelar_pedido(id_pedido)
                print("Resultado:", resultado if resultado else "Pedido no encontrado")

            elif opcion == "3":
                id_pedido = int(input("ID del pedido a confirmar pago: "))
                resultado = self.gestor.confirmar_pago(id_pedido)
                print("Resultado:", resultado if resultado else "Pedido no encontrado")

            elif opcion == "4":
                print("\n--- Lista de pedidos ---")
                for p in self.gestor.listar_pedidos():
                    print(p)

            elif opcion == "5":
                print("Saliendo del sistema...")
                break

            else:
                print("Opción no válida.")


# Ejecutar sistema
SistemaConsola().ejecutar()
