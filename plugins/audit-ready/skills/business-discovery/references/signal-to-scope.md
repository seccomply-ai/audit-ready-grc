# Signal to scope

Each rule turns a profile fact into a scoping proposal. When you use a rule, cite the profile fact (with its source) in `scope.md` or in the `reason` column of `applicability.csv`.

## Frameworks

| Signal | Proposal |
|---|---|
| B2B SaaS, US or global customers, an enterprise tier, or a security questionnaire page | SOC 2 in scope |
| Enterprise customers in EU, UK, India, the Middle East or APAC, government buyers, or an RFP that asks for a certificate | ISO 27001:2022 in scope |
| Users, customers or employees in India; INR pricing; an Indian entity or office; a grievance officer named in the privacy policy | DPDP in scope |
| Card payments handled directly (not only through Stripe or Razorpay hosted pages) | PCI DSS 4.0.1 (`pci-dss`). Ask Q17 to find the SAQ; `/pci-dss:saq-select` helps if that plugin is installed. Hosted checkout only usually means SAQ A, with most requirements out of scope |
| Health records of US patients; covered entity or business associate | HIPAA Security Rule (`hipaa-security`). Ask Q18. Add a BAA item for each vendor that touches ePHI |
| EU or UK residents' personal data | GDPR (`gdpr`). Ask Q16. Evidence overlaps heavily with DPDP and SOC 2 Privacy |
| Customers are EU banks, insurers or investment firms | DORA (`dora`). Ask Q21. For an ICT supplier, scope it as contractual flow-down (Art 28.4, 30.2, 30.3) |
| EU essential or important sector (energy, transport, health, digital infrastructure, managed services), or a listed digital provider | NIS2 (`nis2`). Ask Q20 and confirm the entity classification |
| US federal or defence customers | NIST 800-53 / FedRAMP / CMMC (SCF-backed). Ask about the impact level or CMMC level |
| US enterprise wants a baseline, or there's no certification target | NIST CSF 2.0 (`nist-csf-2.0`). Ask Q19 for the target tier |
| Operates in India (any company with ICT systems there) | CERT-In (`cert-in`): 6-hour incident reporting, 180-day logs kept in India, NTP sync, point of contact. Ask Q22 |
| RBI-regulated entity, or a vendor or payment system participant for one | RBI (`rbi`). Ask Q23. Vendors get the outsourcing flow-down rows |
| SEBI-regulated entity, or a technology vendor to one | SEBI CSCRF (`sebi-cscrf`). Ask Q23 for the RE category |
| The user names any other framework | Look it up in `framework-reference/frameworks.csv` |

## SOC 2 categories

| Signal | Category |
|---|---|
| Uptime SLA, status page, or a "99.9%" claim | Availability |
| Customers upload confidential business data; NDAs or MSAs promise confidentiality | Confidentiality |
| Product computes money, payroll, invoices or regulated reports | Processing Integrity |
| B2C product that collects personal data directly, where customers ask for Privacy | Privacy |

## System boundary

| Signal | Boundary proposal |
|---|---|
| Separate production cloud account, project or subscription | In scope. Dev and sandbox stay out if they hold no production data (state this) |
| Marketing site on a separate host (Webflow, WordPress) | Out of boundary, unless it collects personal data through forms (that matters for DPDP) |
| Mobile app | In scope with the backend |
| Fully remote | Offices are out of scope. Physical controls are inherited from the cloud provider; endpoints stay in scope |

## Inheritance (from the subprocessor list)

| Subprocessor | Usually inherited | Evidence needed |
|---|---|---|
| AWS, GCP or Azure hosting | SOC 2 CC6.4, CC6.5 (physical media), A1.2 (environmental); ISO A.7.1–A.7.14 (except office and endpoint items), A.8.14 partly | The provider's current SOC 2 Type II report or ISO certificate, plus a note that the complementary user entity controls (CUECs) were reviewed |
| Payment processor (Stripe, Razorpay) | Card data handling | The processor's PCI attestation (AOC) |
| Email or support SaaS | Nothing inherited. They are vendors to assess under CC9.2, A.5.19 and DPDP-8-2 | DPA and the vendor's security report |

## Conditional DPDP items

| Signal | Item |
|---|---|
| Signup has no age gate, or product targets students, schools or games | DPDP-9 and DPDP-R10 applicable |
| Large volume of sensitive data, or government notification | DPDP-10 and DPDP-R13 may apply. Ask the user; they apply only when notified |
| Data stored or processed outside India (from the subprocessor list) | DPDP-16 and DPDP-R15 applicable |
| Uses a registered consent manager | DPDP-6-CM applicable |
| E-commerce, gaming or social media platform with a large user base | DPDP-R8 may apply. Ask the user |
