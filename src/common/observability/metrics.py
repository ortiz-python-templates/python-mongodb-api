from prometheus_fastapi_instrumentator import Instrumentator

def setup_metrics(app):
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_instrument_requests_inprogress=True
    )
    instrumentator.instrument(app).expose(app, endpoint="/metrics")
