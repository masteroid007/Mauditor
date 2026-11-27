
import argparse
from collections import Counter
from pathlib import Path
from time import perf_counter

from colored_print import log

from mauditor import __version__
from mauditor.core.auditor import Auditor
from mauditor.core.models import Finding, Severity
from mauditor.core.rules.registry import Registry
from mauditor.cli.formatting import hyperlink
from mauditor.core.report import Report
from mauditor.config.defaults import get_config


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maudit",
        description=(
            "Mauditor - Python Security Auditor\n\n"
            "A static analysis tool designed to identify potential "
            "security vulnerabilities in Python projects."
        ),
        epilog=(
            "Examples:\n"
            "  maudit ./my-project\n"
            "  maudit /path/to/project\n"
            "  maudit --version\n"
            "  maudit --rules\n"
            "  maudit --noreport ./my-project\n\n"
            "Project:\n"
            "  https://github.com/masteroid007/MasterAuditor"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "target",
        type=Path,
        metavar="TARGET",
        nargs="?",
        help="Path to the Python project to analyze.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the program's version number and exit.",
    )

    parser.add_argument(
        "--rules",
        action="store_true",
        help="Show available security rules.",
    )
    
    parser.add_argument(
        "--noreport",
        action="store_true",
        help="Do not generate a report file.",
    )

    return parser


def print_rules() -> None:
    registry = Registry.default()

    config = get_config()
    if config.get("output", {}).get("colors", True):
        log.pink("=" * 80)
        log.pink("  AVAILABLE SECURITY RULES")
        log.pink("=" * 80)

        for rule_id, rule_class in sorted(
            registry.get_all_rules().items()
        ):
            rule = rule_class()

            log.info(
                f"{rule_id:<10} | "
                f"{rule.__class__.__name__:<40} | "
                f"Severity: {rule.severity.name:<8}"
            )

        log.pink("=" * 80)
        log.success(f"Total rules: {len(registry.get_all_rules())}")
    else:
        print("=" * 80)
        print("  AVAILABLE SECURITY RULES")
        print("=" * 80)
        
        for rule_id, rule_class in sorted(
            registry.get_all_rules().items()
        ):
            rule = rule_class()
        
            print(
                f"{rule_id:<10} | "
                f"{rule.__class__.__name__:<40} | "
                f"Severity: {rule.severity.name:<8}"
            )
        
        print("=" * 80)
        print(f"Total rules: {len(registry.get_all_rules())}")


def print_header(target: Path) -> None:
    config = get_config()
    if config.get("output", {}).get("colors", True):
        log.pink("=" * 60)
        log.pink("  MAUDITOR - PYTHON SECURITY AUDITOR")
        log.pink("=" * 60)

        log.info(f"Version: {__version__}")
        log.info(f"Target:  {target.resolve()}")
        log.success("\nStarting security analysis...\n")
    else:
        print("=" * 60)
        print("  MAUDITOR - PYTHON SECURITY AUDITOR")
        print("=" * 60)

        print(f"Version: {__version__}")
        print(f"Target:  {target.resolve()}")
        print("\nStarting security analysis...\n")


def print_finding(index: int, finding: Finding) -> None:
    config = get_config()
    location = hyperlink(
        str(finding.file_path),
        Path(finding.file_path)
        )
    if config.get("output", {}).get("colors", True):
        log("-" * 60)

        log.info(f"Finding #{index}")
        log(f"Rule ID:  {finding.rule_id}")
        log(f"Category: {finding.category}")
        log(f"CWE ID:   {finding.cwe_id}")
        log(f"Message:  {finding.message}")
        log(f"Location: {location}")
        log(f"Line:     {finding.line}")

        severity = finding.severity
        severity_message = f"Severity: {severity.name}"

        if severity == Severity.CRITICAL:
            log.critical(severity_message)
        elif severity == Severity.HIGH:
            log.error(severity_message)
        elif severity == Severity.MEDIUM:
            log.warning(severity_message)
        else:
            log.info(severity_message)
    else:
        print("-" * 60)

        print(f"Finding #{index}")
        print(f"Rule ID:  {finding.rule_id}")
        print(f"Category: {finding.category}")
        print(f"CWE ID:   {finding.cwe_id}")
        print(f"Message:  {finding.message}")
        print(f"Location: {location}")
        print(f"Line:     {finding.line}")

        severity = finding.severity
        severity_message = f"Severity: {severity.name}"

        if severity == Severity.CRITICAL:
            print(severity_message)
        elif severity == Severity.HIGH:
            print(severity_message)
        elif severity == Severity.MEDIUM:
            print(severity_message)
        else:
            print(severity_message)


