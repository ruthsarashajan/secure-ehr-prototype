# Supervisor Meeting Log - 27 July 2026

## Meeting Details

- Student: Ruth Sara Shajan
- Supervisor: Raman Singh
- Date: 27 July 2026
- Meeting type: Online supervisor meeting

## Agenda

1. Review the progress of the prototype.
2. Discuss the planned comparison involving SHA-256 and ML-DSA.
3. Discuss whether the implementations should use the same programming language.
4. Confirm the main priorities before the final report deadline.

## Discussion

- The supervisor advised creating a GitHub account and repository for the project.
- The final report can include a link to the code repository.
- The supervisor advised completing the main implementation before concentrating heavily on the final report.
- An implementation of ML-DSA may be available in C.
- The use of different programming languages for the two implementations was discussed.
- Python can take longer to run than compiled languages, while languages such as Rust may run more quickly.
- A direct performance comparison between implementations written in different languages may not be fair because the programming language could affect the result.
- Where practical, both methods should be evaluated using the same language or environment.
- The comparison does not need to be extensive. It should remain small and relevant to the cybersecurity aim of the project.

## Decisions

- Keep the main prototype focused on role-based access control and tamper-evident audit logging.
- Complete the SHA-256 audit-chain implementation and its security tests first.
- Keep the ML-DSA comparison focused rather than developing a second large system.
- Use the same implementation environment for the comparison where practical.
- Clearly explain any limitations if different languages or libraries have to be used.

## Action Points

- Create a private GitHub repository and use it to back up the project code.
- Complete the audit-chain verification and tampering-detection features.
- Research a practical ML-DSA implementation that can be used from the chosen environment.
- Decide on a small set of comparison measurements, such as execution time, output size and storage overhead.
- Record screenshots, test results and limitations for use in the final report.
- Continue drafting the final report while prioritising completion of the working implementation.

## Reflection

The meeting clarified that comparing implementations written in different programming languages could produce misleading performance results. The comparison must therefore be kept controlled and its limitations must be explained clearly.

