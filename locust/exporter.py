import time

import requests
from prometheus_client import Gauge, start_http_server

from .stats import PERCENTILES_TO_CHART

total_rps_gauge = Gauge("total_rps", "Total number of requests per second")
total_fail_per_sec_gauge = Gauge("total_fail_per_sec", "Total number of failures per second")
total_fail_ratio_gauge = Gauge("total_fail_ratio", "Percentage of total failures out of the total number of requests")
total_avg_response_time_gauge = Gauge("total_avg_response_time", "Total average response time")
user_count_gauge = Gauge("user_count", "Total number of Locust users")
current_response_time_percentiles_gauge = Gauge("current_response_time_percentiles", "Total number of Locust requests")
current_response_time_percentiles_gauges = {
    f"response_time_percentile_{percentile}": Gauge(
        f"current_response_time_{int(percentile * 100)}", f"{percentile}th percentile"
    )
    for percentile in PERCENTILES_TO_CHART
}


class LocustExporter:
    def __init__(self, environment):
        self.environment = environment
        self.stat_entries = {}

        start_http_server(8000)

    def register(self, stat_entries):
        self.stat_entries = stat_entries

    def export(self, stats_key):
        # current_stats = self.stat_entries[stats_key].to_dict()
        total_stats = self.environment.runner.stats.total
        total_stats_dict = total_stats.to_dict()

        total_rps = total_stats_dict["current_rps"]
        total_fail_per_sec = total_stats_dict["current_fail_per_sec"]
        total_fail_ratio = total_stats.fail_ratio
        total_avg_response_time = total_stats_dict["avg_response_time"]
        user_count = self.environment.runner.user_count

        total_rps_gauge.set(total_rps)
        total_fail_per_sec_gauge.set(total_fail_per_sec)
        total_fail_ratio_gauge.set(total_fail_ratio)
        total_avg_response_time_gauge.set(total_avg_response_time)
        user_count_gauge.set(user_count)

        for percentile in PERCENTILES_TO_CHART:
            current_response_time_percentiles_gauges[f"response_time_percentile_{percentile}"].set(
                total_stats.get_current_response_time_percentile(percentile)
            )

        # {__name__=~"total_rps|total_fail_per_sec"}
