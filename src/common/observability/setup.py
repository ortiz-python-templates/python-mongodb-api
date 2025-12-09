from src.common.config.env_config import EnvConfig
from src.common.observability.logger import setup_logger
from src.common.observability.metrics import setup_metrics
from src.common.observability.tracing import setup_tracing


class ObservabilitySetup:

    @classmethod
    def setup(cls, app, service_name=EnvConfig.APP_NAME, jaeger_host="jaeger", jaeger_port=6831):
        # Logger
        cls.logger = setup_logger()

        # Metrics
        setup_metrics(app)

        # Tracing
        setup_tracing(app, service_name=service_name, jaeger_host=jaeger_host, jaeger_port=jaeger_port)
