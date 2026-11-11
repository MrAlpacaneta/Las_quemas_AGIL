# APLICACIÓN - LAS QUEMAS (VERSIÓN 1.0)

import base_datos as bd

def limpiar_pantalla():
    print("\n" * 2)

def menu_principal():
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print("  SISTEMA ESPACIO DEPORTIVO LAS QUEMAS")
        print("=" * 50)
        print("--- RESERVAS ---")
        print("1. Registrar nueva reserva")
        print("2. Calendario de reservas")
        print("\n--- CANCHAS ---")
        print("3. Consultar todas las canchas")
        print("4. Agregar nueva cancha")
        print("5. Editar datos de cancha")
        print("6. Dar de baja/Inactivar cancha")
        print("\n0. Salir del sistema")
        print("=" * 50)
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_registrar_reserva()
        elif opcion == "2":
            menu_calendario_reservas()
        elif opcion == "3":
            menu_consultar_canchas()
        elif opcion == "4":
            menu_agregar_cancha()
        elif opcion == "5":
            menu_editar_cancha()
        elif opcion == "6":
            menu_baja_cancha()
        elif opcion == "0":
            print("\nCerrando el sistema...")
            break
        else:
            print("\n[Error] Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

def menu_consultar_canchas():
    print("\n--- LISTADO DE CANCHAS ---")
    canchas = bd.obtener_canchas()
    
    if len(canchas) == 0:
        print("No hay canchas registradas en el sistema.")
    else:
        print(f"{'N°':<5} | {'TIPO':<10} | {'PRECIO':<10} | {'ESTADO':<10}")
        print("-" * 45)
        for c in canchas:
            print(f"{c[0]:<5} | {c[1]:<10} | ${c[2]:<9} | {c[3]:<10}")
            
    input("\nPresione Enter para volver al menú...")

def menu_agregar_cancha():
    print("\n--- AGREGAR NUEVA CANCHA ---")
    tipo = input("Ingrese el tipo de cancha (Ej: Padel, Futbol): ")

    while True:
        try:
            precio = int(input("Ingrese el precio base de la cancha: "))
            break
        except ValueError:
            print("\n[Error] El precio debe ser un número entero. Intente nuevamente.")
    
    bd.agregar_cancha(tipo, precio)
    
    input("\nPresione Enter para volver al menú...")

def menu_editar_cancha():
    print("\n--- EDITAR DATOS DE CANCHA ---")
    try:
        numero = int(input("Ingrese el número de la cancha a editar: "))
        print("Ingrese los nuevos datos:")
        tipo = input("Nuevo tipo (Padel/Futbol): ")
        precio = int(input("Nuevo precio base: "))
        
        exito, mensaje = bd.actualizar_cancha(numero, tipo, precio)
        print(f"\nResultado: {mensaje}")
    except ValueError:
        print("\n[Error] Formato de número inválido.")
        
    input("\nPresione Enter para volver al menú...")

def menu_baja_cancha():
    print("\n--- DAR DE BAJA UNA CANCHA ---")
    try:
        numero = int(input("Ingrese el número de la cancha a dar de baja: "))
        exito, mensaje = bd.cambiar_estado_cancha(numero, "Inactiva")
        print(f"\nResultado: {mensaje}")
    except ValueError:
        print("\n[Error] Formato de número inválido.")
        
    input("\nPresione Enter para volver al menú...")

def menu_registrar_reserva():
    print("\n--- REGISTRAR NUEVA RESERVA ---")
    
    fecha = input("Fecha (DD/MM/AAAA): ")
    hora = input("Hora (HH:MM): ")
    
    try:
        cancha = int(input("Número de cancha: "))
        jugadores = input("Nombre del titular / Jugadores: ")
        precio = int(input("Precio total a cobrar: "))
        
        exito, mensaje = bd.guardar_reserva(fecha, hora, cancha, jugadores, precio)
        print(f"\nResultado: {mensaje}")
    except ValueError:
        print("\n[Error] La cancha y el precio deben ser valores numéricos.")
        
    input("\nPresione Enter para volver al menú...")

def menu_calendario_reservas():
    print("\n--- CALENDARIO DE RESERVAS ---")
    fecha_busqueda = input("Ingrese la fecha a consultar (DD/MM/AAAA): ")
    
    reservas = bd.consultar_calendario(fecha_busqueda)
    
    if len(reservas) == 0:
        print(f"\nNo hay reservas registradas para el día {fecha_busqueda}.")
    else:
        print(f"\nAgenda ocupada para el día: {fecha_busqueda}")
        # Formateo de tabla (Carolina - Tarea 1.1.2.1)
        print("-" * 65)
        print(f"{'HORA':<8} | {'N° CANCHA':<10} | {'TIPO':<10} | {'TITULAR/JUGADOR':<25}")
        print("-" * 65)
        
        for r in reservas:
            # r[0]=hora, r[1]=n_cancha, r[2]=tipo, r[3]=jugadores
            print(f"{r[0]:<8} | {r[1]:<10} | {r[2]:<10} | {r[3]:<25}")
            
        print("-" * 65)
        
    input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    menu_principal()