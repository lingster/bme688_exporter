import bme680
import time
import asyncio 
import socket
from starlette.applications import Starlette
from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi import FastAPI, BackgroundTasks
from prometheus_client import Counter, Gauge, CollectorRegistry
from prometheus_client.core import CounterMetricFamily, REGISTRY
from loguru import logger


class BME688Collector(object):
    def __init__(self):
        try: 
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        ...

    async def collect(self):
        while not self.sensor.get_sensor_data():
            await asyncio.sleep(1)
        value = CounterMetricFamily("SENSOR_STATUS", "Help Text", labels="value")
        value.add_metric(["temperature"], self.sensor.data.temperature
        value.add_metric(["pressure"], self.sensor.data.temperature
        value.add_metric(["humidity"], self.sensor.data.temperature
        yield value

REGISTRY.register(BME688Collector())



    

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name="bme688", prefix="bme", )
app.add_route("/metrics", handle_metrics)

hostname = socket.gethostname()

registry = CollectorRegistry()
#TEMPERATURE = Gauge("sensor", "temperature_of_device", ("temperature", "pressure", "humidity",), registry=registry)
#TEMPERATURE = Gauge("sensor", "temperature_of_device", ("event_name",), registry=registry)
TEMPERATURE = Gauge("temperature", "temperature", ["event_name",], registry=registry)
TEMPERATURE.labels('Start')
PRESSURE = Gauge("pressure", "air pressure-hPa", ["hostname",], registry=registry)
HUMIDITY = Gauge("humidity", "humidity(%RH)", ["hostname",], registry=registry)

try: 
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

async def get_sensor_data
while not sensor.get_sensor_data(): 
    sleep(0.5)
    logger.info(f"waiting for sensor data")
TEMPERATURE.labels('Start').set(sensor.data.temperature)

async def async_get_temp(): 
    logger.info("starting async_get_temp()")
    while True:
        while not sensor.get_sensor_data():
            logger.info(f'sensor data not ready yet....')
            await asyncio.sleep(1)
        #return (sensor.data.temperature, sensor.data.pressure, sensor.data.humidity) 
        TEMPERATURE.labels(event_name="get_sensor").set(sensor.data.temperature)
        PRESSURE.labels(hostname=hostname).set(sensor.data.pressure)
        HUMIDITY.labels(hostname=hostname).set(sensor.data.humidity)
        await asyncio.sleep(0.5)

bg = asyncio.create_task(async_get_temp())

@app.get("/sensor")
async def get_sensor():
    #logger.info(f"{sensor.data.temperature}c / {sensor.data.pressure} hPa / {sensor.data.humidity} %RH")
    #await async_get_temp()
    sensor.get_sensor_data()
    #TEMPERATURE.labels({"temperature": "c"}).set(sensor.data.temperature)
    #TEMPERATURE.labels({"pressure": "hPa"}).set(sensor.data.pressure)
    #TEMPERATURE.labels({"humidity": "%RH"}).set(sensor.data.humidity)
    #TEMPERATURE.labels(event_name="get_sensor", hostname=hostname).set(sensor.data.temperature)
    #PRESSURE.labels(event_name="get_sensor", hostname=hostname).set(sensor.data.pressure)
    #HUMIDITY.labels(event_name="get_sensor", hostname=hostname).set(sensor.data.humidity)
    TEMPERATURE.labels(event_name="get_sensor").set(sensor.data.temperature)
    #PRESSURE.labels(hostname=hostname).set(sensor.data.pressure)
    #HUMIDITY.labels(hostname=hostname).set(sensor.data.humidity)

    return {"temperature": {sensor.data.temperature}, 
            "pressure": {sensor.data.pressure},
            "humidity": {sensor.data.humidity}}

