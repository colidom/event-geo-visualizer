import src.database
from src.map import *
from src.utils import *
from src.user_input import get_user_input
from src.config import EVENT_GROUPS, EVENT_CONFIG



# --- Inicio del script ---
db_conn = None
try:
    start_date, end_date, selected_event_types = get_user_input()
    
    print("Conectando a la base de datos...")
    db_conn = src.database.connect_to_db()
    
    if db_conn:
        print("Conexión establecida. Obteniendo datos...")
        
        print(f"\n--- Rango de consulta ---")
        print(f"Fecha y hora de inicio: {start_date}")
        print(f"Fecha y hora de fin:    {end_date}")
        print("-------------------------\n")
        
        sql_query = src.database.get_sql_query_string(
            start_date, 
            end_date, 
            selected_event_types
        )
        # ss(sql_query)

        all_events_data = src.database.get_monitored_event_data(
            db_conn, 
            start_date, 
            end_date,
            selected_event_types
        )
        
        if not all_events_data:
            print("No se encontraron datos en la base de datos para el rango de fechas y tipos de evento seleccionados.")
        else:
            generate_map(all_events_data, start_date, end_date)

except Exception as e:
    print(f"\nError durante la ejecución del script: {e}")
finally:
    if 'db_conn' in locals() and db_conn:
        src.database.close_connection(db_conn)
