# ==========================================
# APLICACIÓN PRINCIPAL - LAS QUEMAS (VERSIÓN TERMINAL)
# Desarrollado en Python para consola
# ==========================================

import base_datos as bd

def limpiar_pantalla():
    """Imprime saltos de línea para simular que se limpia la consola (Kevin)"""
    print("\n" * 2)

def menu_principal():
    """Diseño del menú principal interactivo (Tarea de Kevin)"""
    while True:
        limpiar_pantalla()
        print("=" * 50)
        print("  SISTEMA ESPACIO DEPORTIVO LAS QUEMAS - SPRINT 1")
        print("=" * 50)
        print("--- MÓDULO RESERVAS ---")
        print("1. Registrar nueva reserva (HU 1.1.1)")
        print("2. Consultar calendario de reservas (HU 1.1.2) [Próximamente]")
        print("\n--- MÓDULO CANCHAS (CRUD) ---")
        print("3. Consultar todas las canchas (HU 1.3.3)")
        print("4. Agregar nueva cancha (HU 1.3.1)")
        print("5. Editar datos de cancha (HU 1.3.2)")
        print("6. Dar de baja/Inactivar cancha (HU 1.3.4)")
        print("\n0. Salir del sistema")
        print("=" * 50)
        
        opcion = input("Seleccione una opción: ")

        # LÓGICA DE NAVEGACIÓN (Bruno)
        if opcion == "1":
            menu_registrar_reserva()
        elif opcion == "2":
            print("\n[!] Módulo en desarrollo para la próxima sesión.")
            input("Presione Enter para volver...")
        elif opcion == "3":
            menu_consultar_canchas()
        elif opcion == "4":
            menu_agregar_cancha()
        elif opcion == "5":
            menu_editar_cancha()
        elif opcion == "6":
            menu_baja_cancha()
        elif opcion == "0":
            print("\nCerrando el sistema... ¡Hasta pronto!")
            break
        else:
            print("\n[Error] Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

# ==========================================
# FUNCIONES DE INTERFAZ Y LÓGICA
# ==========================================

def menu_consultar_canchas():
    """Muestra los datos en formato de tabla de texto (Tarea de Carolina)"""
    print("\n--- LISTADO DE CANCHAS ---")
    canchas = bd.obtener_canchas()
    
    if len(canchas) == 0:
        print("No hay canchas registradas o no hay conexión a la base de datos.")
    else:
        # Formateo básico para que parezca una tabla
        print(f"{'N°':<5} | {'TIPO':<10} | {'PRECIO':<10} | {'ESTADO':<10}")
        print("-" * 45)
        for c in canchas:
            print(f"{c[0]:<5} | {c[1]:<10} | ${c[2]:<9} | {c[3]:<10}")
            
    input("\nPresione Enter para volver al menú...")

def menu_agregar_cancha():
    """Captura de datos y validación básica para nueva cancha (Bruno y Kevin)"""
    print("\n--- AGREGAR NUEVA CANCHA ---")
    try:
        numero = int(input("Ingrese el número de la cancha: "))
        tipo = input("Ingrese el tipo (Padel/Futbol): ")
        precio = int(input("Ingrese el precio base: "))
        
        # Llamamos al motor de base de datos
        exito, mensaje = bd.agregar_cancha(numero, tipo, precio)
        print(f"\nResultado: {mensaje}")
        
    except ValueError:
        print("\n[Error] El número de cancha y el precio deben ser valores numéricos.")
        
    input("\nPresione Enter para volver al menú...")

def menu_editar_cancha():
    """Captura datos para modificar una cancha existente"""
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
    """Borrado lógico de una cancha"""
    print("\n--- DAR DE BAJA UNA CANCHA ---")
    try:
        numero = int(input("Ingrese el número de la cancha a dar de baja: "))
        exito, mensaje = bd.cambiar_estado_cancha(numero, "Inactiva")
        print(f"\nResultado: {mensaje}")
    except ValueError:
        print("\n[Error] Formato de número inválido.")
        
    input("\nPresione Enter para volver al menú...")

def menu_registrar_reserva():
    """Captura los datos de una reserva validando campos (Bruno)"""
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

# ==========================================
# INICIO DE LA APLICACIÓN
# ==========================================
if __name__ == "__main__":
    menu_principal()