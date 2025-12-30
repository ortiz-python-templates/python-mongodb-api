from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


class TracingSetup:

    @staticmethod
    def setup(app, service_name="python-mongodb-api", jaeger_host="jaeger", jaeger_port=6831):    
        # Set tracer provider
        trace.set_tracer_provider(
            TracerProvider(resource=Resource.create({"service.name": service_name}))
        )

        # Try to configure Jaeger exporter
        try:
            jaeger_exporter = JaegerExporter(
                agent_host_name=jaeger_host,
                agent_port=jaeger_port,
            )
            span_processor = BatchSpanProcessor(jaeger_exporter)
            trace.get_tracer_provider().add_span_processor(span_processor)
            print(f"Jaeger tracing enabled: {jaeger_host}:{jaeger_port}")
        except Exception as e:
            print(f"Could not initialize Jaeger tracing: {e}")
        
        # Instrument FastAPI and requests
        FastAPIInstrumentor.instrument_app(app)
        RequestsInstrumentor().instrument()
