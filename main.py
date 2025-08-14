import os
import sys
import folium
from folium.plugins import TagFilterButton
import src.database
import src.map_markers 

# Rango de fechas y horas para la consulta
START_DATE = '2024-01-13 22:00:00'
END_DATE = '2025-08-14 12:00:00'

db_conn = None
try:
    print("Conectando a la base de datos...")
    db_conn = src.database.connect_to_db()
    
    if db_conn:
        print("Conexión establecida. Obteniendo datos...")
        all_events_data = src.database.get_monitored_event_data(db_conn, START_DATE, END_DATE)
        
        if not all_events_data:
            print("No se encontraron datos en la base de datos para el rango de fechas especificado.")
        else:
            print(f"Datos obtenidos. Procesando {len(all_events_data)} registros...")
            
            m = folium.Map(zoom_start=6)
            all_coords = []
            all_alarm_dates = []

            for row in all_events_data:
                hour_tag, is_defendant = src.map_markers.create_marker(row, m, all_coords)
                if hour_tag:
                    all_alarm_dates.append(hour_tag)

            print("Procesamiento de datos finalizado. Creando mapa...")

            unique_hours = sorted(list(set(all_alarm_dates)))
            TagFilterButton(unique_hours, name='Filtrar por Hora').add_to(m)
            
            if all_coords:
                m.fit_bounds(all_coords)
            else:
                print("No se encontraron coordenadas válidas para mostrar en el mapa.")

            output_file = f"mapa_{START_DATE.replace(' ', '_').replace(':', '')}_to_{END_DATE.replace(' ', '_').replace(':', '')}.html"
            m.save(output_file)
            print(f"\nMapa generado exitosamente. Se ha guardado como '{output_file}'.")

except Exception as e:
    print(f"\nError durante la ejecución del script: {e}")
finally:
    if 'db_conn' in locals() and db_conn:
        src.database.close_connection(db_conn)