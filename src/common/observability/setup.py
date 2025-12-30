from src.common.config.env_config import EnvConfig
from src.common.observability.logger import LoggerSetup
from src.common.observability.metrics import MetricsSetup
from src.common.observability.tracing import TracingSetup


class ObservabilitySetup:

    @classmethod
    def setup(cls, app, service_name=EnvConfig.APP_NAME, jaeger_host="jaeger", jaeger_port=6831):
        # Logger
        cls.logger = LoggerSetup.setup()

        # Metrics
        MetricsSetup.setup(app)

        # Tracing
        TracingSetup.setup(app, service_name=service_name, jaeger_host=jaeger_host, jaeger_port=jaeger_port)
