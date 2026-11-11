import oracledb

def conectar_bd():

    try:
        conexion = oracledb.connect(
            user="MDAGIL",
            password="inacap",
            dsn="localhost:1521/xe"
        )
        return conexion
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

def obtener_canchas():

    conexion = conectar_bd()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT numero_cancha, tipo_cancha, precio_base, estado FROM CANCHAS ORDER BY numero_cancha")
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error al consultar canchas: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()

def agregar_cancha(tipo_cancha, precio_base):
    """
    Agrega una nueva cancha calculando automáticamente el siguiente número (Autoincremental).
    """
    conexion = conectar_bd()
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT NVL(MAX(numero_cancha), 0) + 1 FROM CANCHAS")
        nuevo_numero = cursor.fetchone()[0]
        cursor.execute(
            """
            INSERT INTO CANCHAS (numero_cancha, tipo_cancha, precio_base, estado) 
            VALUES (:1, :2, :3, 'Activa')
            """,
            [nuevo_numero, tipo_cancha, precio_base]
        )
        conexion.commit()
        
        print(f"\nEl registro de la cancha se realizó con éxito. Número asignado: {nuevo_numero}")
        return True
        
    except Exception as e:
        print(f"\nError al registrar la cancha: {e}")
        return False
    finally:
        cursor.close()
        conexion.close()

def actualizar_cancha(numero, tipo, precio):
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

def guardar_reserva(fecha, hora, cancha, jugadores, precio):

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
        return True, "Reserva registrada exitosamente"
    except Exception as e:
        conexion.rollback()
        return False, f"Error al registrar la reserva: {e}"
    finally:
        cursor.close()
        conexion.close()

def consultar_calendario(fecha):

    conexion = conectar_bd()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute(
            """
            SELECT r.hora_reserva, r.numero_cancha, c.tipo_cancha, r.jugadores 
            FROM RESERVAS r
            JOIN CANCHAS c ON r.numero_cancha = c.numero_cancha
            WHERE r.fecha_reserva = :1
            ORDER BY r.hora_reserva, r.numero_cancha
            """,
            [fecha]
        )
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"Error al consultar el calendario: {e}")
        return []
    finally:
        cursor.close()
        conexion.close()