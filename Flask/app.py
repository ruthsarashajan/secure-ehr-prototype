import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, request, session, redirect
from audit_log import log_event, verify_audit_chain

# To create website
app = Flask(__name__)

app.secret_key = "temporary-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database" / "ehr_system.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


# basically says when someone opens this homepage, run this function below
@app.route("/")
# creates homepage function
def home():

    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        connection = get_db_connection()

        user = connection.execute(
            """
            SELECT id, username, password_hash, role
            FROM users
            WHERE username = ? AND is_active = 1
            """,
            (username,),
        ).fetchone()

        connection.close()

        if user and check_password_hash(user["password_hash"], password):
            role = user["role"]

            session["username"] = username
            session["role"] = role
            session["user_id"] = user["id"]

            log_event(
                user_id=user["id"],
                username=user["username"],
                user_role=role,
                action="LOGIN_SUCCESS",
                target_type="session",
                target_id=None,
                outcome="success",
                ip_address=request.remote_addr,
                details="User is logged in successfully!",
            )

            if role == "ADMINISTRATOR":
                return redirect("/admin/dashboard")
            elif role == "DOCTOR":
                return redirect("/doctor/dashboard")
            elif role == "NURSE":
                return redirect("/nurse/dashboard")
            elif role == "GP":
                return redirect("/gp/dashboard")
            elif role == "PATIENT":
                return redirect("/patient/dashboard")
            else:
                return "Role is not defined"
        else:
            log_event(
                user_id=user["id"] if user else None,
                username=username,
                user_role=user["role"] if user else "UNKNOWN",
                action="LOGIN_FAILURE",
                target_type="session",
                target_id=None,
                outcome="failed",
                ip_address=request.remote_addr,
                details="Invalid username or password!",
            )

            return "Invalid login details. Please try again!"

    return render_template("login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    return render_template("admin_dashboard.html", username=session["username"])


@app.route("/admin/users")
def admin_users():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    connection = get_db_connection()

    users = connection.execute("""
        SELECT id, username, full_name, role, is_active
        FROM users
        ORDER BY id
        """).fetchall()

    connection.close()

    return render_template("admin_users.html", users=users)


@app.route("/admin/staff/new", methods=["GET", "POST"])
def admin_create_staff():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    # Display the page when it is first opened
    if request.method == "GET":
        return render_template("admin_create_staff.html")

    # Get the information entered into the form
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    full_name = request.form.get("full_name", "").strip()
    role = request.form.get("role", "").strip()

    allowed_roles = ["DOCTOR", "NURSE", "GP"]

    # Check that all fields were completed
    if not username or not password or not full_name or not role:
        return render_template(
            "admin_create_staff.html", error="Please complete every field."
        )

    # Check the temporary password
    if len(password) < 8:
        return render_template(
            "admin_create_staff.html",
            error="The temporary password must contain at least 8 characters.",
        )

    # Prevent someone from submitting an administrator role manually
    if role not in allowed_roles:
        return render_template(
            "admin_create_staff.html", error="Please select a valid staff role."
        )

    connection = get_db_connection()

    # Check whether the username already exists
    existing_user = connection.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,),
    ).fetchone()

    if existing_user:
        connection.close()

        return render_template(
            "admin_create_staff.html", error="That username is already in use."
        )

    # Hash the temporary password
    password_hash = generate_password_hash(password)

    # Save the new staff account
    staff_cursor = connection.execute(
        """
        INSERT INTO users (
            username,
            password_hash,
            role,
            full_name
        )
        VALUES (?, ?, ?, ?)
        """,
        (username, password_hash, role, full_name),
    )

    staff_id = staff_cursor.lastrowid

    connection.commit()
    connection.close()

    # Record the action in the audit log
    log_event(
        user_id=session.get("user_id"),
        username=session.get("username"),
        user_role=session.get("role"),
        action="STAFF_ACCOUNT_CREATED",
        target_type="user_account",
        target_id=staff_id,
        outcome="success",
        ip_address=request.remote_addr,
        details=(
            "Administrator created "
            + role
            + " account for "
            + full_name
            + " with username "
            + username
            + "."
        ),
    )

    return render_template(
        "admin_create_staff.html",
        success=("Staff account created successfully for " + full_name + "."),
    )


