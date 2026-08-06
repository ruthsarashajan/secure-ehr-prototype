from dilithium_py.ml_dsa import ML_DSA_44

message = b"Simulated EHR audit log entry"

public_key, secret_key = ML_DSA_44.keygen()

signature = ML_DSA_44.sign(secret_key, message)

is_valid = ML_DSA_44.verify(public_key, message, signature)

changed_message = b"Changed simulated EHR audit log entry"

changed_message_is_valid = ML_DSA_44.verify(public_key, changed_message, signature)

print("ML-DSA Signature Created Successfully!")
print("Public Key Length: ", len(public_key), "bytes")
print("Secret Key Length: ", len(secret_key), "bytes")
print("Signarure Length: ", len(signature), "bytes")
print("Signature Valid: ", is_valid)
print("Original Message Signature Valid:", is_valid)
print("Changed Message Signature Valid:", changed_message_is_valid)