import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import extras

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

def get_sql_query_string(start_date, end_date, event_types):
    """
    Genera y devuelve la cadena de la consulta SQL.
    """
    placeholders = ', '.join([f"'{et}'" for et in event_types])
    
    query = f"""
        SELECT
            alarm_date,
            alert_uuid,
            device_id,
            event_iot_type_code as event_type,
            COALESCE(defendant_id, victim_id) as user_id,
            COALESCE(defendant_phone_coordinates, victim_phone_coordinates) as phone_coordinates
        FROM
            monitored_event
        WHERE
            alarm_date >= '{start_date}' AND alarm_date <= '{end_date}'
            AND event_iot_type_code IN ({placeholders});
    """
    return query

def get_monitored_event_data(conn, start_date, end_date, event_types):
    """
    Obtiene los datos de eventos para los tipos seleccionados de PostgreSQL.
    """
    if conn is None or not event_types:
        return []
    
    placeholders = ','.join(['%s'] * len(event_types))
    
    query = f"""
        SELECT
            alarm_date,
            alert_uuid,
            device_id,
            event_iot_type_code as event_type,
            COALESCE(defendant_id, victim_id) as user_id,
            COALESCE(defendant_phone_coordinates, victim_phone_coordinates) as phone_coordinates
        FROM
            monitored_event
        WHERE
            alarm_date >= %s AND alarm_date <= %s
            AND event_iot_type_code IN ({placeholders});
    """
    
    try:
        with conn.cursor(cursor_factory=extras.DictCursor) as cursor:
            params = [start_date, end_date] + event_types
            cursor.execute(query, params)
            combined_data = cursor.fetchall()
        
        return combined_data
    except psycopg2.Error as err:
        print(f"Error al ejecutar la consulta: {err}")
        return []