@app.route("/admin/patients/new", methods=["GET", "POST"])
def admin_create_patient():
    # The user must be logged in
    if "username" not in session:
        return redirect("/login")

    # Only administrators can use this page
    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    error = None
    success = None

    if request.method == "POST":
        # Get the information entered into the form
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        date_of_birth = request.form.get("date_of_birth", "").strip()

        # Check that every field has been completed
        if (
            not username
            or not password
            or not first_name
            or not last_name
            or not date_of_birth
        ):
            error = "Please complete every field."

        # Require a reasonable temporary password
        elif len(password) < 8:
            error = "The temporary password must contain " "at least 8 characters."

        else:
            connection = get_db_connection()

            # Check whether the username already exists
            existing_user = connection.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                (username,),
            ).fetchone()

            if existing_user:
                error = "That username is already in use."
                connection.close()

            else:
                # Create the full name and hash the password
                full_name = first_name + " " + last_name
                password_hash = generate_password_hash(password)

                # Create the patient's login account
                user_cursor = connection.execute(
                    """
                    INSERT INTO users (
                        username,
                        password_hash,
                        role,
                        full_name
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (username, password_hash, "PATIENT", full_name),
                )

                # Get the ID of the new user
                user_id = user_cursor.lastrowid

                # Create the linked patient record
                patient_cursor = connection.execute(
                    """
                    INSERT INTO patients (
                        user_id,
                        first_name,
                        last_name,
                        date_of_birth
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, first_name, last_name, date_of_birth),
                )

                # Get the ID of the new patient record
                patient_id = patient_cursor.lastrowid

                connection.commit()
                connection.close()

                # Record the action in the audit log
                log_event(
                    user_id=session.get("user_id"),
                    username=session.get("username"),
                    user_role=session.get("role"),
                    action="PATIENT_CREATED",
                    target_type="patient_record",
                    target_id=patient_id,
                    outcome="success",
                    ip_address=request.remote_addr,
                    details=(
                        "Administrator created patient "
                        + full_name
                        + " with username "
                        + username
                        + "."
                    ),
                )

                success = "Patient account created successfully for " + full_name + "."

    return render_template("admin_create_patient.html", error=error, success=success)


@app.route("/admin/roles")
def admin_roles():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    return render_template("admin_roles.html")