def print_summary(
    findings: list[Finding],
    scan_duration: float
) -> None:
    config = get_config()
    if config.get("output", {}).get("colors", True):
        log("\n" + "=" * 60)
        log.pink("  SCAN SUMMARY")
        log("=" * 60)

        total = len(findings)
        log(f"Total findings: {total}")

        counts = Counter(finding.severity for finding in findings)

        for severity in Severity:
            count = counts.get(severity, 0)
            message = f"{severity.name:<10}: {count}"

            if severity == Severity.CRITICAL:
                log.critical(message)
            elif severity == Severity.HIGH:
                log.error(message)
            elif severity == Severity.MEDIUM:
                log.warning(message)
            else:
                log.info(message)

        log("=" * 60)

        if total == 0:
            log.success(
                "No findings found. Your scan completed successfully."
            )
        else:
            log.warning(f"Scan completed with {total} finding(s).")
        
        log.info(f"All findings have been filtered starting from {config.get("severity", {}).get("minimum")}")

        log.info(f"Scan time: {scan_duration:.2f} seconds")
    else:
        print("\n" + "=" * 60)
        print("  SCAN SUMMARY")
        print("=" * 60)

        total = len(findings)
        print(f"Total findings: {total}")

        counts = Counter(finding.severity for finding in findings)

        for severity in Severity:
            count = counts.get(severity, 0)
            message = f"{severity.name:<10}: {count}"

            if severity == Severity.CRITICAL:
                print(message)
            elif severity == Severity.HIGH:
                print(message)
            elif severity == Severity.MEDIUM:
                print(message)
            else:
                print(message)

        print("=" * 60)

        if total == 0:
            print(
                "No findings found. Your scan completed successfully."
            )
        else:
            print(f"Scan completed with {total} finding(s).")
        
        print(f"All findings have been filtered starting from {config.get("severity", {}).get("minimum")}")

        print(f"Scan time: {scan_duration:.2f} seconds")


def main() -> int:
    parser = create_parser()
    args = parser.parse_args()
    config = get_config()

    if args.rules:
        print_rules()
        return 0

    target = args.target

    if target is None:
        parser.error(
            "Target path is required. "
            "Please specify a directory to analyze."
        )

    if not target.exists():
        parser.error(f"Target does not exist: {target}")

    if not target.is_dir():
        parser.error(f"Target is not a directory: {target}")

    start_time = perf_counter()

    print_header(target)

    findings = Auditor().run(target)

    for index, finding in enumerate(findings, start=1):
        if config.get("severity", {}).get("minimum", "LOW"):
            print_finding(index, finding)
        elif config.get("severity", {}).get("minimum", "MEDIUM") and str(finding.severity) in ["MEDIUM", "HIGH", "CRITICAL"]:
            print_finding(index, finding)
        elif config.get("severity", {}).get("minimum", "HIGH") and str(finding.severity) in ["HIGH", "CRITICAL"]:
            print_finding(index, finding)
        elif config.get("severity", {}).get("minimum", "CRITICAL") and str(finding.severity) in ["CRITICAL"]:
            print_finding(index, finding)

    scan_duration = perf_counter() - start_time

    if config.get("output", {}).get("show_summary", True):
        print_summary(findings, scan_duration)

    if not args.noreport and config.get("report", {}).get("enabled", True):
        report = Report(
            findings=findings,
            scan_duration=scan_duration,
            directory=str(target.resolve())
        )

        report_path = report.write_json("reports")

    if config.get("report", {}).get("enabled", True) and config.get("output", {}).get("colors", True):
        log.success(f"Report generated: {report_path}")
    elif config.get("report", {}).get("enabled", True):
        print(f"Report generated: {report_path}")

    return 1 if findings else 0