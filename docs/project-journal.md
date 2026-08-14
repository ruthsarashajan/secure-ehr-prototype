# Project Journal

> **Single journal rule:** This is the master journal for the MSc project. Add every future project-journal entry to this file. Do not create a separate journal file elsewhere.

> **Recovered-history note:** On 10 August 2026, the June and July history below was restored from the saved project conversation, meeting logs, implementation checklist and test-results records. Where the original evidence did not contain an exact day, the heading says so instead of inventing a date.

## 1 June 2026 - Introductory Group Supervisor Meeting

### Work completed

- Attended the introductory group meeting led by supervisor Raman Singh.
- Reviewed the main MSc project stages: specification, interim report, implementation or research, evaluation and final dissertation.
- Discussed the need for a clear title, research question, aim, objectives, scope and methodology.

### Decisions and action points

- Keep the project focused and achievable within the MSc timeline.
- Begin preparing the project specification and initial reading.
- Maintain regular documentation and supervisor communication.

### Evidence

- `Meeting logs/01_June_Meeting_Log.md`

## June 2026 - Project Specification Completed

*The exact submission day was not recorded in the surviving evidence.*

### Work completed

- Completed and submitted the original MSc project specification.
- Defined the secure simulated EHR topic, research question, aim, objectives, scope, proposed methodology and ethical approach.
- Confirmed that only fictional patient data would be used.
- Selected Python, Flask, SQLite, HTML/CSS, role-based access control and tamper-evident audit logging as the initial technical direction.

### Why this mattered

The specification created the formal foundation for the project and limited the work to a research prototype rather than a real hospital or NHS system.

### Evidence

- Original `B01828711_Project_specification.docx`

## 15 June 2026 - Project Foundation and Scope Planning

### Work completed

- Prepared the Week 3 project-foundation material.
- Defined the five roles: patient, doctor, nurse, GP and administrator.
- Planned the patient-record structure, database tables, audit events and access-control test scenarios.
- Planned the SHA-256 previous-hash and entry-hash design.
- Identified the implementation order and evidence needed for the final report.

### Scope decision

The application would be a small simulated EHR security prototype. Prescriptions, billing, real healthcare integration, messaging and a full blockchain platform remained outside scope.

## 18 June 2026 - Individual Supervisor Meeting

### Work completed

- Discussed the submitted specification and early project direction with Raman Singh.
- Recorded the supervisor's advice to prioritise the introduction, literature review, research design and methodology before implementation.
- Identified the need for architecture, database, access-control, hash-chain and timeline diagrams.

### Decisions and action points

- Complete the literature review before finalising the detailed scope.
- Explain the research gap and evaluation method clearly.
- Keep the prototype focused on access control and tamper-evident audit logging.
- Complete the interim report before beginning the main build.

### Evidence

- `Meeting logs/18_June_Meeting_Log.md`

## Around 2 July 2026 - Interim Report Completed

### Work completed

- Completed and submitted the interim report.
- Included the introduction, research question, aim, objectives, proposed scope, literature review, methodology, tools, design overview, planned evaluation and ethical considerations.
- Prepared system diagrams and a white-background 15-week Gantt chart.

### Final-report correction retained

- Remove the old ISO 27789 citation from the literature-gap paragraph.
- Use HL7 International (2023) and Kent and Souppaya (2006) instead.
- Use the official NIST SP 800-92 webpage in the final reference list.

## 8 July 2026 - Documents Reviewed and Evidence Pack Started

### Work completed

- Read the project specification and interim report before starting implementation.
- Confirmed the focused Flask/SQLite scope and the use of synthetic patient data only.
- Created the build documentation pack covering requirements, database design, access control, audit design, testing, final-report notes and supervisor progress.
- Created a supervisor progress pack for the next meeting.

### Files created

