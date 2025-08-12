# monitor.py
from fastapi import APIRouter
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time
import psutil

monitor = APIRouter()
start_time = time.time()

# Prometheus metrics
REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")
CPU_USAGE = Gauge("app_cpu_percent", "CPU usage percent")
MEMORY_USAGE = Gauge("app_memory_percent", "Memory usage percent")
UPTIME = Gauge("app_uptime_seconds", "Application uptime in seconds")
REQUEST_DURATION = Histogram("app_request_duration_seconds", "Duration of requests in seconds")

@monitor.get("/health")
def health_check():
    return {"status": "ok"}

@monitor.get("/metrics")
def metrics():
    REQUEST_COUNT.inc()
    uptime = int(time.time() - start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    CPU_USAGE.set(cpu)
    MEMORY_USAGE.set(mem)
    UPTIME.set(uptime)

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
