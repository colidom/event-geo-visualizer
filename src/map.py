import folium
import pandas as pd
import pytz
from src.config import EVENT_CONFIG, EVENT_GROUPS
from folium.plugins import TagFilterButton

def create_marker(row, m, all_coords, all_alarm_dates):
    """
    Procesa las coordenadas y añade un marcador al mapa, decidiendo el color
    y el contenido basado en el tipo de evento.
    """
    coords_str = row.get('phone_coordinates')
    
    event_type = row.get('event_type')
    if event_type:
        event_type = event_type.strip()
    
    if coords_str is not None:
        try:
            coords_str = coords_str.strip()
            coords_parts = coords_str.split(',')
            
            if len(coords_parts) >= 2:
                coords = (float(coords_parts[0]), float(coords_parts[1]))
                all_coords.append(coords)

                alarm_datetime_obj = row.get('alarm_date')
                
                try:
                    alarm_timestamp = pd.to_datetime(alarm_datetime_obj, utc=True)
                    madrid_timezone = pytz.timezone('Europe/Madrid')
                    madrid_datetime = alarm_timestamp.tz_convert(madrid_timezone)
                except Exception as e:
                    print(f"Error al convertir fecha: {e}. Usando objeto original.")
                    madrid_datetime = alarm_datetime_obj
                
                hour_tag = madrid_datetime.floor('h').strftime('%H:00')
                all_alarm_dates.append(hour_tag)
                
                if event_type is not None and event_type in EVENT_CONFIG:
                    config = EVENT_CONFIG.get(event_type)
                    user_tag = config['persona']
                    icon_color = config['color']
                    event_label = config['label']
                else:
                    user_tag = 'Otro'
                    icon_color = 'lightgray'
                    event_label = event_type if event_type else 'Tipo de evento desconocido'
                
                icon_name = 'user'
                user_id_label = "User ID"
                if user_tag == 'Inculpado':
                    icon_name = 'male'
                    user_id_label = 'ID Inculpado'
                elif user_tag == 'Víctima':
                    icon_name = 'female'
                    user_id_label = 'ID Víctima'

                event_group_tags = []
                for group_name, events in EVENT_GROUPS.items():
                    if event_type in events:
                        event_group_tags.append(group_name)
                
                tags = [hour_tag, user_tag] + event_group_tags

                popup_content_list = []
                
                popup_content_list.append(f"<strong>Tipo de Usuario:</strong> {user_tag}")
                popup_content_list.append(f"<strong>Tipo de Evento:</strong> {event_label}")
                popup_content_list.append(f"<strong>{user_id_label}:</strong> {row.get('user_id', 'N/A')}")
                popup_content_list.append(f"<strong>Device ID:</strong> {row.get('device_id', 'N/A')}")
                popup_content_list.append(f"<strong>Coordenada:</strong> {coords_parts[0]}, {coords_parts[1]}")
                popup_content_list.append(f"<strong>Alarm Date:</strong> {madrid_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                popup_content_list.append(f"<strong>Alert UUID:</strong> {row.get('alert_uuid', 'N/A')}")

                popup_html = "<br>".join(popup_content_list)
                
                marker_icon = folium.Icon(color=icon_color, icon=icon_name, prefix='fa')

                folium.Marker(
                    location=coords,
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=marker_icon,
                    tags=tags
                ).add_to(m)
                
                return tags
        except (ValueError, AttributeError, TypeError) as e:
            print(f"ERROR en create_marker: No se pudo procesar. Error: {e}")
    return None

def add_legend(m):
    """
    Crea y añade una leyenda estática y simplificada al mapa de Folium.
    """
    legend_html = """
     <div id="legend-container" style="position: fixed; 
                 bottom: 50px; right: 50px; width: 220px; height: auto; 
                 border:2px solid grey; z-index:9999; font-size:12px;
                 background-color:white; opacity:0.9;">
       <div style="padding: 10px;">
         <h4 style="margin-top:0;">Leyenda de Eventos</h4>
         <div id="legend-items-list">
    """

    unique_legend_items = {}
    
    for event_code, config in EVENT_CONFIG.items():
        # Agrupa por color y la parte genérica de la etiqueta
        generic_label = config['label'].replace(' DLI', '').replace(' DLV', '')
        key = (config['color'], generic_label)
        
        # Agregamos los códigos de evento para saber si tiene una versión DLI y DLV
        if key not in unique_legend_items:
            unique_legend_items[key] = {
                'color': config['color'],
                'label': generic_label,
                'event_codes': {event_code}
            }
        else:
            unique_legend_items[key]['event_codes'].add(event_code)
    
    # Genera los ítems de la leyenda
    for config in unique_legend_items.values():
        final_label = config['label']
        
        has_dli = any('_A' in code for code in config['event_codes'])
        has_dlv = any('_V' in code for code in config['event_codes'])
        
        if has_dli and has_dlv:
            final_label += ' DLI / DLV'
        
        legend_html += f"""
          <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <i style="background-color:{config['color']}; width:16px; height:16px; border-radius:50%; margin-right:8px; border:1px solid black;"></i>
            <span>{final_label}</span>
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
                legendContainer.style.display = 'block';
                
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
        marker_tags = create_marker(row, m, all_coords, all_alarm_dates)
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
    
    unique_event_groups = sorted(list(EVENT_GROUPS.keys()))
    TagFilterButton(
        unique_event_groups,
        name='Tipo de Evento'
    ).add_to(m)

    add_legend(m)

    if all_coords:
        m.fit_bounds(all_coords)
    else:
        print("No se encontraron coordenadas válidas para mostrar en el mapa.")

    output_file = f"mapa_{start_date.strftime('%Y-%m-%d')}_to_{end_date.strftime('%Y-%m-%d')}.html"
    m.save(output_file)
    print(f"\nMapa generado exitosamente. Se ha guardado como '{output_file}'.")
