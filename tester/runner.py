from datetime import datetime, timezone
from math import ceil

from tester.tests import get_all_tests


def calculate_p95(latencies):
    if not latencies:
        return 0

    sorted_latencies = sorted(latencies)
    index = ceil(0.95 * len(sorted_latencies)) - 1
    index = max(0, min(index, len(sorted_latencies) - 1))
    return sorted_latencies[index]


def run_all_tests():
    tests = get_all_tests()
    results = []

    for test_func in tests:
        result = test_func()
        results.append(result)

    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")

    latencies = [
        r["latency_ms"]
        for r in results
        if isinstance(r.get("latency_ms"), (int, float))
    ]

    latency_avg = round(sum(latencies) / len(latencies), 2) if latencies else 0
    latency_p95 = round(calculate_p95(latencies), 2) if latencies else 0
    error_rate = round(failed / len(results), 3) if results else 0
    availability = "UP" if passed > 0 else "DOWN"

    return {
        "api": "Agify",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": error_rate,
            "latency_ms_avg": latency_avg,
            "latency_ms_p95": latency_p95,
            "availability": availability
        },
        "tests": results
    }