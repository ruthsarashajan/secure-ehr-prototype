# SHA-256 and ML-DSA-44 Experiment Results

Five experiment runs were completed. Each run contained 30 repetitions.

| Measure | SHA-256 | ML-DSA-44 |
|---|---:|---:|
| Average hashing time | 0.0021 ms | Not applicable |
| Average key-generation time | Not applicable | 16.57 ms |
| Average signing time | Not applicable | 100.43 ms |
| Average verification time | Not applicable | 19.71 ms |
| Digest/signature size | 32 bytes | 2420 bytes |
| Public-key size | Not applicable | 1312 bytes |
| Secret-key size | Not applicable | 2560 bytes |
| Tampering detected | 5 out of 5 runs | 5 out of 5 runs |

## Simple Interpretation

SHA-256 was considerably faster and produced a much smaller output. This makes it suitable for creating a lightweight hash-chained audit log.

ML-DSA-44 required more processing time and storage. However, it provides a digital signature that can verify both data integrity and the authenticity of the signer.

The algorithms serve different purposes, so the results do not mean that one algorithm is universally better than the other.