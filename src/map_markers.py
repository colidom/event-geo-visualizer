import folium
import pandas as pd
import pytz
import datetime

def create_marker(row, m, all_coords):
    """
    Procesa las coordenadas y añade un marcador al mapa, decidiendo el color
    y el contenido basado en el tipo de evento.
    """
    coords_str = row.get('phone_coordinates')
    event_type = row.get('event_type')

    if coords_str is not None:
        try:
            coords_parts = coords_str.split(',')
            if len(coords_parts) >= 2:
                coords = (float(coords_parts[0]), float(coords_parts[1]))
                all_coords.append(coords)

                # Convertir la fecha a pandas.Timestamp para usar .floor
                alarm_datetime_obj = row.get('alarm_date')
                if isinstance(alarm_datetime_obj, datetime.datetime):
                    alarm_date = pd.Timestamp(alarm_datetime_obj, tz='Europe/Madrid')
                else:
                    alarm_date = pd.Timestamp(alarm_datetime_obj, tz=pytz.timezone('Europe/Madrid'))
                
                hour_tag = alarm_date.floor('h').strftime('%H:00')

                # Decidir el color del icono y el contenido del popup
                if event_type == 'defendant':
                    icon_color = 'red'
                    user_id_label = 'Defendant ID'
                else: # event_type == 'victim'
                    icon_color = 'green'
                    user_id_label = 'Victim ID'

                popup_content_list = []
                popup_content_list.append(f"<strong>{user_id_label}:</strong> {row.get('user_id', 'N/A')}")
                popup_content_list.append(f"<strong>Device ID:</strong> {row.get('device_id', 'N/A')}")
                popup_content_list.append(f"<strong>Coordenada:</strong> {coords_parts[0]}, {coords_parts[1]}")
                popup_content_list.append(f"<strong>Alarm Date:</strong> {row.get('alarm_date', 'N/A').strftime('%Y-%m-%d %H:%M:%S')}")
                popup_content_list.append(f"<strong>Alert UUID:</strong> {row.get('alert_uuid', 'N/A')}")

                popup_html = "<br>".join(popup_content_list)

                folium.Marker(
                    location=coords,
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color=icon_color, icon='info-sign'),
                    tags=[hour_tag]
                ).add_to(m)
                
                return hour_tag, event_type
        except (ValueError, AttributeError, TypeError) as e:
            print(f"ERROR en create_marker: No se pudo procesar. Error: {e}")
    return None, None