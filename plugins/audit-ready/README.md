# Audit Ready plugin

Audit Ready is a GRC assistant inside Claude Code. Scope it, collect it, audit it. It ships curated catalogs for SOC 2, ISO 27001:2022, GDPR, PCI DSS 4.0.1, the HIPAA Security and Breach Notification Rules, NIST CSF 2.0, NIS2, DORA and India's DPDP Act, CERT-In Directions, RBI and SEBI CSCRF, and covers about 240 more frameworks through SCF crosswalks.

- **Scoping.** `/audit-ready:scope <url>` reads the company website, asks only what the site can't show, recommends frameworks, and drafts a Statement of Applicability and a scoping memo.
- **Evidence collection.**
  - `/audit-ready:evidence-plan` turns the scope into a list of evidence to gather.
  - `/audit-ready:collect` runs read-only gh, aws, gam, gcloud and az commands after you approve them, then hashes and indexes what they return.
  - `/audit-ready:request` drafts the requests to evidence owners.
  - `/audit-ready:inbox` files what owners send back.
- **Internal audit.** `/audit-ready:audit <function>` tests evidence, takes samples, and proposes verdicts and rated findings. It writes the internal audit report after you approve.
- **Status.** `/audit-ready:status` shows readiness per framework, computed from the files.
- **Hand-off.** `/audit-ready:package <fingerprint>` builds an encrypted, hash-manifested evidence bundle for the auditor.
- **claude-grc-engineering (optional).** Inspector runs and gap assessments are imported as evidence, and their failures become proposed findings.

Start with `/audit-ready:start`. Everything the plugin produces is plain Markdown or CSV in `compliance/`. See the repository README for details, safety rules and examples.
