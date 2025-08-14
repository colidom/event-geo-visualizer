# Diccionario para agrupar tipos de evento
EVENT_GROUPS = {
    'PROX': ['PROX'], 'SZEM': ['SZEM'], 'EZEM': ['EZEM'], 'SZEF': ['SZEF'],
    'EZEF': ['EZEF'], 'CONNB_A': ['CONNB_A'], 'DISCONB_A': ['DISCONB_A'],
    'BATCF_A': ['BATCF_A'], 'BATCN_A': ['BATCN_A'], 'SSC': ['SSC_A', 'SSC_V'],
    'PWRF': ['PWRF_A', 'PWRF_V'], 'PWRN': ['PWRN_A', 'PWRN_V'],
}

# Diccionario de configuración para todos los tipos de eventos
EVENT_CONFIG = {
    'SSC_A': {'color': 'red', 'label': 'Inculpado'},
    'SSC_V': {'color': 'blue', 'label': 'Víctima'},
    'PROX': {'color': 'green', 'label': 'Proximidad'},
    'EZEF': {'color': 'darkred', 'label': 'Entrada en Zona Fija)'},
    'EZEM': {'color': 'darkred', 'label': 'Entrada en Zona Móvil'},
    'SZEF': {'color': 'darkpurple', 'label': 'Salida de Zona Fija'},
    'SZEM': {'color': 'darkpurple', 'label': 'Salida de Zona Móvil'},
    'PWRF_V': {'color': 'black', 'label': 'Apagado DLV'},
    'PWRF_A': {'color': 'black', 'label': 'Apagado DLI'},
    'PWRN_V': {'color': 'orange', 'label': 'Encendido DLV'},
    'PWRN_A': {'color': 'orange', 'label': 'Encendido DLI'},
    'CONNB_A': {'color': 'darkgreen', 'label': 'Conexión Brazalete'},
    'DISCONB_A': {'color': 'darkgreen', 'label': 'Desconexión Brazalete'},
    'BATCN_A': {'color': 'lightred', 'label': 'Enchufado DLI'},
    'BATCF_A': {'color': 'lightred', 'label': 'Desenchufado DLI'}
}