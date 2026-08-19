import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "ehr_system.db"
SCHEMA = BASE_DIR / "schema.sql"

seed_users = [
    ("admin", "admin123", "ADMINISTRATOR", "System Administrator"),
    ("doctor", "doctor123", "DOCTOR", "Dr. Helen Carter"),
    ("nurse", "nurse123", "NURSE", "Nurse Vanessa Miller"),
    ("gp", "gp123", "GP", "Dr. Nathan Wolff"),
    ("patient1", "patient123", "PATIENT", "Leyon Potts"),
    ("patient2", "patient2123", "PATIENT", "Isla Olaf"),
]

seed_patients = [
    (
        "patient1",
        "Leyon",
        "Potts",
        "1988-04-15",
        "Male",
        "10 Mayfair Avenue, Glasgow",
        "0770090001",
        "Maya Potts - 0770894573",
        "Penicillin",
        "Salbutamol inhaler",
        "Asthma",
        "Use inhaler as prescribed and attend an annual review",
        "Registered",
    ),
    (
        "patient2",
        "Isla",
        "Olaf",
        "2002-09-22",
        "Female",
        "25 Garden Road, Oxford",
        "0986783462",
        "Noah Kelp - 077238974",
        "None Known",
        "None",
        "Migraine",
        "Record migraine triggers and review if symptoms worsen",
        "Not_Registered",
    ),
]

seed_assignments = [
    ("patient1", "doctor", "doctor", "admin"),
    ("patient1", "nurse", "nurse", "admin"),
    ("patient1", "gp", "gp", "admin"),
]

connection = sqlite3.connect(DATABASE)

with open(SCHEMA, "r") as schema_file:
    connection.executescript(schema_file.read())

for username, password, role, full_name in seed_users:
    password_hash = generate_password_hash(password)

    connection.execute(
        """
        INSERT INTO users (username, password_hash, role, full_name)
        VALUES (?, ?, ?, ?)
        """,
        (username, password_hash, role, full_name),
    )

for patient in seed_patients:
    connection.execute(
        """
        INSERT INTO patients (user_id, first_name, last_name, date_of_birth, gender, address, phone, emergency_contact, allergies, medication, diagnosis, treatment_plan, gp_registration_status)
        VALUES ((SELECT id FROM users WHERE username = ?),?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        patient,
    )

for (
    patient_username,
    clinician_username,
    assignment_type,
    created_by_username,
) in seed_assignments:
    connection.execute(
        """
        INSERT INTO patient_assignments (patient_id, clinician_id, assignment_type, created_by)
        VALUES (
            (
                SELECT patients.id
                FROM patients
                JOIN users ON patients.user_id = users.id
                WHERE users.username = ?
            ),
            (SELECT id FROM users WHERE username = ?),
            ?,
            (SELECT id FROM users WHERE username = ?)
        )
        """,
        (patient_username, clinician_username, assignment_type, created_by_username),
    )

connection.commit()

users = connection.execute(
    "SELECT username, role, substr(password_hash, 1, 12) FROM users"
).fetchall()

patients = connection.execute(
    "SELECT patients.id, users.username, patients.first_name, patients.last_name, patients.gp_registration_status FROM patients JOIN users ON patients.user_id = users.id ORDER BY patients.id"
).fetchall()

assignments = connection.execute("""
    SELECT patients.first_name, patients.last_name, users.full_name, patient_assignments.assignment_type FROM patient_assignments JOIN patients
    ON patient_assignments.patient_id = patients.id JOIN users 
    ON patient_assignments.clinician_id = users.id ORDER BY patient_assignments.id
    """).fetchall()

connection.close()

print("Database created and seeded successfully!")
print("Seeded Users: ")
for user in users:
    print(user)

print("Seeded Patients: ")
for patient in patients:
    print(patient)

print("Seeded Assignments:")
for assignment in assignments:
    print(assignment)
