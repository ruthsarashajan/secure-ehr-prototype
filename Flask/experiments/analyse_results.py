import csv
from statistics import mean
from pathlib import Path

current_folder = Path(__file__).resolve().parent
results_file = current_folder / "security_comparison_results.csv"

with open(results_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    rows = list(reader)

print("Results file opened successfully!")
print("Number of saved experiment runs:", len(rows))

sha256_times = []

for row in rows:
    sha256_times.append(float(row["sha256_average_ms"]))

print("Overall SHA-256 average:")
print(mean(sha256_times), "milliseconds")

ml_dsa_keygen_times = []
ml_dsa_signing_times = []
ml_dsa_verify_times = []

for row in rows:
    ml_dsa_keygen_times.append(float(row["ml_dsa_keygen_average_ms"]))
    ml_dsa_signing_times.append(float(row["ml_dsa_signing_average_ms"]))
    ml_dsa_verify_times.append(float(row["ml_dsa_verification_average_ms"]))

print()
print("Overall ML-DSA averages:")
print("Key generation:", mean(ml_dsa_keygen_times), "milliseconds")
print("Signing:", mean(ml_dsa_signing_times), "milliseconds")
print("Verification:", mean(ml_dsa_verify_times), "milliseconds")

sha_detection_count = 0
ml_dsa_detection_count = 0

for row in rows:
    if row["sha256_detected_change"].strip().lower() == "true":
        sha_detection_count += 1

    if row["ml_dsa_detected_change"].strip().lower() == "true":
        ml_dsa_detection_count += 1

print()
print("Tampering detection results:")
print("SHA-256 detected changes in", sha_detection_count, "out of", len(rows), "runs")
print("ML-DSA detected changes in", ml_dsa_detection_count, "out of", len(rows), "runs")

sha256_sizes = []
ml_dsa_public_key_sizes = []
ml_dsa_secret_key_sizes = []
ml_dsa_signature_sizes = []

for row in rows:
    sha256_sizes.append(int(row["sha256_digest_bytes"]))
    ml_dsa_public_key_sizes.append(int(row["ml_dsa_public_key_bytes"]))
    ml_dsa_secret_key_sizes.append(int(row["ml_dsa_secret_key_bytes"]))
    ml_dsa_signature_sizes.append(int(row["ml_dsa_signature_bytes"]))

print()
print("Storage size results:")
print("SHA-256 digest:", mean(sha256_sizes), "bytes")
print("ML-DSA public key:", mean(ml_dsa_public_key_sizes), "bytes")
print("ML-DSA secret key:", mean(ml_dsa_secret_key_sizes), "bytes")
print("ML-DSA signature:", mean(ml_dsa_signature_sizes), "bytes")