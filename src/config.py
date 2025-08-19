# Diccionario de configuración para todos los tipos de eventos
# {'green', 'gray', 'lightgreen', 'lightblue', 'blue', 'red', 'orange', 'cadetblue', 'lightgray', 'darkblue', 'white', 'darkgreen', 'pink', 'lightred', 'purple', 'darkpurple', 'darkred', 'black', 'beige'}
EVENT_CONFIG = {
    'SSC_A': {'color': 'gray', 'label': 'Sin comunicacion DLI (SSC)', 'persona': 'Inculpado'},
    'SSC_V': {'color': 'gray', 'label': 'Sin comunicacion DLV (SSC)', 'persona': 'Víctima'},
    'CSSC_A': {'color': 'lightblue', 'label': 'Con comunicacion DLI (CSSC)', 'persona': 'Inculpado'},
    'CSSC_V': {'color': 'lightblue', 'label': 'Con comunicacion DLV (CSSC)', 'persona': 'Víctima'},
    'PROX': {'color': 'darkred', 'label': 'Proximidad (PROX)', 'persona': 'Inculpado'},
    'EZEF': {'color': 'red', 'label': 'Entrada en Zona Fija (EZEF)', 'persona': 'Inculpado'},
    'EZEM': {'color': 'red', 'label': 'Entrada en Zona Móvil (EZEM)', 'persona': 'Inculpado'},
    'SZEF': {'color': 'cadetblue', 'label': 'Salida de Zona Fija (SZEF)', 'persona': 'Inculpado'},
    'SZEM': {'color': 'cadetblue', 'label': 'Salida de Zona Móvil (SZEM)', 'persona': 'Inculpado'},
    'PWRF_V': {'color': 'black', 'label': 'Apagado DLV (PWRF_V)', 'persona': 'Víctima'},
    'PWRF_A': {'color': 'black', 'label': 'Apagado DLI (PWRF_A)', 'persona': 'Inculpado'},
    'PWRN_V': {'color': 'green', 'label': 'Encendido DLV (PWRN_V)', 'persona': 'Víctima'},
    'PWRN_A': {'color': 'green', 'label': 'Encendido DLI (PWRN_A)', 'persona': 'Inculpado'},
    'CONNB_A': {'color': 'lightgreen', 'label': 'Conexión Brazalete DLI (CONNB_A)', 'persona': 'Inculpado'},
    'DISCONB_A': {'color': 'gray', 'label': 'Desconexión Brazalete DLI (DISCONB_A)', 'persona': 'Inculpado'},
    'BATCN_A': {'color': 'orange', 'label': 'Enchufado cargador DLI (BATCN_A)', 'persona': 'Inculpado'},
    'BATCF_A': {'color': 'lightgray', 'label': 'Desenchufado cargador DLI (BATCF_A)', 'persona': 'Inculpado'},
    'BATCN_V': {'color': 'orange', 'label': 'Enchufado cargador DLV (BATCN_V)', 'persona': 'Víctima'},
    'BATCF_V': {'color': 'lightgray', 'label': 'Desenchufado cargador DLV (BATCF_V)', 'persona': 'Víctima'},
    'BCS_A': {'color': 'orange', 'label': 'Batería Crítica DLI (BCS_A)', 'persona': 'Inculpado'},
    'BCS_V': {'color': 'orange', 'label': 'Batería Crítica DLV (BCS_V)', 'persona': 'Víctima'},
    'CBCS_A': {'color': 'green', 'label': 'Fin Batería Crítica DLI (CBCS_A)', 'persona': 'Inculpado'},
    'CBCS_V': {'color': 'green', 'label': 'Fin Batería Crítica DLV (CBCS_V)', 'persona': 'Víctima'}
}

# Diccionario para agrupar tipos de evento
EVENT_GROUPS = {
    'Encendido': ['PWRN_A', 'PWRN_V'],
    'Apagado': ['PWRF_A', 'PWRF_V'],
    'Sin Comunicacion': ['SSC_A', 'SSC_V'],
    'Con Comunicacion': ['CSSC_A', 'CSSC_V'],
    'Proximidad': ['PROX'],
    'Entrada en Zona': ['EZEF', 'EZEM'],
    'Salida de Zona': ['SZEF', 'SZEM'],
    'Conexión Brazalete': ['CONNB_A'],
    'Desconexión Brazalete': ['DISCONB_A'],
    'Cargador Conectado': ['BATCN_A', 'BATCN_V'],
    'Cargador Desconectado': ['BATCF_A', 'BATCF_V'],
    'Batería Crítica': ['BCS_A', 'BCS_V'],
    'Fin Batería Crítica': ['CBCS_A', 'CBCS_V'],
}

# Lista para definir el orden de los filtros en el mapa
EVENT_GROUP_ORDER = [
    'Encendido',
    'Apagado',
    'Proximidad',
    'Con Comunicacion',
    'Sin Comunicacion',
    'Conexión Brazalete',
    'Desconexión Brazalete',
    'Entrada en Zona',
    'Salida de Zona',
    'Cargador Conectado',
    'Cargador Desconectado',
    'Batería Crítica',
    'Fin Batería Crítica'
]