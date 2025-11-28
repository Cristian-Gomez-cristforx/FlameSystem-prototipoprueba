import random
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
        user=Usuario(name,email,password,rol,docu,phone)
        Usuario.usuarios_registrados.append(user)
        print(f"Usuario de tipo {user.rol} registrado con éxito")
        return

    def iniciar_sesion(self,correo_actual,contra_actual):
        for usuari in Usuario.usuarios_registrados:
            if usuari.correo == correo_actual and usuari.contraseña == contra_actual:
                return usuari
        return None
    def restablecer_contraseña(self):

        while True:   
            verificar_correo=input("\nIngrese la dirección de correo asociada a su cuenta: ")

            for cuenta in Usuario.usuarios_registrados:
                if  cuenta.correo == verificar_correo:
                    codigo_aleatorio = random.randint(100000,999999)
                    arroba_index = cuenta.correo.find("@")#la funcion find, me da la poscion del arroba, le paso como parametro, eso que debe buscar

                    nombre_usuario = cuenta.correo[:arroba_index]#usoun slicing,que empieza desde lo normal, hasta el indice que me da la función find, cuando devuelve el arroba.

                    caracteres_a_mostrar = 3 

                    largo_oculto = len(nombre_usuario) - caracteres_a_mostrar#Hago una resta para saber cuales son los carcateres que quedan para tapar con asteriscos

                    parte_oculta = "*" * largo_oculto

                    parte_visible = nombre_usuario[:caracteres_a_mostrar]

                    correo_enmascarado = parte_visible + parte_oculta + cuenta.correo[arroba_index:]
                    print(f"\nHemos enviado un codigo de 6 digitos a la dirección de correo: {correo_enmascarado}\n")
                    print(f"--FlameSystem--\n\nEste es tú codigo solicitado para cambio de contraseña: {codigo_aleatorio}")
                    while True:
                        
                        ingreso_codigo=pedir_entero("Ingrese el código:  ")
                        if codigo_aleatorio==ingreso_codigo:
                            contra_nueva=input("\nIngrese su nueva contraseña: ")
                            confirmar_contraseña=input("\nConfirme su contraseña, para estar seguro: ")
                            if contra_nueva==confirmar_contraseña:
                               cuenta.contraseña=contra_nueva
                               print("\nSu contraseña ha sido cambiada con éxito")
                               return True
                            else:
                              print("\nLas contraseñas no coinciden, vuelva a ingresar")
                        else:
                           print("\n¡Error!.El código ingresado es no coincide")
                        
                         
                else:
                    print("\nLa dirección de correo electronico ingresada, no esta asociada a una cuenta ")

    def __str__(self):
        return f"Usuario: {self.nombre}| \ncorreo: {self.correo}| \nContraseña: {self.contraseña}| \nRol: {self.rol}| \nCedula: {self.documento}| \nTelefono: {self.telefono}"
                

def pedir_entero(texto):
    while True:
        try:
            numero = int(input(texto))
            if numero < 0:
                print("Error: Ingrese un número entero positivo.")
                continue
            return numero
        except ValueError:
            print("Error: Ingrese un número entero válido.")
            
def verificar_correo(text):
    while True:
        corre=input(text)
        if "@" in corre and "com" in corre:
           for us in Usuario.usuarios_registrados:
               if us.correo==corre:
                  print(f"Lo sentimos este correo ya se encuentra asociado a uan cuenta con el rol: {us.rol}.\n Pruebe de neuvo con otro")
                  break
           else:#else del for, se ejcuta cuando el for termina sin un break, osea de manera natural, no se cumple el if, recorre todo y no entra al if
                return corre
        else:
            print("¡Error!.Ingrese un formato de correo electrónico válido")
            
       
    
if __name__=="__main__":
    admin=Usuario("Felipe Dominguez","felipe@gmail.com","flamepipe7040","admin",1090350760,3134206754)
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
                        options=input("\n1.Registrar Usuarios\n2.Registrar producto\n3.Mostrar clientes\n4.Cerrar Sesión\nIngrese el numero de la opcion para usar: ")
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
                            pass
                        elif options=="3":
                            contador=0
                            for usu in Usuario.usuarios_registrados:
                                contador+=1
                                print(f"\n--Usuario número: {contador}-{usu}--")
                            
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

