import time
import requests

DEFAULT_TIMEOUT = 3
MAX_RETRIES = 1


def get_with_retry(url, params=None, timeout=DEFAULT_TIMEOUT, max_retries=MAX_RETRIES):
    attempt = 0
    last_error = None

    while attempt <= max_retries:
        start = time.perf_counter()

        try:
            response = requests.get(url, params=params, timeout=timeout)
            latency_ms = round((time.perf_counter() - start) * 1000, 2)

            if response.status_code == 429:
                if attempt < max_retries:
                    time.sleep(1)
                    attempt += 1
                    continue

            if 500 <= response.status_code <= 599:
                if attempt < max_retries:
                    time.sleep(1)
                    attempt += 1
                    continue

            return {
                "success": True,
                "response": response,
                "latency_ms": latency_ms,
                "error": None
            }

        except requests.Timeout:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            last_error = f"Timeout après {timeout}s"

            if attempt < max_retries:
                time.sleep(1)
                attempt += 1
                continue

            return {
                "success": False,
                "response": None,
                "latency_ms": latency_ms,
                "error": last_error
            }

        except requests.RequestException as e:
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            last_error = str(e)

            if attempt < max_retries:
                time.sleep(1)
                attempt += 1
                continue

            return {
                "success": False,
                "response": None,
                "latency_ms": latency_ms,
                "error": last_error
            }

    return {
        "success": False,
        "response": None,
        "latency_ms": 0,
        "error": last_error or "Erreur inconnue"
    }