class Usuario:
    usuarios_registrados= []
    def __init__(self,nombre,correo,contraseña,rol,documento,telefono):
        self.nombre= nombre
        self.correo= correo
        self.contraseña= contraseña
        self.rol= rol
        self.documento= documento
        self.telefono= telefono

    def registrar_usuario(self,name,email,password,rol,docu,phone):
        for usuario in Usuario.usuarios_registrados:
            if usuario.documento== docu and usuario.rol == rol:#Para que pueda un admin tener una cuenta para acceder a funcionalidades de pedidos, asi tener diferentes roles.
               print(f"Este usuario ya se encuentra registrado con el rol de: {usuario.rol}")
               return
        else:
            user=Usuario(name,email,password,rol,docu,phone)
            Usuario.usuarios_registrados.append(user)
            print(f"Usuario de tipo {user.rol} registrado con éxito")
            return

    def iniciar_sesion(self,correo_actual,contra_actual):
        for usuari in Usuario.usuarios_registrados:
            if usuari.correo == correo_actual and usuari.contraseña == contra_actual:
                return usuari
        return None
    def restablecer_contraseña():
        print("Hola olvidadizo")
        pass

    
if __name__=="__main__":
    admin=Usuario("Felipe Dominguez","felipe@gmail.com","flamepipe7040","Admin",1090350760,3134206754)
    Usuario.usuarios_registrados.append(admin)
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
                   print("Inicio de sesión fallido, algunos de los datos no coinciden")
                   intentos_de_inicio+=1
                   if intentos_de_inicio>=3:
                       print("Haz intentado inciar sesión 3 veces y has fallado")
                       elegir=input("¿Deseas Restablecer la contraseña?:\nsi/no: ")
                       if elegir.lower()=="si":
                           admin.restablecer_contraseña()
                       elif elegir.lower()=="no":
                           print("Ok,volviendo al menú incial...")
                           break
                       else:
                           print("Ingrese solo si o no")
                   continue
                if usuario_login.rol.lower()=="admin":
                    print(f"--Bienvenido a su Menú de {usuario_login.rol}, Usuario {usuario_login.nombre}--")
                    while True:
                        options=input("\n 1.Registrar Usuarios\n2.Registrar producto\n3.Registrar insumos\n4.Cerrar Sesión\nIngrese el numero de la opcion para usar: ")
                        if options== "1":
                           print("Ingrese los datos, para registar un Usuario: ")
                           nombr= input("Ingrese un nombre completo(con apellidos): ")
                           email_correo=input("Ingrese un correo electrónico: ")
                           contra=input("Ingrese la contraseña que quiere asignar: ")
                           rol=input("Ingrese el tipo de Rol que le quiera asignar")
                           number_docu=int(input("Ingrese un número de identificación: "))
                           number_phone=int(input("Ingrese un número de teléfono:"))
                           admin.registrar_usuario(nombr,email_correo,contra,rol,number_docu,number_phone)
                        elif options=="2":
                            pass
                        elif options=="3":
                            pass
                        elif options=="4":
                            print("Cerrando sesión...")
                            usuario_deicidio_salir=True
                            break
                        
                            
                elif usuario_login.rol.lower()=="mesero":
                    print(f"--Bienvenido a su Menú de {usuario_login.rol}, Usuario {usuario_login.nombre}--")
                    while True:
                        options=input("\n1.Registrar pedido\n2.Cancelar pedido\n3.Confirmar pago de pedido\n4.Cerrar Sesión\nIngrese el numero de la opcion para usar: ")
                        if options== "1":
                          pass
                        elif options=="2":
                            pass
                        elif options=="3":
                            pass
                        elif options=="4":
                            print("Cerrando sesión...")
                            usuario_deicidio_salir=True
                            break
                if usuario_deicidio_salir:
                    break

