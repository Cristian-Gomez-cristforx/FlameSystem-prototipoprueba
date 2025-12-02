# Gestion_Pedidos.py
# Gestión de pedidos (modelo B: soporte de omisiones por unidad)
# Versión final: sin getattr/hasattr/@property, flujo de creación único, edición por tipo, un solo marcar_cocinado lógico.

from datetime import datetime

# -----------------------------
# Modelos
# -----------------------------
class LineaProducto:
    """
    producto: objeto Producto (desde inventario.productos)
    cantidad: int
    omitidos_por_unidad: dict { unit_index: set(ins_id, ...) }
    """
    def __init__(self, producto, cantidad, omitidos_por_unidad=None):
        self.producto = producto
        self.cantidad = cantidad
        self.omitidos_por_unidad = {}
        if omitidos_por_unidad:
            for k, v in omitidos_por_unidad.items():
                self.omitidos_por_unidad[int(k)] = set(v)

    def nombre(self):
        return self.producto.nombre

    def contar_omitidos_por_insumo(self):
        """Devuelve dict ins_id -> numero de unidades que omitieron ese insumo."""
        contador = {}
        for ins_set in self.omitidos_por_unidad.values():
            for ins_id in ins_set:
                contador[ins_id] = contador.get(ins_id, 0) + 1
        return contador

    def consumo_por_insumo_tras_omisiones(self):
        """
        Devuelve dict ins_id -> cantidad final que se debe consumir (teniendo en cuenta omisiones por unidad).
        Usa self.producto.ingredientes que debe ser { ins_id: qty_por_unidad }.
        """
        resultado = {}
        ingredientes = self.producto.ingredientes  # dict {ins_id: por_unidad}
        omitidos = self.contar_omitidos_por_insumo()  # ins_id -> unidades_omitidas
        for ins_id, por_unidad in ingredientes.items():
            omitted_units = omitidos.get(ins_id, 0)
            used_units = self.cantidad - omitted_units
            if used_units < 0:
                used_units = 0
            resultado[ins_id] = por_unidad * used_units
        return resultado

    def consumo_total_ignorando_omisiones(self):
        """Devuelve consumo por insumo si no existieran omisiones."""
        resultado = {}
        for ins_id, por_unidad in self.producto.ingredientes.items():
            resultado[ins_id] = por_unidad * self.cantidad
        return resultado

class LineaBebida:
    def __init__(self, bebida, cantidad):
        self.bebida = bebida
        self.cantidad = cantidad

class Pedido:
    def __init__(self, id_pedido, mesero, cliente="", tipo_pedido="mesa"):
        self.id_pedido = id_pedido
        self.mesero = mesero
        self.cliente = cliente or ""
        self.tipo_pedido = tipo_pedido  # "mesa", "domicilio", "recoger"
        self.estado = "EN_CONSTRUCCION"  # EN_CONSTRUCCION | EN_COLA | COCINADO | FINALIZADO | CANCELADO

        self.lineas_productos = []  # [LineaProducto,...]
        self.lineas_bebidas = []    # [LineaBebida,...]
        self.comentarios = ""

        self.pagado = False
        self.cocinado = False
        self.consumo_aplicado = False
        self.consumo_detallado = None  # {'insumos':{id:qty}, 'bebidas':{id:qty}, 'detalle_lineas':{...}}

        self.fecha_creacion = datetime.now()
        self.fecha_finalizacion = None

        self.total_venta = None
        self.total_costo_insumos = None

    def es_modificable(self):
        return (not self.cocinado) and (self.estado not in ("FINALIZADO", "CANCELADO"))

    def resumen(self):
        estado = self.estado
        if self.cocinado and self.pagado and self.consumo_aplicado:
            estado = "FINALIZADO"
        return f"[{self.id_pedido}] Mesero:{self.mesero} Cliente:{self.cliente or '-'} Tipo:{self.tipo_pedido} Estado:{estado}"

    def detalles(self):
        print("\n--- DETALLES PEDIDO ---")
        print(self.resumen())
        if self.lineas_productos:
            print("Productos:")
            for i, lp in enumerate(self.lineas_productos):
                print(f"  {i}) {lp.producto.nombre} x{lp.cantidad}")
                if lp.omitidos_por_unidad:
                    print("    Omitidos por unidad:")
                    for unit, ins in lp.omitidos_por_unidad.items():
                        print(f"      Unidad {unit}: {', '.join(str(x) for x in ins)}")
        else:
            print("Productos: (ninguno)")
        if self.lineas_bebidas:
            print("Bebidas:")
            for lb in self.lineas_bebidas:
                print(f"  - {lb.bebida.nombre} x{lb.cantidad}")
        if self.comentarios:
            print("Comentarios:")
            print(self.comentarios)
        if self.total_venta is not None:
            print(f"Total venta guardado: {self.total_venta:.2f}")
        if self.total_costo_insumos is not None:
            print(f"Total costo insumos guardado: {self.total_costo_insumos:.2f}")
        print("-----------------------\n")

