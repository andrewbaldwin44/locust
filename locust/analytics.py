import locust

import os
import platform
import time
import uuid

import configargparse
from posthog import Posthog

from .argument_parser import LocustArgumentParser
from .config import LOCUST_CONF_FILE, Analytics, Config, read_config, write_config

ENABLED_MESSAGE = """*Attention*: Locust now collects completely anonymous analytics regarding usage.
This data is used to improve Locust and prioritize features.
You can learn more, including how to opt-out, by visiting the following URL:
https://docs.locust.io/en/stable/index.html"""
DISABLED_MESSAGE = f"""Your preference has been saved to {LOCUST_CONF_FILE}.

Status: Disabled

You have opted-out of Locust's anonymous analytics program.
No data will be collected from your machine.

Hint: Use LOCUST_DISABLE_ANALYTICS=1 to disable analytics for CLI runs

Learn more: https://docs.locust.io/en/stable/index.html"""

ph = None
anonymous_id = None


def analytics_init(args: configargparse.Namespace, parser: LocustArgumentParser):
    global ph
    global anonymous_id

    config = read_config()
    if args.disable_analytics or not config.analytics.enabled:
        if config.analytics.enabled and not os.environ.get("LOCUST_DISABLE_ANALYTICS"):
            print(DISABLED_MESSAGE)
            write_config(Config(analytics=Analytics(enabled=False)))
        return

    if not config.analytics.notifiedAt:
        print(ENABLED_MESSAGE)
        write_config(
            Config(
                analytics=Analytics(
                    enabled=True,
                    notifiedAt=int(time.time()),
                    anonymousId=str(uuid.uuid4()),
                )
            )
        )
        # Don't enable analytics until they have had a chance to opt-out
        return

    ph = Posthog(
        "phc_qpEEsMexMgX3Lo6AqxZqGpsCnhbwj8AtyuTRepBaypn",
        host="https://us.i.posthog.com",
    )
    anonymous_id = config.analytics.anonymousId

    ph.capture(
        distinct_id=anonymous_id,
        event="$identify",
        properties={
            "os": platform.system().lower(),
            "python_version": platform.python_version(),
            "locust_version": locust.__version__,
        },
    )

    # Track boolean args to know if / how many users are using these features
    features = [
        "num_users",
        "spawn_rate",
        "run_time",
        "headless",
        "autostart",
        "autoquit",
        "headful",
        "web_auth",
        "web_login",
        "class_picker",
        "legacy_ui",
        "master",
        "expect_workers",
        "expect_workers_max_wait",
        "processes",
        "stats_history_enabled",
        "print_stats",
        "only_summary",
        "reset_stats",
        "json",
        "skip_log_setup",
        "show_task_ratio",
        "show_task_ratio_json",
        "exit_code_on_error",
        "otel",
        "cloud",
    ]

    raw_args = vars(args)
    default_args = vars(parser.parse_args(args=[]))
    sanitized_args = {
        arg_name: raw_args[arg_name] for arg_name in features if default_args[arg_name] != raw_args[arg_name]
    }

    ph.capture(distinct_id=anonymous_id, event="cli_args", properties=sanitized_args)
