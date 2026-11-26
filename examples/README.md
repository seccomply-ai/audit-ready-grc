# Examples

Both companies are fictional. They let you test Audit Ready end to end without touching a real business.

| Example | What it shows | Use it to test |
|---|---|---|
| `acme-saas/` | A complete `compliance/` folder partway through a programme: confirmed profile, approved scope (SOC 2 Security + Availability, DPDP), an 11-item evidence plan, 4 filed and hashed artifacts, assessments, findings and an internal audit report | `/audit-ready:status`, `/audit-ready:inbox`, `/audit-ready:audit`, the CSV validation, and hash verification |
| `kirana-pay/` | A company brief and the scoping outcome a tester should expect (ISO 27001 + DPDP, children's data, RBI overlay) | `/audit-ready:scope` and `/audit-ready:evidence-plan` |

## Try it

```bash
cp -r examples/acme-saas /tmp/acme && cd /tmp/acme
claude
> /audit-ready:status
```

The expected status shows SOC 2 readiness at 6% (1 satisfied, 2 partial, 36 applicable) and DPDP at 0%. It lists 3 open findings (1 major) and 4 requested owner items.

To check evidence integrity by hand:

```bash
cd compliance/evidence
tail -n +2 index.csv | python3 -c "import csv,sys; [print(r[6]+'  '+r[0]) for r in csv.reader(sys.stdin)]" | sha256sum -c
```
