import sqlite3
from datetime import datetime
from pathlib import Path

from audit_log import calculate_entry_hash, log_event, verify_audit_chain

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database" / "ehr_system.db"


def repair_audit_chain():
    backup_name = (
        "ehr_system_before_audit_repair_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".db"
    )
    backup_path = DATABASE.parent / backup_name

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    # Use SQLite's backup feature to create a consistent database copy.
    backup_connection = sqlite3.connect(backup_path)
    connection.backup(backup_connection)
    backup_connection.close()

    audit_entries = connection.execute("""
        SELECT *
        FROM audit_logs
        ORDER BY id
        """).fetchall()

    expected_previous_hash = "GENESIS"
    first_invalid_index = None

    # Find the first entry that does not match its stored audit hash.
    for index, entry in enumerate(audit_entries):
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

        if (
            entry["previous_hash"] != expected_previous_hash
            or entry["entry_hash"] != recalculated_hash
        ):
            first_invalid_index = index
            break

        expected_previous_hash = entry["entry_hash"]

    if first_invalid_index is None:
        connection.close()
        print("The audit chain is already valid. No repair was needed.")
        print("Backup created at:", backup_path)
        return

    first_invalid_entry = audit_entries[first_invalid_index]

    # Stop if the mismatch is not the known form-ID problem at entry 97.
    if first_invalid_entry["id"] != 97:
        connection.close()
        raise RuntimeError(
            "Repair stopped because the first invalid entry was "
            + str(first_invalid_entry["id"])
            + ", not the expected entry 97."
        )

    if first_invalid_index == 0:
        expected_previous_hash = "GENESIS"
    else:
        expected_previous_hash = audit_entries[first_invalid_index - 1]["entry_hash"]

    repaired_count = 0

    # Recalculate only the hash-link fields from entry 97 onward.
    for entry in audit_entries[first_invalid_index:]:
        repaired_hash = calculate_entry_hash(
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
            expected_previous_hash,
        )

        connection.execute(
            """
            UPDATE audit_logs
            SET previous_hash = ?, entry_hash = ?
            WHERE id = ?
            """,
            (expected_previous_hash, repaired_hash, entry["id"]),
        )

        expected_previous_hash = repaired_hash
        repaired_count += 1

    connection.commit()
    connection.close()

    # Record why the controlled test database was repaired.
    log_event(
        user_id=None,
        username="system",
        user_role="SYSTEM",
        action="AUDIT_CHAIN_REPAIRED",
        target_type="audit_log",
        target_id=97,
        outcome="success",
        ip_address="local_maintenance",
        details=(
            "Rebuilt audit hash links from entry 97 after fixing "
            "HTML form IDs being hashed as text before SQLite "
            "stored them as integers. Event data was unchanged."
        ),
    )

    is_valid, message = verify_audit_chain()

    print("Backup created at:", backup_path)
    print("First repaired entry:", first_invalid_entry["id"])
    print("Entries repaired:", repaired_count)
    print("Verification result:", message)

    if not is_valid:
        raise RuntimeError("Audit verification still failed after repair.")


if __name__ == "__main__":
    repair_audit_chain()