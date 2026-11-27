
import tomllib

from mauditor.config.loader import CONFIG_DIR, CONFIG_PATH
from mauditor.config.validator import validate_config


DEFAULT_CONFIG = """\
[rules]
disabled = []

[severity]
minimum = "LOW"

[report]
enabled = true
output = "reports/report.json"

[output]
colors = true
show_summary = true
"""
# output fatto
# report fatto

def get_config() -> dict:
    if not CONFIG_PATH.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(DEFAULT_CONFIG, encoding="utf-8")

    try:
        with CONFIG_PATH.open("rb") as file:
            config = tomllib.load(file)

    except tomllib.TOMLDecodeError as error:
        raise ValueError(
            f"Invalid TOML configuration: {error}"
        ) from error

    validate_config(config)
    return config
