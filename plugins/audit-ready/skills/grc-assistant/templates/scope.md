# Scoping memo: {{company}}

Status: draft | approved on {{date}} by {{user}}
Prepared by Audit Ready (proposal for the GRC engineer's approval). This is a readiness scoping memo, not certification or legal advice.

## Summary

{{two or three sentences: what the company does, why it needs compliance now, what is in scope}}

## Frameworks

| Framework | Decision | Reason (profile fact) |
|---|---|---|
| SOC 2 | in / out | {{e.g. "US mid-market B2B customers ask for SOC 2 (pricing page lists Enterprise tier)"}} |
| SOC 2 Trust Services Criteria | Security + {{Availability / Confidentiality / Processing Integrity / Privacy}} | {{reason per category}} |
| SOC 2 report type | Type I / Type II, period {{start}} to {{end}} | |
| ISO 27001:2022 | in / out | |
| DPDP Act 2023 + Rules 2025 | in / out | |

## System boundary

- Product / service in scope: {{name}}
- Environments: {{production cloud accounts / projects / subscriptions}}
- Locations: {{offices, remote}}
- People: {{functions and approximate headcount}}
- Out of boundary: {{e.g. marketing site, internal sandbox}} because {{reason}}

## Inherited controls (subprocessors)

| Vendor | What it provides | Requirements inherited | Evidence needed |
|---|---|---|---|
| {{AWS}} | {{hosting, physical security}} | {{soc2:CC6.4; iso27001:A.7.1-A.7.14}} | {{vendor SOC 2 Type II report}} |

## Applicability summary

| Framework | Total | Applicable | Inherited | Not applicable |
|---|---|---|---|---|
| | | | | |

Full detail: `applicability.csv`. Mandatory items (SOC 2 Common Criteria, ISO 27001 clauses 4 to 10) are always applicable.

## Exclusions and reasons

- {{req_id}}: {{reason}}

## Assumptions and open questions

- {{assumption}}

## Next steps

1. `/audit-ready:evidence-plan`
