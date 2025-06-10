# Placeholder: Prometheus metrics exporter
from prometheus_client import start_http_server, Gauge
import time

def start_exporter() -> None:
    g = Gauge('model_latency_seconds', 'Model prediction latency')
    start_http_server(8001)
    while True:
        g.set(0.1)  # Dummy value
        time.sleep(5)

if __name__ == "__main__":
    start_exporter() 