# -----------------------------
# Gestor (lógica / API)
# -----------------------------
class GestorPedidos:
    def __init__(self, inventario):
        """
        inventario: instancia de Inventario (debe exponer: productos, insumos, bebidas)
        """
        self.inventario = inventario
        self.pedidos = {}        # id -> Pedido
        self.historial = {}      # id -> Pedido finalizado
        self.historial_orden = []
        self._next_id = 1

        # registros compactos para reportes: lista de dicts {pedido_id, fecha, insumos, bebidas, total_costo, total_venta}
        self.registros_consumo = []

    def _generar_id(self):
        nid = self._next_id
        self._next_id += 1
        return nid

    def obtener_pedido(self, pid):
        return self.pedidos.get(pid)

    # ------------- Creación / edición -------------
    def crear_pedido(self, mesero, cliente="", tipo_pedido="mesa"):
        pid = self._generar_id()
        p = Pedido(pid, mesero, cliente, tipo_pedido)
        self.pedidos[pid] = p
        return p

    def agregar_producto(self, pedido_id, producto_id, cantidad, omitidos_por_unidad=None):
        """
        Añade un producto a un pedido validando stock. omitidos_por_unidad: {unit_idx: [ins_id,...]}
        Devuelve True/False.
        """
        p = self.obtener_pedido(pedido_id)
        if not p or not p.es_modificable():
            return False
        if not self.inventario:
            return False
        prod = self.inventario.productos.get(producto_id)
        if not prod:
            return False
        if cantidad <= 0:
            return False

        # validar stock usando consumo con omisiones
        lp_temp = LineaProducto(prod, cantidad, omitidos_por_unidad)
        consumo_necesario = lp_temp.consumo_por_insumo_tras_omisiones()
        for iid, qty in consumo_necesario.items():
            ins = self.inventario.insumos.get(iid)
            if not ins or ins.cantidad < qty:
                return False

        lp = LineaProducto(prod, cantidad, omitidos_por_unidad)
        p.lineas_productos.append(lp)
        return True

    def agregar_bebida(self, pedido_id, bebida_id, cantidad):
        p = self.obtener_pedido(pedido_id)
        if not p or not p.es_modificable():
            return False
        if not self.inventario:
            return False
        bev = self.inventario.bebidas.get(bebida_id)
        if not bev:
            return False
        if cantidad <= 0 or bev.cantidad < cantidad:
            return False
        lb = LineaBebida(bev, cantidad)
        p.lineas_bebidas.append(lb)
        return True

    def confirmar_envio_cocina(self, pedido_id):
        p = self.obtener_pedido(pedido_id)
        if not p:
            return False
        p.estado = "EN_COLA"
        return True

    def cancelar_pedido(self, pedido_id):
        p = self.obtener_pedido(pedido_id)
        if not p:
            return False
        if p.cocinado:
            return False
        p.estado = "CANCELADO"
        return True

    def marcar_pagado(self, pedido_id):
        p = self.obtener_pedido(pedido_id)
        if not p or p.estado == "CANCELADO":
            return False
        p.pagado = True
        # intentar finalizar si ya está cocinado
        self._intentar_finalizar(p)
        return True

    # ---------------- marcar cocinado (no-interactivo: única lógica que aplica cambios) ----------------
    def marcar_cocinado_no_interactivo(self, pedido_id, omisiones_por_linea_unit):
        """
        omisiones_por_linea_unit: dict:
          { linea_idx: { unit_idx: [ins_id, ...], ... }, ... }
        """
        p = self.obtener_pedido(pedido_id)
        if not p:
            return False
        if p.estado == "CANCELADO" or p.cocinado:
            return False

        consumo_insumos = {}
        consumo_bebidas = {}
        detalle_lineas = {}

        # aplicar omisiones por unidad a cada línea y calcular consumo real
        for idx, lp in enumerate(p.lineas_productos):
            omit_map = {}
            if omisiones_por_linea_unit and idx in omisiones_por_linea_unit:
                for unit_idx, ins_list in omisiones_por_linea_unit[idx].items():
                    omit_map[int(unit_idx)] = set(ins_list)
            lp.omitidos_por_unidad = omit_map  # almacenar en la línea

            consumo_lp = lp.consumo_por_insumo_tras_omisiones()
            for iid, q in consumo_lp.items():
                consumo_insumos[iid] = consumo_insumos.get(iid, 0) + q

            detalle_lineas[idx] = {
                'producto_id': lp.producto.id,
                'cantidad_linea': lp.cantidad,
                'omitidos_por_unidad': {k: list(v) for k, v in lp.omitidos_por_unidad.items()}
            }

        # bebidas: asumimos servidas todas
        for lb in p.lineas_bebidas:
            consumo_bebidas[lb.bebida.id] = consumo_bebidas.get(lb.bebida.id, 0) + lb.cantidad

        p.consumo_detallado = {'insumos': consumo_insumos, 'bebidas': consumo_bebidas, 'detalle_lineas': detalle_lineas}
        p.cocinado = True
        p.estado = "COCINADO"

        # intentar finalizar (si ya está pagado)
        self._intentar_finalizar(p)
        return True

    # ---------------- marcar cocinado interactivo (wrapper UX) ----------------
    def marcar_cocinado_interactivo(self):
        """
        Interactivo: pregunta por cada línea y por cada unidad qué insumos omite,
        construye omisiones_por_linea_unit y llama a marcar_cocinado_no_interactivo.
        """
        try:
            pid = int(input("ID pedido a marcar como COCINADO: ").strip())
        except:
            print("ID inválido.")
            return
        p = self.obtener_pedido(pid)
        if not p:
            print("Pedido no encontrado.")
            return
        if p.estado == "CANCELADO":
            print("Pedido cancelado.")
            return
        if p.cocinado:
            print("Pedido ya marcado como cocinado.")
            return

        p.detalles()
        omisiones = {}
        for idx, lp in enumerate(p.lineas_productos):
            if lp.cantidad <= 0:
                continue
            print(f"\nLínea {idx} - {lp.producto.nombre} x{lp.cantidad}")
            om_map = {}
            for unit in range(lp.cantidad):
                entrada = input(f"Unidad {unit} - insumos a omitir (IDs separados por coma) o ENTER: ").strip()
                if entrada == "":
                    continue
                try:
                    ids = set(int(x.strip()) for x in entrada.split(",") if x.strip())
                except:
                    print("IDs inválidos para esta unidad. Se ignora."); continue
                if ids:
                    om_map[unit] = ids
            if om_map:
                omisiones[idx] = om_map

        confirma = input("Confirmar marcar como COCINADO y registrar consumos? (s/n): ").strip().lower()
        if confirma != "s":
            print("Operación cancelada.")
            return

        ok = self.marcar_cocinado_no_interactivo(pid, omisiones)
        print("Marcado como COCINADO." if ok else "No se pudo marcar como cocinado.")

    # ---------------- intentar finalizar ----------------
    def _intentar_finalizar(self, pedido):
        """
        Aplica el consumo al inventario y guarda registro compacto cuando
        pedido.cocinado and pedido.pagado and not pedido.consumo_aplicado.
        """
        if not (pedido and pedido.cocinado and pedido.pagado):
            return
        if pedido.consumo_aplicado:
            return

        consumo_insumos = {}
        consumo_bebidas = {}
        if pedido.consumo_detallado:
            consumo_insumos = dict(pedido.consumo_detallado.get('insumos', {}))
            consumo_bebidas = dict(pedido.consumo_detallado.get('bebidas', {}))
        else:
            # asumir todo si no definió cocinero
            for lp in pedido.lineas_productos:
                c = lp.consumo_total_ignorando_omisiones()
                for iid, q in c.items():
                    consumo_insumos[iid] = consumo_insumos.get(iid, 0) + q
            for lb in pedido.lineas_bebidas:
                consumo_bebidas[lb.bebida.id] = consumo_bebidas.get(lb.bebida.id, 0) + lb.cantidad

        # valora con precios actuales del inventario (insumos/bebidas)
        insumos_valorados = {}
        for iid, qty in consumo_insumos.items():
            ins = self.inventario.insumos.get(iid) if self.inventario else None
            unit_price = 0.0
            if ins:
                unit_price = float(ins.precio)
            total = qty * unit_price
            insumos_valorados[iid] = {'qty': qty, 'unit_price': unit_price, 'total': total}

        bebidas_valoradas = {}
        for bid, qty in consumo_bebidas.items():
            bev = self.inventario.bebidas.get(bid) if self.inventario else None
            unit_price = 0.0
            if bev:
                unit_price = float(bev.precio)
            total = qty * unit_price
            bebidas_valoradas[bid] = {'qty': qty, 'unit_price': unit_price, 'total': total}

        total_costo_insumos = sum(v['total'] for v in insumos_valorados.values()) + sum(v['total'] for v in bebidas_valoradas.values())

        # calcular total venta (según precio en inventario en el momento)
        total_venta = 0.0
        for lp in pedido.lineas_productos:
            prod = self.inventario.productos.get(lp.producto.id) if self.inventario else None
            if prod:
                total_venta += lp.cantidad * float(prod.precio)
        for lb in pedido.lineas_bebidas:
            bev = self.inventario.bebidas.get(lb.bebida.id) if self.inventario else None
            if bev:
                total_venta += lb.cantidad * float(bev.precio)

        # aplicar descuentos en inventario (evitar negativos)
        if self.inventario:
            for iid, qty in consumo_insumos.items():
                ins = self.inventario.insumos.get(iid)
                if ins:
                    ins.cantidad = max(0, ins.cantidad - qty)
            for bid, qty in consumo_bebidas.items():
                bev = self.inventario.bebidas.get(bid)
                if bev:
                    bev.cantidad = max(0, bev.cantidad - qty)

        # marcar finalizado y guardar registros
        pedido.consumo_aplicado = True
        pedido.estado = "FINALIZADO"
        pedido.fecha_finalizacion = datetime.now()
        pedido.total_venta = total_venta
        pedido.total_costo_insumos = total_costo_insumos

        pedido.consumo_detallado = pedido.consumo_detallado or {}
        pedido.consumo_detallado['insumos_valorados'] = insumos_valorados
        pedido.consumo_detallado['bebidas_valoradas'] = bebidas_valoradas

        self.historial[pedido.id_pedido] = pedido
        self.historial_orden.append(pedido.id_pedido)

        registro = {
            "pedido_id": pedido.id_pedido,
            "fecha": pedido.fecha_finalizacion,
            "insumos": insumos_valorados,
            "bebidas": bebidas_valoradas,
            "total_costo": total_costo_insumos,
            "total_venta": total_venta
        }
        self.registros_consumo.append(registro)

    # ---------- listados ----------
    def listar_pedidos_para_cocina(self):
        return [p for p in self.pedidos.values() if p.estado == "EN_COLA" and not p.cocinado and p.estado != "CANCELADO"]

    def listar_pedidos_activos(self):
        return [p for p in self.pedidos.values() if p.estado not in ("FINALIZADO", "CANCELADO")]

    def listar_pedidos_por_mesero(self, mesero_nombre):
        return [p for p in self.pedidos.values() if p.mesero.lower() == mesero_nombre.lower() and p.estado in ("EN_CONSTRUCCION", "EN_COLA")]

    def ver_historial(self):
        return [self.historial[pid] for pid in self.historial_orden]

    # ---------- auxiliares interactivos para probar ----------
    def _agregar_producto_interactivo(self, pedido):
        if not self.inventario:
            print("Inventario no disponible.")
            return
        entrada = input("ID o nombre del producto (c cancelar): ").strip()
        if entrada.lower() == 'c':
            return
        prod = None
        if entrada.isdigit():
            prod = self.inventario.productos.get(int(entrada))
        else:
            for p in self.inventario.productos.values():
                if p.nombre.strip().lower() == entrada.strip().lower():
                    prod = p; break
        if not prod:
            print("Producto no encontrado."); return
        try:
            cantidad = int(input("Cantidad: ").strip())
            if cantidad <= 0:
                print("Cantidad inválida."); return
        except:
            print("Cantidad inválida."); return

        # preguntar omisiones por unidad (opcional)
        omit_map = {}
        if input("¿Desea indicar omisiones por unidad? (s/n): ").strip().lower() == "s":
            for unit in range(cantidad):
                ent = input(f"Unidad {unit} - insumos a omitir (IDs separados por coma) o ENTER: ").strip()
                if not ent:
                    continue
                try:
                    ids = set(int(x.strip()) for x in ent.split(",") if x.strip())
                except:
                    print("Entrada inválida para unidad, se ignora."); continue
                if ids:
                    omit_map[unit] = ids

        # validar stock
        lp_temp = LineaProducto(prod, cantidad, omit_map)
        consumo_necesario = lp_temp.consumo_por_insumo_tras_omisiones()
        for iid, qty in consumo_necesario.items():
            ins_obj = self.inventario.insumos.get(iid)
            if not ins_obj or ins_obj.cantidad < qty:
                print(f"Insumo {iid} insuficiente. No se puede agregar."); return

        lp = LineaProducto(prod, cantidad, omit_map)
        pedido.lineas_productos.append(lp)
        print("Producto añadido.")

    def _agregar_bebida_interactivo(self, pedido):
        if not self.inventario:
            print("Inventario no disponible.")
            return
        entrada = input("ID o nombre bebida (c cancelar): ").strip()
        if entrada.lower() == 'c': return
        bev = None
        if entrada.isdigit():
            bev = self.inventario.bebidas.get(int(entrada))
        else:
            for b in self.inventario.bebidas.values():
                if b.nombre.strip().lower() == entrada.strip().lower():
                    bev = b; break
        if not bev:
            print("Bebida no encontrada."); return
        try:
            cantidad = int(input("Cantidad: ").strip())
            if cantidad <= 0:
                print("Cantidad inválida."); return
        except:
            print("Cantidad inválida."); return
        if bev.cantidad < cantidad:
            print("Stock insuficiente."); return
        lb = LineaBebida(bev, cantidad)
        pedido.lineas_bebidas.append(lb)
        print("Bebida añadida.")

