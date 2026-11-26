# Examples

Both companies are fictional. They let you test Audit Ready end to end without touching a real business.

| Example | What it shows | Use it to test |
|---|---|---|
| `acme-saas/` | A complete `compliance/` folder partway through a programme: confirmed profile, approved scope (SOC 2 Security + Availability, DPDP), an 11-item evidence plan, 4 filed and hashed artifacts, assessments, findings and an internal audit report | `/audit-ready:status`, `/audit-ready:inbox`, `/audit-ready:audit`, the CSV validation, and hash verification |
| `kirana-pay/` | Company brief and expected outcome: ISO 27001, DPDP (children's data), CERT-In, RBI as a vendor | `/audit-ready:scope` and `/audit-ready:evidence-plan` |
| `ledgerloop/` | Company brief and expected outcome: EU ICT supplier to banks, covering DORA supplier mode, GDPR controller and processor, an NIS2 open question, a PCI negative case, and CERT-In and DPDP for an India subsidiary | `/audit-ready:scope` |
| `carecadence/` | Company brief and expected outcome: US health-tech business associate, covering HIPAA addressable specs, PCI SAQ A, SOC 2 categories and a NIST CSF target tier | `/audit-ready:scope` |

Each example has an `expected.csv`. After a scoping run, check the result with `tests/check_scope_result.py`; see `tests/README.md`.

## Try it

```bash
cp -r examples/acme-saas /tmp/acme && cd /tmp/acme
claude
> /audit-ready:status
```

The expected status shows SOC 2 readiness at 4% (0 satisfied, 3 partial, 36 applicable; CC6.1 is partial because the worst verdict counts) and DPDP at 0%. It lists 3 open findings (1 major) and 4 requested owner items.

To check evidence integrity by hand:

```bash
cd compliance/evidence
tail -n +2 index.csv | python3 -c "import csv,sys; [print(r[6]+'  '+r[0]) for r in csv.reader(sys.stdin)]" | sha256sum -c
```
