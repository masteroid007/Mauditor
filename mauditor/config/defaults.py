
import tomllib

from mauditor.config.loader import CONFIG_DIR, CONFIG_PATH
from mauditor.config.validator import validate_config


DEFAULT_CONFIG = """\
[scanner]
exclude = [
    "__pycache__",
    ".venv",
    "venv",
    ".git"
]

[rules]
disabled = []

[severity]
minimum = "LOW"

[report]
enabled = True
output = "reports/report.json"

[output]
colors = True
show_summary = True 
"""
# summary fatto
# report fatto

def get_config() -> dict:
    if not CONFIG_PATH.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(DEFAULT_CONFIG, encoding="utf-8")

    with CONFIG_PATH.open("rb") as file:
        config = tomllib.load(file)
    
    validate_config(config)
    return config
    
