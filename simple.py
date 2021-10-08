import bme680
import time
import asyncio 
import socket
from starlette.applications import Starlette
from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi import FastAPI, BackgroundTasks
from prometheus_client import Counter, Gauge, CollectorRegistry, start_http_server
from prometheus_client.core import CounterMetricFamily, REGISTRY, GaugeMetricFamily

from loguru import logger


class BME688Collector(object):
    def __init__(self):
        try: 
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        ...

    def collect(self):
        logger.info("collecting metrics")
        while not self.sensor.get_sensor_data():
            time.sleep(1)

        logger.info("yielding counter")
        #yield GaugeMetricFamily("my_gauge", "help text", value=7)
        value = CounterMetricFamily("SENSOR_STATUS", "Sensor Status", labels="value")
        value.add_metric(["temperature"], self.sensor.data.temperature)
        value.add_metric(["pressure"], self.sensor.data.pressure)
        value.add_metric(["humidity"], self.sensor.data.humidity)
        yield value

REGISTRY.register(BME688Collector())

logger.info("starting server...")
start_http_server(9756)
logger.info("done server...")

while True:
    time.sleep(2)
