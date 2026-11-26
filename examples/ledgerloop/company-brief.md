# Company brief: LedgerLoop (fictional)

Use this fictional brief to test `/audit-ready:scope` for an **EU ICT supplier to financial entities**. Run `/audit-ready:scope` with no URL, say the site is unavailable, and paste this brief as your answers. Facts from it are recorded with the source `user`.

| Area | Fact |
|---|---|
| Product | B2B SaaS for payment reconciliation and exception handling, used by banks and payment institutions to match settlement files against ledgers |
| Customers | 23 EU banks and licensed payment institutions in the Netherlands, Germany and Ireland. Three tier-1 banks have sent a "DORA ICT third-party addendum" to sign, and they classify LedgerLoop as supporting a critical or important function |
| Entity | LedgerLoop B.V., Amsterdam (EU establishment), not licensed by any financial regulator. A wholly owned engineering subsidiary in Pune, India (LedgerLoop Technologies Pvt Ltd) |
| Size | 140 staff (95 in Pune, 45 in Amsterdam), EUR 18M turnover |
| Data | Settlement files with payer and payee names, IBANs, amounts and references, processed **on behalf of** the banks. LedgerLoop's own employee data (both countries), plus marketing leads in a CRM. **No card numbers (PAN).** |
| Cloud | AWS eu-central-1 (Frankfurt) for production. Engineers in Pune reach production via SSO plus a bastion; no production data is stored in India |
| Identity | Google Workspace (SSO for AWS and GitHub) |
| Code | GitHub (org `ledgerloop`), GitHub Actions deploy to AWS |
| HR | Personio (NL), Keka (India) |
| Ticketing | Jira; PagerDuty on call |
| Ask | The banks want ISO 27001 certification and DORA contract compliance. Legal asked whether NIS2 applies, and for a GDPR view |

## Expected scoping outcome (for testers)

Machine-checkable expectations are in `expected.csv`. After running `/audit-ready:scope`, run:

```bash
python tests/check_scope_result.py --compliance <your-run>/compliance --expected examples/ledgerloop/expected.csv
```

The main judgements and why:

- **DORA: supplier mode.** LedgerLoop isn't a financial entity, so Arts 5–27 are `no`, with reason "not a financial entity; obligations flow down via customer contracts". Exceptions are the Art 9–12 controls the addenda impose: the brief says the addenda require ICT security, detection, BCP and backup controls, so expect Art 9–12 = `yes` (contractual). Art 28.4, 30.2 and 30.3 are `yes`, because the addenda follow Art 30 and the service supports a critical or important function.
- **GDPR: controller and processor.** It is a processor for the banks' settlement data and a controller for its own employee and lead data. So the rights articles (12–21) stay `yes` (controller duties for its own data), and Art 28 is `yes` (processor duties). Art 27 (EU representative) is `no`, because it has an EU establishment. Art 8 (children) is `no`. Arts 44–46 are `yes`, because staff in India can access EU data (a transfer, through remote access).
- **NIS2: an open question, not in by default.** A reconciliation SaaS isn't obviously a "managed service provider" in Annex I. It is a medium-sized company and could be in scope if the Dutch transposition treats it as an MSP. Expect the scope memo to raise this as an open question for counsel. Either outcome is acceptable, as long as the IR-* rows are `no` unless the user confirms MSP status.
- **ISO 27001:** in scope, because the banks ask for it. Clauses 4.1–10.2 are mandatory. A.7.x is mostly `inherited` from AWS; the office rows stay `yes` for Amsterdam and Pune.
- **CERT-In and DPDP:** in scope for the Pune subsidiary (ICT systems and employee personal data in India). CERTIN-6 and CERTIN-7 are `no`.
- **PCI DSS: not recommended.** IBANs and settlement data aren't cardholder data. The memo should say so in one line.
- **SOC 2:** not recommended. No US customers.
- **Playbooks:** aws, gh and gam. gcloud and az don't apply.
