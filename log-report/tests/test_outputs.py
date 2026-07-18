import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    top_path = paths.most_common(1)[0][0] if paths else None
    return {"total_requests": total, "unique_ips": len(ips), "top_path": top_path}


def _load_report():
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    try:
        return json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_report_has_required_fields():
    report = _load_report()
    for field in ("total_requests", "unique_ips", "top_path"):
        assert field in report, f"missing required field '{field}'"


def test_total_requests_correct():
    report = _load_report()
    expected = _expected()
    assert report["total_requests"] == expected["total_requests"], (
        f"total_requests: got {report['total_requests']}, expected {expected['total_requests']}"
    )


def test_unique_ips_correct():
    report = _load_report()
    expected = _expected()
    assert report["unique_ips"] == expected["unique_ips"], (
        f"unique_ips: got {report['unique_ips']}, expected {expected['unique_ips']}"
    )


def test_top_path_correct():
    report = _load_report()
    expected = _expected()
    assert report["top_path"] == expected["top_path"], (
        f"top_path: got {report['top_path']!r}, expected {expected['top_path']!r}"
    )
