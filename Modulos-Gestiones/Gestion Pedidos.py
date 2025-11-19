from datetime import datetime

# "Base de datos" temporal en memoria
pedidos = []
id_actual = 1

# FUNCIÓN: Registrar un pedido
def registrar_pedido(cliente, items, total):
    """
    Crea un nuevo pedido y lo guarda en memoria.
    """
    global id_actual

    pedido = {
        "id": id_actual,
        "cliente": cliente,
        "items": items,
        "total": total,
        "estado": "creado",        # estado inicial
        "pagado": False,           # pago aún no confirmado
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    pedidos.append(pedido)
    id_actual += 1

    return pedido

# FUNCIÓN: Cancelar un pedido por ID
def cancelar_pedido(id_pedido):
    """
    Cambia el estado del pedido a 'cancelado' si existe.
    """
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            pedido["estado"] = "cancelado"
            pedido["pagado"] = False
            return pedido

    return None

# FUNCIÓN: Confirmar pago de un pedido
def confirmar_pago(id_pedido):
    """
    Marca un pedido como pagado y cambia su estado.
    """
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            pedido["pagado"] = True
            pedido["estado"] = "pagado"
            return pedido

    return None

# FUNCIÓN: Listar todos los pedidos
def listar_pedidos():
    """
    Devuelve la lista completa de pedidos registrados.
    """
    return pedidos

# MENÚ DE CONSOLA
def mostrar_menu():
    print("\n=== GESTIÓN DE PEDIDOS (Flameburg.co) ===")
    print("1. Registrar pedido")
    print("2. Cancelar pedido")
    print("3. Confirmar pago")
    print("4. Visualizar pedidos")
    print("5. Salir")
    return input("Seleccione una opción: ")

# SISTEMA DE CONSOLA
def ejecutar_consola():
    while True:
        opcion = mostrar_menu()

        # Registrar pedido
        if opcion == "1":
            cliente = input("Nombre del cliente: ")
            items = input("Items (separados por coma): ").split(",")
            total = int(input("Valor total del pedido: "))
            pedido = registrar_pedido(cliente, items, total)
            print("Pedido registrado:", pedido)

        # Cancelar pedido
        elif opcion == "2":
            id_pedido = int(input("ID del pedido a cancelar: "))
            resultado = cancelar_pedido(id_pedido)
            print("Resultado:", resultado if resultado else "Pedido no encontrado")

        # Confirmar pago
        elif opcion == "3":
            id_pedido = int(input("ID del pedido a confirmar pago: "))
            resultado = confirmar_pago(id_pedido)
            print("Resultado:", resultado if resultado else "Pedido no encontrado")

        # Listar pedidos
        elif opcion == "4":
            print("\n--- Lista de pedidos ---")
            for p in listar_pedidos():
                print(p)

        # Salir
        elif opcion == "5":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    ejecutar_consola()
