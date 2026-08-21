import csv
from datetime import datetime
from pathlib import Path
import hashlib
import time
from statistics import mean
from dilithium_py.ml_dsa import ML_DSA_44

message =  b"Simulated EHR audit log entry"
number_of_tests = 30

print("Security Comparison Experiment Ready!")
print("Number of Tests: ", number_of_tests)
print("Message: ", message.decode())

sha256_times = []

sha256_repetitions = 10000

for test in range(number_of_tests):
    start_time = time.perf_counter()

    for repetition in range(sha256_repetitions):
        sha256_digest = hashlib.sha256(message).digest()

    end_time = time.perf_counter()

    batch_time = (end_time - start_time) * 1000
    time_per_hash = batch_time / sha256_repetitions

    sha256_times.append(time_per_hash)

print()
print("SHA-256 Results Are Here As Follows: ")
print("Average Hashing Time: ", mean(sha256_times), "milliseconds")
print("Digest Length: ", len(sha256_digest), "bytes")
print("Example Digest: ", sha256_digest.hex())

ml_dsa_keygen_times = []
ml_dsa_signing_times = []
ml_dsa_verify_times = []

for test in range(number_of_tests):
    start_time = time.perf_counter()
    public_key, secret_key = ML_DSA_44.keygen()
    end_time = time.perf_counter()

    keygen_time = (end_time - start_time) * 1000
    ml_dsa_keygen_times.append(keygen_time)

    start_time = time.perf_counter()
    signature = ML_DSA_44.sign(secret_key, message)
    end_time = time.perf_counter()

    signing_time = (end_time - start_time) * 1000
    ml_dsa_signing_times.append(signing_time)

    start_time = time.perf_counter()
    signature_is_valid = ML_DSA_44.verify(public_key, message, signature)
    end_time = time.perf_counter()

    verify_time = (end_time - start_time) * 1000
    ml_dsa_verify_times.append(verify_time)

print()
print("ML-DSA-44 Results Are Here As Follows: ")#
print("Average Key Generation Times: ", mean(ml_dsa_keygen_times), "milliseconds")
print("Average Signing Times: ", mean(ml_dsa_signing_times), "milliseconds")
print("Average Verification Time: ", mean(ml_dsa_verify_times), "milliseconds")
print("Public Key Length: ", len(public_key), "bytes")
print("Secret Key Length: ", len(secret_key), "bytes")
print("Signature Length: ", len(signature), "bytes")
print("Is Signature Valid: ", signature_is_valid)

changed_message = b"Changed Simulated EHR Audit Log Entry"

changed_sha256_digest = hashlib.sha256(changed_message).digest()
sha256_detected_change = sha256_digest != changed_sha256_digest

changed_signature_is_valid = ML_DSA_44.verify(public_key, changed_message, signature)

ml_dsa_detected_change = not changed_signature_is_valid

print()
print("Tampering Test Results: ")
print("SHA-256 Detected Changed Data: ", sha256_detected_change)
print("ML-DSA Dectected Changed Data: ", ml_dsa_detected_change)

results_file = Path(__file__).resolve().parent / "security_comparison_results.csv"

file_already_exists = results_file.exists()

with open(results_file, "a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    if not file_already_exists:
        writer.writerow([
            "timestamp",
            "number_of_tests",
            "sha256_average_ms",
            "sha256_digest_bytes",
            "ml_dsa_keygen_average_ms",
            "ml_dsa_signing_average_ms",
            "ml_dsa_verification_average_ms",
            "ml_dsa_public_key_bytes",
            "ml_dsa_secret_key_bytes",
            "ml_dsa_signature_bytes",
            "sha256_detected_change",
            "ml_dsa_detected_change",
        ])

    writer.writerow([
        datetime.now().isoformat(timespec="seconds"),
        number_of_tests,
        mean(sha256_times),
        len(sha256_digest),
        mean(ml_dsa_keygen_times),
        mean(ml_dsa_signing_times),
        mean(ml_dsa_verify_times),
        len(public_key),
        len(secret_key),
        len(signature),
        sha256_detected_change,
        ml_dsa_detected_change,
    ])

print("Results saved to:", results_file)