- `docs/project-journal.md`
- `docs/requirements.md`
- `docs/database-design.md`
- `docs/access-control-design.md`
- `docs/audit-log-design.md`
- `docs/test-plan.md`
- `docs/test-results.md`
- `docs/final-report-notes.md`
- `docs/implementation-checklist.md`
- `docs/supervisor-progress-pack-2026-07-08.md`

## 8 July 2026 - First Flask Skeleton Tested

### Work completed

- Created the first Flask application skeleton, HTML templates, CSS, requirements file and run instructions.
- Created a private Python virtual environment and installed Flask.
- Added a homepage and login placeholder.

### Check performed

- Confirmed that the homepage and login page both returned HTTP `200`.
- Confirmed that the local application responded at `http://127.0.0.1:5000`.

### Issue encountered and fix

The plain `python` command was not available in the original terminal environment. The run instructions were changed to use the Windows Python launcher or the virtual environment's Python executable.

## 9 July 2026 - Basic Login and Role Behaviour

### Work completed

- Built Flask routes and HTML templates manually as a learning exercise.
- Changed the login form to submit using `POST`.
- Added temporary fake accounts for administrator, doctor, nurse, GP and patient roles.
- Added the first role-based responses and separate dashboard templates.

### Issues encountered and fixes

- Corrected role-value mismatches caused by capitalisation and changed role names.
- Added missing nurse and GP role checks.

### Result

Valid fake users reached the response for their own role, while invalid credentials were rejected.

## 10 July 2026 - Supervisor Progress Meeting

### Progress discussed

- Demonstrated the basic local Flask application, homepage, login form, fake users, role checking and five dashboards.
- Explained that SQLite, sessions, patient records, auditing and tamper detection were still to be completed.

### Supervisor feedback and decisions

- Keep the prototype small rather than building a complete hospital system.
- Focus the strongest evaluation on audit-log integrity and tamper evidence.
- Continue basic role-based access control as supporting security functionality.
- Investigate a small comparison involving SHA-256 and a post-quantum signature approach such as ML-DSA.
- Correct reference issues in the final report.

### Evidence

- `Meeting logs/10_July_Meeting_Log.md`

## 14 July 2026 - Login, Sessions, Logout and Protected Dashboards

### Work completed

- Completed the login form and corrected the `POST` handling.
- Added separate HTML dashboards for all five roles.
- Stored the username and role in the Flask session after successful login.
- Added logout, which clears the session and redirects to the login page.
- Added protected dashboard routes with login and role checks.
- Tested direct dashboard URL attempts using the wrong role.

### Issues encountered and fixes

- Fixed a login form and request-method mismatch.
- Moved the logout route above `app.run()` so Flask registered it correctly.
- Confirmed logout using HTTP `302` followed by a successful login-page response.

### Why this mattered

The application began enforcing access decisions on the server instead of relying only on which links appeared in the browser.

## 15 July 2026 - Temporary User Password Hashing

### Work completed

- Replaced readable temporary passwords with Werkzeug-generated password hashes.
- Used `check_password_hash()` during login.
- Created a temporary `/debug/users` route solely to confirm that stored values began with `scrypt:` rather than showing plain passwords.
- Disabled the debug route after collecting the development evidence.

### Test result

- PASS - temporary account passwords were stored as hashes.

### Limitation recorded

This check applied to the temporary Python user data. A separate SQLite password-storage check was still required after database migration.

## 16 July 2026 - SQLite Schema and Seeded Users

### Work completed

- Created the SQLite database schema and initialisation script.
- Created the `users` table and seeded administrator, doctor, nurse, GP and patient accounts with hashed passwords.
- Added a reusable database connection helper.

### Issues encountered and fixes

- Fixed a closed-database error caused by trying to use a connection after it had been closed.
- Standardised the user role column name and seed-data structure.

### Result

The database file and fake users were created successfully and could be queried from SQLite.

## 18 July 2026 - Scope and Specification Updated

### Work completed

- Created an updated copy of the project specification without changing the original submitted June file.
- Added the limited SHA-256 and ML-DSA audit-integrity comparison.
- Replaced the proposed two-question structure with one combined research question.
- Updated the matching requirements and final-report notes.
- Rendered and visually checked the five-page updated Word document.

