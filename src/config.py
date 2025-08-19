# Diccionario de configuración para todos los tipos de eventos
# {'green', 'gray', 'lightgreen', 'lightblue', 'blue', 'red', 'orange', 'cadetblue', 'lightgray', 'darkblue', 'white', 'darkgreen', 'pink', 'lightred', 'purple', 'darkpurple', 'darkred', 'black', 'beige'}
EVENT_CONFIG = {
    'SSC_A': {'color': 'gray', 'label': 'Sin comunicacion DLI', 'persona': 'Inculpado'},
    'SSC_V': {'color': 'gray', 'label': 'Sin comunicacion DLV', 'persona': 'Víctima'},
    'CSSC_A': {'color': 'lightblue', 'label': 'Con comunicacion DLI', 'persona': 'Inculpado'},
    'CSSC_V': {'color': 'lightblue', 'label': 'Con comunicacion DLV', 'persona': 'Víctima'},
    'PROX': {'color': 'darkred', 'label': 'Proximidad', 'persona': 'Inculpado'},
    'EZEF': {'color': 'red', 'label': 'Entrada en Zona Fija', 'persona': 'Inculpado'},
    'EZEM': {'color': 'red', 'label': 'Entrada en Zona Móvil', 'persona': 'Inculpado'},
    'SZEF': {'color': 'cadetblue', 'label': 'Salida de Zona Fija', 'persona': 'Inculpado'},
    'SZEM': {'color': 'cadetblue', 'label': 'Salida de Zona Móvil', 'persona': 'Inculpado'},
    'PWRF_V': {'color': 'black', 'label': 'Apagado DLV', 'persona': 'Víctima'},
    'PWRF_A': {'color': 'black', 'label': 'Apagado DLI', 'persona': 'Inculpado'},
    'PWRN_V': {'color': 'green', 'label': 'Encendido DLV', 'persona': 'Víctima'},
    'PWRN_A': {'color': 'green', 'label': 'Encendido DLI', 'persona': 'Inculpado'},
    'CONNB_A': {'color': 'lightgreen', 'label': 'Conexión Brazalete DLI', 'persona': 'Inculpado'},
    'DISCONB_A': {'color': 'gray', 'label': 'Desconexión Brazalete DLI', 'persona': 'Inculpado'},
    'BATCN_A': {'color': 'orange', 'label': 'Conectado cargador DLI', 'persona': 'Inculpado'},
    'BATCF_A': {'color': 'lightgray', 'label': 'Desconectado cargador DLI', 'persona': 'Inculpado'},
    'BATCN_V': {'color': 'orange', 'label': 'Conectado cargador DLV', 'persona': 'Víctima'},
    'BATCF_V': {'color': 'lightgray', 'label': 'Desconectado cargador DLV', 'persona': 'Víctima'},
    'BCS_A': {'color': 'orange', 'label': 'Batería Crítica DLI', 'persona': 'Inculpado'},
    'BCS_V': {'color': 'orange', 'label': 'Batería Crítica DLV', 'persona': 'Víctima'},
    'CBCS_A': {'color': 'green', 'label': 'Fin Batería Crítica DLI', 'persona': 'Inculpado'},
    'CBCS_V': {'color': 'green', 'label': 'Fin Batería Crítica DLV', 'persona': 'Víctima'}
}

# Diccionario para agrupar tipos de evento
EVENT_GROUPS = {
    'Encendido': ['PWRN_A', 'PWRN_V'],
    'Apagado': ['PWRF_A', 'PWRF_V'],
    'Sin Comunicación': ['SSC_A', 'SSC_V'],
    'Con Comunicación': ['CSSC_A', 'CSSC_V'],
    'Proximidad': ['PROX'],
    'Entrada Zona Fija': ['EZEF'],
    'Salida Zona Fija': ['SZEF'],
    'Entrada Zona Movil': ['EZEM'],
    'Salida Zona Movil': ['SZEM'],
    'Conexión Brazalete': ['CONNB_A'],
    'Desconexión Brazalete': ['DISCONB_A'],
    'Cargador Conectado': ['BATCN_A', 'BATCN_V'],
    'Cargador Desconectado': ['BATCF_A', 'BATCF_V'],
    'Bateria Crítica': ['BCS_A', 'BCS_V'],
    'Fin Bateria Critica': ['CBCS_A', 'CBCS_V'],
}
