
import tomllib

from mauditor.config.loader import CONFIG_DIR, CONFIG_PATH


DEFAULT_CONFIG = """\
[scanner]
recursive = true
exclude = [
    "__pycache__",
    ".venv",
    "venv",
    ".git"
]

[rules]
enabled = []
disabled = []

[severity]
minimum = "LOW"

[report]
enabled = true
format = "json"
output = "reports/report.json"

[output]
colors = true
show_summary = true
"""


def get_config() -> dict:
    if not CONFIG_PATH.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(DEFAULT_CONFIG, encoding="utf-8")

    with CONFIG_PATH.open("rb") as file:
        return tomllib.load(file)
