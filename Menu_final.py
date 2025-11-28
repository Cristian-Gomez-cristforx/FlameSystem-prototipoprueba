import random
from Modulos_Gestiones.Gestion_Usuario import Usuario,verificar_correo
from Modulos_Gestiones.Gestion_Pedidos import Pedido,GestorPedidos
from Modulos_Gestiones.Inventario import Insumo,Bebida,Inventario,pedir_entero,pedir_float,menu_inventario
from Modulos_Gestiones.Reportes import Reportes

admin=Usuario("Felipe Dominguez","felipe@gmail.com","flamepipe7040","admin",1090350760,3134206754)
Usuario.usuarios_registrados.append(admin)
inventario = Inventario()
gestor= GestorPedidos()
def menu_mesero(permitir_cerrar_sesion=False,usuario_nombre=None):
                        Mensaje=f"--Bienvenido a su Menú de Mesero, Usuario {usuario_nombre}--" if usuario_nombre else "--Menú de Mesero--"
                        print(Mensaje)
                        while True:
                             manejar_mens_op = "4. Cerrar Sesión" if permitir_cerrar_sesion else "4. Salir del menú"
                             options = input(f"\n1. Registrar pedido\n2. Cancelar pedido\n3. Confirmar pago de pedido\n{manejar_mens_op}\nIngrese el número de la opción: ")
        
                             if options == "1":
                                cliente = input("Nombre del cliente: ")
                                total = pedir_entero("Total del pedido: ")
                                print("Tipo de entrega: 1.Mesa  2.Domicilio  3.Recoger")
                                tp = input("Seleccione tipo: ")
                                tipos = {"1": "Mesa", "2": "Domicilio", "3": "Recoger"}
                                tipo_entrega = tipos.get(tp, "Mesa")
                                pedido = gestor.registrar_pedido(cliente, total, tipo_entrega)
                                print("Pedido registrado:", pedido)
                             elif options=="2":
                                id_pedido=pedir_entero("ID del pedido a cancelar: ")
                                ok = gestor.cancelar_pedido(id_pedido)
                                print("Pedido cancelado." if ok else "Pedido no encontrado.")
                               
                             elif options=="3":
                                id_pedido=pedir_entero("ID del pedido a confirmar pago: ")
                                ok = gestor.confirmar_pago(id_pedido)
                                print("Pago confirmado." if ok else "Pedido no encontrado.")
                             elif options=="4":
                                 if permitir_cerrar_sesion:
                                   print("Cerrando sesión...")
                                   return True
                                 else:
                                    print("Saliendo del menú mesero.....")
                                    return False
                             else: 
                                print("Opción invalida. Por favor, intente de nuevo.")

while True:
        option=input("Presione Enter para Iniciar sesion ")
        usuario_deicidio_salir= False
        if option== "":
            intentos_de_inicio=0
            while True:
                
                actual_correo=input("Ingrese su correo electrónico: ")
                actual_contraseña=input("Ingrese su contraseña: ")
                admin.iniciar_sesion(actual_correo,actual_contraseña)  
                usuario_login= admin.iniciar_sesion(actual_correo,actual_contraseña)
                if usuario_login is None:
                   print("\nInicio de sesión fallido, algunos de los datos no coinciden")
                   intentos_de_inicio+=1
                   if intentos_de_inicio>=3:
                       print("\nHaz intentado inciar sesión 3 veces y has fallado")
                       elegir=input("\n¿Deseas Restablecer la contraseña?:\nsi/no: ")
                       if elegir.lower()=="si":
                           if admin.restablecer_contraseña():
                                break
                           
                       elif elegir.lower()=="no":
                           print("Ok,volviendo al menú incial...")
                           break
                       else:
                           print("Ingrese solo si o no")
                   continue
                if usuario_login.rol.lower()=="admin":
                    print(f"--Bienvenido a su Menú de {usuario_login.rol}, Usuario {usuario_login.nombre}--")
                    while True:
                        options=input("\n1.Registrar Usuarios\n2.Usar menú inventario\n3.Mostrar clientes\n4.Menú de mesero\n5.Cerrar sesión\nIngrese el numero de la opcion para usar: ")
                        if options== "1":
                           print("Ingrese los datos, para registar un Usuario: ")
                           nombr= input("Ingrese un nombre completo(con apellidos): ")
                           email_correo=verificar_correo("Ingrese un correo electrónico: ")
                           contra=input("Ingrese la contraseña que quiere asignar: ")
                           rol=input("Ingrese el tipo de Rol que le quiera asignar: ")
                           while True:
                                number_docu=pedir_entero("Ingrese un número de identificación: ")
                                for usuario in  Usuario.usuarios_registrados:
                                    if usuario.documento==number_docu:
                                       print(f"Este número de documento ya se ecnuentra asociado a una cuenta con rol:{usuario.rol}.\nIngrese otro")
                                       break
                                else:
                                    break
                           while True:
                                number_phone=pedir_entero("Ingrese un número de teléfono:")
                                numberphone_str=str(number_phone)
                                if len(numberphone_str)!=10:
                                    print("El número de teléfono debe contener 10 digitos. Ingrese de nuevo")
                                    continue
                                break
                           admin.registrar_usuario(nombr,email_correo,contra,rol,number_docu,number_phone)
                        elif options=="2":
                            if menu_inventario(inventario):
                                continue
                        elif options=="3":
                            contador=0
                            for usu in Usuario.usuarios_registrados:
                                contador+=1
                                print(f"\n--Usuario número: {contador}-{usu}--")
                        elif options=="4":
                             menu_mesero(permitir_cerrar_sesion=False,usuario_nombre=usuario_login.nombre)
                              
                        elif options=="5":
                            print("Cerrando sesión...")
                            usuario_deicidio_salir=True
                            break
                        
                            
                elif usuario_login.rol.lower()=="mesero":
                     if menu_mesero(permitir_cerrar_sesion=True, usuario_nombre=usuario_login.nombre):
                        usuario_deicidio_salir = True
                        break
                elif usuario_deicidio_salir:
                     break