import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import extras

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def connect_to_db():
    """Establece y devuelve una conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            dbname=os.getenv("DB_NAME")
        )
        print("Conexión a la base de datos establecida correctamente.")
        return conn
    except psycopg2.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

def close_connection(conn):
    """Cierra la conexión a la base de datos."""
    if conn and not conn.closed:
        conn.close()
        print("Conexión a la base de datos cerrada.")

def get_monitored_event_data(conn, start_date, end_date):
    """
    Obtiene los datos de eventos para inculpados y víctimas de PostgreSQL
    en una sola consulta usando UNION ALL.
    """
    if conn is None:
        return []
    
    query_combined = """
        SELECT
            alarm_date,
            alert_uuid,
            device_id,
            'defendant' as event_type,
            defendant_id as user_id,
            defendant_phone_coordinates as phone_coordinates
        FROM
            monitored_event
        WHERE
            alarm_date >= %s AND alarm_date <= %s
            AND event_iot_type_code = 'SSC_A'

        UNION ALL

        SELECT
            alarm_date,
            alert_uuid,
            device_id,
            'victim' as event_type,
            victim_id as user_id,
            victim_phone_coordinates as phone_coordinates
        FROM
            monitored_event
        WHERE
            alarm_date >= %s AND alarm_date <= %s
            AND event_iot_type_code = 'SSC_V';
    """
    
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cursor:
            # Los parámetros deben ser pasados en el mismo orden que aparecen en la query
            cursor.execute(query_combined, (start_date, end_date, start_date, end_date))
            combined_data = cursor.fetchall()
        
        return combined_data
    except psycopg2.Error as err:
        print(f"Error al ejecutar la consulta: {err}")
        return []