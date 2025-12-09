import json
import pathlib
from dataclasses import asdict, dataclass, field

import platformdirs

LOCUST_CONF_FILE = pathlib.Path(platformdirs.user_config_dir(appname="locust"), "config.json")


@dataclass
class Analytics:
    enabled: bool = True
    anonymousId: str | None = None
    notifiedAt: int | None = None


@dataclass
class Config:
    analytics: Analytics | None = field(default_factory=Analytics)


def read_config() -> Config:
    if LOCUST_CONF_FILE.exists():
        with open(LOCUST_CONF_FILE) as f:
            data = json.load(f)
            return Config(analytics=Analytics(**data["analytics"]))

    return Config()


def write_config(config: Config) -> None:
    LOCUST_CONF_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(LOCUST_CONF_FILE, "w") as f:
        json.dump(asdict(config), f)
