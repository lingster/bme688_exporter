#!/bin/sh

uvicorn bme-exporter:app --host 0.0.0.0 --port 9180
