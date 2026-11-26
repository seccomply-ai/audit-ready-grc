# Company brief: KiranaPay (fictional)

Use this fictional brief to test `/audit-ready:scope` with no real website. Run `/audit-ready:scope` with no URL, say the site is unavailable, and paste this brief as your answers. Facts from it are recorded with the source `user`.

| Area | Fact |
|---|---|
| Product | Mobile app and merchant dashboard. Neighbourhood grocery stores (kiranas) use it to take UPI payments, issue digital receipts and run a loyalty programme |
| Customers | About 18,000 merchants in India (B2B), plus about 2 million consumers who download receipts and loyalty points (B2C) |
| Data | Consumer phone numbers, names, purchase history and loyalty balances. Merchant KYC (PAN, bank account). No card data, because payments go through a licensed payment aggregator |
| Children | The loyalty app has no age gate. Some consumers may be under 18 |
| Regulation | A partner bank (RBI-regulated) requires vendor security audits and data localisation for payment data |
| Cloud | GCP (asia-south1) for production; Azure for the analytics data warehouse (Central India) |
| Identity | Microsoft Entra ID with Conditional Access |
| Code | GitHub (org `kiranapay`), deployed with Cloud Build |
| HR | Zoho People, with 120 employees in Pune and Bengaluru |
| Ticketing | Freshservice |
| Ask | The partner bank wants ISO 27001 certification within 9 months. The board wants a DPDP readiness view |

## Expected scoping outcome (for testers)

- **Frameworks:** ISO 27001:2022, DPDP, CERT-In and RBI are in. SOC 2 is not recommended, because the brief shows no US buyers.
- **RBI:** KiranaPay is a vendor to an RBI-regulated bank, not a regulated entity itself. `RBI-OUT-03` to `RBI-OUT-07` apply as contractual flow-down. `RBI-PDL-01` to `RBI-PDL-03` apply because it handles payment system data for the partner. `RBI-ITG-*` rows are `no` unless the bank's contract imposes them.
- **CERT-In:** CERTIN-1 to CERTIN-5 apply. CERTIN-6 and CERTIN-7 are `no` (not a data centre, cloud or VPN provider, and not a VASP).
- **DPDP-9 and DPDP-R10:** applicable, because there is no age gate. Expect an open question about verifiable parental consent.
- **DPDP-10 and DPDP-R13:** an open question, since the volume of consumer and financial data may lead to notification as a significant data fiduciary. Recommend that the user confirms with counsel.
- **DPDP-16:** applicable. Payment data localisation is covered by `RBI-PDL-01`.
- **ISO clauses 4.1–10.2:** all mandatory. Annex A A.7.x is partly inherited from GCP and Azure, and the offices in Pune and Bengaluru are in scope.
- **Playbooks:** gcloud, az and gh. gam does not apply.
- **Out-of-v1 flag:** none for PCI DSS, because no card data is handled.
