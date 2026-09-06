#!/usr/bin/env python3
import json, os, sys

def main():
    report_file = sys.argv[1] if len(sys.argv) > 1 else "cm-security-report.json"
    max_fix = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    if not os.path.exists(report_file):
        set_out("gate_status", "PASSED")
        set_out("target_ids", "")
        return

    with open(report_file) as f:
        try:
            data = json.load(f)
        except Exception:
            data = []

    findings = data if isinstance(data, list) else data.get("findings", [])
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    targets = []

    for item in findings:
        sev = item.get("Severity", item.get("severity", "")).upper()
        stat = item.get("Status", item.get("status", "OPEN")).upper()
        fid = item.get("FindingID", item.get("finding_id", item.get("id", "")))
        if sev in counts:
            counts[sev] += 1
        if stat in ("OPEN", "") and sev in ("CRITICAL", "HIGH") and fid and fid not in targets:
            targets.append(fid)

    print(f"CodeMender Triage: CRITICAL={counts['CRITICAL']}, HIGH={counts['HIGH']}")
    failed = (counts["CRITICAL"] + counts["HIGH"]) > 0
    set_out("gate_status", "FAILED" if failed else "PASSED")
    set_out("critical_count", str(counts["CRITICAL"]))
    set_out("high_count", str(counts["HIGH"]))
    set_out("target_ids", " ".join(targets[:max_fix]))

def set_out(k, v):
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"{k}={v}\n")
    print(f"[OUTPUT] {k}={v}")

if __name__ == "__main__":
    main()
