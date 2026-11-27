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

## Inspector results (claude-grc-engineering imports)

Imported inspector runs and gap reports (`index.csv` rows with `source` starting with an inspector name or `grc-engineer gap-assessment`) are configuration evidence across many resources. Read them with `jq`, never whole.

| Inspector result | Verdict for the linked requirement | Starting severity |
|---|---|---|
| every in-scope resource `pass` | satisfies (for that system) | none |
| any `fail` with severity `critical` or `high` | fails | major |
| any `fail` with severity `medium` | partial, or fails if most resources fail | minor (major when it fails across the board) |
| any `fail` with severity `low` or `info` | partial | observation |
| only `inconclusive`, `skipped` or `not_applicable` | partial, gap "inspector could not evaluate: <message>" | none: plan manual evidence instead |

- The starting severity is a proposal. Apply the rules above: a fail on a mandatory requirement is at least major, and repeated minors with one root cause can add up to a major.
- One finding per root cause and requirement, not per resource. List the affected `resource.id` values (or their count when more than 10) in the finding, and use `remediation.summary` as the starting `fix`.
- Inspector runs are point-in-time. For a period-based requirement they show the current design, not operation over the period; say so in the gap unless a sample covers the period.
