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
            all_event_types = []
            
            # Un solo bucle para procesar todos los eventos
            for row in all_events_data:
                event_type = src.map_markers.create_marker(row, m, all_coords, all_alarm_dates)
                if event_type:
                    all_event_types.append(event_type)

            print("Procesamiento de datos finalizado. Creando mapa...")

            unique_hours = sorted(list(set(all_alarm_dates)))
            unique_event_types = sorted(list(set(all_event_types)))
            
            TagFilterButton(
                unique_event_types, 
                name='Tipo de Evento',
                active=['Inculpado', 'Víctima'] # Los dos tipos estarán activos por defecto
            ).add_to(m)
            
            TagFilterButton(
                unique_hours,
                name='Hora'
            ).add_to(m)
            
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