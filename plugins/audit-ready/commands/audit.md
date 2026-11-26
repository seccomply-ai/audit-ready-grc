---
description: Run an internal (mock external) audit for one business function or all - test evidence, sample, propose verdicts and rated findings, then write the internal audit report after your approval
argument-hint: "[Engineering|IT|HR|Legal|Leadership|all] [--report]"
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Agent
---

# Audit Ready: audit

Pillar 3 is the internal audit. Claude acts as the external auditor and reviews one business function at a time, which keeps each pass focused. Verdicts and findings stay proposals until the user approves them.

## Usage

```
/audit-ready:audit Engineering
/audit-ready:audit all
/audit-ready:audit --report      # only (re)write the report from approved rows
```

## Arguments

Parse `$ARGUMENTS`.
- **Function:** at most one, from `Engineering`, `IT`, `HR`, `Legal`, `Leadership` or `all` (case-insensitive).
- **Flag:** `--report`, optional.
- **No function given:** show each function with its count of filed evidence and requirements, then ask which one to audit.
- **Anything else:** reject it with the usage line.

## Preconditions

- `applicability.csv` must have approved rows and `evidence/index.csv` must have at least one row. If either is missing, suggest the earlier steps.
- Load the skills `audit-ready:grc-assistant`, `audit-ready:framework-reference` and `audit-ready:internal-audit-method`, then validate all the CSVs.

## Steps (per function; for `all`, run Engineering, IT, HR, Legal, Leadership in turn)

1. **Select requirements.** Take the applicable and inherited rows in `applicability.csv` whose catalog `function` matches. Use the shipped catalog for curated frameworks and `compliance/catalogs/<key>.csv` for SCF-backed ones. For SCF-backed rows, the "catalog text" passed to the agents is the SCF control titles, with a note to judge against the requirement id's intent and to flag where the official wording should be checked. If assessments for this function already exist, ask whether to re-audit (which adds new rows dated today) or skip.
2. **Select evidence.** Take the `index.csv` rows whose `requirements` include any of these requirements. Build pairs of evidence × requirement.
3. **Review the evidence in batches.** Split the pairs into batches of about 10 files and launch the `audit-ready:evidence-reviewer` agents, running batches in parallel where possible. Pass each one:
   - the skill path `${CLAUDE_PLUGIN_ROOT}/skills/internal-audit-method/`;
   - the period and the systems from `scope.md`;
   - the items in its batch, with their index rows and catalog text.

   Collect the JSON each one returns. If a result isn't valid JSON, re-run that batch once.
4. **Audit the function.** Launch the `audit-ready:internal-auditor` agent with:
   - the function, frameworks and period;
   - the requirement list;
   - all the reviewer verdicts;
   - the paths to `index.csv` and `evidence-plan.csv`;
   - the next free finding id from `findings.csv`.

   Receive its JSON: assessments, findings, samples, still_needed and summary.
5. **Propose.** Show the user:
   - a verdict table `requirement | evidence | verdict | gap | fix`, with satisfies rows collapsed to a count;
   - the findings table;
   - the samples;
   - the items still needed.

   Label all of it as **proposed**. Ask the user to approve everything, or to change specific rows (a verdict, severity, wording or owner).
6. **Write.** After approval:
   - Append to `audit/assessments.csv` with `reviewer=audit-ready`, `date=today` and `approved=yes`. Rows the user didn't approve go in with `approved=no`.
   - Append the findings to `audit/findings.csv` with `status=open`.
   - Add plan items for anything in `still_needed`, setting `status=planned`.
   - Never edit or delete earlier rows. A re-audit adds new rows, and readiness uses the latest approved verdict per pair.
7. **Report.** When the last selected function is done, or when `--report` is given:
   - Fill `${CLAUDE_PLUGIN_ROOT}/skills/internal-audit-method/templates/internal-audit-report.md` using only approved rows, computing readiness with the grc-assistant formula.
   - Include the sampling appendix, built from the agents' samples.
   - Show the draft. After approval, write it to `audit/<YYYY-MM-DD>-internal-audit-report.md` with the status `approved`. If the file exists, write `-v2`, `-v3` and so on rather than overwriting it.
   - Check that every number in the report matches a recount from `assessments.csv` before writing. Fix any number that doesn't match.

## Output

- Counts per function of satisfies, partial, fails and none.
- New findings by severity.
- The path to the report, if one was written.
- The status block.
- The next step: usually fix the major findings, re-collect, then `/audit-ready:audit <function>` again.

## Guardrails

- Every verdict is a proposal until approved. The report says it is a readiness assessment, not certification or legal advice.
- Read-only. Never change systems or evidence files.
- Refer to people by role or count in findings and the report.
