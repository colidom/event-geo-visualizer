import sys
from datetime import datetime, timedelta
from src.config import EVENT_CONFIG, EVENT_GROUPS

def get_user_input():
    """
    Solicita al usuario un rango de fechas y tipos de eventos.
    Valida que el rango de fechas no sea mayor a una semana.
    """
    def parse_datetime(input_str, is_start=True):
        """Intenta analizar una cadena de fecha con y sin hora."""
        try:
            # Intenta con el formato completo: 'YYYYMMDD HH:MM'
            dt = datetime.strptime(input_str.strip(), '%Y%m%d %H:%M')
            return dt
        except ValueError:
            try:
                # Si falla, intenta con el formato solo de fecha: 'YYYYMMDD'
                dt = datetime.strptime(input_str.strip(), '%Y%m%d')
                if is_start:
                    return dt.replace(hour=0, minute=0, second=0)
                else:
                    return dt.replace(hour=23, minute=59, second=59)
            except ValueError:
                raise ValueError("Formato de fecha u hora incorrecto. Use 'YYYYMMDD' o 'YYYYMMDD HH:MM'.")

    while True:
        try:
            print("\n--- Ingrese el rango de fechas para la consulta ---")
            print("El rango no debe exceder de 1 día.")
            print("Formato: YYYYMMDD HH:MM (la hora es opcional)")
            start_dt_str = input("Ingrese fecha y hora de inicio: ")
            end_dt_str = input("Ingrese fecha y hora de fin: ")
            
            start_date = parse_datetime(start_dt_str, is_start=True)
            end_date = parse_datetime(end_dt_str, is_start=False)

            if start_date > end_date:
                print("La fecha/hora de inicio no puede ser posterior a la fecha/hora de fin. Inténtelo de nuevo.")
                continue

            max_duration = timedelta(days=1)
            if (end_date - start_date) > max_duration:
                print("\nError: El rango de fechas es mayor a 1 día.")
                print("Por favor, vuelva a intentar con un rango de fechas más corto.")
                continue

            break
        except ValueError as e:
            print(f"Error: {e}")
    
    # Lógica de selección de eventos
    while True:
        print("\n--- Seleccione los tipos de eventos a filtrar ---")
        event_options = {}
        print("(0) Todos los eventos")
        
        for i, group_name in enumerate(EVENT_GROUPS.keys(), 1):
            event_codes = EVENT_GROUPS.get(group_name, [])
            simplified_codes = sorted(list(set(code.split('_')[0] for code in event_codes)))
            codes_str = ", ".join(simplified_codes)
            print(f"({i}) Grupo: {group_name} ({codes_str})")
            event_options[i] = EVENT_GROUPS[group_name]
        
        individual_start_index = len(EVENT_GROUPS) + 1
        individual_event_codes = [code for code in EVENT_CONFIG.keys() if code not in [item for sublist in EVENT_GROUPS.values() for item in sublist]]
        for i, event_code in enumerate(sorted(individual_event_codes), individual_start_index):
            print(f"({i}) Evento: {EVENT_CONFIG[event_code]['label']}")
            event_options[i] = [event_code]

        try:
            selection_str = input("Seleccione una o varias opciones (ej: 1, 3, 5): ")
            selections = [int(s.strip()) for s in selection_str.split(',')]
            
            selected_event_codes = []
            if 0 in selections:
                print("\n⚠️  ADVERTENCIA: Ha seleccionado 'Todos los eventos'.")
                print("Esto podría generar una query con un alto consumo de recursos y el mapa resultante podría no ser manejable en el navegador.")
                confirm = input("¿Desea continuar de todos modos? (s/n): ").lower()
                if confirm == 's':
                    selected_event_codes = list(EVENT_CONFIG.keys())
                    break
                else:
                    print("Operación cancelada. Por favor, vuelva a seleccionar.")
                    continue
            
            for sel in selections:
                if sel in event_options:
                    selected_event_codes.extend(event_options[sel])
                else:
                    print(f"Opción inválida: {sel}. Inténtelo de nuevo.")
                    selected_event_codes = []
                    break
            
            if selected_event_codes:
                selected_event_codes = sorted(list(set(selected_event_codes)))
                break

        except ValueError:
            print("Entrada inválida. Por favor, ingrese solo números separados por comas.")

    return start_date, end_date, selected_event_codes
