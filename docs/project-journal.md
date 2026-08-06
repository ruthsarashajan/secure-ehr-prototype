# Project Journal

## 1 August 2026 - SHA-256 Benchmark Baseline

### Work completed

- Created `experiments/crypto_comparison.py` as a separate experiment file.
- Converted a simulated audit-log entry into a consistent format and hashed it with SHA-256.
- Ran the SHA-256 operation 1,000,000 times to measure its performance.
- Confirmed that the SHA-256 output is 32 bytes long.

### Results

- Number of tests: 1,000,000
- Total time: approximately 2.12 seconds
- Average time per SHA-256 operation: approximately 0.00212 milliseconds
- Hash length: 32 bytes

### Issue encountered and fix

The first run produced a Python `SyntaxError` because `bytes..fromhex()` contained two full stops. This was corrected to `bytes.fromhex()`, after which the experiment ran successfully.

### Why this work matters

This experiment provides a measured SHA-256 baseline for the project. The same type of test can later be carried out using the approved ML-DSA implementation. The results can then be discussed in terms of execution time and output or signature size. The final report must also explain that SHA-256 is a hash function, while ML-DSA is a digital-signature algorithm, so they do not perform exactly the same security function.

### Evidence to keep

- Screenshot of the successful terminal output showing the number of tests, total time, average time and 32-byte hash length.
- A copy of `experiments/crypto_comparison.py` used for the test.
## 6 August 2026 - Dependency File Created and Tested

### Work completed
- Created `Flask/requirements.txt`.
- Recorded the external Python packages and versions used by the prototype: `Flask==3.1.3` and `dilithium-py==1.4.0`.
- Ran `py -m pip install -r requirements.txt` from the `Flask` folder.
- The terminal confirmed that the required packages and their dependencies were already installed.

### Why this matters
The requirements file records the exact package versions needed to run the project. This makes the prototype easier to reproduce on another computer and provides evidence of the software environment used for the final report.

### Test result
The installation command completed without errors. No packages needed to be installed again because the required versions were already present.

### Files changed
- `Flask/requirements.txt`
- `docs/project-journal.md`

## 6 August 2026 - Project README Completed

### Work completed
- Created `Flask/README.md` for the prototype.
- Added a simple explanation of the project's purpose and main security features.
- Documented the main technologies and dependencies used, including Flask, SQLite, SHA-256 and `dilithium-py`.
- Added instructions for installing the requirements, creating the database and running the Flask application.
- Added the commands used to run the SHA-256 and ML-DSA comparison experiments.
- Included a reminder that the project uses simulated patient data only.

### Why this matters
The README makes the prototype easier to understand and reproduce. A supervisor or marker can use it to see what the project does, what software it needs and how to run it without first reading every source-code file.

### Files created or changed
- `Flask/README.md`
- `docs/project-journal.md`

### Check performed
- Checked that the README matches the current folder structure and the dependencies listed in `Flask/requirements.txt`.
- The requirements installation command had already confirmed that Flask and `dilithium-py` were available.

### Evidence for the final report
- The completed README can be included as evidence that the prototype was documented for reproducibility.
- A screenshot of the README in VS Code can be captured during the final evidence stage.

### Next step
- Review the completed build, remove or protect any temporary debugging code, and begin the final structured test plan and screenshot collection.
