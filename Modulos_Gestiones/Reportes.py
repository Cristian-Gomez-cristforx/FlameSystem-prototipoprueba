from datetime import datetime

class Reportes:
    def __init__(self, pedidos):
        # Recibe el diccionario de pedidos del sistema principal
        self.pedidos = pedidos

    # ----------------------------------------------------
    # LISTAR TODOS LOS PEDIDOS
    # ----------------------------------------------------
    def listar_pedidos(self):
        if not self.pedidos:
            print("\nNo hay pedidos registrados.")
            return

        print("\n========= LISTA DE PEDIDOS =========")
        for pedido_id, pedido in self.pedidos.items():
            print(f"ID: {pedido_id} | Cliente: {pedido['cliente']} | Estado: {pedido['estado']} | Total: {pedido['total']} COP | Fecha: {pedido['fecha']}")

    # ----------------------------------------------------
    # VER DETALLES COMPLETOS DE UN PEDIDO
    # ----------------------------------------------------
    def ver_detalles(self, pedido_id):
        if pedido_id not in self.pedidos:
            print("\nNo existe un pedido con ese ID.")
            return

        pedido = self.pedidos[pedido_id]

        print("\n========= DETALLES DEL PEDIDO =========")
        print(f"ID: {pedido_id}")
        print(f"Cliente: {pedido['cliente']}")
        print(f"Estado: {pedido['estado']}")
        print(f"Fecha: {pedido['fecha']}")
        print("Productos:")

        for i, prod in enumerate(pedido['productos'], start=1):
            print(f"  {i}. {prod['nombre']} x{prod['cantidad']} = {prod['subtotal']} COP")

        print(f"TOTAL: {pedido['total']} COP")
        print("======================================")

    # ----------------------------------------------------
    # BUSCAR PEDIDO POR ID (RETORNA EL PEDIDO)
    # ----------------------------------------------------
    def buscar_pedido_por_id(self, pedido_id):
        return self.pedidos.get(pedido_id, None)

    # ----------------------------------------------------
    # BUSQUEDA POR RANGO DE FECHAS
    # ----------------------------------------------------
    def buscar_por_fechas(self, fecha_inicio, fecha_fin):
        try:
            f_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            f_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            print("\nFormato incorrecto. Usa AAAA-MM-DD.")
            return

        print(f"\nBuscando pedidos entre {fecha_inicio} y {fecha_fin}...")
        encontrados = []

        for pedido_id, pedido in self.pedidos.items():
            fecha_pedido = datetime.strptime(pedido['fecha'], "%Y-%m-%d")
            if f_inicio <= fecha_pedido <= f_fin:
                encontrados.append((pedido_id, pedido))

        if not encontrados:
            print("No se encontraron pedidos en ese rango.")
            return

        print("\n===== RESULTADOS =====")
        for pid, p in encontrados:
            print(f"ID: {pid} | Cliente: {p['cliente']} | Total: {p['total']} COP | Fecha: {p['fecha']}")

    # ----------------------------------------------------
    # BUSCAR POR ESTADO (Pendiente, En proceso, Entregado...)
    # ----------------------------------------------------
    def buscar_por_estado(self, estado):
        print(f"\nBuscando pedidos con estado '{estado}'...")
        encontrados = [
            (pid, p) for pid, p in self.pedidos.items() if p['estado'].lower() == estado.lower()
        ]

        if not encontrados:
            print("No hay pedidos con ese estado.")
            return

        print("\n===== RESULTADOS =====")
        for pid, p in encontrados:
            print(f"ID: {pid} | Cliente: {p['cliente']} | Total: {p['total']} COP | Fecha: {p['fecha']}")


# ===================================================
#   MENÚ DE REPORTES
# ===================================================

def menu_reportes(reportes):
    while True:
        print("\n======= MENÚ DE REPORTES =======")
        print("1. Listar todos los pedidos")
        print("2. Ver detalles de un pedido por ID")
        print("3. Buscar pedido por ID")
        print("4. Buscar pedidos por rango de fechas")
        print("5. Buscar pedidos por estado")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            reportes.listar_pedidos()

        elif opcion == "2":
            pid = int(input("Ingrese ID del pedido: "))
            reportes.ver_detalles(pid)

        elif opcion == "3":
            pid = int(input("Ingrese ID del pedido: "))
            resultado = reportes.buscar_pedido_por_id(pid)
            if resultado:
                print("\nPedido encontrado:")
                print(resultado)
            else:
                print("No existe un pedido con ese ID.")

        elif opcion == "4":
            fi = input("Fecha inicio (AAAA-MM-DD): ")
            ff = input("Fecha fin (AAAA-MM-DD): ")
            reportes.buscar_por_fechas(fi, ff)

        elif opcion == "5":
            estado = input("Estado a buscar: ")
            reportes.buscar_por_estado(estado)

        elif opcion == "0":
            print("Volviendo...")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")
