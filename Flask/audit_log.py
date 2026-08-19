import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database" / "ehr_system.db"


def calculate_entry_hash(
    timestamp,
    user_id,
    username,
    user_role,
    action,
    target_type,
    target_id,
    outcome,
    ip_address,
    details,
    previous_hash,
):
    entry_data = {
        "timestamp": timestamp,
        "user_id": user_id,
        "username": username,
        "user_role": user_role,
        "action": action,
        "target_type": target_type,
        "target_id": target_id,
        "outcome": outcome,
        "ip_address": ip_address,
        "details": details,
        "previous_hash": previous_hash,
    }

    entry_text = json.dumps(entry_data, sort_keys=True, separators=(",", ":"))

    return hashlib.sha256(entry_text.encode("utf-8")).hexdigest()


def log_event(
    user_id,
    username,
    user_role,
    action,
    target_type,
    target_id,
    outcome,
    ip_address,
    details,
):
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    connection = sqlite3.connect(DATABASE)

    try:
        previous_entry = connection.execute("""
            SELECT entry_hash 
            FROM audit_logs 
            ORDER BY id DESC
            LIMIT 1
            """).fetchone()

        if previous_entry:
            previous_hash = previous_entry[0]
        else:
            previous_hash = "GENESIS"

        entry_hash = calculate_entry_hash(
            timestamp,
            user_id,
            username,
            user_role,
            action,
            target_type,
            target_id,
            outcome,
            ip_address,
            details,
            previous_hash,
        )

        connection.execute(
            """
            INSERT INTO audit_logs (timestamp, user_id, username, user_role, action, target_type, target_id, outcome, ip_address, details, previous_hash, entry_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                user_id,
                username,
                user_role,
                action,
                target_type,
                target_id,
                outcome,
                ip_address,
                details,
                previous_hash,
                entry_hash,
            ),
        )

        connection.commit()
        return entry_hash

    finally:
        connection.close()


def verify_audit_chain():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    try:
        audit_entries = connection.execute("""
            SELECT *
            FROM audit_logs
            ORDER BY id
            """).fetchall()
        expected_previous_hash = "GENESIS"

        for entry in audit_entries:
            if entry["previous_hash"] != expected_previous_hash:
                return False, f"Chain link brokenn at audit entry {entry['id']}"

            recalculated_hash = calculate_entry_hash(
                entry["timestamp"],
                entry["user_id"],
                entry["username"],
                entry["user_role"],
                entry["action"],
                entry["target_type"],
                entry["target_id"],
                entry["outcome"],
                entry["ip_address"],
                entry["details"],
                entry["previous_hash"],
            )

            if recalculated_hash != entry["entry_hash"]:
                return False, f"Audit data changed at entry {entry['id']}"

            expected_previous_hash = entry["entry_hash"]

        return True, "Audit chain is valid."

    finally:
        connection.close()
