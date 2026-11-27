# Question bank

Ask only questions the website did not answer. Ask at most 5 per round, highest priority first. Each question carries its "why it matters" line, written as shown.

## Round 1: systems (drives the evidence plan)

| # | Question | Why it matters |
|---|---|---|
| Q1 | Which cloud providers run production (AWS, GCP, Azure, other)? List account, project or subscription names if you can. | Sets the system boundary and which CLI playbooks can collect evidence automatically. |
| Q2 | Which identity provider do staff sign in with (Google Workspace, Okta, Microsoft Entra ID, other)? Is MFA enforced for everyone? | Access control evidence (SOC 2 CC6.1, ISO A.5.17/A.8.5) comes from here. |
| Q3 | Where is code hosted (GitHub, GitLab, Bitbucket), and how do changes reach production? | Change management evidence (SOC 2 CC8.1, ISO A.8.32) comes from the code host and CI. |
| Q4 | Which HR system holds joiners and leavers (Keka, Zoho People, Darwinbox, BambooHR, spreadsheet)? | Onboarding and offboarding sampling needs a reliable joiner/leaver list. |
| Q5 | Which ticketing tool tracks access requests, incidents and changes (Jira, Linear, Freshservice, other)? | Most manual evidence (approvals, incidents) lives in tickets. |

## Round 2: people and places

| # | Question | Why it matters |
|---|---|---|
| Q6 | Roughly how many employees and contractors, and in which countries? | Sets sampling sizes and which employment and privacy laws apply. |
| Q7 | Do you have offices, or is everyone remote? Where are the offices? | Physical security is either in scope or mostly inherited from the cloud provider. |
| Q8 | How are laptops managed (MDM such as Jamf, Intune, Kandji, none)? | Endpoint evidence (SOC 2 CC6.8, ISO A.8.1) depends on it. |
| Q9 | Who owns security, IT, HR and legal day to day? Give names or roles. | Evidence requests go to these owners. |

## Round 3: audit context

| # | Question | Why it matters |
|---|---|---|
| Q10 | Which framework did a customer, investor or regulator ask for, and by when? | Decides priorities and Type I vs Type II. |
| Q11 | What audit period do you want (for SOC 2 Type II, usually 3 to 12 months)? | Evidence must cover the whole period. |
| Q12 | Do you have existing policies, a risk register or a previous audit report? | Avoids rewriting what exists and shows the starting maturity. |
| Q13 | Do you process personal data of people in India, children's data, card data or health data? | Triggers DPDP and its conditional duties, and PCI DSS or HIPAA. |
| Q14 | Are any of your customers regulated (banks, NBFCs, insurers, healthcare)? | Sector rules (RBI, SEBI, IRDAI) can add requirements such as data localisation. |
| Q15 | Which products or environments should be excluded, and why? | Every exclusion needs a reason in the scoping memo. |

## Round 4: framework-specific (ask only for frameworks in scope)

| # | Question | Why it matters |
|---|---|---|
| Q16 | GDPR: are you a controller, a processor, or both for EU personal data? Do you have an EU establishment? | Decides which GDPR articles apply, and whether an EU representative (Art 27) is needed. |
| Q17 | PCI DSS: how do you take card payments (hosted page or redirect, embedded fields, your own API)? Merchant or service provider? Which SAQ did your acquirer ask for? | The SAQ type decides which PCI requirements apply. With a hosted page, most rows are out of scope. |
| Q18 | HIPAA: are you a covered entity or a business associate? Which systems hold ePHI? | Sets the HIPAA boundary, and which business associate agreements are needed. |
| Q19 | NIST CSF: which target tier (1 to 4) do you aim for, and for which scope? | CSF has no mandatory items; the target profile defines what "ready" means. |
| Q20 | NIS2: which sector are you in, how large are you (staff, turnover), and in which EU countries? Are you a cloud, data centre, MSP or MSSP provider? | Decides whether you are an essential or important entity, which national law applies, and whether the 2024/2690 annex applies. |
| Q21 | DORA: are you a financial entity, or an ICT provider to financial entities? Do your services support their critical or important functions? | Financial entities have direct obligations; suppliers get contract requirements (Art 30). |
| Q22 | India: are you a data centre, VPS, cloud or VPN provider, or a virtual asset service provider? | Adds the CERT-In subscriber-record and KYC obligations (CERTIN-6, CERTIN-7). |
| Q23 | RBI / SEBI: are you a regulated entity (which category), or a technology vendor to one? Do you store or process payment system data? | Decides which RBI or SEBI requirements apply directly and which come through contracts, and whether payment data must stay in India. |
| Q24 | AI: which AI systems do you build, fine-tune, host or buy, and is your role provider, producer or user? Which decisions about people does the AI make or support? | Decides ISO 42001 Annex A applicability (A.6 and A.7 only for those that build AI) and which impact assessments (6.1.4, A.5) are needed. |
