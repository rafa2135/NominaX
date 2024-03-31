#database_manager.py
import pyodbc
import os 
from dotenv import load_dotenv
import time


# Default database connection parameters
DEFAULT_SERVER = os.getenv('DEFAULT_SERVER')
DEFAULT_DATABASE = os.getenv('DEFAULT_DATABASE')
DEFAULT_USERNAME = os.getenv('DEFAULT_USERNAME')
DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD')


def connect(server=DEFAULT_SERVER, database=DEFAULT_DATABASE, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
    #Establece una conexión con la base de datos
    driver = '{ODBC Driver 17 for SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    # esperar la carga del controlador ODBC
    while True:
        try:
            conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
            conn = pyodbc.connect(conn_str)
            
            return conn
        except pyodbc.Error as e:
            print(f'Error de conexión: {str(e)}')
            print("Esperando 5 segundos antes de intentarlo nuevamente...")
            time.sleep(5)  # Esperar 5 segundos antes de volver a intentar establecer la conexión

def insert_data(conn, empleados_data, bonos_data):
    try:
        cursor = conn.cursor()

        # Insertar datos en la tabla de empleados
        empleados_query = "INSERT INTO empleados (cedula, nombre, apellido, seguro_social, seguro_hcm, sueldo_basico) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.executemany(empleados_query, empleados_data)

        # Insertar datos en la tabla de bonos
        bonos_query = "INSERT INTO bonos (cedula, bono_productividad, bono_alimentacion) VALUES (?, ?, ?)"
        cursor.executemany(bonos_query, bonos_data)

        conn.commit()  # Commit de la transacción
        
        return True    
    finally:
        cursor.close()


def close_connection(conn): #Cierra la conexión a la base de datos.
    try:
        conn.close()
        
    except Exception as e:
        print(f'Error closing connection: {str(e)}')

def insert_db(empleados_data,bonos_data): #Conecta y inserta datos en la base de datos.
    conn=connect()
    if conn:
        completado= insert_data(conn,empleados_data,bonos_data)
        close_connection(conn)
        return completado
    else:
        return False

def cedula_existe(conn, table_names, cedula):
    try:
        cursor = conn.cursor()

        for table_name in table_names:
            # check si cedula existe
            select_query = f"SELECT COUNT(*) FROM {table_name} WHERE cedula = ?"

            # Executar SELECT 
            cursor.execute(select_query, (cedula,))
            row_count = cursor.fetchone()[0]

            if row_count > 0:                
                return True
        
        return False

    except Exception as e:
        
        return False

def borrar_usuario(conn, cedula):
    try:
        # validar si cedula existe un una tabla
        if not cedula_existe(conn, ['bonos', 'empleados'], cedula):
            
            return False

        cursor = conn.cursor()

        for table_name in ['bonos', 'empleados']:
            # crear DELETE statement para cada tabla
            delete_query = f"DELETE FROM {table_name} WHERE cedula = ?"

            # ejecutar DELETE statement usando cedula
            cursor.execute(delete_query, (cedula,))  # Pass cedula as a single-element tuple
        
        conn.commit()  # Commit
        
        return True

    except Exception as e:
        conn.rollback()  # Rollback en caso de error
        
        return False

def fetch_todo(conn):
    try:
        cursor = conn.cursor()

        # SQL query to fetch columna específica
        query = """
            SELECT e.Cedula, e.Nombre, e.Apellido, e.sueldo_basico, b.bono_productividad
            FROM empleados e
            INNER JOIN bonos b ON e.Cedula = b.Cedula
        """

        cursor.execute(query)
        data = cursor.fetchall()
        print (data)
        return data
    #Error fetching data
    except Exception as e:
        
        return None
    