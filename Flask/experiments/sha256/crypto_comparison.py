import hashlib
import json
import time

audit_entry = {
    "timestamp": "2026-08-01T12:00:00",
    "username": "patient1",
    "action": "VIEW_PATIENT_RECORD",
    "target_id": 1,
    "outcome": "success",
    "previous_hash": "GENESIS"    
}

entry_bytes = json.dumps(audit_entry, sort_keys=True, separators=(",",":")).encode("utf-8")

number_of_tests = 1000000

start_time = time.perf_counter()

for test in range(number_of_tests):
    sha256_hash = hashlib.sha256(entry_bytes).hexdigest()

end_time = time.perf_counter()

total_time = end_time - start_time
average_time = total_time / number_of_tests

print("SHA256 Benchmark Completed Successfully!")
print("Number of Tests: ", number_of_tests)
print("Total Time Taken: ", total_time, "seconds")
print("Average Time Taken: ", average_time * 1000, "milliseconds")
print("Hash Length: ", len(bytes.fromhex(sha256_hash)), "bytes")
print("Example Hash: ", sha256_hash)
