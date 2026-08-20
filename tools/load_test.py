import time
import statistics
import requests

URL = "http://127.0.0.1:8000/predict"

PAYLOAD = {
    "checking_status": "A11", "duration": 6, "credit_history": "A34", "purpose": "A43",
    "credit_amount": 1169, "savings_status": "A65", "employment": "A75", "installment_rate": 4,
    "personal_status_sex": "A93", "other_parties": "A101", "residence_since": 4,
    "property_magnitude": "A121", "age": 67, "other_payment_plans": "A143", "housing": "A152",
    "existing_credits": 2, "job": "A173", "num_dependents": 1, "own_telephone": "A192",
    "foreign_worker": "A201",
}

def run(n=100):
    latencies = []
    for i in range(n):
        start = time.time()
        try:
            r = requests.post(URL, json=PAYLOAD, timeout=5)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request {i+1} failed: {e}")
            continue
        elapsed = (time.time() - start) * 1000
        latencies.append(elapsed)
        print(f"Request {i+1}/{n}: {elapsed:.1f}ms")

    if not latencies:
        print("No successful requests.")
        return

    latencies.sort()
    n_ok = len(latencies)
    p50 = latencies[int(n_ok * 0.5)]
    p95 = latencies[min(int(n_ok * 0.95), n_ok - 1)]
    print(f"\nn={n_ok} | mean={statistics.mean(latencies):.1f}ms | p50={p50:.1f}ms | p95={p95:.1f}ms")

if __name__ == "__main__":
    run()