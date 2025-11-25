# FlameSystem-prototipo.
Proyecto para desarrollar las funcionalidades(solo backend prueba) del proyecto para Flameburg.co  

#  FlameSystem — Backend (Prototipo)

FlameSystem es el backend inicial del sistema POS de **FlameBurg**, diseñado para gestionar inventario, productos, ventas y otros módulos internos del restaurante.  
Este repositorio contiene una versión prototipo enfocada en pruebas y desarrollo.

---

## Características principales

- Gestión de productos e insumos  
- Actualización de cantidades  
- Manejo de menú y estructura del sistema POS  
- Código modular para expansión futura  
- Preparado para integrarse a un frontend o app POS

---
---

## Instalación y ejecución

### Clonar el repositorio  
```bash
git clone https://github.com/Cristian-Gomez-cristforx/FlameSystem-prototipoprueba.git
cd FlameSystem-prototipoprueba

## Historias de usuario
 1.Inventario
01 — Registrar insumos

Como administrador del restaurante
Quiero registrar nuevos insumos con nombre, cantidad y precio
Para mantener un control claro de los recursos disponibles.

Criterios de aceptación:

Se debe poder ingresar nombre, cantidad y precio.

Si falta un dato obligatorio → mostrar error.

El insumo se debe guardar en el inventario.

No se deben permitir insumos repetidos.

- Actualizar cantidad de insumos

Como encargado de inventario
Quiero modificar la cantidad existente de un insumo
Para mantener actualizado el stock real.

Criterios de aceptación:

Permite aumentar o disminuir cantidad.

No permite dejar stock negativo.

Muestra mensaje confirmando actualización.

HU-INV-003 — Mostrar inventario completo

Como usuario del sistema
Quiero ver un listado con todos los insumos y sus cantidades
Para conocer qué recursos hay disponibles.

Criterios de aceptación:

Mostrar nombre, cantidad y precio de cada insumo.

El listado debe ser legible.

Si no hay insumos → mostrar mensaje “Inventario vacío”.

HU-INV-004 — Descontar insumos usados en productos

Como sistema POS
Quiero descontar automáticamente los insumos usados cuando se vende un producto
Para mantener el inventario exacto.

Criterios de aceptación:

El descuento solo ocurre cuando la venta se confirma/paga.

No descuenta en pruebas o simulaciones.

Si no hay suficiente inventario → impedir la venta.

🍔 2. Gestión de Productos
HU-PRO-001 — Registrar productos

Como administrador
Quiero crear nuevos productos indicando ingredientes e insumos
Para ofrecerlos en el menú.

Criterios de aceptación:

Permite registrar nombre, precio, cantidad y lista de ingredientes.

Validar que los insumos existan en el inventario.

Producto no se registra si falta información.

HU-PRO-002 — Actualizar productos

Como administrador
Quiero editar el nombre, precio, cantidad o ingredientes de un producto
Para mantener actualizado el menú.

Criterios de aceptación:

No permite duplicar productos.

Permite modificar ingredientes.

Guarda cambios correctamente.

HU-PRO-003 — Mostrar productos existentes

Como usuario del sistema
Quiero ver una lista de los productos registrados
Para conocer la oferta disponible para ventas.

Criterios de aceptación:

Mostrar nombre, precio y disponibilidad.

Marcar productos sin inventario suficiente como “agotados”.

HU-PRO-004 — Calcular disponibilidad según inventario

Como vendedor
Quiero que el sistema muestre si un producto se puede vender según insumos disponibles
Para evitar ventas de productos sin ingredientes.

Criterios de aceptación:

Comprobar disponibilidad antes de permitir venta.

Mostrar razón si no se puede (ej: “Falta carne”).

💵 3. Ventas / POS
HU-VEN-001 — Registrar una venta

Como cajero
Quiero registrar una venta con uno o varios productos
Para llevar el control diario de ventas.

Criterios de aceptación:

Permite seleccionar productos y cantidades.

Valida inventario antes de confirmar.

Muestra total a pagar.

HU-VEN-002 — Confirmar/pagar la venta

Como cliente/cajero
Quiero que el sistema confirme el pago
Para completar la transacción.

Criterios de aceptación:

Después de pagar → descontar insumos.

Guardar datos de fecha, hora, total.

Generar número de venta.

HU-VEN-003 — Cancelar venta

Como cajero
Quiero poder cancelar una venta antes de pagar
Para corregir errores sin afectar inventario.

Criterios de aceptación:

No descuenta insumos.

Limpia los productos seleccionados.

📊 4. Reportes
HU-REP-001 — Reporte de ventas por día

Como administrador
Quiero ver las ventas del día con totales
Para evaluar rendimiento.

Criterios de aceptación:

Mostrar número de ventas.

Total vendido.

Productos más vendidos.

HU-REP-002 — Reporte de inventario crítico

Como administrador
Quiero ver los insumos con poca existencia
Para planear compras.

Criterios de aceptación:

Mostrar insumos cuya cantidad sea < umbral.

Debe permitir configurar el umbral.

🧑‍💻 5. Administración del sistema
HU-ADM-001 — Crear usuarios del sistema

Como administrador
Quiero registrar nuevos usuarios (cajeros, administradores)
Para controlar el acceso al sistema.

Criterios de aceptación:

Registrar nombre, usuario y contraseña.

Permitir roles.

Validar contraseñas seguras.

HU-ADM-002 — Iniciar sesión

Como usuario del sistema
Quiero iniciar sesión con un usuario y contraseña
Para acceder a mis herramientas.

Criterios de aceptación:

Mostrar error si las credenciales son incorrectas.

Redirigir según rol.