### Scope decision

SHA-256 would remain the audit hash-chain mechanism. ML-DSA would be evaluated as a small digital-signature enhancement rather than being described as another hash function or a replacement for SHA-256.

### Evidence

- `deliverables/B01828711_Project_specification_UPDATED_2026-07-18_v2.docx`

## 20 July 2026 - Database-Backed Login Completed

### Work completed

- Replaced the temporary Python user lookup with a parameterised SQLite query.
- Read the user ID, username, password hash and role from `ehr_system.db`.
- Tested valid login and dashboard redirection for all five roles.
- Confirmed that invalid credentials were rejected.

### Issue encountered and fix

A missing comma caused an SQL parameter-binding error. The tuple passed to the query was corrected and login then worked normally.

### Test result

- PASS - all valid roles reached their correct dashboards using database accounts.

## 21-22 July 2026 - Fake Patient Records and Scope Cleanup

### Work completed

- Added the `patients` table and two fictional patient records.
- Kept Leyon Potts as the assigned test patient and Isla Olaf as the unassigned comparison patient.
- Archived the old `users_data.py` approach after database-backed login was working.
- Recorded supervisor approval of the updated specification.
- Narrowed the remaining build to two main security demonstrations: server-side access control and tamper-evident audit logging, followed by the small SHA-256/ML-DSA evaluation.

### Why this mattered

Two patients allowed the evaluation to demonstrate both permitted and denied access without using real health information.

## 22 July 2026 - Patient-Clinician Assignments

### Work completed

- Created the `patient_assignments` table.
- Assigned Leyon Potts to Dr. Helen Carter, Nurse Vanessa Miller and Dr. Nathan Wolff.
- Deliberately left Isla Olaf unassigned for negative access-control tests.

### Issues encountered and fixes

- Corrected username capitalisation.
- Corrected a misspelled `assignment_type` column.
- Corrected the number of values supplied to an SQL insert.

### Test result

- PASS - all three assignments were stored and displayed correctly.

## 22 July 2026 - Protected Patient-Record Route and Doctor Test

### Work completed

- Created the `/patient/<id>` record route.
- Added server-side rules for administrator access, patient ownership and clinician assignments.
- Created the patient-record HTML template.

### Test result

- The doctor opened assigned patient 1 successfully with HTTP `200`.
- Changing the URL to unassigned patient 2 returned HTTP `403`.
- The results were initially recorded as partial passes because audit logging had not yet been connected.

## 24 July 2026 - Role and URL-Bypass Access Tests

### Tests completed

- Patient 1 viewed patient 1 and was denied access to patient 2.
- Patient 2 viewed patient 2 and was denied access to patient 1.
- The nurse viewed assigned patient 1 and was denied access to patient 2.
- The GP viewed assigned patient 1 and was denied access to patient 2.
- The administrator viewed both patient records successfully.

### Results

- Allowed requests returned HTTP `200`.
- Direct URL bypass attempts returned HTTP `403`.
- A mistyped `/nurse/patient/1` address returned `404` and was correctly treated as a navigation mistake rather than a failed security control.

### Evidence

- Screenshots were retained under `evidence/screenshots/2026-07-24`.
- Spelling mistakes in the second fictional patient's diagnosis and treatment text were corrected before later evidence capture.

## 24 July 2026 - SHA-256 Entry-Hash Function Tested

### Work completed

- Created `calculate_entry_hash()` in `Flask/audit_log.py`.
- Converted the important audit-event fields into consistent text and calculated a SHA-256 digest.

### Tests performed

- Confirmed that the output was a 64-character hexadecimal hash.
- Repeated the same input and received the same hash.
- Changed only the details field and received a completely different hash.

### Issues encountered and fixes

- Ran the first command from the wrong folder and corrected the working directory.
- Corrected `hashib` to `hashlib`.

### Test result

