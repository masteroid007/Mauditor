
from mauditor.core.models import Severity


def validate_config(config: dict) -> None:
    if not isinstance(config, dict):
        raise TypeError("Configuration must be a dictionary.")

    validate_scanner(config.get("scanner", {}))
    validate_rules(config.get("rules", {}))
    validate_severity(config.get("severity", {}))
    validate_report(config.get("report", {}))
    validate_output(config.get("output", {}))


def validate_scanner(scanner: dict) -> None:
    if not isinstance(scanner, dict):
        raise TypeError("'scanner' must be a table.")

    if "recursive" in scanner:
        if not isinstance(scanner["recursive"], bool):
            raise TypeError("'scanner.recursive' must be a boolean.")

    if "exclude" in scanner:
        if not isinstance(scanner["exclude"], list):
            raise TypeError("'scanner.exclude' must be a list.")

        if not all(isinstance(item, str) for item in scanner["exclude"]):
            raise TypeError("'scanner.exclude' must contain only strings.")


def validate_rules(rules: dict) -> None:
    if not isinstance(rules, dict):
        raise TypeError("'rules' must be a table.")

    for key in ("enabled", "disabled"):
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

    if "format" in report:
        if report["format"] not in ("json",):
            raise ValueError("'report.format' must be 'json'.")

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