@app.route("/admin/assignments", methods=["GET", "POST"])
def admin_assignments():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    connection = get_db_connection()

    if request.method == "POST":
        patient_id = request.form.get("patient_id", type=int)
        gp_id = request.form.get("gp_id", type=int)

        # Make sure both options were selected
        if not patient_id or not gp_id:
            connection.close()
            return "Please select both a patient and a GP.", 400

        # Check that the patient exists
        patient = connection.execute(
            """
            SELECT id, first_name, last_name
            FROM patients
            WHERE id = ?
            """,
            (patient_id,),
        ).fetchone()

        # Check that the selected user is an active GP
        gp = connection.execute(
            """
            SELECT id, full_name
            FROM users
            WHERE id = ?
            AND role = 'GP'
            AND is_active = 1
            """,
            (gp_id,),
        ).fetchone()

        # Check whether this patient already has a GP
        existing_gp = connection.execute(
            """
            SELECT id
            FROM patient_assignments
            WHERE patient_id = ?
            AND assignment_type = 'gp'
            """,
            (patient_id,),
        ).fetchone()

        if patient is None or gp is None:
            connection.close()
            return "The selected patient or GP is invalid.", 400

        if existing_gp:
            connection.close()
            return "This patient already has a GP.", 400

        # Save the new GP assignment
        connection.execute(
            """
            INSERT INTO patient_assignments (
                patient_id,
                clinician_id,
                assignment_type,
                created_by
            )
            VALUES (?, ?, ?, ?)
            """,
            (patient_id, gp_id, "gp", session.get("user_id")),
        )

        # Update the patient's GP registration status
        connection.execute(
            """
            UPDATE patients
            SET gp_registration_status = 'Registered',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (patient_id,),
        )

        connection.commit()
        connection.close()

        patient_name = patient["first_name"] + " " + patient["last_name"]

        # Record the assignment in the audit log
        log_event(
            user_id=session.get("user_id"),
            username=session.get("username"),
            user_role=session.get("role"),
            action="GP_ASSIGNED",
            target_type="patient_record",
            target_id=patient_id,
            outcome="success",
            ip_address=request.remote_addr,
            details=(
                "Administrator assigned patient "
                + patient_name
                + " to GP "
                + gp["full_name"]
                + "."
            ),
        )

        return redirect("/admin/assignments")
    assignments = connection.execute("""
        SELECT
            patient_assignments.id,
            patients.first_name || ' ' || patients.last_name
                AS patient_name,
            users.full_name AS clinician_name,
            users.role AS clinician_role,
            patient_assignments.assignment_type
        FROM patient_assignments
        JOIN patients
            ON patient_assignments.patient_id = patients.id
        JOIN users
            ON patient_assignments.clinician_id = users.id
        ORDER BY patient_assignments.id
        """).fetchall()

    patients_without_gp = connection.execute("""
        SELECT patients.id, patients.first_name, patients.last_name, patients.gp_registration_status
        FROM patients
        WHERE NOT EXISTS (
            SELECT 1
            FROM patient_assignments
            WHERE patient_assignments.patient_id = patients.id
            AND patient_assignments.assignment_type = 'gp'
        )
        ORDER BY patients.first_name, patients.last_name
        """).fetchall()

    gps = connection.execute("""
        SELECT id, full_name
        FROM users
        WHERE role = 'GP'
        AND is_active = 1
        ORDER BY full_name
        """).fetchall()

    all_patients = connection.execute("""
        SELECT id, first_name, last_name
        FROM patients
        ORDER BY first_name, last_name
        """).fetchall()

    clinical_staff = connection.execute("""
        SELECT id, full_name, role
        FROM users
        WHERE role IN ('DOCTOR', 'NURSE')
        AND is_active = 1
        ORDER BY role, full_name
        """).fetchall()

    connection.close()

    return render_template(
        "admin_assignments.html",
        assignments=assignments,
        patients_without_gp=patients_without_gp,
        gps=gps,
        all_patients=all_patients,
        clinical_staff=clinical_staff,
    )


@app.route("/admin/assignments/clinician", methods=["POST"])
def assign_clinician():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    patient_id = request.form.get("patient_id", type=int)
    clinician_id = request.form.get("clinician_id", type=int)

    if not patient_id or not clinician_id:
        return "Please select a patient and a clinician.", 400

    connection = get_db_connection()

    patient = connection.execute(
        """
        SELECT id, first_name, last_name
        FROM patients
        WHERE id = ?
        """,
        (patient_id,),
    ).fetchone()

    clinician = connection.execute(
        """
        SELECT id, full_name, role
        FROM users
        WHERE id = ?
        AND role IN ('DOCTOR', 'NURSE')
        AND is_active = 1
        """,
        (clinician_id,),
    ).fetchone()

    if patient is None or clinician is None:
        connection.close()
        return "The selected patient or clinician is invalid.", 400

    assignment_type = clinician["role"].lower()

    existing_assignment = connection.execute(
        """
        SELECT id
        FROM patient_assignments
        WHERE patient_id = ?
        AND clinician_id = ?
        AND assignment_type = ?
        """,
        (patient_id, clinician_id, assignment_type),
    ).fetchone()

    if existing_assignment:
        connection.close()
        return "This clinician is already assigned to this patient.", 400

    connection.execute(
        """
        INSERT INTO patient_assignments (
            patient_id,
            clinician_id,
            assignment_type,
            created_by
        )
        VALUES (?, ?, ?, ?)
        """,
        (patient_id, clinician_id, assignment_type, session.get("user_id")),
    )

    connection.commit()
    connection.close()

    patient_name = patient["first_name"] + " " + patient["last_name"]

    log_event(
        user_id=session.get("user_id"),
        username=session.get("username"),
        user_role=session.get("role"),
        action="CLINICIAN_ASSIGNED",
        target_type="patient_record",
        target_id=patient_id,
        outcome="success",
        ip_address=request.remote_addr,
        details=(
            "Administrator assigned patient "
            + patient_name
            + " to "
            + clinician["role"]
            + " "
            + clinician["full_name"]
            + "."
        ),
    )

    return redirect("/admin/assignments")


@app.route("/admin/audit-logs")
def admin_audit_logs():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access denied: Administrators Only!", 403

    connection = get_db_connection()

    audit_entries = connection.execute("""
        SELECT id, timestamp, username, user_role, action, target_type, target_id, outcome, ip_address, details 
        FROM audit_logs 
        ORDER BY id DESC
        """).fetchall()

    connection.close()

    return render_template("audit_logs.html", audit_entries=audit_entries)


@app.route("/admin/verify-audit-chain")
def admin_verify_audit_chain():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    is_valid, message = verify_audit_chain()

    return render_template(
        "audit_verification.html", is_valid=is_valid, message=message
    )


@app.route("/doctor/dashboard")
def doctor_dashboard():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "DOCTOR":
        return "Access Denied: Doctors Only!", 403

    connection = get_db_connection()

    patients = connection.execute(
        """
        SELECT
            patients.id,
            patients.first_name,
            patients.last_name
        FROM patient_assignments
        JOIN patients
            ON patient_assignments.patient_id = patients.id
        WHERE patient_assignments.clinician_id = ?
          AND patient_assignments.assignment_type = 'doctor'
        ORDER BY patients.first_name
        """,
        (session["user_id"],),
    ).fetchall()

    connection.close()

    return render_template(
        "doctor_dashboard.html", username=session["username"], patients=patients
    )


@app.route("/nurse/dashboard")
def nurse_dashboard():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "NURSE":
        return "Access Denied: Nurses Only!", 403

    connection = get_db_connection()

    patients = connection.execute(
        """
        SELECT
            patients.id,
            patients.first_name,
            patients.last_name
        FROM patient_assignments
        JOIN patients
            ON patient_assignments.patient_id = patients.id
        WHERE patient_assignments.clinician_id = ?
          AND patient_assignments.assignment_type = 'nurse'
        ORDER BY patients.first_name
        """,
        (session["user_id"],),
    ).fetchall()

    connection.close()

    return render_template(
        "nurse_dashboard.html", username=session["username"], patients=patients
    )


@app.route("/gp/dashboard")
def gp_dashboard():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "GP":
        return "Access Denied: GPs Only!", 403

    connection = get_db_connection()

    patients = connection.execute(
        """
        SELECT
            patients.id,
            patients.first_name,
            patients.last_name
        FROM patient_assignments
        JOIN patients
            ON patient_assignments.patient_id = patients.id
        WHERE patient_assignments.clinician_id = ?
          AND patient_assignments.assignment_type = 'gp'
        ORDER BY patients.first_name
        """,
        (session["user_id"],),
    ).fetchall()

    connection.close()

    return render_template(
        "gp_dashboard.html", username=session["username"], patients=patients
    )


@app.route("/patient/dashboard")
def patient_dashboard():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "PATIENT":
        return "Access Denied: Patients Only!", 403

    connection = get_db_connection()

    patient = connection.execute(
        """
        SELECT id, gp_registration_status
        FROM patients
        WHERE user_id = ?
        """,
        (session["user_id"],),
    ).fetchone()

    connection.close()

    if patient is None:
        return "Patient record not found.", 404

    return render_template(
        "patient_dashboard.html", username=session["username"], patient=patient
    )


@app.route("/patient/request-gp", methods=["POST"])
def request_gp_registration():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "PATIENT":
        return "Access Denied: Patients Only!", 403

    connection = get_db_connection()

    patient = connection.execute(
        """
        SELECT id, gp_registration_status
        FROM patients
        WHERE user_id = ?
        """,
        (session["user_id"],),
    ).fetchone()

    if patient is None:
        connection.close()
        return "Patient record not found.", 404

    existing_gp = connection.execute(
        """
        SELECT id
        FROM patient_assignments
        WHERE patient_id = ?
        AND assignment_type = 'gp'
        """,
        (patient["id"],),
    ).fetchone()

    if existing_gp:
        connection.close()
        return redirect("/patient/dashboard")

    if patient["gp_registration_status"] == "Pending":
        connection.close()
        return redirect("/patient/dashboard")

    connection.execute(
        """
        UPDATE patients
        SET gp_registration_status = 'Pending',
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (patient["id"],),
    )

    connection.commit()
    connection.close()

    log_event(
        user_id=session.get("user_id"),
        username=session.get("username"),
        user_role=session.get("role"),
        action="GP_REGISTRATION_REQUESTED",
        target_type="patient_record",
        target_id=patient["id"],
        outcome="success",
        ip_address=request.remote_addr,
        details="Patient requested registration with a GP.",
    )

    return redirect("/patient/dashboard")


