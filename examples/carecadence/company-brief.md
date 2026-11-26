# Company brief: CareCadence (fictional)

Use this fictional brief to test `/audit-ready:scope` for a **US health-tech business associate**. Run `/audit-ready:scope` with no URL, say the site is unavailable, and paste this brief as your answers. Facts from it are recorded with the source `user`.

| Area | Fact |
|---|---|
| Product | Remote patient monitoring platform. Clinics enrol patients, who send blood pressure and glucose readings from connected devices to a mobile app. Clinicians review them in a web dashboard. There's also a separate consumer "wellness" subscription app for people who aren't patients of a clinic |
| Customers | 60 US clinics and two regional health systems (HIPAA covered entities), which sign a BAA with CareCadence. Consumers pay USD 9/month for the wellness app |
| Entity | CareCadence Inc., Delaware; staff remote across the US. No office |
| Size | 55 employees |
| Data | ePHI of clinic patients (readings, diagnoses, medications, clinician notes). Consumer wellness data (not from a covered entity). Card payments for consumer subscriptions go through **Stripe Checkout** (a hosted payment page; CareCadence never sees card numbers) |
| Cloud | AWS us-east-1 and us-west-2 (DR). One production account and one staging account with synthetic data only |
| Identity | Okta (SSO and MFA), Google Workspace for email |
| Code | GitHub (org `carecadence`) |
| Endpoints | Kandji (macOS MDM) |
| HR | Rippling |
| Ask | Health systems want a SOC 2 Type II report and HIPAA Security Rule assurance. One asks for NIST CSF 2.0 alignment at target Tier 3. Stripe's acquirer asks for an annual PCI SAQ |

## Expected scoping outcome (for testers)

Machine-checkable expectations are in `expected.csv`. After running `/audit-ready:scope`, run:

```bash
python tests/check_scope_result.py --compliance <your-run>/compliance --expected examples/carecadence/expected.csv
```

The main judgements and why:

- **HIPAA: business associate.**
  - Standards and required specs are `yes`.
  - Addressable specs are `yes`, with the reason "addressable: implemented" or "addressable: alternative documented". They are never `no` just because they're addressable.
  - `164.308(a)(4)(ii)(A)` (clearinghouse) is `no`: not a clearinghouse.
  - `164.314(b)(1)` (group health plans) is `no`: not a group health plan.
  - `164.310(a)(2)(*)` facility rows are mostly `inherited` from AWS, since there's no office.
- **Consumer wellness app:** not ePHI under HIPAA, because the data doesn't come from a covered entity. The memo should flag the FTC Health Breach Notification Rule and state consumer-health laws as **out of Audit Ready's catalogs** and needing counsel review.
- **PCI DSS: SAQ A.** The hosted Stripe Checkout means most requirements are `no`, with reason "SAQ A". In scope are the SAQ A rows:
  - parts of Req 2 (vendor defaults), 3.1 and 6.3 (vulnerabilities on the site that redirects to Stripe), and 8 (accounts with admin access to that site);
  - Req 9.4 (media), 11.3 (external ASV scan of the redirecting site), 12.8 (TPSP management) and 12.10.
  - Under the January 2025 SAQ A revision, 6.4.3 and 11.6.1 were replaced by an eligibility confirmation that the site isn't susceptible to script attacks. Verify against the current SAQ A.
  - Expect 12.8 = `yes`, 3.5 = `no` and 1.3 = `no`.
- **SOC 2:** Security + Availability (health systems depend on uptime) + Confidentiality (clinical data under BAA). Privacy is optional; expect a stated reason either way.
- **NIST CSF 2.0:** in scope, with target Tier 3 recorded in `scope.md`. No row is mandatory. Expect all subcategories `yes`, unless the user excludes some with reasons.
- **Not recommended:** GDPR, DPDP and CERT-In, because there are no EU or Indian users or systems.
- **Playbooks:** aws, gh and gam. Okta has no Audit Ready playbook; suggest owner exports, or claude-grc-engineering's `okta-inspector` if it is installed.
