import os
import sys
import folium
from folium.plugins import TagFilterButton
from datetime import datetime, timedelta
import src.database
import src.map_markers 

# Diccionario para agrupar tipos de evento
EVENT_GROUPS = {
    'PROX': ['PROX'], 'SZEM': ['SZEM'], 'EZEM': ['EZEM'], 'SZEF': ['SZEF'],
    'EZEF': ['EZEF'], 'CONNB_A': ['CONNB_A'], 'DISCONB_A': ['DISCONB_A'],
    'BATCF_A': ['BATCF_A'], 'BATCN_A': ['BATCN_A'], 'SSC': ['SSC_A', 'SSC_V'],
    'PWRF': ['PWRF_A', 'PWRF_V'], 'PWRN': ['PWRN_A', 'PWRN_V'],
}

def get_user_input():
    """
    Solicita al usuario el rango de fechas y los tipos de eventos a visualizar.
    """
    while True:
        try:
            start_date_str = input("Introduce la fecha de inicio (YYYY-MM-DD): ")
            end_date_str = input("Introduce la fecha de fin (YYYY-MM-DD): ")

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
            
            # Limitar el rango de fechas a una semana (168 horas) para evitar mapas demasiado grandes.
            if end_date - start_date > timedelta(hours=168):
                print("Error: El rango de fechas no puede ser superior a 1 semana.")
                continue

            break
        except ValueError:
            print("Formato de fecha incorrecto. Usa el formato YYYY-MM-DD.")
    
    available_event_types = sorted(list(EVENT_GROUPS.keys()))

    while True:
        print("\nTipos de evento disponibles:")
        for i, event_type in enumerate(available_event_types, 1):
            print(f"{i}: {event_type}")
        
        user_choice = input("Selecciona los tipos de evento por número (ej: 1,3,5): ")
        
        selected_event_types = []
        try:
            choices = [int(c.strip()) for c in user_choice.split(',')]
            for choice in choices:
                if 1 <= choice <= len(available_event_types):
                    selected_event_types.append(available_event_types[choice - 1])
            if selected_event_types:
                break
            else:
                print("Selección inválida. Por favor, introduce números válidos.")
        except ValueError:
            print("Entrada incorrecta. Por favor, introduce números separados por comas.")

    db_event_codes = []
    for event_group in selected_event_types:
        db_event_codes.extend(EVENT_GROUPS[event_group])

    return start_date, end_date, db_event_codes

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
            print(f"Datos obtenidos. Procesando {len(all_events_data)} registros...")
            
            m = folium.Map(zoom_start=6)
            all_coords = []
            all_alarm_dates = []
            all_event_tags = [] # 🚨 Nueva lista para recolectar las etiquetas de tipo de evento
            
            for row in all_events_data:
                marker_tags = src.map_markers.create_marker(row, m, all_coords, all_alarm_dates)
                if marker_tags:
                    all_event_tags.append(marker_tags[1]) # Obtener la segunda etiqueta (el tipo de evento)

            print("Procesamiento de datos finalizado. Creando mapa...")

            unique_hours = sorted(list(set(all_alarm_dates)))
            unique_event_tags = sorted(list(set(all_event_tags))) # 🚨 Obtener etiquetas de evento únicas
            
            # 🚨 Botón de filtro para tipos de evento
            TagFilterButton(
                unique_event_tags,
                name='Tipo de Evento'
            ).add_to(m)

            # Botón de filtro para horas
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

except Exception as e:
    print(f"\nError durante la ejecución del script: {e}")
finally:
    if 'db_conn' in locals() and db_conn:
        src.database.close_connection(db_conn)