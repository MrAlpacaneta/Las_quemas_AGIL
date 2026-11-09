# ==========================================
# MÓDULO DE BASE DE DATOS - LAS QUEMAS
# Conexión a Oracle SQL Developer (oracledb)
# ==========================================

import oracledb

def conectar_bd():
    """
    Establece la conexión con la base de datos Oracle local
    utilizando el usuario MDAGIL y la contraseña inacap.
    """
    try:
        # Usamos el modo "thin" que no requiere instalar Oracle Client por separado
        conexion = oracledb.connect(
            user="MDAGIL",
            password="inacap",
            dsn="localhost:1521/xe"
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a la Base de Datos: {e}")
        return None

# ==========================================
# 1. FUNCIONES PARA EL MÓDULO DE CANCHAS (CRUD)
# ==========================================

def obtener_canchas():
    """
    Retorna una lista con todas las canchas registradas en la base de datos.
    Utilizado por Carolina para la grilla (Tarea 1.3.3.2).
    """
    conexion = conectar_bd()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        # Seleccionamos todas las canchas ordenadas por número
        cursor.execute("SELECT numero_cancha, tipo_cancha, precio_base, estado FROM CANCHAS ORDER BY numero_cancha")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error al consultar canchas: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def agregar_cancha(numero, tipo, precio):
    """
    Inserta una nueva cancha en la base de datos con estado 'Activa' por defecto.
    Asociado a la Tarea 1.3.1.2 (Verenise).
    """
    conexion = conectar_bd()
    if not conexion:
        return False, "Error de conexión"
    
    try:
        cursor = conexion.cursor()
        # Insertamos el registro
        cursor.execute(
            "INSERT INTO CANCHAS (numero_cancha, tipo_cancha, precio_base, estado) VALUES (:1, :2, :3, 'Activa')",
            [numero, tipo, precio]
        )
        conexion.commit()
        return True, "Cancha agregada exitosamente"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al agregar cancha (¿El número ya existe?): {e}"
    finally:
        cursor.close()
        conexion.close()

def actualizar_cancha(numero, tipo, precio):
    """
    Modifica los datos de una cancha existente (UPDATE).
    Asociado a la Tarea 1.3.2.1 (Bruno).
    """
    conexion = conectar_bd()
    if not conexion:
        return False, "Error de conexión"
    
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE CANCHAS SET tipo_cancha = :1, precio_base = :2 WHERE numero_cancha = :3",
            [tipo, precio, numero]
        )
        conexion.commit()
        return True, "Cancha actualizada exitosamente"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al actualizar: {e}"
    finally:
        cursor.close()
        conexion.close()

def cambiar_estado_cancha(numero, nuevo_estado):
    """
    Realiza un borrado lógico cambiando el estado a 'Inactiva'.
    Asociado a la Tarea 1.3.4.1 (Verenise).
    """
    conexion = conectar_bd()
    if not conexion:
        return False, "Error de conexión"
    
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE CANCHAS SET estado = :1 WHERE numero_cancha = :2",
            [nuevo_estado, numero]
        )
        conexion.commit()
        return True, f"Cancha marcada como {nuevo_estado}"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al cambiar estado: {e}"
    finally:
        cursor.close()
        conexion.close()

# ==========================================
# 2. FUNCIONES PARA EL MÓDULO DE RESERVAS
# ==========================================

def guardar_reserva(fecha, hora, cancha, jugadores, precio):
    """
    Registra una nueva reserva de cancha en el sistema.
    Asociado a la Historia 1.1.1.
    """
    conexion = conectar_bd()
    if not conexion:
        return False, "Error de conexión"
    
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            INSERT INTO RESERVAS (fecha_reserva, hora_reserva, numero_cancha, jugadores, precio_total) 
            VALUES (:1, :2, :3, :4, :5)
            """,
            [fecha, hora, cancha, jugadores, precio]
        )
        conexion.commit()
        return True, "¡Reserva registrada con éxito!"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al registrar reserva: {e}"
    finally:
        cursor.close()
        conexion.close()