- PASS - the function was deterministic and detected changed input through a different hash.

## 27 July 2026 - Persistent Two-Entry Audit Hash Chain

### Work completed

- Added the `audit_logs` table and the `log_event()` storage function.
- Stored the first event with `previous_hash = "GENESIS"`.
- Stored a second event whose `previous_hash` exactly matched the first entry's `entry_hash`.

### Issues encountered and fixes

- Corrected `ip+address` to `ip_address` in the SQL insert statement.
- Confirmed both records by querying SQLite in ID order.

### Test result

- PASS - a persistent two-entry SHA-256 hash chain was created successfully.

## 27 July 2026 - Supervisor Meeting and Comparison Controls

### Discussion and decisions

- Reviewed the working access-control prototype and early two-entry hash chain.
- Agreed to complete the core implementation before focusing heavily on the final report.
- Discussed the risk of an unfair performance comparison if SHA-256 and ML-DSA used different programming languages or environments.
- Agreed to keep the ML-DSA experiment small and use the same environment where practical.
- Selected execution time, output size and storage overhead as suitable comparison measurements.
- Agreed to create a private GitHub repository for source-code backup.

### Evidence

- `Meeting logs/27_July_Meeting_Log.md`

## 27-28 July 2026 - Audit Verification and Tampering Development Check

### Work completed

- Created `verify_audit_chain()` to read entries in ID order, verify each previous-hash link and recalculate each stored hash.
- Confirmed that the untouched chain returned `(True, 'Audit chain is valid.')`.
- Backed up the database before the deliberate test.
- Manually changed the details of the first audit entry without changing its hash.
- Confirmed that verification returned `False` and identified that entry 1 had changed.
- Restored the clean database after the development check.

### Issues encountered and fixes

- Moved `verify_audit_chain()` out of `log_event()` by correcting indentation.
- Corrected the misspelled variable `audit_entires` to `audit_entries`.
- Moved the successful return statement outside the loop so every entry was checked.

### Result

- PASS - ordinary modification of an older audit entry was detected.
- The formal deletion test and final screenshots remained outstanding.

## 28 July 2026 - Successful and Failed Login Auditing

### Work completed

- Connected `log_event()` to the Flask login process.
- Added `LOGIN_SUCCESS` for valid authentication.
- Added `LOGIN_FAILURE` for rejected authentication.
- Stored the user ID, username, role, outcome and IP address without recording the password.

### Test result

- Valid login still redirected to the appropriate dashboard.
- Invalid login remained on the login page with a general error message.
- Both actions were confirmed in SQLite and correctly linked into the SHA-256 chain.

## 28-29 July 2026 - Logout and Patient-Record Access Auditing

### Work completed

- Added a `LOGOUT` event before clearing the session.
- Confirmed the database stored the administrator logout as a successful audit event.
- Added `VIEW_PATIENT_RECORD` for authorised record access.
- Added `ACCESS_DENIED` before returning HTTP `403` for an unauthorised URL attempt.

### Test result

- Patient 1 viewed their own record successfully and was denied access to patient 2.
- Both decisions were stored in the audit log.
- The audit-chain verification result remained valid after the new events.

## 29 July 2026 - Administrator Audit-Log Viewer

### Work completed

- Created the protected `/admin/audit-logs` route and `audit_logs.html` table.
- Displayed stored login, logout, allowed-access and denied-access events with their main security fields.
- Confirmed that only the administrator role could open the route.

### Issue encountered and fix

The query originally used `.fetchone()`, causing the template to iterate through values from one row and display blank results. Changing it to `.fetchall()` returned every audit entry and populated the table correctly.

### Evidence

- Retain a screenshot of the populated administrator audit table and a non-administrator HTTP `403` response.

## 30 July 2026 - Administrator-Only Audit Verification Route

### Work completed

- Added `/admin/verify-audit-chain` using the existing verification function.
- Added a link from the administrator dashboard.

### Test result

