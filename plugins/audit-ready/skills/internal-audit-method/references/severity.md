# Finding severity

| Severity | Definition | Examples |
|---|---|---|
| **major** | Likely to cause a qualified SOC 2 opinion, an ISO major nonconformity, or a DPDP compliance failure. This covers a control that's missing or not working across the board, and a mandatory requirement with no evidence. | MFA not enforced for staff or admins; no risk assessment in the period; no internal audit or management review (ISO 9.2, 9.3); changes merged to production without review as standard practice; no breach notification process (DPDP-8-6); leavers keep access for weeks |
| **minor** | The control exists and mostly works, but has isolated exceptions or gaps in documentation that an auditor would raise as an exception or a minor nonconformity. | 1 of 25 sampled PRs merged without approval; policy not reviewed in 12 months; 2 of 40 users without MFA; access review done for 3 of 4 quarters |
| **observation** | Not a failure today. An improvement or risk to note before the audit. | Log retention is exactly 365 days with no margin; super admins at the limit; evidence is a screenshot where an export would be stronger |

Rules:

- A `fails` verdict on a mandatory requirement (SOC 2 CC, ISO clauses 4–10) is at least `major`, unless it is only missing documentation and the control demonstrably works.
- Multiple minor findings with the same root cause can add up to one major finding. Say so in the finding.
- Severity reflects audit impact, not effort to fix.
