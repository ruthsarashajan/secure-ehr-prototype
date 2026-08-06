from werkzeug.security import generate_password_hash

users = {
    "admin": {
        "password_hash": generate_password_hash("admin123"),
        "role": "ADMINISTRATOR"
    },
    "doctor": {
        "password_hash": generate_password_hash("doctor123"),
        "role": "DOCTOR"
    },
    "nurse": {
        "password_hash": generate_password_hash("nurse123"),
        "role": "NURSE"
    },
    "gp": {
            "password_hash": generate_password_hash("gp123"),
            "role": "GP"
    },
    "patient1": {
            "password_hash": generate_password_hash("patient123"),
            "role": "PATIENT"
    },
}