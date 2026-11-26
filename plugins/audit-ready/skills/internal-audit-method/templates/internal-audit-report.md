# Internal audit report: {{company}}

**Date:** {{YYYY-MM-DD}} | **Status:** draft | approved on {{date}} by {{user}}
**Frameworks:** {{SOC 2 (Security, Availability) Type II period ...; ISO 27001:2022; DPDP Act 2023 + Rules 2025}}
**Functions audited:** {{Engineering, IT, HR, Legal, Leadership}}

> This is an internal readiness assessment prepared with Audit Ready. It is not an audit opinion, a certification, or legal advice. The verdicts are proposals that {{user}} reviewed and approved. The requirement descriptions are paraphrases keyed to the official ids.

## 1. Summary

{{3–5 sentences: overall readiness, the biggest risks, and what to fix before the external audit}}

## 2. Readiness by framework

Computed from `applicability.csv` and `audit/assessments.csv` (approved rows only):

| Framework | Applicable | Satisfied | Partial | Fails / no evidence | Readiness |
|---|---|---|---|---|---|
| {{SOC 2}} | {{50}} | {{31}} | {{4}} | {{15}} | {{66%}} |

## 3. Readiness by function

| Function | Requirements | Satisfied | Partial | Fails | Open findings (major / minor / obs.) |
|---|---|---|---|---|---|

## 4. Findings

| Id | Severity | Requirement(s) | Finding | Fix | Owner |
|---|---|---|---|---|---|
| {{F-001}} | {{major}} | {{soc2:CC6.1; iso27001:A.8.5}} | {{4 of 38 active Google Workspace users are not enforced for 2SV}} | {{Enforce 2SV for all OUs; re-run /audit-ready:collect gam}} | {{IT lead}} |

## 5. Detail by function

### {{Engineering}}

| Requirement | Procedure | Evidence | Verdict | Gap | Fix |
|---|---|---|---|---|---|
| {{soc2:CC8.1}} | {{Inspection + sample 25 PRs}} | {{soc2_CC8.1/2026-11-26_gh_branch-protection_api.json; ...}} | {{partial}} | {{1 of 25 PRs merged without approval (#482)}} | {{Enable "include administrators"}} |

## 6. Sampling appendix

| Test | Population file | N | n | Method | Selected | Exceptions |
|---|---|---|---|---|---|---|
| {{Change management}} | {{soc2_CC8.1/2026-11-26_gh_merged-prs_api.json}} | {{612}} | {{25}} | {{interval k=24, s=12, sorted by PR number}} | {{#…}} | {{1}} |

## 7. Evidence integrity

{{n}} files relied on. All of them have sha256 values in `evidence/index.csv`. {{Hash mismatches: none | list}}.

## 8. Not yet assessed

{{Requirements without an approved assessment, so they count as 0 in readiness}}
