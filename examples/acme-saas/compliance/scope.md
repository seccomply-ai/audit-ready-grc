# Scoping memo: Acme Shift (fictional)

Status: approved on 2026-11-20 by user
Prepared by Audit Ready as a proposal for the GRC engineer's approval. This is a readiness scoping memo, not certification or legal advice.

## Summary

Acme Shift sells B2B shift-scheduling SaaS to retail and logistics companies in India, the UAE and the US. A US enterprise prospect has asked for SOC 2, and most end users are Indian data principals. Scope is SOC 2 (Security and Availability) and the DPDP Act 2023 with the Rules 2025.

## Frameworks

| Framework | Decision | Reason (profile fact) |
|---|---|---|
| SOC 2 | in | US enterprise prospect asked for it (user) |
| SOC 2 TSC | Security + Availability | Security is mandatory. Availability: Enterprise tier promises a 99.9% SLA (site: /pricing). Confidentiality, Processing Integrity and Privacy are not selected (see applicability.csv) |
| SOC 2 report type | Type I in Q1 2027, then Type II | No prior audits (site: /security) |
| ISO 27001:2022 | out for now | No customer has asked yet; revisit for UAE enterprise deals |
| DPDP Act 2023 + Rules 2025 | in | Processes personal data of Indian employees of customers (site: /privacy) |

## System boundary

- Product in scope: Acme Shift web app, mobile app and API.
- Environments: AWS production account. Staging is out of scope because it holds no production data (user).
- Locations: the Bengaluru co-working office has no servers; staff are remote in India.
- People: all 42 employees and 3 contractors.

## Inherited controls

| Vendor | What it provides | Requirements inherited | Evidence needed |
|---|---|---|---|
| AWS | Data centre physical security | soc2:CC6.4 | AWS SOC 2 Type II report and CUEC review (EV-010) |

## Applicability summary

| Framework | Total | Applicable | Inherited | Not applicable |
|---|---|---|---|---|
| SOC 2 | 61 | 35 | 1 | 25 |
| DPDP | 32 | 24 | 0 | 8 |

## Next steps

1. `/audit-ready:evidence-plan`