- The administrator successfully received `Audit chain is valid.`
- A patient who manually entered the same URL received HTTP `403 Access Denied`.
- This confirmed that changing the URL did not bypass the server-side role check.

### Remaining work recorded

- Complete the deletion test.
- Produce the final styled verification result and formal screenshots.

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

## 1 August 2026 - Initial ML-DSA Signing Experiment

### Work completed

- Reviewed the documented `dilithium-py` ML-DSA-44 API.
- Adapted the documented key-generation, signing and verification process to a fictional EHR audit-log message.
- Added output lines to record whether verification succeeded and to measure the key and signature sizes.

### Results

- Public key: 1,312 bytes
- Secret key: 2,560 bytes
- Signature: 2,420 bytes
- Original signature verification: `True`

### Important technical distinction

ML-DSA is a digital-signature algorithm, while SHA-256 is a hash function. The experiment evaluates their different contributions to audit-log protection rather than claiming they perform the same operation.

### Evidence

- `Flask/experiments/mldsa/ml_dsa_test.py`
- Screenshot of the successful signing and verification output.

## 3 August 2026 - Thirty-Test ML-DSA Benchmark

### Work completed

- Expanded the ML-DSA-44 benchmark from 10 to 30 tests to obtain more reliable average measurements.
- Measured key generation, signing and verification separately.
- Recorded the key and signature sizes.
- Recorded the supervisor's approval to use the `dilithium-py` implementation.

### Results

- Average key-generation time: 17.811 milliseconds
- Average signing time: 102.297 milliseconds
- Average verification time: 19.378 milliseconds
- Public key: 1,312 bytes
- Secret key: 2,560 bytes
- Signature: 2,420 bytes
- Final signature valid: `True`

### Evidence

- `Flask/experiments/mldsa/ml_dsa_benchmark.py`

## 3 August 2026 - Combined Security Comparison Experiment Setup

### Work completed

- Created `experiments/security_comparison.py` as one script for the SHA-256 and ML-DSA comparison.
- Imported `hashlib`, `time`, `mean`, and the supervisor-approved `ML_DSA_44` implementation from `dilithium-py`.
- Set one simulated audit-log message and a shared test count of 30 so both techniques could be evaluated using the same input and repeat count.
- Ran the script successfully. It displayed the setup message, test count and decoded audit-log text.

### Why this matters

This created a fair and repeatable starting point for comparing SHA-256 hashing with ML-DSA signing and verification. The two mechanisms perform different security functions, so the comparison focuses on timing, output or storage size and tamper-detection behaviour rather than treating ML-DSA as a hash.

### Files changed

- `Flask/experiments/security_comparison.py`

### Result

The combined experiment setup ran without errors. No benchmark measurements were collected in this step.

### Next step

Add SHA-256 timing and digest-size measurements to the combined experiment, followed by ML-DSA key generation, signing, verification and size measurements.

## 3 August 2026 - ML-DSA Altered-Message Test

### Work completed

- Used `Flask/experiments/ml_dsa_test.py` to test whether an ML-DSA-44 digital signature could detect a change to a simulated EHR audit-log message.
- Generated a signature for the original message and verified it successfully.
- Changed the message and attempted verification using the original signature.

### Results

- Original-message signature valid: `True`
- Changed-message signature valid: `False`

### What this demonstrates

The ML-DSA signature is linked to the original message. If the signed audit data is changed, the original signature no longer verifies. This provides evidence of message integrity and authenticity. ML-DSA complements the SHA-256 audit hash chain rather than replacing it.

### Next step

Use the SHA-256 and ML-DSA results in the evaluation and comparison section of the final report.

## 4 August 2026 - Experiment Results Summary Completed

### Work completed

- Created `docs/experiment-results.md`.
- Summarised five saved SHA-256 and ML-DSA-44 comparison runs, using 30 repetitions in each run.
- Recorded the timing, storage-size and tampering-detection results.

### Results recorded