# -----------------------------
# Menús de prueba integrados
# -----------------------------
def agregar_producto_interactivo_a_pedido(gestor, pedido_id):
    inv = gestor.inventario
    if not inv:
        print("Inventario no disponible.")
        return False

    while True:
        entrada = input("ID o NOMBRE del producto (o 'c' cancelar): ").strip()
        if entrada.lower() == 'c':
            return False

        prod = None
        if entrada.isdigit():
            prod = inv.productos.get(int(entrada))
        else:
            for p in inv.productos.values():
                if p.nombre.strip().lower() == entrada.strip().lower():
                    prod = p
                    break
        if not prod:
            print("Producto no encontrado. Intente de nuevo.")
            continue

        try:
            cantidad = int(input("Cantidad: ").strip())
            if cantidad <= 0:
                print("Cantidad inválida (>0)."); continue
        except:
            print("Cantidad inválida."); continue

        # preguntar omisiones por unidad (opcional)
        omit_map = {}
        if input("¿Indicar omisiones por unidad? (s/n): ").strip().lower() == 's':
            for unit in range(cantidad):
                ent = input(f"Unidad {unit} - IDs de insumos a omitir (coma separado) o ENTER: ").strip()
                if not ent:
                    continue
                try:
                    ids = set(int(x.strip()) for x in ent.split(",") if x.strip())
                except:
                    print("Entrada inválida para esta unidad. Se ignora."); continue
                if ids:
                    omit_map[unit] = ids

        # calcular consumo requerido teniendo en cuenta omisiones
        consumo_requerido = {}
        for ins_id, por_unidad in prod.ingredientes.items():
            omitted_units = 0
            for s in omit_map.values():
                if ins_id in s:
                    omitted_units += 1
            used_units = cantidad - omitted_units
            if used_units < 0:
                used_units = 0
            consumo_requerido[ins_id] = por_unidad * used_units

        # verificar faltantes
        faltantes = []
        for iid, needed in consumo_requerido.items():
            ins_obj = inv.insumos.get(iid)
            stock = ins_obj.cantidad if ins_obj else 0
            if stock < needed:
                falta = needed - stock
                nombre_ins = ins_obj.nombre if ins_obj else f"ID {iid}"
                faltantes.append((iid, nombre_ins, falta))

        if faltantes:
            print("\nNo se puede agregar el producto: faltan insumos:")
            for iid, nombre, falta in faltantes:
                print(f" - ID {iid} | {nombre} -> falta {falta}")
            print("Opciones: (r) cambiar cantidad / (i) intentar otro producto / (c) cancelar añadir")
            opt = input("Opción: ").strip().lower()
            if opt == 'r':
                continue
            elif opt == 'i':
                continue
            else:
                return False

        # todo ok -> usar API del gestor
        ok = gestor.agregar_producto(pedido_id, prod.id_producto, cantidad, omit_map if omit_map else None)
        if ok:
            print(f"Producto '{prod.nombre}' x{cantidad} añadido al pedido.")
            return True
        else:
            print("No se pudo añadir el producto (validación fallida). Intente de nuevo o cancele.")
            if input("Reintentar (s) / Salir (n): ").strip().lower() != 's':
                return False

