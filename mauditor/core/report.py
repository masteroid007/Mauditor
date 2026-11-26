
import json
import time
from collections import Counter
from pathlib import Path

from mauditor import __version__


class Report:
    def __init__(
        self,
        findings: list,
        scan_duration: float,
        directory: str,
    ):
        self.findings = findings
        self.scan_duration = scan_duration
        self.directory = directory

    def generate_metadata(self) -> dict:
        return {
            "tool": "Mauditor",
            "version": __version__,
            "generated_at": time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime()
            ),
            "target": self.directory,
            "scan_duration": round(self.scan_duration, 2),
        }

    def generate_summary(self) -> dict:
        severities = Counter(
            finding.severity.name
            if hasattr(finding.severity, "name")
            else str(finding.severity)
            for finding in self.findings
        )

        summary = {
            "total_findings": len(self.findings),
        }

        for severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"):
            summary[severity.lower()] = severities.get(severity, 0)

        return summary

    def generate_finding(self, finding, index: int) -> dict:
        severity = (
            finding.severity.name
            if hasattr(finding.severity, "name")
            else str(finding.severity)
        )

        return {
            "index": index,
            "rule_id": finding.rule_id,
            "category": finding.category or "N/A",
            "cwe_id": finding.cwe_id or "N/A",
            "message": finding.message or "N/A",
            "location": str(finding.file_path),
            "line": finding.line,
            "severity": severity,
        }

    def generate_json(self) -> dict:
        return {
            "metadata": self.generate_metadata(),
            "summary": self.generate_summary(),
            "findings": [
                self.generate_finding(finding, index)
                for index, finding in enumerate(self.findings, start=1)
            ],
        }

    def write_json(self, directory: str) -> str:
        output_dir = Path(directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        report_path = output_dir / "report.json"

        with report_path.open("w", encoding="utf-8") as file:
            json.dump(
                self.generate_json(),
                file,
                indent=4,
                ensure_ascii=False,
            )
            file.write("\n")

        return str(report_path)
