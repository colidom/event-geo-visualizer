# src/user_input.py
from datetime import datetime, timedelta
from src.config import EVENT_GROUPS

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