def agregar_bebida_interactivo_a_pedido(gestor, pedido_id):
    inv = gestor.inventario
    if not inv:
        print("Inventario no disponible.")
        return False

    while True:
        entrada = input("ID de la bebida (o 'c' cancelar): ").strip()
        if entrada.lower() == 'c': return False
        if not entrada.isdigit():
            print("ID inválido. Ingrese el número.")
            continue
        bid = int(entrada)
        bev = inv.bebidas.get(bid)
        if not bev:
            print("Bebida no encontrada.")
            continue
        try:
            cantidad = int(input("Cantidad: ").strip())
            if cantidad <= 0:
                print("Cantidad inválida."); continue
        except:
            print("Cantidad inválida."); continue
        if bev.cantidad < cantidad:
            print(f"No hay stock suficiente. Stock actual: {bev.cantidad}")
            opt = input("Cambiar cantidad (c) / Cancelar añadir (x): ").strip().lower()
            if opt == 'c':
                continue
            else:
                return False
        ok = gestor.agregar_bebida(pedido_id, bid, cantidad)
        if ok:
            print(f"Bebida '{bev.nombre}' x{cantidad} añadida.")
            return True
        else:
            print("No se pudo añadir la bebida.")
            return False

def crear_pedido_interactivo(gestor, mesero_nombre):
    """
    Flujo único de creación: pide cliente/tipo, permite agregar productos/bebidas con validación,
    ver líneas, confirmar (envía a cocina) o cancelar (descarta borrador).
    """
    cliente = input("Nombre del cliente (opcional): ").strip()
    print("Tipos: 1) Mesa  2) Domicilio  3) Recoger")
    tipo_in = input("Seleccione tipo (1/2/3) [1]: ").strip() or "1"
    tipos_map = {"1": "mesa", "2": "domicilio", "3": "recoger"}
    tipo = tipos_map.get(tipo_in, "mesa")

    pedido = gestor.crear_pedido(mesero_nombre, cliente, tipo)
    pid = pedido.id_pedido
    print(f"\nSe creó borrador de pedido ID {pid}. Ahora puede agregar productos y bebidas.")

    while True:
        print("\n--- Construyendo pedido ---")
        print("A) Agregar producto")
        print("B) Agregar bebida")
        print("V) Ver líneas actuales")
        print("F) Finalizar y enviar a cocina")
        print("X) Cancelar creación (descartar borrador)")
        opt = input("Opción: ").strip().lower()
        if opt == 'a':
            agregar_producto_interactivo_a_pedido(gestor, pid)
        elif opt == 'b':
            agregar_bebida_interactivo_a_pedido(gestor, pid)
        elif opt == 'v':
            p = gestor.obtener_pedido(pid)
            if p:
                p.detalles()
            else:
                print("Pedido no encontrado (error).")
        elif opt == 'f':
            if not pedido.lineas_productos and not pedido.lineas_bebidas:
                if input("El pedido está vacío. ¿Desea enviarlo vacío? (s/n): ").strip().lower() != 's':
                    continue
            gestor.confirmar_envio_cocina(pid)
            print(f"Pedido {pid} confirmado y enviado a cocina (EN_COLA).")
            return pid
        elif opt == 'x':
            if input("Confirmar cancelar borrador? (s/n): ").strip().lower() == 's':
                try:
                    del gestor.pedidos[pid]
                except:
                    pass
                print("Borrador descartado.")
                return None
        else:
            print("Opción inválida. Use A/B/V/F/X.")

