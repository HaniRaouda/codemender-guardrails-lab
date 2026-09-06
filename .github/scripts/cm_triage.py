#!/usr/bin/env python3
import json, os, sys

def main():
    report_file = sys.argv[1] if len(sys.argv) > 1 else "cm-security-report.json"
    max_fix_count = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    if not os.path.exists(report_file):
        set_output("gate_status", "PASSED")
        set_output("target_ids", "")
        return

    with open(report_file, "r") as f:
        try:
            data = json.load(f)
        except Exception as e:
            data = []

    findings = data if isinstance(data, list) else data.get("findings", [])
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    targets = []

    for item in findings:
        severity = item.get("Severity", item.get("severity", "")).upper()
        status = item.get("Status", item.get("status", "OPEN")).upper()
        finding_id = item.get("FindingID", item.get("finding_id", item.get("id", "")))
        vuln_type = item.get("VulnType", "").lower()

        if severity in severity_counts:
            severity_counts[severity] += 1

        # Block on CRITICAL, HIGH, or any Hardcoded Credential / MEDIUM finding
        if status in ("OPEN", "") and (severity in ("CRITICAL", "HIGH") or "credential" in vuln_type or severity == "MEDIUM"):
            if finding_id and finding_id not in targets:
                targets.append(finding_id)

    print(f"CodeMender Triage: CRITICAL={severity_counts['CRITICAL']}, HIGH={severity_counts['HIGH']}, MEDIUM={severity_counts['MEDIUM']}")
    gate_failed = len(targets) > 0
    gate_status = "FAILED" if gate_failed else "PASSED"
    selected_targets = targets[:max_fix_count]
    target_ids_str = " ".join(selected_targets)

    print(f"Gate Status: {gate_status}")
    print(f"Target IDs for auto-fix: {target_ids_str}")

    set_output("gate_status", gate_status)
    set_output("critical_count", str(severity_counts["CRITICAL"]))
    set_output("high_count", str(severity_counts["HIGH"]))
    set_output("target_ids", target_ids_str)

def set_output(name, value):
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{name}={value}\n")
    print(f"[OUTPUT] {name}={value}")

if __name__ == "__main__":
    main()
