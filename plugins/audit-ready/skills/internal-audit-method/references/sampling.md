# Sampling

## Sample sizes

These sizes are based on how often the control runs, which is the convention most SOC 2 and ISO auditors use. When the population is smaller than the sample size, test every item.

| How often the control runs | Typical population per year | Sample size | Tolerable exceptions |
|---|---|---|---|
| Annually | 1 | 1 | 0 |
| Quarterly | 4 | 2 | 0 |
| Monthly | 12 | 2 | 0 |
| Weekly | 52 | 5 | 0 |
| Daily | 365 | 20 | 0 |
| Many times a day / event-driven (changes, joiners, leavers, tickets) | > 250 | 25 | 0, or 1 with a strong explanation |
| Event-driven, small population | < 250 | 10, or 10% (whichever is larger), up to 25 | 0 |

Scale the sample down in proportion when the audit period is shorter than a year. For a 6-month period, the annual control is still tested once, and quarterly becomes 2.

For readiness work, any exception means the verdict is `partial` at best, and the finding should say how many failed out of how many sampled.

## Reproducible selection

Select samples so another person can check and repeat the selection:

1. Use the population file that was filed as evidence (for example, `gh_merged-prs_<repo>.json` or the HR leaver export), and cite it.
2. Sort the population by a stable key, such as id or date.
3. Pick the items using one of the following, and record which method you used:
   - **Interval:** pick every k-th item, where k = floor(N / n), starting at a start position s < k. Record N, n, k and s.
   - **Seeded random:** a seeded selection, where you record the seed (for example `20261126`) and the list of indices chosen.
   Never pick "interesting" items by hand without saying so.
4. Write the selection in the report's sampling appendix: the population file, N, n, the method, and the selected ids.

## Common tests

| Control | Population | Test per sample | Requirements |
|---|---|---|---|
| Change management | Merged PRs to production branches in the period | An approved review by someone other than the author before merge; CI checks passed; no bypass of protection | soc2:CC8.1; iso27001:A.8.32 |
| Joiners | HR joiners in the period | Background check (where allowed by law) before the start date; signed NDA or code of conduct; security training within 30 days; access request approved | soc2:CC1.1, CC1.4, CC2.2, CC6.2; iso27001:A.6.1, A.6.2, A.6.3, A.6.6 |
| Leavers | HR leavers in the period | IdP account suspended within the SLA (usually 1 business day, or what the policy says); code host and cloud access removed; assets returned | soc2:CC6.2, CC6.3; iso27001:A.5.11, A.5.18, A.6.5 |
| Access reviews | Quarterly reviews in the period | Review done, with the reviewer named, the date recorded, and the changes actioned | soc2:CC6.3; iso27001:A.5.18 |
| Incidents | Incident tickets in the period | Triaged, responded to and closed per the IR plan; postmortem for high-severity incidents; DPDP breach notified within 72 hours where personal data was involved | soc2:CC7.3–CC7.5; iso27001:A.5.24–A.5.27; dpdp:DPDP-8-6, DPDP-R7 |
| Vulnerabilities | Critical and high alerts opened in the period | Fixed within the policy SLA | soc2:CC7.1; iso27001:A.8.8 |
| Backups | Backup jobs in the period, plus restore tests | Jobs succeeded; at least one restore test in the period | soc2:A1.2, A1.3; iso27001:A.8.13 |
| Vendors | New vendors in the period | Risk assessment and a DPA or security review before onboarding | soc2:CC9.2; iso27001:A.5.19, A.5.20; dpdp:DPDP-8-2 |

For leaver testing, match HR leavers against the active accounts in the IdP and code host exports, by email or by name when emails differ. When a match is ambiguous, list it for the user to confirm. Never mark a person a leaver who is still active without asking.