def listar_pedidos_por_tipo_interactivo(gestor, tipo):
    res = []
    for p in gestor.pedidos.values():
        if p.tipo_pedido == tipo and p.estado not in ("FINALIZADO", "CANCELADO"):
            res.append(p)
    return sorted(res, key=lambda x: x.id_pedido)

def buscar_y_editar_por_tipo_interactivo(gestor, mesero_nombre):
    print("Seleccione tipo para filtrar pedidos:")
    print("1) Mesa  2) Domicilio  3) Recoger")
    tipo_in = input("Tipo (1/2/3) [1]: ").strip() or "1"
    tipos_map = {"1": "mesa", "2": "domicilio", "3": "recoger"}
    tipo = tipos_map.get(tipo_in, "mesa")

    pedidos = listar_pedidos_por_tipo_interactivo(gestor, tipo)
    if not pedidos:
        print("No hay pedidos de ese tipo activos.")
        return

    print("\nPedidos disponibles:")
    for p in pedidos:
        print(f"ID {p.id_pedido} | Mesero: {p.mesero} | Cliente: {p.cliente or '-'} | Estado: {p.estado}")

    try:
        pid = int(input("Ingrese ID del pedido a seleccionar (o 0 para cancelar): ").strip())
    except:
        print("ID inválido."); return
    if pid == 0:
        return
    pedido = gestor.obtener_pedido(pid)
    if not pedido:
        print("Pedido no encontrado."); return
    if not pedido.es_modificable():
        print("Pedido no modificable (puede estar cocinado/finalizado/cancelado).")
        return

    while True:
        print(f"\n--- Editando Pedido {pid} ---")
        print("1) Añadir producto")
        print("2) Añadir bebida")
        print("3) Añadir comentario")
        print("4) Marcar pedido como PAGADO")
        print("5) Cancelar pedido")
        print("6) Ver detalles")
        print("0) Volver")
        op = input("Opción: ").strip()
        if op == "1":
            agregar_producto_interactivo_a_pedido(gestor, pid)
        elif op == "2":
            agregar_bebida_interactivo_a_pedido(gestor, pid)
        elif op == "3":
            c = input("Comentario a añadir: ").strip()
            if c:
                pedido.comentarios += ("\n" + c)
                print("Comentario añadido.")
        elif op == "4":
            ok = gestor.marcar_pagado(pid)
            print("Pedido marcado como PAGADO." if ok else "No se pudo marcar como pagado.")
        elif op == "5":
            ok = gestor.cancelar_pedido(pid)
            print("Pedido cancelado." if ok else "No se pudo cancelar (quizá ya está cocinado).")
            if ok:
                return
        elif op == "6":
            pedido.detalles()
        elif op == "0":
            return
        else:
            print("Opción inválida.")

