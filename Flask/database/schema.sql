DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS patient_assignments;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(1000) NOT NULL,
    role CHAR(50) NOT NULL,
    full_name CHAR(100) NOT NULL,
    is_active INT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender CHAR(20),
    address VARCHAR(200),
    phone VARCHAR(50),
    emergency_contact VARCHAR(200),
    allergies VARCHAR(500),
    medication VARCHAR(500),
    diagnosis VARCHAR(500),
    treatment_plan VARCHAR(1000),
    gp_registration_status VARCHAR(30) NOT NULL DEFAULT 'Not_Registered',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE patient_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INT NOT NULL,
    clinician_id INTEGER NOT NULL,
    assignment_type VARCHAR(30) NOT NULL,
    created_by INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (clinician_id) REFERENCES users(id),
    FOREIGN KEY (created_by) REFERENCES users(id),

    UNIQUE (patient_id, clinician_id, assignment_type)
);

CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    username VARCHAR(100),
    user_role VARCHAR(50),
    action VARCHAR(100) NOT NULL,
    target_type VARCHAR(50),
    target_id INT,
    outcome VARCHAR(20) NOT NULL,
    ip_address VARCHAR(50),
    details TEXT,
    previous_hash VARCHAR(64) NOT NULL,
    entry_hash VARCHAR(64) NOT NULL
);
