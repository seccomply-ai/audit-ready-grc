# Sampling

## Sample sizes

Sample sizes depend on how often the control runs, as most SOC 2 and ISO auditors size them. Audit Ready uses the **readiness minimum** column. It's the smallest sample that gives a meaningful internal signal. External auditors often test more, and their firm's methodology decides. When the population is smaller than the sample size, test every item.

| How often the control runs | Typical population per year | Readiness minimum (Audit Ready) | Typical external auditor range | Tolerable exceptions |
|---|---|---|---|---|
| Annually | 1 | 1 | 1 | 0 |
| Quarterly | 4 | 2 | 2 | 0 |
| Monthly | 12 | 3 | 2–5 | 0 |
| Weekly | 52 | 10 | 5–15 | 0 |
| Daily | 365 | 25 | 25–40 | 0 |
| Many times a day / event-driven (changes, joiners, leavers, tickets) | > 250 | 25 | 25–60 | 0, or 1 with a strong explanation |
| Event-driven, small population | < 250 | 10, or 10% (whichever is larger), up to 25 | 10–25 | 0 |

For a period shorter than a year, scale only the periodic controls (annual, quarterly, monthly, weekly) down in proportion. For a 6-month period, the annual control is still tested once and quarterly becomes 2. Daily and event-driven samples stay at the minimum.

Say in the report that these are readiness minimums. Recommend asking the external auditor for their sample sizes before fieldwork.

For readiness work, any exception means the verdict is `partial` at best, and the finding should say how many failed out of how many sampled.

## Reproducible selection

Select samples so another person can check and repeat the selection:

Audit Ready uses **systematic interval selection only**. Random selection can't be reproduced exactly with the read-only tools the agents have, so it isn't used.

1. Use the population file that was filed as evidence (for example, `gh_merged-prs_<repo>.json` or the HR leaver export), and cite it.
2. Sort the population by a stable key, such as the PR number, employee id or date. Name the key.
3. Compute `k = floor(N / n)` (at least 1), and use the fixed start `s = floor(k / 2)`, counting from 0. Never choose `s` by hand. The selected positions are `s, s+k, s+2k, …`, taking the first `n` of them.
4. Use exactly one of these recipes, and paste it into the sampling appendix so anyone can re-run it:

   JSON array population (`jq`):

   ```bash
   jq --argjson k 24 --argjson s 12 --argjson n 25 \
     'sort_by(.number) | [range($s; length; $k)] as $idx | [$idx[:$n][] as $i | .[$i] | .number]' \
     compliance/evidence/soc2_CC8.1/2026-11-24_gh_merged-prs_api.json
   ```

   CSV population (header on line 1; sort on column 1; GNU `sed` with `first~step` addressing, available in Git Bash and on Linux):

   ```bash
   tail -n +2 compliance/evidence/soc2_CC6.2/2026-11-25_hr_leavers-h2-2026.csv \
     | sort -t, -k1,1 | sed -n '13~24p' | head -n 25
   ```

   In `sed`, line numbers start at 1, so the start line is `s + 1`.
5. Write the selection in the report's sampling appendix: the population file, sort key, N, n, k, s, the exact command, and the selected ids.

Never add "interesting" items to the sample. If something outside the sample looks wrong, raise it as a separate observation, not as part of the sample result.

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
