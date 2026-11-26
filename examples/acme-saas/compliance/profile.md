# Business profile: Acme Shift (fictional)

Status: confirmed on 2026-11-20 by user

> Fictional sample company for testing Audit Ready. `acme-shift.example` is not a real website. Sources are marked `site` (the sample brief) or `user`.

## Company

| Fact | Value | Source |
|---|---|---|
| Legal / trading name | Acme Shift Technologies Pvt Ltd | site: /about |
| Website | https://acme-shift.example | site |
| What the product does | B2B SaaS that schedules shifts and tracks attendance for retail and logistics staff | site: / |
| Customers | Mid-market retail and logistics companies (B2B) | site: /customers |
| Customer geographies | India, UAE, United States | site: /customers |
| Pricing model / enterprise tier | Per-seat; Enterprise tier with SSO and a 99.9% uptime SLA | site: /pricing |
| Headcount (approx.) | 42 employees, 3 contractors | user |
| Offices and remote countries | Bengaluru co-working office; remote staff in India | user |

## Data handled

| Fact | Value | Source |
|---|---|---|
| Personal data of customers' users | Name, phone, work email, shift and attendance records of customers' employees | site: /privacy |
| Personal data of Indian data principals | Yes: most end users are in India | site: /privacy |
| Children's data | No: end users are employees aged 18+ | user |
| Payment card data | No: billing via Razorpay hosted checkout | site: /privacy |
| Data residency / regions | AWS ap-south-1 (Mumbai) | site: /subprocessors |

## Technology and tools

| Area | Tool | Source |
|---|---|---|
| Cloud | AWS (1 production account, 1 staging account) | site: /subprocessors; user |
| Identity provider / SSO | Google Workspace | user |
| Code host | GitHub (org `acme-shift`) | user |
| CI/CD | GitHub Actions | user |
| Ticketing | Jira | user |
| HRMS | Keka | user |
| Endpoint management / MDM | None yet | user |

## Trust signals

| Fact | Value | Source |
|---|---|---|
| Existing certifications / reports | None | site: /security |
| Subprocessor list | AWS (hosting, India), Razorpay (billing, India), Freshdesk (support, US), SendGrid (email, US) | site: /subprocessors |
| Grievance officer | Named on privacy page | site: /privacy |

## Audit context

| Fact | Value | Source |
|---|---|---|
| Target framework(s) asked for | SOC 2 (US enterprise prospect); DPDP readiness | user |
| Target audit date | Q1 2027 Type I, then Type II | user |
| Audit period | 2026-06-01 to 2026-11-30 (readiness window) | user |