def menu_mesero_prueba(gestor, nombre):
    while True:
        print(f"\n--- Menú Mesero (usuario: {nombre}) ---")
        print("1) Crear pedido (flujo completo)")
        print("2) Buscar y editar pedido por TIPO (mesa/recoger/domicilio)")
        print("3) Ver mis pedidos (en construcción / enviados)")
        print("4) Ver pedidos activos (todos)")
        print("5) Ver historial (finalizados)")
        print("0) Volver")
        opt = input("Opción: ").strip()
        if opt == "1":
            pid = crear_pedido_interactivo(gestor, nombre)
            if pid:
                print(f"Pedido creado y enviado (o en cola): ID {pid}")
            else:
                print("Creación cancelada o no se creó pedido.")
        elif opt == "2":
            buscar_y_editar_por_tipo_interactivo(gestor, nombre)
        elif opt == "3":
            ps = gestor.listar_pedidos_por_mesero(nombre)
            if not ps:
                print("No tienes pedidos en construcción o en cola.")
            else:
                print("Tus pedidos (borradores/en cola):")
                for p in sorted(ps, key=lambda x: x.id_pedido):
                    print(p.resumen())
                try:
                    sel = input("Ingrese ID para ver detalles o ENTER para volver: ").strip()
                    if sel:
                        pid = int(sel)
                        p = gestor.obtener_pedido(pid)
                        if p and p.mesero.lower() == nombre.lower():
                            p.detalles()
                        else:
                            print("Pedido no encontrado o no es tuyo.")
                except:
                    print("ID inválido.")
        elif opt == "4":
            activos = gestor.listar_pedidos_activos()
            if not activos:
                print("No hay pedidos activos.")
            else:
                for p in sorted(activos, key=lambda x: x.id_pedido):
                    print(p.resumen())
        elif opt == "5":
            hist = gestor.ver_historial()
            if not hist:
                print("No hay pedidos finalizados.")
            else:
                for p in hist:
                    print(f"{p.resumen()} -> {p.fecha_finalizacion}")
        elif opt == "0":
            return
        else:
            print("Opción inválida. Intente de nuevo.")

