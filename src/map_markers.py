import folium
import pandas as pd
import pytz
import datetime
from src.config import EVENT_CONFIG

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
                if user_tag == 'Inculpado':
                    icon_name = 'male'
                elif user_tag == 'Víctima':
                    icon_name = 'female'

                tags = [hour_tag, user_tag]

                popup_content_list = []
                
                user_id_label = "User ID"
                if user_tag == 'Inculpado':
                    user_id_label = 'ID Inculpado'
                elif user_tag == 'Víctima':
                    user_id_label = 'ID Víctima'
                
                popup_content_list.append(f"<strong>Tipo de Usuario:</strong> {user_tag}")
                popup_content_list.append(f"<strong>Tipo de Evento:</strong> {event_label}")
                popup_content_list.append(f"<strong>{user_id_label}:</strong> {row.get('user_id', 'N/A')}")
                popup_content_list.append(f"<strong>Device ID:</strong> {row.get('device_id', 'N/A')}")
                popup_content_list.append(f"<strong>Coordenada:</strong> {coords_parts[0]}, {coords_parts[1]}")
                popup_content_list.append(f"<strong>Alarm Date:</strong> {madrid_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                popup_content_list.append(f"<strong>Alert UUID:</strong> {row.get('alert_uuid', 'N/A')}")

                popup_html = "<br>".join(popup_content_list)

                folium.Marker(
                    location=coords,
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color=icon_color, icon=icon_name, prefix='fa'),
                    tags=tags
                ).add_to(m)
                
                return tags
        except (ValueError, AttributeError, TypeError) as e:
            print(f"ERROR en create_marker: No se pudo procesar. Error: {e}")
    return None