import os
import sys
import folium
from folium.plugins import TagFilterButton
from datetime import datetime, timedelta
import src.database
import src.map_markers 
from src.user_input import get_user_input
from src.config import EVENT_GROUPS, EVENT_CONFIG

def add_legend(m):
    """
    Crea y añade una leyenda estática al mapa de Folium con un botón para mostrar/ocultar.
    """
    legend_html = """
     <div id="legend-container" style="position: fixed; 
                 bottom: 50px; right: 50px; width: 200px; height: auto; 
                 border:2px solid grey; z-index:9999; font-size:12px;
                 background-color:white; opacity:0.9;">
       <div style="padding: 10px;">
         <h4 style="margin-top:0;">Leyenda de Eventos</h4>
         <div id="legend-items-list">
    """

    grouped_legend_items = {'Víctima': [], 'Inculpado': []}
    unique_items_seen = set()

    for event_code, config in EVENT_CONFIG.items():
        key = (config['color'], config['label'], config['persona'])
        if key not in unique_items_seen:
            grouped_legend_items[config['persona']].append(config)
            unique_items_seen.add(key)
    
    legend_html += "<h5 style='margin-top: 10px; margin-bottom: 5px;'>Víctima</h5>"
    for config in grouped_legend_items['Víctima']:
        legend_html += f"""
          <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <i style="background-color:{config['color']}; width:16px; height:16px; border-radius:50%; margin-right:8px; border:1px solid black;"></i>
            <span>{config['label']}</span>
          </div>
        """
    
    legend_html += "<hr style='border:1px solid #ccc; margin: 10px 0;'>"

    legend_html += "<h5 style='margin-top: 10px; margin-bottom: 5px;'>Inculpado</h5>"
    for config in grouped_legend_items['Inculpado']:
        legend_html += f"""
          <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <i style="background-color:{config['color']}; width:16px; height:16px; border-radius:50%; margin-right:8px; border:1px solid black;"></i>
            <span>{config['label']}</span>
          </div>
        """
    
    legend_html += """
        </div>
       </div>
     </div>
    """
    
    toggle_button_html = """
    <div style="position: fixed; bottom: 20px; right: 50px; z-index: 10000;">
        <button id="toggle-legend" style="background-color: #f8f9fa; border: 1px solid #ccc; border-radius: 5px; padding: 5px 10px; cursor: pointer;">
            Mostrar/Ocultar Leyenda
        </button>
    </div>
    """

    js_code = """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const toggleButton = document.getElementById('toggle-legend');
            const legendContainer = document.getElementById('legend-container');

            if (toggleButton && legendContainer) {
                legendContainer.style.display = 'block'; // Asegurar que es visible al cargar
                
                toggleButton.addEventListener('click', function() {
                    if (legendContainer.style.display === 'none') {
                        legendContainer.style.display = 'block';
                    } else {
                        legendContainer.style.display = 'none';
                    }
                });
            }
        });
    </script>
    """
    
    m.get_root().html.add_child(folium.Element(legend_html + toggle_button_html + js_code))


def generate_map(all_events_data, start_date, end_date):
    """
    Genera y guarda el mapa de eventos con marcadores y filtros.
    """
    print(f"Datos obtenidos. Procesando {len(all_events_data)} registros...")
    
    m = folium.Map(zoom_start=6)
    all_coords = []
    all_alarm_dates = []
    all_user_tags = []

    for row in all_events_data:
        marker_tags = src.map_markers.create_marker(row, m, all_coords, all_alarm_dates)
        if marker_tags:
            all_user_tags.append(marker_tags[1])

    print("Procesamiento de datos finalizado. Creando mapa...")

    unique_hours = sorted(list(set(all_alarm_dates)))
    unique_user_tags = sorted(list(set(all_user_tags)))
    
    TagFilterButton(
        unique_user_tags,
        name='Tipo de Usuario'
    ).add_to(m)

    TagFilterButton(
        unique_hours,
        name='Filtro por Hora'
    ).add_to(m)

    add_legend(m)

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