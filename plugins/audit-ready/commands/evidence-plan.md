---
description: Turn the approved Statement of Applicability into a tool-specific evidence plan, deduplicated across frameworks
argument-hint: "[--refresh]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# Audit Ready: evidence plan

Pillar 2, collection. Builds `compliance/evidence-plan.csv`: one row per evidence artifact. Each row is specific to the company's tools ("Okta MFA policy export", not "MFA evidence") and lists every requirement it covers.

## Usage

```
/audit-ready:evidence-plan
/audit-ready:evidence-plan --refresh   # add items for newly applicable requirements; keep existing rows
```

## Arguments

Parse `$ARGUMENTS`. The only accepted flag is `--refresh`; reject anything else. Without the flag:
- If the plan is empty, build it.
- If the plan has rows, behave like `--refresh` and say so.

Never delete or renumber existing rows.

## Preconditions

- `scope.md` says `approved` and `applicability.csv` has approved rows. If not, stop and suggest `/audit-ready:scope`.
- Load the skills `audit-ready:grc-assistant`, `audit-ready:framework-reference` and `audit-ready:evidence-playbooks`. Validate the CSVs.

## Steps

1. **Gather inputs.**
   - Applicable and inherited rows from `applicability.csv`.
   - The tools in `profile.md` (cloud, IdP, code host, HRMS, ticketing, MDM).
   - The playbooks for the CLIs those tools map to: AWS → aws, GCP → gcloud, Azure → az, GitHub → gh, Google Workspace → gam.
2. **CLI items first.**
   - For each playbook row, keep the requirement keys that are applicable.
   - For SCF-backed frameworks, and for curated ones the row doesn't list, add the applicable requirements whose `scf_ids` intersect the row's `SCF` column. See "Requirement keys and SCF tags" in evidence-playbooks.
   - Skip rows with no applicable requirement.
   - Each kept row becomes one plan item:
     - `method=cli`, `tool=<cli>`, `command_ref=<playbook id>` such as `GH-06`;
     - `owner` is the system owner role from the profile;
     - `period` is `point-in-time` for configuration, or the audit period for populations and logs;
     - `due=` today + 14 days;
     - `status=planned`.
3. **Owner items for everything else.**
   - For each applicable requirement not yet covered by a CLI item, read `typical_evidence` from its catalog row. SCF-backed rows only have SCF evidence-request ids, so write the item from the SCF control titles in the row's `title` and the company's tools.
   - Write concrete, tool-specific items. Name the system: "Keka export of joiners in the period with background check status", not "HR records".
   - Set `method=owner`, `tool` to the system or `document`, an empty `command_ref`, the owner by function (HR, Legal, Engineering lead, IT, CEO or CTO), and `period` and `due` as above.
4. **Inherited requirements** get one item per vendor, such as "AWS SOC 2 Type II report (current period) and bridge letter". Use `method=owner` and owner `Legal` or `Security`.
5. **Deduplicate.**
   - Merge items that ask for the same artifact. Use the dedupe table in framework-reference: one "IdP MFA policy export" covers `soc2:CC6.1;iso27001:A.5.17;iso27001:A.8.5;dpdp:DPDP-R6`.
   - Across any frameworks, owner items for requirements that share SCF ids are candidates to merge. Merge them only when the same document would really satisfy both.
   - Join all covered keys with `;` in `requirements`.
6. **Sampling populations.**
   - For tests that need sampling (joiners, leavers, changes, access reviews, incidents), plan the **population** item, such as "HR leaver list for the period" or "merged PR list".
   - Samples are chosen later in `/audit-ready:audit`.
7. **Coverage check.** Every applicable or inherited requirement must appear in at least one item's `requirements`. List any gaps and add items for them.
8. **Optional cross-check.** If claude-grc-engineering framework plugins are installed (see the grc-assistant skill), mention that `/soc2:evidence-checklist`, `/iso27001:evidence-checklist` or `/ind-dpdpa:evidence-checklist` can be used as a second opinion.
9. **Show and approve.**
   - Show the counts by method, tool and owner, plus the 10 items that cover the most requirements.
   - After approval, write the rows to `evidence-plan.csv` with ids `EV-001` and up. With `--refresh`, continue from the highest existing id.

## Output

Print:
- the number of items, the CLI share (`n of N items, x%`) and the items per owner;
- the coverage result: `all N applicable requirements covered` or the gap list;
- the status block;
- the next step: `/audit-ready:collect` for CLI items, or `/audit-ready:request` for owner items.