- SHA-256 average hashing time: approximately 0.0021 milliseconds. Its digest size was 32 bytes.
- ML-DSA-44 average key-generation time: approximately 16.57 milliseconds.
- ML-DSA-44 average signing time: approximately 100.43 milliseconds.
- ML-DSA-44 average verification time: approximately 19.71 milliseconds.
- The ML-DSA public key was 1,312 bytes, the secret key was 2,560 bytes and the signature was 2,420 bytes.
- SHA-256 and ML-DSA both detected the changed test data in all five saved experiment runs.

### What I learned

- SHA-256 is much faster and uses far less storage, making it suitable for the prototype's audit hash chain.
- ML-DSA is slower and uses larger keys and signatures, but it can also verify who signed the data.
- The two methods perform different security jobs, so one is not simply better in every situation.
- The ML-DSA results came from the educational pure-Python `dilithium-py` implementation. They should be described as prototype results rather than optimised production performance.

### Evidence produced

- `docs/experiment-results.md`
- `Flask/experiments/security_comparison_results.csv`
- `Flask/experiments/analyse_results.py`

## 4 August 2026 - Backup Before Final Testing

### Work completed

- Created a complete backup of the working Flask prototype before beginning final testing and deliberate audit-log tampering tests.

### Why this matters

The tampering tests intentionally modify audit-log data. The backup protects the completed implementation and allows the database and code to be restored if needed.

### Files or folders affected

- Created the backup folder `Flask_before_final_testing_2026-08-04`.
- No application code was changed.

### Check performed

- Confirmed that the backup folder contained the Flask application files and database.
- Continued working only in the original `Flask` folder.

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

## 10 August 2026 - Admin Pages and Access-Control Testing

### Work completed

- Created read-only administrator pages for viewing users, user-role permissions and patient-clinician assignments.
- Updated the Admin Dashboard with working links to each page.
- Confirmed that the users page does not display password hashes.

### Access-control test

- Logged in using a patient account.
- Attempted to open `/admin/users`, `/admin/roles` and `/admin/assignments` directly in the browser.
- Every route returned `403 Access Denied`, confirming that server-side role checks prevented direct URL bypass.

### Files created or changed

- `Flask/app.py`
- `Flask/templates/admin_dashboard.html`
- `Flask/templates/admin_users.html`
- `Flask/templates/admin_roles.html`
- `Flask/templates/admin_assignments.html`
- `Flask/static/css/style.css`
- `docs/project-journal.md`

### Test result

- PASS - administrators could view the new pages, while a patient account was denied access to all three routes.

### Evidence to keep

- Screenshots of the users, roles and patient-assignments pages while logged in as the administrator.
- Screenshots showing `Access Denied: Administrators Only!` for the three direct URL attempts made using a patient account.

## 10 August 2026 - Patient and Clinician Dashboards Completed

### Work completed

- Styled the patient, doctor, nurse and GP dashboards using the shared project CSS.
- Styled the shared patient-record page and added a role-aware Back to Dashboard link.
- Added `/patient/my-record`, which finds the record connected to the logged-in patient's user ID.
- Updated the doctor, nurse and GP dashboard routes to query and display only patients assigned to the logged-in clinician.
- Added working patient-record links to each clinician dashboard.
- Kept the original plain access-denied responses after deciding not to use the proposed custom error-page design.

### Server-side access checks

- Patient 1 was automatically directed to patient record 1.
- Patient 2 was automatically directed to patient record 2.
- Patient 2 was denied when manually changing the URL to patient record 1.
- The doctor, nurse and GP dashboards displayed only assigned patient Leyon Potts.
- The doctor, nurse and GP could open assigned patient record 1.
- Each clinician was denied access to unassigned patient record 2.

### Files created or changed

- `Flask/app.py`
- `Flask/templates/patient_dashboard.html`
- `Flask/templates/doctor_dashboard.html`
- `Flask/templates/nurse_dashboard.html`
- `Flask/templates/gp_dashboard.html`
- `Flask/templates/patient_record.html`
- `docs/project-journal.md`

### Test result

