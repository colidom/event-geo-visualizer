# Diccionario para agrupar tipos de evento
EVENT_GROUPS = {
    'PROX': ['PROX'], 'SZEM': ['SZEM'], 'EZEM': ['EZEM'], 'SZEF': ['SZEF'],
    'EZEF': ['EZEF'], 'CONNB_A': ['CONNB_A'], 'DISCONB_A': ['DISCONB_A'],
    'BATCF_A': ['BATCF_A'], 'BATCN_A': ['BATCN_A'], 'SSC': ['SSC_A', 'SSC_V'],
    'PWRF': ['PWRF_A', 'PWRF_V'], 'PWRN': ['PWRN_A', 'PWRN_V'],
}

# Diccionario de configuración para todos los tipos de eventos
# {'green', 'gray', 'lightgreen', 'lightblue', 'blue', 'red', 'orange', 'cadetblue', 'lightgray', 'darkblue', 'white', 'darkgreen', 'pink', 'lightred', 'purple', 'darkpurple', 'darkred', 'black', 'beige'}
EVENT_CONFIG = {
    'SSC_A': {'color': 'gray', 'label': 'DLI sin comunicacion', 'persona': 'Inculpado'},
    'SSC_V': {'color': 'gray', 'label': 'DLV sin comunicacion', 'persona': 'Víctima'},
    'PROX': {'color': 'darkred', 'label': 'Proximidad', 'persona': 'Inculpado'},
    'EZEF': {'color': 'red', 'label': 'Entrada en Zona Fija', 'persona': 'Inculpado'},
    'EZEM': {'color': 'red', 'label': 'Entrada en Zona Móvil', 'persona': 'Inculpado'},
    'SZEF': {'color': 'cadetblue', 'label': 'Salida de Zona Fija', 'persona': 'Inculpado'},
    'SZEM': {'color': 'cadetblue', 'label': 'Salida de Zona Móvil', 'persona': 'Inculpado'},
    'PWRF_V': {'color': 'black', 'label': 'Apagado DLV', 'persona': 'Víctima'},
    'PWRF_A': {'color': 'black', 'label': 'Apagado DLI', 'persona': 'Inculpado'},
    'PWRN_V': {'color': 'green', 'label': 'Encendido DLV', 'persona': 'Víctima'},
    'PWRN_A': {'color': 'green', 'label': 'Encendido DLI', 'persona': 'Inculpado'},
    'CONNB_A': {'color': 'lightgreen', 'label': 'Conexión Brazalete', 'persona': 'Inculpado'},
    'DISCONB_A': {'color': 'gray', 'label': 'Desconexión Brazalete', 'persona': 'Inculpado'},
    'BATCN_A': {'color': 'orange', 'label': 'Enchufado cargador DLI', 'persona': 'Inculpado'},
    'BATCF_A': {'color': 'lightgray', 'label': 'Desenchufado cargador DLI', 'persona': 'Inculpado'}
}