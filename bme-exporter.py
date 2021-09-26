#import bme680
import time

from starlette.applications import Starlette
from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi import FastAPI
from prometheus_client import Counter, Gauge

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name="bme688", prefix="bme", )
app.add_route("/metrics", handle_metrics)


TEMPERATURE = Gauge("temperature", "temperature_of_device")

async def some_view(request):
    TEMPERATURE.labels("some_view").inc()
    return 

def metrics():
    pass