- PASS - each dashboard displayed the correct data, assigned-record links worked and direct URL bypass attempts remained blocked on the server.

### Evidence to keep

- Screenshots of each styled role dashboard.
- Screenshots of patient 1 and patient 2 viewing their own records.
- Screenshots of assigned clinician access and an unassigned-record denial.

## 12 August 2026 - Website Patient Creation and GP Registration Workflow

### Work completed

- Added an administrator form for creating a patient login account and linked patient record through the website.
- Created the fictional Kelly Rowland test account without manually inserting database data.
- Added an administrator form for assigning patients without a GP to an active GP account.
- Added server-side checks confirming that the selected patient exists, the selected user is an active GP and the patient does not already have a GP.
- Updated the patient's GP registration status to `Registered` when an assignment is approved.
- Added a patient-side GP registration request button for patients whose status is `Not_Registered`.
- Changed Isla Olaf's status to `Pending` when the request was submitted and displayed that status to the administrator.
- Approved Isla's request through the administrator assignment page.
- Added `PATIENT_CREATED`, `GP_REGISTRATION_REQUESTED` and `GP_ASSIGNED` audit events with explanatory details.

### Workflow testing

- Confirmed that Kelly appeared in the system users list and could log in to view her linked patient record.
- Confirmed that assigning Kelly to Dr. Nathan Wolff through the website immediately added her to the GP dashboard.
- Confirmed that the GP could open Kelly's record after assignment.
- Confirmed that Isla could request GP registration and that her status changed from `Not_Registered` to `Pending`.
- Confirmed that the administrator could see Isla's pending status, assign a GP and change her status to `Registered`.
- Confirmed that the audit log recorded the patient request, administrator assignment and subsequent record access.

### Audit-chain issue and controlled repair

- Audit verification correctly detected a mismatch at entry 97 after the first form-based GP assignment.
- The cause was identified as an ID type-normalisation issue: HTML supplied the patient ID as text, while SQLite stored it as an integer.
- Updated the form handling to convert `patient_id` and `gp_id` to integers before database and audit processing.
- Created `Flask/repair_audit_chain.py` to perform a controlled repair of the test audit chain.
- The repair utility used SQLite's backup feature before making changes and stopped unless entry 97 was confirmed as the first mismatch.
- Recalculated only `previous_hash` and `entry_hash` from entry 97 onward; the stored audit-event data was not changed.
- Added an `AUDIT_CHAIN_REPAIRED` maintenance event explaining the reason for the repair.
- Retained the pre-repair backup as `Flask/database/ehr_system_before_audit_repair_20260812_142001.db`.

### Files created or changed

- `Flask/app.py`
- `Flask/templates/admin_create_patient.html`
- `Flask/templates/admin_assignments.html`
- `Flask/templates/patient_dashboard.html`
- `Flask/repair_audit_chain.py`
- `Flask/database/ehr_system.db`
- `Flask/database/ehr_system_before_audit_repair_20260812_142001.db`
- `docs/project-journal.md`

### Test result

- PASS - patient creation, patient GP requests, administrator GP assignments and assignment-based GP access all worked through the website.
- PASS - the repaired audit chain was verified as valid after 23 affected hash-link records were recalculated.

### Evidence to keep

- Screenshots of the Add Patient form and Kelly's newly created record.
- Screenshots of Kelly and Isla appearing on the GP dashboard after administrator assignment.
- Screenshots showing Isla's `Pending` and `Registered` GP registration states.
- Screenshot of the audit log containing `GP_REGISTRATION_REQUESTED` and `GP_ASSIGNED`.
- Screenshots of the verifier detecting entry 97 and confirming a valid chain after the controlled repair.

## 12 August 2026 - Website Staff Creation and Clinician Assignment

### Work completed

