
from mauditor.core.models import Severity


def validate_config(config: dict) -> None:
    if not isinstance(config, dict):
        raise TypeError("Configuration must be a dictionary.")

    validate_rules(config.get("rules", {}))
    validate_severity(config.get("severity", {}))
    validate_report(config.get("report", {}))
    validate_output(config.get("output", {}))


def validate_rules(rules: dict) -> None:
    if not isinstance(rules, dict):
        raise TypeError("'rules' must be a table.")

    for key in ("enabled"):
        if key in rules:
            if not isinstance(rules[key], list):
                raise TypeError(f"'rules.{key}' must be a list.")

            if not all(isinstance(item, str) for item in rules[key]):
                raise TypeError(f"'rules.{key}' must contain only strings.")


def validate_severity(severity: dict) -> None:
    if not isinstance(severity, dict):
        raise TypeError("'severity' must be a table.")

    if "minimum" in severity:
        valid_severities = {item.name for item in Severity}

        if severity["minimum"] not in valid_severities:
            raise ValueError(
                f"Invalid minimum severity: {severity['minimum']}"
            )


def validate_report(report: dict) -> None:
    if not isinstance(report, dict):
        raise TypeError("'report' must be a table.")

    if "enabled" in report:
        if not isinstance(report["enabled"], bool):
            raise TypeError("'report.enabled' must be a boolean.")

    if "output" in report:
        if not isinstance(report["output"], str):
            raise TypeError("'report.output' must be a string.")


def validate_output(output: dict) -> None:
    if not isinstance(output, dict):
        raise TypeError("'output' must be a table.")

    for key in ("colors", "show_summary"):
        if key in output:
            if not isinstance(output[key], bool):
                raise TypeError(f"'output.{key}' must be a boolean.")