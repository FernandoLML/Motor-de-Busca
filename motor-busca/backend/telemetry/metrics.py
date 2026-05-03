from opentelemetry import metrics

_meter = None


def get_meter():
    global _meter
    if _meter is None:
        _meter = metrics.get_meter("motor-busca")
    return _meter


def get_instruments():
    meter = get_meter()
    return {
        "search_duration": meter.create_histogram(
            name="search_duration_ms",
            description="Tempo de execução da busca em milissegundos",
            unit="ms",
        ),
        "search_requests": meter.create_counter(
            name="search_requests_total",
            description="Total de requisições de busca",
        ),
        "document_size": meter.create_histogram(
            name="document_size_chars",
            description="Tamanho do documento em caracteres",
            unit="chars",
        ),
    }


# Singleton instruments
_instruments = None


def instruments():
    global _instruments
    if _instruments is None:
        _instruments = get_instruments()
    return _instruments
