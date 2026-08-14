import time
from statistics import mean
from dilithium_py.ml_dsa import ML_DSA_44

message = b"Simulated EHR audit log entry"
number_of_tests = 30

keygen_times = []
signing_times = []
verification_times = []

for test in range(number_of_tests):
    start_time = time.perf_counter()
    public_key, secret_key = ML_DSA_44.keygen()
    end_time = time.perf_counter()

    keygen_time = (end_time - start_time) *1000
    keygen_times.append(keygen_time)

    start_time = time.perf_counter()
    signature = ML_DSA_44.sign(secret_key, message)
    end_time = time.perf_counter()

    signing_time = (end_time - start_time) * 1000
    signing_times.append(signing_time)

    start_time = time.perf_counter()
    is_valid = ML_DSA_44.verify(public_key, message, signature)
    end_time = time.perf_counter()

    verification_time = (end_time - start_time) * 1000
    verification_times.append(verification_time)

    if not is_valid:
        print("Verification Failed During Test", test + 1)

print("ML-DSA-44 Benchmark Has Been Completed Successfully!")
print("Number of Tests: ", number_of_tests)
print("Average Key Generation Times: ", mean(keygen_times), "milliseconds")
print("Average Signing Times: ", mean(signing_times), "milliseconds")
print("Average Verification Times: ", mean(verification_times), "milliseconds")

print("Public Key Length: ", len(public_key), "bytes")
print("Secret Key Length: ", len(secret_key), "bytes")
print("Signature Length: ", len(signature), "bytes")
print("Final Signature Valid: ", is_valid)
      
