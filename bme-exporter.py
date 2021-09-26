import bme680
import time
import asyncio 
import socket
from starlette.applications import Starlette
from starlette_exporter import PrometheusMiddleware, handle_metrics
from fastapi import FastAPI
from prometheus_client import Counter, Gauge, CollectorRegistry
from loguru import logger

app = FastAPI()
app.add_middleware(PrometheusMiddleware, app_name="bme688", prefix="bme", )
app.add_route("/metrics", handle_metrics)

hostname = socket.gethostname()

registry = CollectorRegistry()
#TEMPERATURE = Gauge("sensor", "temperature_of_device", ("temperature", "pressure", "humidity",), registry=registry)
#TEMPERATURE = Gauge("sensor", "temperature_of_device", ("event_name",), registry=registry)
TEMPERATURE = Gauge("temperature", "temperature", ["event_name",], registry=registry)
TEMPERATURE.labels('Start')
#PRESSURE = Gauge("pressure", "air pressure-hPa", ("hostname",), registry=registry)
#HUMIDITY = Gauge("humidity", "humidity(%RH)", ("hostname",), registry=registry)

try: 
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

while not sensor.get_sensor_data(): 
    sleep(0.5)
    logger.info(f"waiting for sensor data")
TEMPERATURE.labels('Start').set(sensor.data.temperature)

async def async_get_temp(): 
    while not sensor.get_sensor_data():
        logger.info(f'sensor data not ready yet....')
        asyncio.sleep(1)
    return (sensor.data.temperature, sensor.data.pressure, sensor.data.humidity) 

@app.get("/sensor")
async def get_sensor():
    #logger.info(f"{sensor.data.temperature}c / {sensor.data.pressure} hPa / {sensor.data.humidity} %RH")
    await async_get_temp()
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


