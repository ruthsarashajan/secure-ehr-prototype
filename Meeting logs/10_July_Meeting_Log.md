## Supervisor Meeting - 10 July 2026

**Supervisor:** Raman Singh  
**Student:** Ruth Sara Shajan  
**Project:** Secure web-based access control and tamper-evident audit logging framework for simulated EHRs

### Purpose of meeting

To update the supervisor on early implementation progress and confirm whether the project scope and direction are still suitable before continuing with the prototype.

### Progress discussed

I explained that I had started building the Flask prototype. At this stage, the prototype includes:

- a basic Flask web application running locally;
- a homepage;
- a login page;
- a login form using POST;
- temporary fake users;
- role checking for admin, doctor, nurse, GP, and patient;
- separate dashboard pages for each role.

I explained that the database, password hashing, sessions, patient records, access-control checks, audit logs, and tamper-detection features are not complete yet.

### Supervisor feedback

The supervisor advised that the project does not need to become a full working hospital system. The project should stay focused and prove one clear security feature properly.

The supervisor said I could either use an existing website or continue building my own small prototype. The important point is that the prototype should support the security feature being evaluated.

The supervisor asked whether the project is using blockchain. I clarified that the project is not using a full blockchain platform, but is using blockchain-inspired tamper-evident logging ideas.

The supervisor suggested comparing SHA-based audit-log protection with a post-quantum digital signature method, such as ML-DSA or FN-DSA.

The supervisor also said not to worry about the interim report reference issue, but I should make sure the final report references are correct and complete.

### Decisions after meeting

The project will continue as a small Flask and SQLite simulated EHR prototype.

The main focus will be narrowed toward audit-log integrity and tamper evidence.

The prototype will still include basic role-based access control, but the strongest evaluation feature will be the audit log.

The audit-log evaluation may compare:

- SHA-256 hash-chain audit logging;
- ML-DSA or FN-DSA signed audit-log entries.

### Questions/issues to follow up

- Confirm whether ML-DSA or FN-DSA should be used.
- Confirm whether the project specification needs formal updating, or whether this can be explained as a refinement in the final report.
- Check what Python library can be used safely for ML-DSA or FN-DSA.
- Keep the fake patient data fully synthetic, not real patient data.

### Action points

- Record this meeting in the project process documentation.
- Continue building the Flask prototype.
- Avoid adding unnecessary healthcare features.
- Focus on login, roles, patient records, audit logs, and tamper-evidence testing.
- Fix reference issues properly in the final report.