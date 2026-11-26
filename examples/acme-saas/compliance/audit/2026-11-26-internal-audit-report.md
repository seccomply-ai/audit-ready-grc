# Internal audit report: Acme Shift (fictional)

**Date:** 2026-11-26 | **Status:** approved on 2026-11-26 by user (partial pass, sample data)
**Frameworks:** SOC 2 (Security, Availability), readiness window 2026-06-01 to 2026-11-30; DPDP Act 2023 + Rules 2025
**Functions audited:** IT (partial), Engineering (partial), Leadership (partial)

> This is an internal readiness assessment prepared with Audit Ready. It is not an audit opinion, a certification, or legal advice. The verdicts are proposals that the user reviewed and approved. The requirement descriptions are paraphrases keyed to the official ids.

## 1. Summary

This was an early pass with only 4 artifacts filed, so readiness is low because most requirements have no evidence yet. The control that tested best is the GitHub organisation 2FA requirement. The risk assessment for the period is missing (major), and two configuration gaps were found in Workspace 2SV and branch protection (minor). Collect the planned AWS items and the requested owner documents, then re-audit.

## 2. Readiness by framework

| Framework | Applicable | Satisfied | Partial | Fails / no evidence | Readiness |
|---|---|---|---|---|---|
| SOC 2 | 36 | 1 | 2 | 33 | 6% |
| DPDP | 24 | 0 | 0 | 24 | 0% |

## 3. Findings

| Id | Severity | Requirement(s) | Finding | Fix | Owner |
|---|---|---|---|---|---|
| F-003 | major | soc2:CC3.2 | No risk assessment has been performed for the audit period | Run a risk assessment, record it in a risk register and have the CEO approve it | CEO |
| F-001 | minor | soc2:CC6.1; dpdp:DPDP-R6 | 2 of 26 active Google Workspace users are not enforced for 2-step verification | Enforce 2SV for all OUs and re-collect GWS-02 | IT lead |
| F-002 | minor | soc2:CC8.1 | Branch protection on the production API repo can be bypassed by admins | Enable enforce_admins and document an emergency change procedure | CTO |

## 4. Detail

| Requirement | Procedure | Evidence | Verdict | Gap | Fix |
|---|---|---|---|---|---|
| soc2:CC6.1 | Inspection | soc2_CC6.1/2026-11-24_gh_org-settings.json | satisfies | | |
| soc2:CC6.1 | Inspection | soc2_CC6.1/2026-11-24_gam_users-2sv.csv | partial | 2 of 26 active users not enforced for 2SV | Enforce 2SV; re-collect GWS-02 |
| soc2:CC8.1 | Inspection (sample pending) | soc2_CC8.1/2026-11-24_gh_branch-protection_api.json | partial | Admins can bypass; PR sample not yet tested | Enable enforce_admins; collect GH-08/GH-09 |
| soc2:CC6.2 | Inspection (sample pending) | soc2_CC6.2/2026-11-25_hr_leavers-h2-2026.csv | partial | Removal dates not evidenced for 3 of 3 leavers | Collect GWS-07 |
| soc2:CC3.2 | Inquiry | (none) | fails | No evidence filed | Run a risk assessment |

## 5. Sampling appendix

The leaver test was not yet sampled: the population has N=3, so all 3 would be tested, but the removal-date evidence (GWS-07) has not been collected. The change-management sample is pending because EV-004 (the merged PR list) is still planned.

## 6. Evidence integrity

This report relies on 4 files. All 4 have sha256 values in `evidence/index.csv`, and there are no hash mismatches.
