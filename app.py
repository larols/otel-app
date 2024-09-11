import time
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import Counter

# Initialize the OTLP metric exporter
exporter = OTLPMetricExporter(endpoint="http://otel-collector.default.svc.cluster.local:4317", insecure=True)

# Set up the MeterProvider and exporter
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Create a counter for test metrics
requests_counter = meter.create_counter(
    name="otel.requests",  # Updated metric name to include 'otel'
    description="A simple counter for test requests",
)

# Generate test metrics
def main():
    for i in range(100):
        requests_counter.add(1)  # Increment the counter
        print(f"Sent metric {i+1}")
        time.sleep(1)

if __name__ == "__main__":
    main()
