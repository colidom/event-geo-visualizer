import folium
from folium.plugins import TagFilterButton
import src.database
import src.map_markers 
from src.user_input import get_user_input

def generate_map(all_events_data, start_date, end_date):
    """
    Genera y guarda el mapa de eventos con marcadores y filtros.
    """
    print(f"Datos obtenidos. Procesando {len(all_events_data)} registros...")
    
    m = folium.Map(zoom_start=6)
    all_coords = []
    all_alarm_dates = []
    all_event_tags = []
    
    for row in all_events_data:
        marker_tags = src.map_markers.create_marker(row, m, all_coords, all_alarm_dates)
        if marker_tags:
            all_event_tags.append(marker_tags[1])

    print("Procesamiento de datos finalizado. Creando mapa...")

    unique_hours = sorted(list(set(all_alarm_dates)))
    unique_event_tags = sorted(list(set(all_event_tags)))
    
    TagFilterButton(
        unique_event_tags,
        name='Tipo de Usuario'
    ).add_to(m)

    TagFilterButton(
        unique_hours,
        name='Filtro por Hora'
    ).add_to(m)

    if all_coords:
        m.fit_bounds(all_coords)
    else:
        print("No se encontraron coordenadas válidas para mostrar en el mapa.")

    output_file = f"mapa_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.html"
    m.save(output_file)
    print(f"\nMapa generado exitosamente. Se ha guardado como '{output_file}'.")


# --- Inicio del script ---
db_conn = None
try:
    start_date, end_date, selected_event_types = get_user_input()
    
    print("Conectando a la base de datos...")
    db_conn = src.database.connect_to_db()
    
    if db_conn:
        print("Conexión establecida. Obteniendo datos...")
        
        sql_query = src.database.get_sql_query_string(
            start_date.strftime('%Y-%m-%d %H:%M:%S'), 
            end_date.strftime('%Y-%m-%d %H:%M:%S'), 
            selected_event_types
        )
        print("\n--- Consulta SQL a ejecutar ---")
        print(sql_query)
        print("-------------------------------\n")

        all_events_data = src.database.get_monitored_event_data(
            db_conn, 
            start_date.strftime('%Y-%m-%d %H:%M:%S'), 
            end_date.strftime('%Y-%m-%d %H:%M:%S'),
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