- Added an administrator page for creating Doctor, Nurse and GP accounts through the website.
- Restricted the staff-account page to users with the `ADMINISTRATOR` role.
- Added server-side validation to ensure that all fields are completed.
- Required temporary passwords to contain at least eight characters.
- Prevented duplicate usernames.
- Restricted the submitted role to `DOCTOR`, `NURSE` or `GP`.
- Hashed temporary passwords before storing them in the database.
- Added a `STAFF_ACCOUNT_CREATED` audit event with the new staff member's name, username and role.
- Created the fictional Doctor account for Jalen Herts through the website.
- Extended the Patient Assignments page so an administrator can assign patients to Doctors and Nurses.
- Added server-side checks confirming that the patient exists and the selected clinician is an active Doctor or Nurse.
- Added a duplicate-assignment check.
- Added a `CLINICIAN_ASSIGNED` audit event containing the patient, clinician and role.
- Assigned Isla Olaf to Doctor Jalen Herts.
- Assigned Kelly Rowland to Nurse Vanessa Miller.

### Workflow testing

- Confirmed that Jalen Herts appeared in the System Users table as an active Doctor.
- Confirmed that Jalen could log in successfully.
- Confirmed that Jalen's Doctor Dashboard displayed only assigned patient Isla Olaf.
- Confirmed that Jalen could open Isla's patient record.
- Confirmed that the assignment appeared in the administrator's Current Assignments table.
- Confirmed that the audit log recorded the staff-account creation, login, logout and clinician-assignment events.

### Security controls demonstrated

- Staff accounts can only be created by an authenticated administrator.
- A submitted administrator role is rejected by the server-side role allow-list.
- Passwords are stored as hashes rather than readable plaintext.
- Clinical roles do not automatically provide access to every patient.
- Patient access is determined using the clinician assignments stored in the database.
- Administrative actions are recorded in the tamper-evident audit log.

### Files created or changed

- `Flask/app.py`
- `Flask/templates/admin_create_staff.html`
- `Flask/templates/admin_assignments.html`
- `Flask/templates/admin_dashboard.html`
- `Flask/database/ehr_system.db`
- `docs/project-journal.md`

### Test result

- PASS - the administrator could create a staff account through the website.
- PASS - the administrator could assign patients to Doctors and Nurses.
- PASS - the newly created Doctor could see and open only their assigned patient.
- PASS - the relevant actions appeared in the detailed audit log.

### Evidence to keep

- Screenshot of the completed Add Staff Account page.
- Screenshot of Jalen Herts in the System Users table.
- Screenshot of Isla Olaf assigned to Jalen Herts.
- Screenshot of Jalen's Doctor Dashboard displaying Isla Olaf.
- Screenshot of the `STAFF_ACCOUNT_CREATED` audit event.
- Screenshot of the `CLINICIAN_ASSIGNED` audit event.

### Next step

Run the final structured role-based access-control and audit-integrity test checklist, capture the final evidence and then freeze the prototype before completing the report analysis.

## 12 August 2026 – Final Structured Prototype Testing

| Test | Security control tested | Result |
|---|---|---|
| 1 | Invalid credentials rejected | PASS |
| 2 | Administrator access and password-data protection | PASS |
| 3 | Non-administrator blocked from admin functions | PASS |
| 4 | Patient restricted to their own record | PASS |
| 5 | Doctor restricted to assigned patients | PASS |
| 6 | Nurse restricted to assigned patients | PASS |
| 7 | GP access to registered patients and denial of admin access | PASS |
| 8 | Detailed recording of successful and denied actions | PASS |
| 9 | Audit-chain integrity verification | PASS |
| 10 | Logout clears the authenticated session | PASS |

### Summary

The structured testing confirmed that authentication, role-based access control, patient and clinician assignment checks, audit logging, audit-chain verification and session termination worked as intended.

Unauthorised attempts to access patient records or administrator functions were rejected. Successful and denied actions were recorded with the user, role, target, outcome, IP address and readable details.

### Overall result

- PASS – 10 out of 10 tests produced the expected result.
- No unresolved functional errors were identified during final testing.
- The prototype was frozen after testing so the implementation and report evidence remained consistent.