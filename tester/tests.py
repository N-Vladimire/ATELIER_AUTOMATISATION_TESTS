from tester.client import get_with_retry

BASE_URL = "https://api.agify.io"


def build_result(name, status, details="", latency_ms=None):
    return {
        "name": name,
        "status": status,
        "details": details,
        "latency_ms": latency_ms
    }


def test_status_code_200():
    result = get_with_retry(BASE_URL, params={"name": "michael"})
    if not result["success"]:
        return build_result("HTTP 200", "FAIL", result["error"], result["latency_ms"])

    response = result["response"]
    if response.status_code == 200:
        return build_result("HTTP 200", "PASS", "Code 200 reçu", result["latency_ms"])

    return build_result("HTTP 200", "FAIL", f"Code reçu : {response.status_code}", result["latency_ms"])


def test_content_type_json():
    result = get_with_retry(BASE_URL, params={"name": "michael"})
    if not result["success"]:
        return build_result("Content-Type JSON", "FAIL", result["error"], result["latency_ms"])

    content_type = result["response"].headers.get("Content-Type", "")
    if "application/json" in content_type:
        return build_result("Content-Type JSON", "PASS", content_type, result["latency_ms"])

    return build_result("Content-Type JSON", "FAIL", f"Content-Type reçu : {content_type}", result["latency_ms"])


def test_field_name_present():
    result = get_with_retry(BASE_URL, params={"name": "michael"})
    if not result["success"]:
        return build_result("Champ name présent", "FAIL", result["error"], result["latency_ms"])

    data = result["response"].json()
    if "name" in data:
        return build_result("Champ name présent", "PASS", "Champ présent", result["latency_ms"])

    return build_result("Champ name présent", "FAIL", "Champ manquant", result["latency_ms"])


def test_field_count_is_int():
    result = get_with_retry(BASE_URL, params={"name": "michael"})
    if not result["success"]:
        return build_result("Champ count entier", "FAIL", result["error"], result["latency_ms"])

    data = result["response"].json()
    if "count" in data and isinstance(data["count"], int):
        return build_result("Champ count entier", "PASS", "Type int valide", result["latency_ms"])

    return build_result("Champ count entier", "FAIL", "count absent ou type invalide", result["latency_ms"])


def test_field_age_type():
    result = get_with_retry(BASE_URL, params={"name": "michael"})
    if not result["success"]:
        return build_result("Champ age type valide", "FAIL", result["error"], result["latency_ms"])

    data = result["response"].json()
    if "age" in data and (isinstance(data["age"], int) or data["age"] is None):
        return build_result("Champ age type valide", "PASS", "age valide", result["latency_ms"])

    return build_result("Champ age type valide", "FAIL", "age absent ou type invalide", result["latency_ms"])


def test_empty_name_handled():
    result = get_with_retry(BASE_URL, params={"name": ""})
    if not result["success"]:
        return build_result("Entrée vide gérée", "FAIL", result["error"], result["latency_ms"])

    response = result["response"]
    if response.status_code == 200:
        return build_result("Entrée vide gérée", "PASS", "Réponse gérée sans crash", result["latency_ms"])

    return build_result("Entrée vide gérée", "FAIL", f"Code reçu : {response.status_code}", result["latency_ms"])


def get_all_tests():
    return [
        test_status_code_200,
        test_content_type_json,
        test_field_name_present,
        test_field_count_is_int,
        test_field_age_type,
        test_empty_name_handled,
    ]