@app.route("/patient/my-record")
def patient_my_record():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "PATIENT":
        return "Access Denied: Patients Only!", 403

    connection = get_db_connection()

    patient = connection.execute(
        """
        SELECT id
        FROM patients
        WHERE user_id = ?
        """,
        (session["user_id"],),
    ).fetchone()

    connection.close()

    if patient is None:
        return "Patient record not found.", 404

    return redirect(f"/patient/{patient['id']}")


@app.route("/patient/<int:patient_id>")
def view_patient_record(patient_id):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    role = session["role"]

    connection = get_db_connection()

    patient = connection.execute(
        """
        SELECT patients.*, users.username AS patient_username
        FROM patients
        JOIN users ON patients.user_id = users.id
        WHERE patients.id = ?
        """,
        (patient_id,),
    ).fetchone()

    if patient is None:
        connection.close()
        return "Patient record not found", 404

    access_allowed = False

    if role == "ADMINISTRATOR":
        access_allowed = True

    elif role == "PATIENT":
        access_allowed = username == patient["patient_username"]

    elif role in ["DOCTOR", "NURSE", "GP"]:
        assignment_types = {"DOCTOR": "doctor", "NURSE": "nurse", "GP": "gp"}

        assignment = connection.execute(
            """
            SELECT id
            FROM patient_assignments
            WHERE patient_id = ?
              AND clinician_id = (
                  SELECT id FROM users WHERE username = ?
              )
              AND assignment_type = ?
            """,
            (patient_id, username, assignment_types[role]),
        ).fetchone()

        access_allowed = assignment is not None

    connection.close()

    if not access_allowed:
        log_event(
            user_id=session.get("user_id"),
            username=username,
            user_role=role,
            action="ACCESS_DENIED",
            target_type="patient_record",
            target_id=patient_id,
            outcome="denied",
            ip_address=request.remote_addr,
            details="User attempted to view an unauthorised patient record.",
        )

        return "Access denied: You cannot view this patient record.", 403

    log_event(
        user_id=session.get("user_id"),
        username=username,
        user_role=role,
        action="VIEW_PATIENT_RECORD",
        target_type="patient_record",
        target_id=patient_id,
        outcome="success",
        ip_address=request.remote_addr,
        details="User viewed an authorised patient record.",
    )

    return render_template("patient_record.html", patient=patient)


"""
@app.route("/debug/users")
def debug_users():
    return str(users)
"""


@app.route("/logout")
def logout():
    if "username" in session:
        log_event(
            user_id=session.get("user_id"),
            username=session.get("username"),
            user_role=session.get("role"),
            action="LOGOUT",
            target_type="session",
            target_id=None,
            outcome="success",
            ip_address=request.remote_addr,
            details="User logged out.",
        )

    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
