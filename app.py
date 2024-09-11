import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPTraceExporter
from opentelemetry.sdk.trace import Span

# Initialize the OTLP trace exporter
trace_exporter = OTLPTraceExporter(endpoint="http://otel-collector.default.svc.cluster.local:4317", insecure=True)

# Set up the TracerProvider and span processor
trace_provider = TracerProvider()
trace.set_tracer_provider(trace_provider)
tracer = trace.get_tracer(__name__)

span_processor = BatchSpanProcessor(trace_exporter)
trace_provider.add_span_processor(span_processor)

# Generate test traces
def main():
    for i in range(100):
        with tracer.start_as_current_span(f"test-span-{i}") as span:
            span.set_attribute("test.attribute", "value")
            print(f"Sent trace {i+1}")
            time.sleep(1)

if __name__ == "__main__":
    main()