def menu_cocinero(gestor,usuario_login):
    print(f"--Bienvenido a su Menú de {usuario_login.rol}, Usuario {usuario_login.nombre}--")
    while True:
        print("\n--- Menú Cocinero ---")
        print("1) Ver pedidos para cocina")
        print("2) Marcar pedido como COCINADO (interactivo)")
        print("0) cerrar sesión")
        opt = input("Opción: ").strip()
        if opt == "1":
            cola = gestor.listar_pedidos_para_cocina()
            if not cola:
                print("No hay pedidos en cola.")
            else:
                for p in sorted(cola, key=lambda x: x.id_pedido):
                    print(p.resumen())
        elif opt == "2":
            gestor.marcar_cocinado_interactivo()
        elif opt == "0":
            return True
        else:
            print("Opción inválida.")

# ---------------------
# Permite ejecutar como archivo de pruebas
# ---------------------
if __name__ == "__main__":
    inv = None
    try:
        from Inventario import Inventario
        inv = Inventario()
        print("Inventario instanciado.")
    except Exception as e:
        print("No se pudo instanciar Inventario (se puede usar None para pruebas):", e)
        inv = None

    gestor = GestorPedidos(inv)
    print("Gestor creado. Entrando en menú de pruebas.")
    while True:
        print("\n=== MENÚ PRUEBAS ===")
        print("1) Menú Mesero")
        print("2) Menú Cocinero")
        print("0) Salir")
        o = input("Opción: ").strip()
        if o == "1":
            nombre = input("Nombre mesero (para pruebas): ").strip() or "mesero"
            menu_mesero_prueba(gestor, nombre)
        elif o == "2":
            menu_cocinero(gestor)
        elif o == "0":
            break
        else:
            print("Opción inválida.")
    print("Fin pruebas.")






