---
description: Show readiness per framework, evidence coverage and the top open items, computed from the compliance/ files
argument-hint: "[framework key]  (e.g. soc2, iso27001, dpdp, pci-dss; default: all in scope)"
allowed-tools: Read, Glob, Grep
---

# Audit Ready: status

Read-only summary of where the programme stands. Every number is computed from the CSVs; nothing is typed in or remembered.

## Usage

```
/audit-ready:status
/audit-ready:status soc2
```

## Arguments

Parse `$ARGUMENTS`. Accept zero or one framework key. The key must appear in the `framework` column of `applicability.csv`, which means it is in scope. Reject anything else with a usage error that lists the keys in scope. If `compliance/` does not exist, say so and suggest `/audit-ready:start`.

## Steps

1. Load the `audit-ready:grc-assistant` skill. Validate the CSVs you read; report malformed files first.
2. Read `scope.md` (status line), `applicability.csv`, `evidence-plan.csv`, `evidence/index.csv`, `audit/assessments.csv`, `audit/findings.csv`, and list `evidence/_inbox/`.
3. Compute:
   - **Scope:** frameworks in scope and whether `scope.md` says approved.
   - **Applicability:** per framework, counts of applicable / inherited / not applicable.
   - **Plan coverage:** applicable requirements with at least one plan item, and those with none (list up to 10 ids).
   - **Collection:** plan items by status; items past `due` that are not collected (overdue).
   - **Evidence:** files in `index.csv`; rows with empty `sha256` (integrity gaps); files in `_inbox/` waiting.
   - **Audit:** functions audited (distinct functions in assessments via the catalogs' `function` column, curated or generated in `compliance/catalogs/`), proposed vs approved assessments.
   - **Catalog tier:** mark SCF-backed frameworks with `(SCF)` in the readiness line, for example `PCI DSS (SCF) 41%`.
   - **Findings:** open findings by severity.
   - **Readiness:** per framework, using the skill's formula, always with counts.
4. **Top open items**, at most 7, ordered: open major findings, applicable requirements with no plan item, overdue owner requests, open minor findings, inbox files waiting.

## Output

The status block from the skill, then a "Top open items" list, then exactly one suggested next command. Keep it under 30 lines. Do not modify any file.
