# Simulated EHR Security Prototype

## Project purpose

This MSc Cyber Security prototype tests role-based access control and tamper-evident audit logging using simulated patient records.

## Technologies

- Python
- Flask
- SQLite
- Werkzeug password hashing
- SHA-256
- ML-DSA-44 using dilithium-py

## Main security features

- Hashed passwords
- Login, logout and sessions
- Role-based access control
- Patient and clinician assignment checks
- Direct URL bypass protection
- Hash-chained audit logs
- Audit-chain verification and tamper detection
- SHA-256 and ML-DSA comparison experiment

## Install the required packages

Run this from the Flask folder:

```powershell
py -m pip install -r requirements.txt
```

## Run the web prototype

```powershell
py app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Create or reset the database

Warning: this command deletes and recreates the demonstration database, including its existing audit logs. Create a backup first if evidence needs to be preserved.

```powershell
py init_db.py
```

## Run the security comparison

```powershell
py experiments\security_comparison.py
py experiments\analyse_results.py
```

## Data notice

All users and patient records are fictional and are used only for testing.