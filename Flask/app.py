import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, session, redirect
from audit_log import log_event, verify_audit_chain

#To create website
app = Flask(__name__)

app.secret_key = "temporary-secret-key"

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "ehr_system.db"

def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

#basically says when someone opens this homepage, run this function below
@app.route("/")
#creates homepage function
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
                details="User is logged in successfully!"
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
                details="Invalid username or password!"
            )

            return "Invalid login details. Please try again!"

    return render_template("login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "username" not in session:
        return redirect("/login")
    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!"

    return render_template("admin_dashboard.html", username=session["username"])

@app.route("/admin/audit-logs")
def admin_audit_logs():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access denied: Administrators Only!", 403

    connection = get_db_connection()

    audit_entries = connection.execute(
        """
        SELECT id, timestamp, username, user_role, action, target_type, target_id, outcome, ip_address 
        FROM audit_logs 
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template("audit_logs.html", audit_entries=audit_entries)

@app.route("/admin/verify-audit-chain")
def admin_verify_audit_chain():
    if "username" not in session:
        return redirect("/login")

    if session.get("role") != "ADMINISTRATOR":
        return "Access Denied: Administrators Only!", 403

    is_valid, message = verify_audit_chain()

    return f"Verification result: {message}"

@app.route("/doctor/dashboard")
def doctor_dashboard():
    if "username" not in session:
        return redirect("/login")
    if session.get("role") != "DOCTOR":
        return "Access Denied: Doctors Only!"

    return render_template("doctor_dashboard.html", username=session["username"])

@app.route("/nurse/dashboard")
def nurse_dashboard():
    if "username" not in session:
        return redirect("/login")
    if session.get("role") != "NURSE":
        return "Access Denied: Nurses Only!"

    return render_template("nurse_dashboard.html", username=session["username"])

@app.route("/gp/dashboard")
def gp_dashboard():
    if "username" not in session:
        return redirect("/login")
    if session.get("role") != "GP":
        return "Access Denied: GPs Only!"

    return render_template("gp_dashboard.html", username=session["username"])

@app.route("/patient/dashboard")
def patient_dashboard():
    if "username" not in session:
        return redirect("/login")
    if session.get("role") != "PATIENT":
        return "Access Denied: Patients Only!"

    return render_template("patient_dashboard.html", username=session["username"])

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
        assignment_types = {
            "DOCTOR": "doctor",
            "NURSE": "nurse",
            "GP": "gp"
        }

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
            details="User attempted to view an unauthorised patient record."
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
        details="User viewed an authorised patient record."
    )

    return render_template("patient_record.html", patient=patient)

'''
@app.route("/debug/users")
def debug_users():
    return str(users)
'''

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
            details="User logged out."
        )

    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)