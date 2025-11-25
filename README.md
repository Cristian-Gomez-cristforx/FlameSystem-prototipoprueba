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

MÓDULO: INVENTARIO

1. Registrar Insumo
Como administrador, quiero registrar insumos con nombre, cantidad y precio para controlar los recursos del restaurante.

2. Actualizar Cantidad de Insumo
Como administrador, quiero aumentar o disminuir la cantidad de un insumo para mantener el inventario actualizado.

3. Eliminar Insumo
Como administrador, quiero eliminar un insumo que ya no uso para mantener limpio el inventario.

4. Registrar Producto
Como administrador, quiero registrar un producto con precio, cantidad y sus ingredientes para venderlo en el POS.

5. Actualizar Producto
Como administrador, quiero actualizar precio, stock o ingredientes de un producto para mantenerlo actualizado.

6. Eliminar Producto
Como administrador, quiero eliminar productos que ya no se venden para mantener la carta limpia.

7. Listar Insumos
Como usuario, quiero ver todos los insumos registrados para revisar el stock disponible.

8. Listar Productos
Como usuario, quiero ver todos los productos para conocer su disponibilidad.

9. Ver Detalles de Producto
Como administrador, quiero ver precio, stock e ingredientes del producto para gestionarlo fácilmente.

10. Alertas de Stock Bajo
Como administrador, quiero recibir alertas cuando un insumo esté bajo para poder reabastecer.



MÓDULO: VENTAS / POS

11. Iniciar Venta
Como cajero, quiero iniciar una venta para registrar el pedido de un cliente.

12. Agregar Productos
Como cajero, quiero agregar productos a una venta para construir el pedido del cliente.

13. Calcular Total Automático
Como cajero, quiero que el sistema calcule automáticamente subtotal, IVA y total para agilizar la venta.

14. Eliminar Ítems 
Como cajero, quiero eliminar productos para corregir errores del pedido.

15. Aplicar Descuentos
Como cajero, quiero aplicar cupones o descuentos manuales para promociones especiales.

16. Registrar Método de Pago
Como cajero, quiero registrar si la venta es en efectivo, tarjeta, Nequi o Daviplata.

17. Confirmar Venta y Generar Recibo
Como cajero, quiero completar la venta y que el sistema genere un recibo para el cliente.

18. Descontar Insumos al Pagar
Como sistema, quiero descontar los insumos usados únicamente cuando la venta se paga.

19. Cancelar Venta
Como cajero, quiero cancelar una venta antes de pagar si el cliente se arrepiente.



MÓDULO: USUARIOS Y ROLES

20. Registrar Usuario
Como administrador, quiero registrar usuarios para que puedan acceder al sistema.

21. Asignar Roles
Como administrador, quiero asignar roles como Cajero, Administrador o Cocinero para controlar permisos.

22. Login Seguro
Como usuario, quiero acceder con usuario y contraseña para entrar a mis funciones.

23. Recuperar Contraseña
Como usuario, quiero recuperar mi contraseña si la olvido para volver a iniciar sesión.

24. Ver Perfil
Como usuario, quiero ver mis datos para confirmar mi información.

25. Cerrar Sesión
Como usuario, quiero cerrar sesión para proteger mi cuenta.



MÓDULO: COCINA

26. Ver Pedidos Pendientes
Como cocinero, quiero ver las órdenes que están en preparación para empezar a cocinar.

27. Actualizar Estado del Pedido
Como cocinero, quiero marcar un pedido como "En preparación", "Listo" o "Entregado".

28. Ver Ingredientes por Pedido
Como cocinero, quiero saber los ingredientes necesarios para cada producto.



MÓDULO: REPORTES

29. Reporte de Ventas por Día
Como administrador, quiero ver cuánto vendí hoy para analizar ingresos diarios.

30. Reporte de Ventas por Mes
Como administrador, quiero ver ventas mensuales para evaluar el rendimiento del negocio.

31. Reporte de Productos Más Vendidos
Como administrador, quiero saber qué productos son más populares.

32. Reporte de Insumos Más Consumidos
Como administrador, quiero ver cuáles insumos se usan más para planear compras.

33. Exportar Reportes (PDF/Excel)
Como administrador, quiero exportar los reportes en PDF o Excel para revisarlos.



MÓDULO: CONFIGURACIÓN

34. Configurar Impuestos
Como administrador, quiero configurar el IVA aplicado a mis ventas.

35. Configurar Stock Mínimo
Como administrador, quiero ajustar el nivel que activa la alerta de insumo bajo.

36. Configurar Datos del Restaurante
Como administrador, quiero modificar nombre, NIT, dirección y teléfono para los recibos.



MÓDULO: CAJA

37. Apertura de Caja
Como cajero, quiero ingresar el monto inicial de la caja para iniciar el turno.

38. Cierre de Caja
Como cajero, quiero cerrar la caja al final del día y ver los totales generados.

39. Registrar Ingresos Extras
Como cajero, quiero registrar ingresos adicionales en caja (propinas, ajustes).

40. Registrar Egresos
Como cajero, quiero registrar pagos como domicilios o compras urgentes.

