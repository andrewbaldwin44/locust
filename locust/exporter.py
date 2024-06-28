import atexit
import csv
import os
from datetime import datetime

import gevent
import requests
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


class LocustExporter:
    def __init__(self):
        self.stat_entries = {}
        self._points = []
        client = InfluxDBClient(
            url="http://localhost:8086",
            token=os.environ.get("INFLUXDB_TOKEN"),
            org="ORG",
        )
        self._bucket = "bucket"
        self._write_api = client.write_api(write_options=SYNCHRONOUS)
        self._query_api = client.query_api()

        self._greenlet = gevent.spawn(self._on_start)

        atexit.register(self._on_exit)

    def _on_start(self):
        while True:
            # Copy and clear list so only new points are sent each cycle
            points = self._points.copy()
            self._points.clear()
            self._write_api.write(record=points, bucket=self._bucket)
            gevent.sleep(0.5)

    def _format_point(self, measurement, tags, fields):
        return {"measurement": measurement, "tags": tags, "fields": fields, "time": datetime.utcnow().isoformat()}

    def _on_exit(self):
        self._greenlet.kill()

    def register(self, stat_entries):
        self.stat_entries = stat_entries

    def export(self, name, method, success=True, **fields):
        measurement = "request_success" if success else "request_failure"
        point = self._format_point(measurement, tags={"name": name, "method": method}, fields=fields)

        self._points.append(point)

    def get_stats(self):
        try:
            influxql_query = f"""
                from(bucket: "{self._bucket}")
                    |> range(start: -5m)
                    |> filter(fn: (r) => r["_measurement"] == "request_success" and r["_field"] == "response_time")
                    |> aggregateWindow(every: 1s, fn: max, createEmpty: false)
                    |> yield(name: "max")

                from(bucket: "{self._bucket}")
                            |> range(start: -5m)
                            |> filter(fn: (r) => r["_measurement"] == "request_success" and r["_field"] == "response_time")
                            |> aggregateWindow(every: 1s, fn: median, createEmpty: false)
                            |> aggregateWindow(every: 1s, fn: min, createEmpty: false)
                            |> yield(name: "min")

                from(bucket: "{self._bucket}")
                            |> range(start: -5m)
                            |> filter(fn: (r) => r["_measurement"] == "request_success" and r["_field"] == "response_time")
                            |> aggregateWindow(every: 1s, fn: median, createEmpty: false)
                            |> yield(name: "median")
            """
            response = self._query_api.query(influxql_query)
            return response
        except Exception as e:
            print(e)
